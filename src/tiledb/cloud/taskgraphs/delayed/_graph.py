import abc
import warnings
from typing import Any, Callable, Iterable, List, Optional, TypeVar, Union

from tiledb.cloud import taskgraphs
from tiledb.cloud._common import futures
from tiledb.cloud._common import ordered
from tiledb.cloud._common import visitor
from tiledb.cloud.taskgraphs import builder
from tiledb.cloud.taskgraphs import depgraph
from tiledb.cloud.taskgraphs import executor
from tiledb.cloud.taskgraphs import registration
from tiledb.cloud.taskgraphs import types

_T = TypeVar("_T")

ValOrNode = Union[_T, "Node[_T]"]
ValOrNodeSeq = Union[
    ValOrNode[types.NativeSequence[_T]],
    types.NativeSequence[ValOrNode[_T]],
]

_ExecNode = executor.Node[executor.Executor, _T]
"""Shortcut for the type of an executed task graph node."""


class Node(futures.FutureLike[_T], metaclass=abc.ABCMeta):
    """A single node in a Delayed graph."""

    def __init__(self, owner: "DelayedGraph"):
        self._owner = owner
        """The graph that this Node belongs to.

        This may change during the building process, but is fixed once execution
        starts.
        """
        self._builder_node: Optional[builder.Node[_T]] = None
        """The builder node that this represents when the graph is built/run.

        This is used both in the process of building the graph using the
        :class:`builder.TaskGraphBuilder` (as the node to build, and as the
        input to downstream nodes) and during execution as a way to get the
        :class:`executor.Node` which represents what is actually happening.

        This is only set up when the graph is actually built for either
        registration or startup.
        """
        self._pre_start_callbacks: List[Callable[[Node[_T]], Any]] = []
        """``done_callback``s that were added before this Node was started."""

    def depends_on(self, other: "Node") -> None:
        """Manually defines that this Node needs to run after the provided Node.

        This is usually not needed; when a node is used as an input to another
        Node, their dependency is automatically recorded, and it's recommended
        that you represent dependencies by explicitly passing data from parent
        to child. This method allows you to record a dependency not reflected
        in the graph's data flow.
        """
        self._owner._absorb(other._owner)
        self._owner._add_dep(parent=other, child=self)

    # Methods around managing the lifecycle of a Node.

    def start(self, *, name: Optional[str] = None) -> None:
        """Starts the task graph associated with this Node.

        When executed, all the nodes in a task graph are built and "finalized";
        no changes to data or structure are possible. This method is idempotent;
        calling ``start`` on a node of an already-started Delayed graph has no
        effect.

        While Delayed graph construction is not thread-safe, once this function
        completes, all execution-related functionality (reading results,
        cancelling, retrying, etc.) *is* thread-safe.

        :param name: The name of this execution of the Delayed graph to display
            in task graph logs.
        """
        self._owner._start(name=name)

    def compute(
        self, timeout: Optional[float] = None, *, name: Optional[str] = None
    ) -> _T:
        """Starts this graph and gets this node's results.

        :param timeout: The *client-side* timeout for *waiting for results*.
            This is only passed to the `Future`-like :meth:`result` method.
            Setting it only constrains how long this code will wait for a result
            to appear you make this call; it does not stop execution after that
            time has elapsed.
        :param name: The name of this execution of the Delayed graph to display
            in task graph logs.
        """
        self.start(name=name)
        return self.result(timeout)

    # FutureLike methods.

    def result(self, timeout: Optional[float] = None) -> _T:
        """Gets the result of executing this node, just like a ``Future``.

        The semantics of calling this are the same as those of a traditional
        ``Future``: it will return the result if the node was successful, or
        raise an exception if the node failed.

        This method (along with most ``Future``-like methods) is only valid
        after the Delayed graph this Node belongs to has been started.
        """
        return self._exec_node().result(timeout)

    def add_done_callback(self, fn: Callable[["Node[_T]"], None]) -> None:
        """Adds a callback that will be called once this Node completes.

        While this method is ``Future``-like, it *may* be called before the
        graph started. Like a done callback on a raw task graph, this may be
        called multiple times if the Node is retried.

        :param fn: The function to call. When called, it will be provided with
            a reference to this Node.
        """

        def proxy(_):
            del _
            return fn(self)

        if self._finalized:
            self._exec_node().add_done_callback(proxy)
        else:
            self._pre_start_callbacks.append(proxy)

    def cancel(self) -> bool:
        """Attempts to cancel execution of this node.

        This method (along with most ``Future``-like methods) is only valid
        after the Delayed graph this Node belongs to has been started.
        """
        return self._exec_node().cancel()

    def cancelled(self) -> bool:
        """Returns True if this Node has been cancelled."""
        try:
            return self._exec_node().cancelled()
        except futures.InvalidStateError:
            return False

    def running(self) -> bool:
        """Returns True if this Node is currently running."""
        try:
            return self._exec_node().running()
        except futures.InvalidStateError:
            return False

    def done(self) -> bool:
        """Returns True if this Node's execution has completed."""
        try:
            return self._exec_node().done()
        except futures.InvalidStateError:
            return False

    def exception(self, timeout: Optional[float] = None) -> Optional[BaseException]:
        """Returns the execution raised by this Node's execution, if present.

        If the Node completed successfully, returns None. If the node failed,
        returns the exception. If the Node was cancelled, *raises* an exception.

        This method (along with most ``Future``-like methods) is only valid
        after the Delayed graph this Node belongs to has been started.
        """
        return self._exec_node().exception(timeout)

    # Task graph bonus methods.

    def retry(self) -> bool:
        """Retries this Node of the graph, if necessary.

        If this node has not run, or it ran successfully, this is a no-op.
        This method (along with most ``Future``-like methods) is only valid
        after the Delayed graph this Node belongs to has been started.
        """
        return self._exec_node().retry()

    def retry_all(self):
        """Retries all failed Nodes in the graph.

        If this node has not run, or it ran successfully, this is a no-op.
        This method (along with most ``Future``-like methods) is only valid
        after the Delayed graph this Node belongs to has been started.
        """
        self._owner._get_execution().retry_all()

    @property
    def status(self) -> executor.Status:
        """The status of this Node."""
        try:
            return self._exec_node().status
        except futures.InvalidStateError:
            return executor.Status.WAITING

    def register(self, name: str, *, namespace: Optional[str] = None) -> None:
        """Registers the task graph that this Delayed node is part of.

        :param name: The name to register the graph with. This must be
            a bare name, with no namespace (i.e. ``my-graph``,
            not ``me/my-graph``).
        """
        self._owner._register(name, namespace=namespace)

    def visualize(self) -> Any:
        """Returns a visualization of the graph for a Jupyter notebook."""
        return self._owner._get_execution().visualize()

    # Internals.

    def _exec_node(self) -> _ExecNode[_T]:
        """The execution node this node maps to."""
        return self._owner._exec_node(self)

    def _finalized(self) -> bool:
        return bool(self._owner._execution)

    def _to_builder_node(self, grf: builder.TaskGraphBuilder) -> builder.Node[_T]:
        """Builds this node into the provided graph and returns the result."""
        self._builder_node = self._to_builder_node_impl(grf)
        return self._builder_node

    @abc.abstractmethod
    def _to_builder_node_impl(self, grf: builder.TaskGraphBuilder) -> builder.Node[_T]:
        """The type-specific implementation that builds a builder Node."""
        raise NotImplementedError()


