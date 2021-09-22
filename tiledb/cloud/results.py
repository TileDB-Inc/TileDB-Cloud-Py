"""Handles the tracking and decoding of task results."""

import abc
import dataclasses
import json
import threading
import uuid
from concurrent import futures
from typing import Any, Optional, Union

import cloudpickle
import pandas
import pyarrow
import urllib3

from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error as tce
from tiledb.cloud.rest_api import models

TASK_ID_HEADER = "X-TILEDB-CLOUD-TASK-ID"


class AbstractDecoder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def decode(self, data: bytes) -> Any:
        raise NotImplementedError()


# Not frozen to avoid generating unsafe methods like `__hash__`,
# but you should still *treat* it like it's frozen.
@dataclasses.dataclass()
class Response:
    """A response from running a UDF."""

    def decode(self) -> Any:
        try:
            return self.decoder.decode(self.body)
        except ValueError as ve:
            inner_msg = f": {ve.args[0]}" if ve.args else ""
            raise tce.TileDBCloudError(
                f"Error decoding response from TileDB Cloud{inner_msg}"
            ) from ve


    # The HTTP content of the body that was returned.
    body: bytes
    # The server-generated UUID of the task.
    task_id: Optional[uuid.UUID]
    # The decoder that was used to decode the results.
    decoder: AbstractDecoder
    # True if the results were stored, false otherwise.
    results_stored: bool


class AsyncResponse:
    """Asynchronous wrapper for compatibility with the old array.TaskResult."""

    def __init__(self, future: "futures.Future[Response]"):
        """Creates a new AsyncResponse wrapping the given Future."""
        self._future = future
        self._id_lock = threading.Lock()
        self._task_id: Optional[uuid.UUID] = None
        self._future.add_done_callback(self._set_task_id)

    def get(self, timeout: Optional[float] = None) -> Any:
        """Gets the result from this response, with Future's timeout rules."""
        return self._future.result(timeout).decode()

    @property
    def task_id(self):
        """Gets the task ID, or None if not complete or failed with no ID."""
        with self._id_lock:
            return self._task_id

    def _set_task_id(self, _):
        """Sets the task ID once the Future has completed."""
        try:
            res = self._future.result()
        except rest_api.ApiException as exc:
            with self._id_lock:
                self._task_id = extract_task_id(exc)
        except:  # noqa: E722 We don't care about other exceptions, period.
            pass
        else:
            with self._id_lock:
                self._task_id = res.task_id


def _load_arrow(data: bytes):
    reader = pyarrow.RecordBatchStreamReader(data)
    return reader.read_all()


_DECODE_FNS = {
    models.ResultFormat.NATIVE: cloudpickle.loads,
    models.ResultFormat.JSON: json.loads,
    models.ResultFormat.ARROW: _load_arrow,
}


@dataclasses.dataclass(frozen=True)
class Decoder(AbstractDecoder):

    format: str

    def decode(self, data: bytes) -> Any:
        try:
            decoder = _DECODE_FNS[self.format]
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


def extract_task_id(
    thing: Union[rest_api.ApiException, urllib3.HTTPResponse],
) -> Optional[uuid.UUID]:
    """Pulls the task ID out of a response or an exception."""
    id_hdr = thing.headers and thing.headers.get(TASK_ID_HEADER)
    return _maybe_uuid(id_hdr)


def _maybe_uuid(id_str: Optional[str]) -> Optional[uuid.UUID]:
    """Parses a hex string into a UUID if present and valid."""
    if not id_str:
        return None
    try:
        return uuid.UUID(hex=id_str)
    except ValueError:
        return None
