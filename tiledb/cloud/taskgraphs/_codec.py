import abc
import base64
import json
import re
from typing import Any, Dict, Optional, TypeVar, Union

import attrs
import cloudpickle
import numpy as np
import pyarrow
import urllib3

from tiledb.cloud._common import visitor
from tiledb.cloud._results import decoders
from tiledb.cloud.taskgraphs import types

_T = TypeVar("_T")
TOrDict = Union[_T, Dict[str, Any]]

_PICKLE_PROTOCOL = 4
_ARROW_VERSION = pyarrow.MetadataVersion.V5
SENTINEL_KEY = "__tdbudf__"
"""General sentinel for special TileDB UDF dictionaries."""
ESCAPE_CODE = "__escape__"
"""Code used to indicate escaping a dictionary which has SENTINEL_KEY in it."""
SLICE = "__slice__"
"""Code used to indicate an encoded slice value."""
NP_TIME = "__np_time__"
"""Code to indicate an encoded numpy timedelta or timedelta64."""


class TDBJSONEncodable(metaclass=abc.ABCMeta):
    """Interface defining a type that can be encoded into TileDB JSON."""

    __slots__ = ()

    @abc.abstractmethod
    def _tdb_to_json(self):
        """Converts this object to a JSON-serializable form."""
        raise NotImplementedError()


_NP_DTYPES = re.compile(r"^(datetime64|timedelta64)\[(.+?)\]$")


class Unescaper(visitor.ReplacingVisitor):
    """A general-purpose replacer to unescape sentinel-containing structures.

    This descends through data structures and replaces dictionaries containing
    ``__tdbudf__`` values with the unescaped values. This base implementation
    handles only the basics; you can create a derived version to handle specific
    situations (building arguments, replacing values, etc.).

    The data that is returned from this is generally a ``types.NativeValue``.
    """

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if not isinstance(arg, dict):
            return None
        if SENTINEL_KEY not in arg:
            return None
        sentinel_name = arg[SENTINEL_KEY]
        return self._replace_sentinel(sentinel_name, arg)

    def _replace_sentinel(
        self,
        kind: str,
        value: Dict[str, Any],
    ) -> Optional[visitor.Replacement]:
        """The base implementation of a sentinel-replacer.

        It is passed the kind and value of a ``__tdbudf__``–containing object::

            # Given this:
            the_object = {"__tdbudf__": "node_data", "data": "abc"}
            # This will be called:
            self._replace_sentinel("node_data", the_object)

        This implementation handles replacing values that do not require any
        external information. Derived implementations should handle their own
        keys and end with a call to
        ``return super()._replace_sentinel(kind, value)``.
        """
        handlers = {
            ESCAPE_CODE: self._handle_escape,
            SLICE: self._handle_slice,
            NP_TIME: self._handle_np_time,
            "immediate": self._handle_immediate,
        }
        try:
            handler = handlers[kind]
        except KeyError:
            raise ValueError(f"Unknown sentinel type {kind!r}") from None
        return handler(value)

    def _handle_escape(self, value: Dict[str, Any]):
        """Handles an escaped dict which has the sentinel in it."""
        inner_value = value[ESCAPE_CODE]
        return visitor.Replacement({k: self.visit(v) for (k, v) in inner_value.items()})

    def _handle_slice(self, value: Dict[str, Any]):
        """Handles an encoded slice."""
        start_stop_step = (
            self.visit(value.get(attr)) for attr in ("start", "stop", "step")
        )
        return visitor.Replacement(slice(*start_stop_step))

    def _handle_immediate(self, value: Dict[str, Any]):
        """Handles an immediate value (i.e. base64'd data)."""
        fmt = value["format"]
        base64d = value["base64_data"]
        data = base64.b64decode(base64d)
        return visitor.Replacement(_LOADERS[fmt](data))

    def _handle_np_time(self, value: Dict[str, Any]):
        """Handles an encoded numpy datetime64/timedelta64."""
        int_val = value["int"]
        dtype = value["dtype"]

        match = _NP_DTYPES.match(dtype)
        if not match:
            raise ValueError(f"numpy dtype value {dtype!r} is invalid")
        typ, unit = match.groups()
        builder = {
            "datetime64": np.datetime64,
            "timedelta64": np.timedelta64,
        }[typ]
        return visitor.Replacement(builder(int_val, unit))