class DelayedGraph:
    """The combination builder/executor used to manage delayed Node instances.

    A DelayedGraph is an all-in-one wrapper over the graph pre-building (using
    delayed Nodes), main building (using the Builder), and execution phases of
    DAG management. It allows users to build task graphs from delayed Nodes
    without their having to worry about the DAG instances themselves, by
    automatically managing graph structure and unifying nodes into a single
    DelayedGraph as previously-independent Nodes merge together.

    A DelayedGraph has two primary overall states: graph construction (where
    the graph's structure can be added to and changed) and execution (where the
    structure of the graph is finalized, it is built, and handed off to an
    Executor to be run).

    While the graph-construction process is *not* thread-safe, after the graph
    starts execution, all execution-lifecycle–related methods *are* thread-safe.

    Users are not expected to ever deal with DelayedGraph instances manully;
    the complete user-facing API is exposed in Node.
    """

    def __init__(self):
        self._deps = depgraph.DepGraph[Node]()
        """All the Nodes in this graph and their dependencies."""

        self._builder: Optional[builder.TaskGraphBuilder] = None
        """If this graph has been built, the Builder that was used to do it.

        We lazily build the graph only when it is needed: when the user
        registers it or we start executing it.
        """

        self._execution: Optional[executor.Executor] = None
        """If this graph has been started, the executor that is running it."""

    def _absorb(self, other: "DelayedGraph") -> None:
        """Merges another DelayedGraph into this one.

        Because a DelayedGraph is created for each set of independent nodes,
        when two sets of independent nodes are united, those two independent
        DelayedGraphs need to be merged into one. For example, if nodes A and B
        are currently in two indepentent DelayedGraphs, and node C takes both
        as a parameter, all of A, B, and C need to be in the same graph after
        that delayed call is set up.
        """
        if self._execution or other._execution:
            raise futures.InvalidStateError(
                "Cannot add new nodes to an already-executing graph."
            )
        if other is self:
            return
        other._invalidate_builder()
        for node in other._deps:
            node._owner = self
            self._add(node, parents=other._deps.parents_of(node))

    def _add(self, n: Node, *, parents: Iterable[Node]) -> None:
        """Adds a single new Node to this graph."""
        self._invalidate_builder()
        if self._execution:
            raise futures.InvalidStateError(
                "Cannot add new nodes to an already-executing graph."
            )
        self._deps.add_new_node(n, parents)

    def _get_execution(self) -> executor.Executor:
        if not self._execution:
            raise futures.InvalidStateError(
                "Cannot manage lifecycle of an unstarted Delayed task graph."
                " Before calling this method, ensure that you have called"
                " some_node.start() or some_node.compute()."
            )
        return self._execution

    def _exec_node(self, n: Node[_T]) -> _ExecNode[_T]:
        """Gets the execution node associated with the given Delayed node."""
        exec = self._get_execution()
        bn = n._builder_node
        assert bn, "node must be built if executing"
        return exec.node(bn)

    def _add_dep(self, *, parent: Node, child: Node) -> None:
        """Records a dependency between parent and child node."""
        self._invalidate_builder()
        self._deps.add_edge(parent=parent, child=child)

    def _invalidate_builder(self) -> None:
        """Deletes the current Builder for when we modify graph structure.

        We don't want spooky action at a distance (modifying a graph locally
        unexpectedly updating the registered instance). There's also no good
        outcome if somebody merges together two previously-registered
        sub-graphs (e.g. `node_a.register()`; `node_b.register()`;
        `some_udf(a, b)`).
        """
        if not self._builder:
            return
        warnings.warn(
            UserWarning(
                "Modifying a Delayed graph that has already been registered"
                " will not update the registered version of the graph."
            )
        )
        self._builder = None
        for node in self._deps:
            node._builder_node = None

    def _build(self, name: Optional[str] = None) -> builder.TaskGraphBuilder:
        """Transforms this graph into its TaskGraphBuilder (if needed)."""
        if not self._builder:
            bld = builder.TaskGraphBuilder(name)
            for node in self._deps:
                builder_node = node._to_builder_node(bld)
                # Include parent–child relationships that are not specified
                # by the params.
                for parent in self._deps.parents_of(node):
                    built_parent = parent._builder_node
                    bld.add_dep(parent=built_parent, child=builder_node)
            self._builder = bld
        return self._builder

    def _register(self, name: str, *, namespace: Optional[str] = None) -> None:
        bld = self._build(name)
        registration.register(bld, name, namespace=namespace)

    def _start(self, name: Optional[str] = None) -> None:
        """Starts execution of this graph (if not yet started)."""
        if self._execution:
            return
        bld = self._build(name)
        self._execution = taskgraphs.execute(bld)
        # Ensure that all the ``done_callback``s that were registered before
        # starting the graph are executed.
        for node in self._deps:
            exec_node = self._exec_node(node)
            for cb in node._pre_start_callbacks:
                exec_node.add_done_callback(cb)


