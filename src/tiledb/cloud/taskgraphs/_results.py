import abc
import threading
import uuid
from typing import Optional

import urllib3
from typing_extensions import Protocol

from .. import client as client_mod
from .. import rest_api
from .._common import utils
from .._results import codecs
from . import types


class Result(Protocol):
    """Interface for the results of a task graph node."""

    __slots__ = ()

    @abc.abstractmethod
    def decode(self) -> types.NativeValue:
        """Decodes this Result into native Python data."""
        raise NotImplementedError()

    @abc.abstractmethod
    def _tdb_to_json(self) -> types.TileDBJSONValue:
        """Encodes this into a TileDB JSON value."""
        raise NotImplementedError()


class LazyResult(Result):
    """Wrapper for a lazily-downloaded UDF result."""

    def __init__(self, client: client_mod.Client, task_id: uuid.UUID):
        self._client = client
        self._task_id = task_id
        """The server-side ID of the task."""
        self._result: Optional[codecs.BinaryBlob] = None
        """The lazily-downloaded result."""
        self._lock = threading.Lock()

    def decode(self) -> types.NativeValue:
        result = self._download()
        return result.decode()

    def _tdb_to_json(self) -> types.CallArg:
        result = self._download()
        return result._tdb_to_json()

    def _download(self) -> codecs.BinaryBlob:
        with self._lock:
            if not self._result:
                api_instance = self._client.build(rest_api.TasksApi)
                resp: urllib3.HTTPResponse = api_instance.task_id_result_get(
                    str(self._task_id),
                    _preload_content=False,
                )
                try:
                    self._result = codecs.BinaryBlob.from_response(resp)
                finally:
                    utils.release_connection(resp)
            return self._result

    def __repr__(self) -> str:
        loaded_str = "loaded" if self._result else "unloaded"
        return f"<LazyResult {self._task_id} ({loaded_str})>"
