"""Generic interfaces for task graph executors."""

import abc
import enum
import logging
import threading
import uuid
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union

from tiledb.cloud.taskgraphs import builder
from tiledb.cloud.taskgraphs import depgraph

_log = logging.getLogger(__name__)


class Status(enum.Enum):
    """The current status of a Node (or a graph)."""

    WAITING = enum.auto()
    """A Node is waiting for input values."""
    READY = enum.auto()
    """All the inputs of a Node have resolved and it can run."""
    RUNNING = enum.auto()
    """The Node is currently running."""
    SUCCEEDED = enum.auto()
    """The Node completed successfully."""
    FAILED = enum.auto()
    """The Node failed to complete."""
    CANCELLED = enum.auto()
    """The Node was cancelled before it could complete."""


GraphStructure = Union[Dict[str, Any], builder.TaskGraphBuilder]
"""The structure of a task graph, as the JSON serialization or a Builder."""
_N = TypeVar("_N", bound="Node")
"""The specific type of Node that an executor uses."""


class Executor(Generic[_N], metaclass=abc.ABCMeta):
    """An interface allowing for execution and management of a task graph.

    This is the basic interface fulfilled by any task graph executor. While some
    implementations may provide more control, these operations, to the extent
    that they are supported, are universal across task graph implementations.
    """

    def __init__(self, graph: GraphStructure):
        if isinstance(graph, builder.TaskGraphBuilder):
            graph_json = graph._tdb_to_json()
        else:
            graph_json = graph
        self._graph_json = graph_json
        self._deps = depgraph.DepGraph[_N]()
        self._by_id: Dict[uuid.UUID, _N] = {}
        self._by_name: Dict[str, _N] = {}

        json_nodes = graph_json["nodes"]
        for node_json in json_nodes:
            self._add_node(node_json)

    # Public API.

    def node(self, nid: Union[str, uuid.UUID, builder.Node]) -> _N:
        """Gets the node identified either by name, ID, or builder node.

        When passed:
        - a ``str``: The node with the given name.
        - a :class:`uuid.UUID`: The node with the given ID.
        - a :class:`builder.Node`: The execution node corresponding to the given
          node from the :class:`builder.Builder`.
        """
        if isinstance(nid, str):
            return self._by_name[nid]
        if isinstance(nid, builder.Node):
            nid = nid.id
        if not isinstance(nid, uuid.UUID):
            raise TypeError(
                f"Nodes must be accessed by name, ID, or builder node, not {type(nid)}."
            )
        return self._by_id[nid]

    @abc.abstractmethod
    def execute(self, **inputs: Any) -> None:
        """Starts execution of this graph with the given input values."""
        del inputs
        raise NotImplementedError()

    def cancel(self) -> bool:
        """If possible, cancels further execution of this graph.

        Like ``futures.Future.cancel``, this returns ``True`` if the graph could
        be cancelled, and ``False`` if not.
        """
        return False

    @property
    @abc.abstractmethod
    def status(self) -> Status:
        """The status of the entire graph."""
        raise NotImplementedError()

    @abc.abstractmethod
    def wait(self, timeout: Optional[float] = None) -> None:
        """Waits for the execution of this task graph to complete."""
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def server_graph_uuid(self) -> Optional[uuid.UUID]:
        """The UUID of this execution's log as returned by the server.

        If log submission failed (or the graph was not yet submitted), None.
        """

    # Internals.

    def _add_node(self, node_json: Dict[str, Any]) -> None:
        """Internal function to add a Node object to common data structures.

        Subclasses should not need to override this, since this has no
        Executor implementation–specific behavior.
        """
        uid = uuid.UUID(node_json["client_node_id"])
        name = node_json.get("name")
        node = self._make_node(uid, name, node_json)
        dep_strs = node_json.get("depends_on", ())
        dep_ids = (uuid.UUID(hex=dep_id) for dep_id in dep_strs)
        deps = [self._by_id[dep] for dep in dep_ids]
        self._deps.add_new_node(node, deps)
        self._by_id[node.id] = node
        if node.name is not None:
            if self._by_name.setdefault(node.name, node) is not node:
                raise KeyError(f"Duplicate node with name {node.name!r}")
            self._by_name[node.name] = node

    @abc.abstractmethod
    def _make_node(
        self,
        uid: uuid.UUID,
        name: Optional[str],
        node_json: Dict[str, Any],
    ) -> _N:
        """Internal abstract function to turn a Node's JSON into a Node object.

        An implementation should provide this to turn the JSON descriptions of
        a Node into the concrete ``Node`` object that the executor uses to
        handle actually running the graph.
        """
        raise NotImplementedError()


_ET = TypeVar("_ET", bound=Executor)
"""The type of the executor of a node."""
_T = TypeVar("_T")
"""The type of the value that a Node yields."""