class Merger(visitor.ReplacingVisitor):
    """Crawls data structures to find parent delayed Nodes to merge together."""

    def __init__(self):
        super().__init__()
        self.has_nodes = False
        """Has this visitor seen any parent Nodes?

        Both unexecuted and executed Nodes are included in this set, since
        previously-executed nodes must still have their results substituted in
        at execution time.
        """

        self.unexecuted_nodes = ordered.Set[Node]()
        """All the nodes seen by this visitor from not-yet-executed graphs.

        Nodes that are not part of graphs that are being executed can have their
        graph structure (and what graph they are a part of) changed at will.
        Nodes that are part of graphs that have been executed are finalized and
        cannot have their structure changed; instead they must be treated as
        regular input data.
        """

    def merge_visited(self) -> DelayedGraph:
        """Merges all unexecuted Nodes into the same DelayedGraph, returning it.

        The DelayedGraph returned by this method is used as the owner of the
        newly-built Node.
        """
        new_owner: Optional[DelayedGraph] = None
        for parent in self.unexecuted_nodes:
            if new_owner is None:
                new_owner = parent._owner
            else:
                new_owner._absorb(parent._owner)
        return new_owner or DelayedGraph()

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if isinstance(arg, Node):
            self.has_nodes = True
            # We need to discern between parent nodes that have been executed
            # (i.e. nodes that are on old graphs that were already started)
            # and parent nodes that are on new graphs that have not yet been
            # started. Nodes that are on graphs that were already started are
            # ignored for now (we will substitute values in at execution time),
            # but nodes on fresh graphs need to be united.
            if not arg._finalized():
                self.unexecuted_nodes.add(arg)
        return None


class BuilderNodeReplacer(visitor.ReplacingVisitor):
    """Replaces delayed Nodes with builder Nodes for building a task graph."""

    def __init__(self, dg: DelayedGraph):
        super().__init__()
        self._dg = dg

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if isinstance(arg, Node):
            if arg._owner is self._dg:
                # Normal case: We're assembling a node from our same graph
                # into the ouput builder graph. Because `DelayedGraph.start`
                # iterates over Nodes in dependency order, we are guaranteed
                # that all our parent nodes have already been built.
                assert arg._builder_node, "Input arg was not already built."
                return visitor.Replacement(arg._builder_node)
            # Abnormal case: We're reading data from a previously-executed
            # Delayed graph. Rather than treating it as a node in our graph,
            # we need to extract its value.
            return visitor.Replacement(arg.result())
        return None
