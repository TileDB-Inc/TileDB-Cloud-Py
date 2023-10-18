"""Things that help you keep track of task results and how to decode them."""

import abc
import threading
import uuid
from typing import Any, Callable, Generic, Optional, TypeVar, Union

import attrs
import urllib3

from .. import client
from .. import rest_api
from .. import tiledb_cloud_error as tce
from .._common import futures
from .._common import utils
from . import codecs
from . import decoders
from . import stored_params

TASK_ID_HEADER = "X-TILEDB-CLOUD-TASK-ID"
_T = TypeVar("_T")


class Result(Generic[_T], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self) -> _T:
        """Gets the value stored in this Result."""
        raise NotImplementedError()

    def to_stored_param(self) -> stored_params.StoredParam:
        raise TypeError("This result cannot be converted to a StoredParam.")


@attrs.define(frozen=True)
class LocalResult(Result[_T], Generic[_T]):
    """A result from running a function in a Node locally."""

    it: _T

    def get(self) -> _T:
        return self.it

    @classmethod
    def wrap(cls, func: Callable[..., _T]) -> Callable[..., Result[_T]]:
        return lambda *args, **kwargs: cls(func(*args, **kwargs))


_SENTINEL: Any = attrs.make_class("Sentinel", (), frozen=True, slots=True)()


# Not frozen, but externally immutable, and callers should *treat* it like it's
# frozen.
@attrs.define()
class RemoteResult(Result[_T], Generic[_T]):
    """A response from running a UDF remotely."""

    def get(self) -> _T:
        """Decodes the response from the server."""
        try:
            with self._result_lock:
                if self._decoded is _SENTINEL:
                    if self._body is not None:
                        self._decoded = self.decoder.decode(self._body)
                        # Now that we've decoded, we don't need the body text.
                        self._body = None
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

    task_id: Optional[uuid.UUID] = attrs.field()
    """The server-generated UUID of the task."""

    decoder: decoders.AbstractDecoder[_T] = attrs.field()
    """The Decoder that was used to decode the results."""

    results_stored: bool = attrs.field()
    """True if the results were stored, false otherwise."""

    _body: Optional[bytes] = attrs.field()
    """The HTTP content of the body that was returned.

    If None, the result body was either not yet downloaded or was already
    decoded.
    """

    @_body.validator  # mypy: disable=union-attr (this is an attr at this point)
    def _validate(self, attribute, value):
        del attribute, value  # unused
        if self.results_stored and not self.task_id:
            raise ValueError("task_id must be set for stored results")
        if not self.results_stored and self._body is None:
            raise ValueError(
                "no way to access Node results;"
                " they must be either stored or downloaded"
            )

    _result_lock: threading.Lock = attrs.field(factory=threading.Lock)
    """Lock to avoid duplicating work downloading the body or decoding."""
    _decoded: Any = attrs.field(default=_SENTINEL)


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


def fetch_remote(
    task_id: uuid.UUID, decoder: Optional[decoders.AbstractDecoder[Any]] = None
) -> object:
    api_instance = client.build(rest_api.TasksApi)
    try:
        resp: urllib3.HTTPResponse = api_instance.task_id_result_get(
            str(task_id),
            _preload_content=False,
        )
    except rest_api.ApiException as exc:
        raise tce.check_exc(exc) from None
    if decoder is None:
        return codecs.BinaryBlob.from_response(resp).decode()
    try:
        return decoder.decode(resp.data)
    finally:
        utils.release_connection(resp)
