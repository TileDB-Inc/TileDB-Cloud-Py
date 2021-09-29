"""Classes that know how to decode UDF results."""

import abc
import dataclasses
import json
from typing import Any, Generic, TypeVar

import cloudpickle
import pandas
import pyarrow

from tiledb.cloud import tiledb_cloud_error as tce
from tiledb.cloud.rest_api import models

_T = TypeVar("_T")


class AbstractDecoder(Generic[_T], metaclass=abc.ABCMeta):
    """Interface for something that knows how to decode a byte response."""

    @abc.abstractmethod
    def decode(self, data: bytes) -> Any:
        raise NotImplementedError()


def _load_arrow(data: bytes) -> pyarrow.Table:
    reader = pyarrow.RecordBatchStreamReader(data)
    return reader.read_all()


_DECODE_FNS = {
    models.ResultFormat.NATIVE: cloudpickle.loads,
    models.ResultFormat.JSON: json.loads,
    models.ResultFormat.ARROW: _load_arrow,
}


@dataclasses.dataclass(frozen=True)
class Decoder(AbstractDecoder[_T], Generic[_T]):
    """General decoder for the formats we support.

    The exact name and location of this class is important, because instances
    are sent as pickles when making UDF requests.
    """

    format: str

    def decode(self, data: bytes) -> _T:
        try:
            decoder = _DECODE_FNS[self.format]
        except KeyError:
            raise tce.TileDBCloudError(f"{self.format!r} is not a valid result format.")
        return decoder(data)


@dataclasses.dataclass(frozen=True)
class PandasDecoder(AbstractDecoder[pandas.DataFrame]):
    """Decoder which turns things into DataFrames.

    The exact name and location of this class is important, because instances
    are sent as pickles when making UDF requests.
    """

    format: str

    def decode(self, data: bytes) -> pandas.DataFrame:
        if self.format == models.ResultFormat.ARROW:
            reader = pyarrow.RecordBatchStreamReader(data)
            return reader.read_pandas()
        return pandas.DataFrame(Decoder(self.format).decode(data))
