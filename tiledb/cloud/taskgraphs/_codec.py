import abc
import base64
import json
import threading
import uuid
from typing import Any, Dict, Optional, TypeVar, Union

import attrs
import cloudpickle
import pyarrow
import urllib3

from tiledb.cloud import client as client_mod
from tiledb.cloud import rest_api
from tiledb.cloud import utils
from tiledb.cloud._common import visitor
from tiledb.cloud._results import decoders
from tiledb.cloud.taskgraphs import types

_T = TypeVar("_T")
TOrDict = Union[_T, Dict[str, Any]]

_PICKLE_PROTOCOL = 4
_ARROW_VERSION = pyarrow.MetadataVersion.V5
SENTINEL_KEY = "__tdbudf__"
ESCAPE_CODE = "__escape__"


class TDBJSONEncodable(metaclass=abc.ABCMeta):
    """Interface defining a type that can be encoded into TileDB JSON."""

    __slots__ = ()

    @abc.abstractmethod
    def _tdb_to_json(self):
        """Converts this object to a JSON-serializable form."""
        raise NotImplementedError()


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
        if kind == ESCAPE_CODE:
            # An escaped value.
            inner_value = value[ESCAPE_CODE]
            return visitor.Replacement(
                {k: self.visit(v) for (k, v) in inner_value.items()}
            )
        if kind == "immediate":
            fmt = value["format"]
            base64d = value["base64_data"]
            data = base64.b64decode(base64d)
            return visitor.Replacement(_LOADERS[fmt](data))
        raise ValueError(f"Unknown sentinel type {kind!r}")


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


class Result(TDBJSONEncodable, metaclass=abc.ABCMeta):
    """Interface for the results of a task graph node."""

    __slots__ = ()

    @abc.abstractmethod
    def decode(self) -> types.NativeValue:
        """Decodes this Result into native Python data."""
        raise NotImplementedError()


@attrs.define(frozen=True, slots=False)
class BinaryResult(Result):
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


class LazyResult(Result):
    """Wrapper for a lazily-downloaded UDF result."""

    def __init__(self, client: client_mod.Client, task_id: uuid.UUID):
        self._client = client
        self._task_id = task_id
        """The server-side ID of the task."""
        self._result: Optional[BinaryResult] = None
        """The lazily-downloaded result."""
        self._lock = threading.Lock()

    def decode(self) -> types.NativeValue:
        result = self._download()
        return result.decode()

    def _tdb_to_json(self) -> types.CallArg:
        result = self._download()
        return result._tdb_to_json()

    def _download(self) -> BinaryResult:
        with self._lock:
            if not self._result:
                api_instance = self._client.build(rest_api.TasksApi)
                resp: urllib3.HTTPResponse = api_instance.task_id_result_get(
                    str(self._task_id),
                    _preload_content=False,
                )
                try:
                    self._result = BinaryResult.from_response(resp)
                finally:
                    utils.release_connection(resp)
            return self._result


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
