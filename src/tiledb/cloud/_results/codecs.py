import abc
import base64
import json
from typing import Any, Generic, Tuple, Type, TypeVar

import attrs
import cloudpickle
import pyarrow
import urllib3
from typing_extensions import Self

# This is a circular dependency since we need to be able to decode `tiledb_json`
# format data.
from . import tiledb_json
from . import types

_ARROW_VERSION = pyarrow.MetadataVersion.V5
_PICKLE_PROTOCOL = 4
_T = TypeVar("_T")


class Codec(Generic[_T], metaclass=abc.ABCMeta):
    """Translates objects to bytes and vice versa. Purely classmethods."""

    __slots__ = ()

    NAME: str
    """The name to use for the codec, as used in ``result_format``."""

    MIME: str
    """The MIME type identifying this codec."""

    @classmethod
    @abc.abstractmethod
    def encode(cls, obj: _T) -> bytes:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def decode(cls, data: bytes) -> _T:
        raise NotImplementedError()

    @classmethod
    def decode_base64(cls, data: str) -> _T:
        data_bytes = base64.b64decode(data)
        return cls.decode(data_bytes)

    @classmethod
    def encode_base64(cls, obj: _T) -> str:
        data_bytes = cls.encode(obj)
        return base64.b64encode(data_bytes).decode("utf-8")


class ArrowCodec(Codec[pyarrow.Table]):
    """Encodes Arrow data into its default stream format."""

    NAME = "arrow"
    MIME = "application/vnd.apache.arrow.stream"

    @classmethod
    def encode(cls, tbl: pyarrow.Table) -> bytes:
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

    @classmethod
    def decode(cls, data: bytes) -> pyarrow.Table:
        # If a UDF didn't return any rows, there will not have been any batches
        # of data to write to the output, and thus it will not include any content
        # at all. (SQL queries will include headers.)
        if not data:
            # In this case, we need to return an empty table.
            return pyarrow.Table.from_pydict({})
        reader = pyarrow.RecordBatchStreamReader(data)
        return reader.read_all()


class BytesCodec(Codec[bytes]):
    """Does nothing to bytes."""

    NAME = "bytes"
    MIME = "application/octet-stream"

    @classmethod
    def encode(cls, obj: bytes) -> bytes:
        return obj

    @classmethod
    def decode(cls, data: bytes) -> bytes:
        return data


class JSONCodec(Codec[object]):
    """Dumps/loads JSON."""

    NAME = "json"
    MIME = "application/json"

    @classmethod
    def encode(cls, obj: object) -> bytes:
        return json.dumps(obj).encode("utf-8")

    @classmethod
    def decode(cls, data: bytes) -> object:
        return json.loads(data)


class PickleCodec(Codec[object]):
    """Pickles objects using CloudPickle."""

    NAME = "python_pickle"
    MIME = "application/vnd.tiledb.python-pickle"

    @classmethod
    def encode(cls, obj: object) -> bytes:
        return cloudpickle.dumps(obj, protocol=_PICKLE_PROTOCOL)

    @classmethod
    def decode(cls, data: bytes) -> object:
        return cloudpickle.loads(data)


class TileDBJSONCodec(Codec[object]):
    """Serializes objects with TileDB JSON."""

    NAME = "tiledb_json"
    MIME = "application/vnd.tiledb.udf-data+json"

    @classmethod
    def encode(cls, obj: object) -> bytes:
        return tiledb_json.dumps(obj)

    @classmethod
    def decode(cls, data: bytes) -> object:
        return tiledb_json.loads(data)


ALL_CODECS: Tuple[Type[Codec[Any]], ...] = (
    ArrowCodec,
    BytesCodec,
    JSONCodec,
    PickleCodec,
    TileDBJSONCodec,
)
"""Every codec we have."""
CODECS_BY_FORMAT = {c.NAME: c for c in ALL_CODECS}
CODECS_BY_FORMAT["native"] = PickleCodec
CODECS_BY_MIME = {c.MIME: c for c in ALL_CODECS}


@attrs.define(frozen=True, slots=False)
class BinaryBlob:
    """Container for a binary-encoded value, decoded on-demand.

    This is used to store results obtained from the server, such that it is not
    necessary to decode them between stages, and they only are decoded upon
    request.
    """

    format: str
    """The TileDB Cloud name of the data's format (see ``CODECS_BY_FORMAT``)."""
    data: bytes
    """The binary data itself."""

    @classmethod
    def from_response(cls, resp: urllib3.HTTPResponse) -> Self:
        """Reads a urllib3 response into an encoded result."""
        full_mime = resp.getheader("Content-type") or "application/octet-stream"
        mime, _, _ = full_mime.partition(";")
        mime = mime.strip()
        try:
            format_name = CODECS_BY_MIME[mime].NAME
        except KeyError:
            format_name = "mime:" + mime
        data = resp.data
        return cls(format_name, data)

    def decode(self) -> types.NativeValue:
        """Decodes this result into native Python data."""
        # This is not lock-protected because we're ok with decoding twice.
        try:
            return self.__dict__["_decoded"]
        except KeyError:
            pass
        try:
            loader = CODECS_BY_FORMAT[self.format].decode
        except KeyError:
            raise ValueError(f"Cannot decode {self.format!r} data")
        self.__dict__["_decoded"] = loader(self.data)
        return self.__dict__["_decoded"]

    def _tdb_to_json(self) -> types.TileDBJSONValue:
        return types.TileDBJSONValue(
            {
                "__tdbudf__": "immediate",
                "format": self.format,
                "base64_data": base64.b64encode(self.data).decode("ascii"),
            }
        )

    @classmethod
    def of(cls, obj: Any) -> Self:
        """Turns a non–JSON-encodable object into a ``BinaryBlob``."""
        if isinstance(obj, bytes):
            return cls("bytes", obj)
        if isinstance(obj, pyarrow.Table):
            return cls("arrow", ArrowCodec.encode(obj))
        return cls("python_pickle", PickleCodec.encode(obj))
