"""Things that help you keep track of task results and how to decode them."""

import abc
import threading
import uuid
from concurrent import futures
from typing import Any, Callable, Generic, Optional, TypeVar, Union

import attr
import urllib3

from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error as tce
from tiledb.cloud._results import decoders
from tiledb.cloud._results import stored_params

TASK_ID_HEADER = "X-TILEDB-CLOUD-TASK-ID"
_T = TypeVar("_T")


class Result(Generic[_T], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self) -> _T:
        """Gets the value stored in this Result."""
        raise NotImplementedError()

    def to_stored_param(self) -> stored_params.StoredParam:
        raise TypeError("This result cannot be converted to a StoredParam.")


@attr.s(frozen=True, auto_attribs=True)
class LocalResult(Result[_T], Generic[_T]):
    """A result from running a function in a Node locally."""

    it: _T

    def get(self) -> _T:
        return self.it

    @classmethod
    def wrap(cls, func: Callable[..., _T]) -> Callable[..., Result[_T]]:
        return lambda *args, **kwargs: cls(func(*args, **kwargs))


_SENTINEL = object()


# Not frozen, but externally immutable, and callers should *treat* it like it's
# frozen.
@attr.s()
class RemoteResult(Result[_T], Generic[_T]):
    """A response from running a UDF remotely."""

    def get(self) -> _T:
        """Decodes the response from the server."""
        try:
            with self._result_lock:
                if self._decoded is _SENTINEL:
                    if self._body is not None:
                        self._decoded = self.decoder.decode(self._body)
                    else:
                        assert self.task_id
                        self._decoded = fetch_remote(self.task_id, self.decoder)
                return self._decoded

        except ValueError as ve:
            inner_msg = f": {ve.args[0]}" if ve.args else ""
            raise tce.TileDBCloudError(
                f"Error decoding response from TileDB Cloud{inner_msg}"
            ) from ve

    def to_stored_param(self) -> stored_params.StoredParam:
        if not (self.results_stored and self.task_id):
            raise ValueError("A result must be stored to create a StoredParam.")
        return stored_params.StoredParam(
            decoder=self.decoder,
            task_id=self.task_id,
        )

    task_id = attr.ib(type=Optional[uuid.UUID])
    """The server-generated UUID of the task."""

    decoder = attr.ib(type=decoders.AbstractDecoder[_T])
    """The Decoder that was used to decode the results."""

    results_stored = attr.ib(type=bool)
    """True if the results were stored, false otherwise."""

    _body = attr.ib(type=Optional[bytes])
    """The HTTP content of the body that was returned.

    If None, the result was not downloaded (yet).
    """

    @_body.validator
    def _validate(self, attribute, value):
        del attribute, value  # unused
        if self.results_stored and not self.task_id:
            raise ValueError("task_id must be set for stored results")
        if not self.results_stored and not self._body:
            raise ValueError(
                "no way to access Node results; neither stored nor downloaded"
            )

    # Lock to avoid duplicating work downloading the body or decoding results.
    _result_lock = attr.ib(factory=threading.Lock)
    _decoded = attr.ib(type=Any, default=_SENTINEL)


def unwrapper_proxy(ft: "futures.Future[Result[_T]]") -> "futures.Future[_T]":
    """Creates a Future proxy that unwraps the results of the parent Future."""
    new_ft: "futures.Future[_T]" = futures.Future()
    new_ft.cancel = ft.cancel  # type: ignore[assignment]

    def _forward(_):
        del _  # unused
        if ft.cancelled():
            new_ft.cancel()
            return
        exc = ft.exception()
        if exc:
            new_ft.set_exception(exc)
            return
        new_ft.set_result(ft.result().get())

    ft.add_done_callback(_forward)
    return new_ft


class AsyncResult(Generic[_T]):
    """Asynchronous wrapper for compatibility with the old array.TaskResult."""

    def __init__(self, future: "futures.Future[Result[_T]]"):
        """Creates a new AsyncResponse wrapping the given Future."""
        self._future = future
        self._id_lock = threading.Lock()
        self._task_id: Optional[uuid.UUID] = None
        self._future.add_done_callback(self._set_task_id)

    def get(self, timeout: Optional[float] = None) -> _T:
        """Gets the result from this response, with Future's timeout rules."""
        return self._future.result(timeout).get()

    @property
    def task_id(self) -> Optional[uuid.UUID]:
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


def fetch_remote(task_id: uuid.UUID, decoder: decoders.AbstractDecoder[_T]) -> _T:
    api_instance = client.client.tasks_api
    try:
        resp: urllib3.HTTPResponse = api_instance.task_id_result_get(
            str(task_id),
            _preload_content=False,
        )
    except rest_api.ApiException as exc:
        raise tce.check_exc(exc) from None
    return decoder.decode(resp.data)
