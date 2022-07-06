"""Classes and helpers for dealing with concurrency and futures.

This is intended to be a drop-in replacement for the ``concurrent.futures``
module (to the extent that we use it).
"""

import abc
import sys
import threading
import warnings
from concurrent import futures
from typing import Callable, Generic, Iterable, Optional, TypeVar

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
