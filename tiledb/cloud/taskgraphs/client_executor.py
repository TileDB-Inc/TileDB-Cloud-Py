"""A client-side implementation of a task graph Executor.

This module implements a task graph Executor that coordinates the execution of
graph nodes on the client side.
"""

import abc
import enum
import queue
import threading
import uuid
from concurrent import futures
from typing import Any, Dict, Optional, Set, TypeVar

from tiledb.cloud import client
from tiledb.cloud.taskgraphs import executor

Status = executor.Status
_T = TypeVar("_T")
"""Value that a Node yields."""


class LocalExecutor(executor.Executor["Node"]):
    """Coordinates the execution of a task graph locally."""

    def __init__(
        self,
        graph: executor.GraphStructure,
        namespace: Optional[str] = None,
        api_client: Optional[client.Client] = None,
        name: Optional[str] = None,
    ):
        super().__init__(graph)
        self.name = name
        self._namespace = namespace or client.default_charged_namespace()
        self._done_node_queue: "queue.Queue[Node]" = queue.Queue()
        """Queue where completed nodes are added as they are done.

        This acts as the event loop for ``_exec_loop.``
        """
        self._inputs: Dict[uuid.UUID, Any] = {}
        self._client = api_client or client.client

        self._active_deps = self._deps.copy()
        self._running_nodes: Set[Node] = set()
        self._failed_nodes: Set[Node] = set()
        self._succeeded_nodes: Set[Node] = set()

        self._lifecycle_lock = threading.Lock()
        self._status: Status = Status.WAITING

        if self.name:
            thread_name = f"Task graph {self.name} executor"
        else:
            thread_name = f"{self!r} executor"
        self._event_loop_thread = threading.Thread(
            name=thread_name,
            target=self._run,
            daemon=True,
        )
        self._done_event = threading.Event()
        self._exception: Optional[BaseException] = None

    @property
    def status(self) -> Status:
        with self._lifecycle_lock:
            return self._status

    def execute(self, **inputs: Any) -> None:
        raise NotImplementedError()

    def cancel(self) -> bool:
        with self._lifecycle_lock:
            if self._status in (Status.SUCCEEDED, Status.FAILED):
                return False
            self._status = Status.CANCELLED
        for node in self._active_deps.topo_sorted:
            node.cancel()
        return True

    def wait(self, timeout: Optional[float] = None) -> None:
        self._done_event.wait(timeout)

    def _make_node(
        self,
        uid: uuid.UUID,
        name: Optional[str],
        node_json: Dict[str, Any],
    ) -> "Node":
        raise NotImplementedError()

    def _run(self):
        """The main event loop of this Executor."""
        raise NotImplementedError()


class _ParamFormat(enum.Enum):
    """The format used to encode the result of a parent node for a child."""

    STORED_PARAMS = enum.auto()
    """The node result is encoded in ``CallArgStoredParams`` format.

    Rather than including the actual value in the UDF's parameter list sent to
    the server, this will (when possible) provide the result ID to be
    substituted in server-side. If the node is purely local (e.g., an input),
    this will encode the value itself.
    """
    VALUES = enum.auto()
    """The node result is encoded directly, in ``CallArg`` format.

    This will include the actual result of the node in the parameter list,
    without the need for any server-side processing.
    """


class Node(executor.Node[LocalExecutor, _T], metaclass=abc.ABCMeta):
    """Base class for Nodes to be executed locally.

    All public-facing methods MUST be thread-safe.
    """

    def __init__(self, *args):
        super().__init__(*args)
        self._event = threading.Event()
        self._status: Status = Status.WAITING
        self._exception: Optional[Exception] = None

    # External API

    def result(self, timeout: Optional[float] = None) -> _T:
        self._event.wait(timeout)
        # Because it's guaranteed that `exception` will *never be written to*
        # after the `_event` is set, we don't need to hold a lock here.
        if self._exception:
            raise self._exception
        return self._result_impl()

    def exception(self, timeout: Optional[float] = None) -> Optional[Exception]:
        self._event.wait(timeout)
        if self._status is Status.CANCELLED:
            raise futures.CancelledError()
        return self._exception

    def cancel(self) -> bool:
        cancelled = self._set_status_if_can_start(Status.CANCELLED)
        if cancelled:
            # If we were successful at cancelling this Node, we effectively
            # "own" the result fields on this thread. We can set them safely
            # ourselves before firing the Event.
            self._exception = futures.CancelledError()
            self._event.set()
            self._do_callbacks()
        return cancelled

    # Internals

    def _status_impl(self) -> Status:
        return self._status

    def _exec(self, parents: Dict[uuid.UUID, "Node"], input_value: Any) -> None:
        """The boilerplate for the ``_exec`` implementation for local Nodes.

        This handles all the lifecycle management for Node execution. It should
        only ever be called by the Executor. Subclasses should instead implement
        ``_exec_impl``, which contains the type-specific behavior.
        """
        if not self._set_status_if_can_start(Status.RUNNING):
            return

        try:
            self._exec_impl(parents, input_value)
        except Exception as ex:
            with self._lifecycle_lock:
                self._status = Status.FAILED
                self._exception = ex
            raise
        else:
            with self._lifecycle_lock:
                self._status = Status.SUCCEEDED
        finally:
            self._event.set()
            self._do_callbacks()

    @abc.abstractmethod
    def _exec_impl(self, parents: Dict[uuid.UUID, "Node"], input_value: Any) -> None:
        """The type-specific behavior of executing a Node."""
        raise NotImplementedError()

    @abc.abstractmethod
    def _result_impl(self) -> _T:
        """Returns the result of this node's execution, if applicable.

        This will only ever be called after ``_event`` is set and the state is
        ``SUCCEEDED``. It should only ever be called inside ``result()``.
        """
        raise NotImplementedError()

    def _assert_succeeded(self) -> None:
        if self._status is not Status.SUCCEEDED:
            raise AssertionError("_encoded_result is only valid for successful nodes")

    def _set_ready(self) -> None:
        self._set_status_if_can_start(Status.READY)

    def _set_status_if_can_start(self, status: Status) -> bool:
        """If this node is allowed to start, updates its status.

        Updates the status of this node, but only if it's unstarted (and is able
        to be started). Used to implement both :meth:`cancel` and the equivalent
        of ``Future.set_running_or_notify_cancel``.
        """
        with self._lifecycle_lock:
            if self._status in (Status.WAITING, Status.READY):
                self._status = status
                return True
            return False

    @abc.abstractmethod
    def _encode_for_param(self, mode: _ParamFormat) -> Any:
        """Encodes the result of this node for use in a JSON parameter list.

        This is used to pass the output of this Node into the parameters of a
        following Node.
        """
        raise NotImplementedError()
