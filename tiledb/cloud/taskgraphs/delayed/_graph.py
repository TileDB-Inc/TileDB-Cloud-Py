from typing import Iterable, Optional

from tiledb.cloud._common import futures
from tiledb.cloud._common import ordered
from tiledb.cloud._common import visitor
from tiledb.cloud.taskgraphs import depgraph
from tiledb.cloud.taskgraphs import executor


class Node:
    """A single node in a Delayed graph."""

    def __init__(self, owner: "DelayedGraph"):
        self._owner = owner

    def depends_on(self, other: "Node") -> None:
        self._owner._absorb(other._owner)
        self._owner._add_dep(parent=other, child=self)

    # Internals.

    def _finalized(self) -> bool:
        return bool(self._owner._execution)


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
        for node in other._deps:
            node._owner = self
            self._add(node, parents=other._deps.parents_of(node))

    def _add(self, n: Node, *, parents: Iterable[Node]) -> None:
        """Adds a single new Node to this graph."""
        if self._execution:
            raise futures.InvalidStateError(
                "Cannot add new nodes to an already-executing graph."
            )
        self._deps.add_new_node(n, parents)

    def _add_dep(self, *, parent: Node, child: Node) -> None:
        """Records a dependency between parent and child node."""
        self._deps.add_edge(parent=parent, child=child)


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
