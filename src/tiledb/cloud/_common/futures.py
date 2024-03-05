"""Classes and helpers for dealing with concurrency and futures.

This is intended to be a drop-in replacement for the ``concurrent.futures``
module (to the extent that we use it).
"""

import abc
import sys
import threading
import warnings
from concurrent import futures
from typing import Callable, Generic, Iterable, Optional, Tuple, TypeVar

_T = TypeVar("_T")

# Re-exports from the built-in futures module.
Future = futures.Future
CancelledError = futures.CancelledError
TimeoutError = futures.TimeoutError
Executor = futures.Executor
ProcessPoolExecutor = futures.ProcessPoolExecutor
ThreadPoolExecutor = futures.ThreadPoolExecutor

if sys.version_info < (3, 8):

    class InvalidStateError(futures._base.Error):
        """The operation is not allowed in this state."""

else:
    InvalidStateError = futures.InvalidStateError

# New stuff.


class FutureLike(Generic[_T], metaclass=abc.ABCMeta):
    """The public-facing API of Futures.

    Ideally this would be a Protocol, but those aren't in Python before 3.8.

    Implementations of this class may have different behaviors than standard
    Futures if they support additional operations (like retrying), but when
    a client does not use those operations, it should behave just like a
    standard :class:`futures.Future`.
    """

    @abc.abstractmethod
    def cancel(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def cancelled(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def running(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def done(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def exception(self, timeout: Optional[float] = None) -> Optional[BaseException]:
        raise NotImplementedError()

    @abc.abstractmethod
    def result(self, timeout: Optional[float] = None) -> _T:
        raise NotImplementedError()

    @abc.abstractmethod
    def add_done_callback(self, fn: Callable[["FutureLike[_T]"], None]) -> None:
        raise NotImplementedError()


FutureLike.register(Future)


def wait_for(
    w: threading.Condition, pred: Callable[[], bool], timeout: Optional[float]
) -> None:
    """Waits for a condition variable or raises an error on timeout."""
    if not w.wait_for(pred, timeout):
        raise TimeoutError(f"timed out after {timeout} sec")


def execute_callbacks(thing: _T, callbacks: Iterable[Callable[[_T], None]]) -> None:
    """Runs callback functions and swallows errors."""

    for cb in callbacks:
        try:
            cb(thing)
        except Exception as exc:
            warnings.warn(UserWarning(f"{exc} in callback {cb}({thing!r})"))


class CallbackRunner(Generic[_T]):
    """Handles executing callbacks on a separate thread.

    This will lazily create a callback thread and dispatch callbacks on that
    thread, without blocking the place that is sending out the callbacks.
    """

    def __init__(
        self,
        owner: _T,
        *,
        thread_name: Optional[str] = None,
    ) -> None:
        """Initializer.

        :param owner: The owner of this callback runner, i.e., the object which
            will be passed to the callback.
        :param thread_name: If set, the name to use for the thread which runs
            the callbacks.
        """
        self._owner = owner
        self._thread_name = thread_name or f"{self._owner}-callback-runner"
        self._lock = threading.Lock()
        """Guards ``_to_run`` and ``_callback_thread``."""
        self._to_run: Tuple[Callable[[_T], None], ...] = ()
        self._callback_thread: Optional[threading.Thread] = None
        """
        If set, the thread running callbacks.
        If None, there is no callback thread running.
        """

    def run_callbacks(self, to_run: Iterable[Callable[[_T], None]]) -> None:
        """Sets up to call the given callbacks on the callback-running thread.

        If callbacks are currently running, the new callbacks will start
        immediately after the currently-running ones have completed. If there
        are already callbacks enqueued, the newly-passed callbacks will
        completely replace the previous callbacks. This is on the assumption
        that a previous recipient that is no longer on the new list has
        unsubscribed from the callback (or that the callback list only ever
        grows).
        """
        with self._lock:
            self._to_run = tuple(to_run)
            if not self._to_run:
                # Bail out early to avoid spinning up a new thread
                # if there's no work to be done.
                return
            if not self._callback_thread:
                self._callback_thread = threading.Thread(
                    name=self._thread_name,
                    target=self._run_callbacks,
                )
                self._callback_thread.start()

    def _run_callbacks(self) -> None:
        """Actually calls the callbacks on the internal thread."""
        while True:
            with self._lock:
                if not self._to_run:
                    # We're done for now! Record that we are no longer running.
                    self._callback_thread = None
                    return
                # Grab all the callbacks we need to run and note that we have
                # started running this round.
                to_run = self._to_run
                self._to_run = ()

            execute_callbacks(self._owner, to_run)
