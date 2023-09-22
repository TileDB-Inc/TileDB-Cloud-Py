"""Classes that know how to decode UDF results."""

import abc
import dataclasses
from typing import TYPE_CHECKING, Any, Generic, TypeVar

import pyarrow

from tiledb.cloud import tiledb_cloud_error as tce
from tiledb.cloud.rest_api import models

from . import codecs

if TYPE_CHECKING:
    import pandas

_T = TypeVar("_T")


class AbstractDecoder(Generic[_T], metaclass=abc.ABCMeta):
    """Interface for something that knows how to decode a byte response."""

    @abc.abstractmethod
    def decode(self, data: bytes) -> Any:
        raise NotImplementedError()


@dataclasses.dataclass(frozen=True)
class Decoder(AbstractDecoder[_T]):
    """General decoder for the formats we support.

    The exact name and location of this class is important, because instances
    are sent as pickles when making UDF requests.
    """

    format: str

    def decode(self, data: bytes) -> _T:
        try:
            codec = codecs.CODECS_BY_FORMAT[self.format]
        except KeyError:
            raise tce.TileDBCloudError(f"{self.format!r} is not a valid result format.")
        return codec.decode(data)


@dataclasses.dataclass(frozen=True)
class PandasDecoder(AbstractDecoder["pandas.DataFrame"]):
    """Decoder which turns things into DataFrames.

    The exact name and location of this class is important, because instances
    are sent as pickles when making UDF requests.
    """

    format: str

    def decode(self, data: bytes) -> "pandas.DataFrame":
        if self.format == models.ResultFormat.ARROW:
            reader = pyarrow.RecordBatchStreamReader(data)
            return reader.read_pandas()
        import pandas

        return pandas.DataFrame(Decoder(self.format).decode(data))
