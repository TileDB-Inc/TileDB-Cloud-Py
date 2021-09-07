"""Handles the tracking and decoding of task results."""

import abc
import dataclasses
import json
from typing import Any

import cloudpickle
import pandas
import pyarrow

from tiledb.cloud import tiledb_cloud_error as tce
from tiledb.cloud.rest_api import models


class AbstractDecoder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def decode(self, data: bytes) -> Any:
        raise NotImplementedError()


def _load_arrow(data: bytes):
    reader = pyarrow.RecordBatchStreamReader(data)
    return reader.read_all()


@dataclasses.dataclass(frozen=True)
class Decoder(AbstractDecoder):

    format: str

    _DECODE_FNS = {
        models.ResultFormat.NATIVE: cloudpickle.loads,
        models.ResultFormat.JSON: json.loads,
        models.ResultFormat.ARROW: _load_arrow,
    }

    def decode(self, data: bytes) -> Any:
        try:
            decoder = self._DECODE_FNS[self.format]
        except KeyError:
            raise tce.TileDBCloudError(f"{self.format!r} is not a valid result format.")
        return decoder(data)


@dataclasses.dataclass(frozen=True)
class PandasDecoder(AbstractDecoder):

    format: str

    def decode(self, data: bytes) -> pandas.DataFrame:
        if self.format == models.ResultFormat.ARROW:
            reader = pyarrow.RecordBatchStreamReader(data)
            return reader.read_pandas()
        return pandas.DataFrame(Decoder(self.format).decode(data))