class Escaper(visitor.ReplacingVisitor):
    """Turns arbitrary Python values into TileDB JSON.

    This escapes arbitrary native values so that they can be JSON-serialized.
    It should only be used with ``NativeValue``s—that is, values that are
    already JSON-serializable, like ``RegisteredArg``s or ``CallArg``s, should
    *not* be passed to an ``Escaper``. The base implementation will return
    fully self-contained JSON-serializable objects, i.e. ``CallArg``s.
    """

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if isinstance(arg, TDBJSONEncodable):
            return visitor.Replacement(arg._tdb_to_json())
        if isinstance(arg, slice):
            output = {SENTINEL_KEY: SLICE}
            for attr in ("start", "stop", "step"):
                val = getattr(arg, attr)
                if val is not None:
                    output[attr] = self.visit(val)
            return visitor.Replacement(output)
        if isinstance(arg, (np.datetime64, np.timedelta64)):
            return visitor.Replacement(
                {
                    SENTINEL_KEY: NP_TIME,
                    "dtype": str(arg.dtype),
                    "int": int(arg.astype("int64")),
                }
            )
        if is_jsonable_shallow(arg):
            if isinstance(arg, dict):
                if SENTINEL_KEY in arg:
                    return visitor.Replacement(
                        {
                            SENTINEL_KEY: ESCAPE_CODE,
                            ESCAPE_CODE: {k: self.visit(v) for (k, v) in arg.items()},
                        }
                    )
            return None
        return visitor.Replacement(BinaryResult.of(arg)._tdb_to_json())


_MIME_TO_FORMAT = {
    "application/octet-stream": "bytes",
    "application/json": "json",
    "application/vnd.tiledb.python-pickle": "python_pickle",
    "application/vnd.tiledb.r-serialization": "r_serialization",
    "application/vnd.apache.arrow.stream": "arrow",
    # TODO: The server should stop returning "udf-native" as a type soon.
    # After that, we can remove this entry, since it's ambiguous for non-Python
    # UDFs.
    "application/vnd.tiledb.udf-native": "python_pickle",
}

# TODO: Move these to decoders._DECODE_FNS functions once our API is firmed up.
_LOADERS = {
    "arrow": decoders._load_arrow,
    "bytes": bytes,
    "json": json.loads,
    "native": cloudpickle.loads,
    "python_pickle": cloudpickle.loads,
}


@attrs.define(frozen=True, slots=False)
class BinaryResult(TDBJSONEncodable):
    """Container for a binary-encoded value, decoded on-demand.

    This is used to store results obtained from the server, such that it is not
    necessary to decode them between stages, and they only are decoded upon
    request.
    """

    format: str
    """The TileDB Cloud name of the data's format (see ``_MIME_TO_FORMAT``)."""
    data: bytes
    """The binary data itself."""

    @classmethod
    def from_response(cls, resp: urllib3.HTTPResponse) -> "BinaryResult":
        """Reads a urllib3 response into an encoded result."""
        full_mime = resp.getheader("Content-type", "application/octet-stream")
        mime, _, _ = full_mime.partition(";")
        mime = mime.strip()
        format = _MIME_TO_FORMAT.get(mime, "mime:" + mime)
        data = resp.data
        return cls(format, data)

    def decode(self) -> types.NativeValue:
        """Decodes this result into native Python data."""
        # This is not lock-protected because we're ok with decoding twice.
        try:
            return self.__dict__["_decoded"]
        except KeyError:
            pass
        try:
            loader = _LOADERS[self.format]
        except KeyError:
            raise ValueError(f"Cannot decode {self.format!r} data")
        self.__dict__["_decoded"] = loader(self.data)
        return self.__dict__["_decoded"]

    def _tdb_to_json(self) -> types.CallArg:
        return {
            "__tdbudf__": "immediate",
            "format": self.format,
            "base64_data": base64.b64encode(self.data).decode("ascii"),
        }

    @classmethod
    def of(cls, obj: Any) -> "BinaryResult":
        """Turns a non–JSON-encodable object into a ``BinaryResult``."""
        if isinstance(obj, bytes):
            return cls("bytes", obj)
        if isinstance(obj, pyarrow.Table):
            return cls("arrow", _arrow_to_bytes(obj))
        return cls("python_pickle", pickle(obj))


def _arrow_to_bytes(tbl: pyarrow.Table) -> bytes:
    sink = pyarrow.BufferOutputStream()
    writer = pyarrow.RecordBatchStreamWriter(
        sink,
        tbl.schema,
        options=pyarrow.ipc.IpcWriteOptions(
            metadata_version=_ARROW_VERSION,
            compression="zstd",
        ),
    )
    writer.write(tbl)
    return sink.getvalue()


def pickle(obj) -> bytes:
    return cloudpickle.dumps(obj, protocol=_PICKLE_PROTOCOL)


def b64_str(val: bytes) -> str:
    return base64.b64encode(val).decode("ascii")


_NATIVE_JSONABLE = (
    str,
    int,
    bool,
    float,
    type(None),
    list,
    tuple,
)
"""Types whose direct values can always be turned into JSON."""


def is_jsonable_shallow(obj) -> bool:
    if isinstance(obj, _NATIVE_JSONABLE):
        return True
    if not isinstance(obj, dict):
        # Apart from the above types, only dicts are JSONable.
        return False
    # For a dict to be JSONable, all keys must be strings.
    return all(isinstance(key, str) for key in obj)
