import abc
import base64
import json
import sys
from typing import TYPE_CHECKING, Any, Generic, Tuple, Type, TypeVar

import attrs
import cloudpickle
import pyarrow
import urllib3
from typing_extensions import Self, TypeGuard

# This is a circular dependency since we need to be able to decode `tiledb_json`
# format data.
from . import tiledb_json
from . import types

if TYPE_CHECKING:
    import pandas

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

    @classmethod
    def to_blob(cls, obj: _T) -> "BinaryBlob":
        return BinaryBlob(cls.NAME, cls.encode(obj))


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


class ArrowDataFrameCodec(Codec["pandas.DataFrame"]):
    """Encodes Pandas DataFrames as Arrow data."""

    NAME = "arrow_dataframe"
    # We don't actually serve this MIME type; it is subject to change.
    MIME = "application/vnd.tiledb.arrow-dataframe"

    @classmethod
    def encode(cls, data: "pandas.DataFrame") -> bytes:
        """Converts a Pandas array to the byte format of an Arrow table."""
        tbl = pyarrow.Table.from_pandas(data)
        return ArrowCodec.encode(tbl)

    @classmethod
    def decode(cls, data: bytes) -> "pandas.DataFrame":
        reader = pyarrow.RecordBatchStreamReader(data)
        return reader.read_pandas()


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
    ArrowDataFrameCodec,
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
    def of(cls, obj: object) -> "BinaryBlob":
        """Turns a non–JSON-encodable object into a ``BinaryBlob``."""
        if isinstance(obj, bytes):
            return BytesCodec.to_blob(obj)
        if isinstance(obj, pyarrow.Table):
            return ArrowCodec.to_blob(obj)
        if _is_dataframe(obj):
            try:
                return ArrowDataFrameCodec.to_blob(obj)
            except pyarrow.ArrowInvalid:
                # We can't encode this as an Arrow dataframe for some reason
                # (usually, a Python object column), so we fall back to pickle.
                # This means that the client/server Pandas versions will have
                # to be in sync, but this is a fairly rare situation. Besides,
                # storing and serializing raw Python objects in dataframes is
                # already fairly fragile.
                pass
        # If all else fails, just pickle it.
        return PickleCodec.to_blob(obj)


def _is_dataframe(obj: object) -> TypeGuard["pandas.DataFrame"]:
    """``isinstance``, but doesn't require importing Pandas first."""
    try:
        pandas = sys.modules["pandas"]
    except KeyError:
        return False
    return isinstance(obj, pandas.DataFrame)