class Node(Generic[_ET, _T]):
    """An abstract type specifying the operations on a Node of a task graph.

    Executor implementations will return instances of implementations of these
    Nodes when executing a task graph. If a caller uses only the methods here
    when manipulating task graph nodes, the actions they take will work (to the
    extent that they are supported) no matter the specifics of the executor
    itself (client-side, server-side, etc.).

    The external-facing API matches that of ``futures.Future``, with some added
    niceties (like ``status``), and without the internal methods that are only
    "meant for use in unit tests and Executor implementations":
    ``set_running_or_notify_cancel``, ``set_result``, and ``set_exception``.

    The generic types on this (which are really only of concern to Executor
    implementors) represent the ``Executor`` type and the type the ``Node``
    yields::

        Node[MyExecutor, int]
        # A Node subtype that is executed by a MyExecutor
        # and whose .result() is an int.
    """

    # TODO: Retry functionality. When we do add retry functionality, assumptions
    # around a node "finishing" exactly once will be broken.

    def __init__(self, uid: uuid.UUID, owner: _ET, name: Optional[str]):
        self.id = uid
        """The client-generated UUID of this node."""
        self.owner = owner
        """The executor which this node belongs to."""
        self.name = name
        """The name of the node, if present."""

        self._lifecycle_lock = threading.Lock()
        """A lock to protect lifecycle events and callback list management."""
        self._callbacks: List[Callable[[Node[_ET, _T]], None]] = []
        """Callbacks that will be called when the Node completes."""

    # Node-specific APIs.

    @property
    def status(self) -> Status:
        """The current lifecycle state of this Node."""
        with self._lifecycle_lock:
            return self._status_impl()

    @abc.abstractmethod
    def _status_impl(self) -> Status:
        """Abstract method for implementation of the status property.

        ``_lifecycle_lock`` must be held by the caller.
        """
        raise NotImplementedError()

    @property
    def display_name(self) -> str:
        """The name for this node that should show up in UIs."""
        if self.name is not None:
            return self.name
        uid_str = str(self.id)[-12:]
        return f"{self.fallback_name} ({uid_str})"

    @property
    def fallback_name(self) -> str:
        """A fallback name for this node if unnamed."""
        return type(self).__name__

    @abc.abstractmethod
    def wait(self, timeout: Optional[float] = None) -> None:
        """Waits for the given amount of time for this Node to complete."""
        raise NotImplementedError()

    # Public interface of `futures.Future`.

    @abc.abstractmethod
    def result(self, timeout: Optional[float] = None) -> _T:
        """The value resulting from executing this node.

        Returns the result if present, or raises an exception if execution
        raised an exception.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def exception(self, timeout: Optional[float] = None) -> Optional[Exception]:
        """If this node failed, the exception that was raised.

        If the Node succeeded, returns None. If the Node was cancelled, a
        ``futures.CancelledError`` will be *raised* rather than returned.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def cancel(self) -> bool:
        """If possible, cancels execution of this node.

        Returns True if cancellation succeeded, False if we could not cancel.
        """
        raise NotImplementedError()

    def cancelled(self) -> bool:
        """Returns True if the Node was cancelled."""
        return self.status is Status.CANCELLED

    def running(self) -> bool:
        """Returns True if the Node is currently executing."""
        return self.status is Status.RUNNING

    def done(self) -> bool:
        """Returns True if this Node has completed or been cancelled."""
        with self._lifecycle_lock:
            return self._done()

    def add_done_callback(self, fn: Callable[["Node[_ET, _T]"], None]) -> None:
        """Adds a callback that will be called when this Node completes.

        While the current behavior is similar to the way ``add_done_callback``
        on a regular ``Future`` works, we don't guarantee that it will remain
        the same (e.g. will it be called immediately, on what thread).
        Particularly, when retry functionality is later added to Nodes, this
        behavior is likely to change.
        """
        with self._lifecycle_lock:
            if not self._done():
                self._callbacks.append(fn)
                return

        try:
            fn(self)
        except Exception:
            _log.exception("%r callback %r failed", self, fn)

    # Internals to handle Future methods.

    def _done(self) -> bool:
        """Internal implementation of ``done``.

        The caller must already hold ``_lifecycle_lock``.

        This needs to be separated from the ``done`` method so that
        ``add_done_callback`` works correctly and can add a callback atomically,
        without a race condition if a client adds a callback at the same time
        as the Node completes.
        """
        return self._status_impl() in (
            Status.CANCELLED,
            Status.SUCCEEDED,
            Status.FAILED,
        )

    def _do_callbacks(self) -> None:
        """Actually performs the callbacks when a Node completes.

        This should be called by the Node implementation exactly once,
        with ``_lifecycle_lock`` *not* held.
        """
        assert self.done(), "_do_callbacks called when Node is not done"

        # We don't need to hold _lifecycle_lock to iterate through _callbacks
        # because add_done_callbacks guarantees that if the node is done,
        # no more callbacks will be added to the list.
        for fn in self._callbacks:
            try:
                fn(self)
            except Exception:
                _log.exception("%r callback %r failed", self, fn)
