"""The code to build task graphs for later registration and execution."""

import abc
import uuid
from typing import (
    AbstractSet,
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Optional,
    TypeVar,
    Union,
)

import numpy as np

from tiledb.cloud._common import ordered
from tiledb.cloud._common import visitor
from tiledb.cloud.taskgraphs import _codec
from tiledb.cloud.taskgraphs import depgraph
from tiledb.cloud.taskgraphs import types

_T = TypeVar("_T")
"""A generic type."""
ValOrNode = Union[_T, "Node[_T]"]
"""Type indicating that you can pass either a direct value or an input node."""
ValOrNodeSeq = Union[
    ValOrNode[types.NativeSequence[_T]],
    types.NativeSequence[ValOrNode[_T]],
]
"""Either a Node that yields a sequence or a sequence that may contain nodes."""
ArrayMultiIndex = Dict[str, np.ndarray]
"""Type returned from an array query."""
Funcable = Union[str, Callable[..., _T]]
"""Either a Python function or the name of a registered UDF."""


class TaskGraphBuilder:
    """The thing you use to build a task graph.

    This class only *builds* task graphs. The graphs it builds are static and
    only represent the steps to run (the recipe). The actual execution will be
    later performed by the executor.
    """

    def __init__(
        self,
        name: Optional[str] = None,
    ):
        self.name = name
        """A name for this graph. Read-only."""
        self._by_id: Dict[uuid.UUID, Node] = {}
        """The nodes in the graph."""
        self._by_name: Dict[str, Node] = {}
        """The named nodes in the graph, by name."""
        self._deps = depgraph.DepGraph[Node]()
        """A mapping from child to set of parents."""

    def add_dep(self, *, parent: "Node", child: "Node") -> None:
        """Manually requires that the ``parent`` must happen before ``child``.

        This should rarely be necessary; including a parent node within
        the parameter list of a child node automatically adds a dependency.
        """
        self._deps.add_edge(child=child, parent=parent)

    def _add_node(self, node: "Node") -> "Node":
        self._deps.add_new_node(node, node.deps)
        self._by_id[node.id] = node
        if node.name is not None:
            if self._by_name.setdefault(node.name, node) is not node:
                self._deps.remove(node)
                raise ValueError(f"A node named {node.name!r} already exists.")

        return node

    def _tdb_to_json(self):
        """Converts this task graph to a registerable/executable format."""
        nodes = self._deps.topo_sorted
        node_jsons = [n.to_registration_json() for n in nodes]
        for n, n_json in zip(nodes, node_jsons):
            n_json["depends_on"] = [
                str(parent.id) for parent in self._deps.parents_of(n)
            ]
        return dict(
            name=self.name,
            nodes=node_jsons,
        )


class Node(_codec.TDBJSONEncodable, Generic[_T]):
    """The root type of a Node when building a task graph.

    The basic building block of a task graph. Nodes represent the data and
    execution steps within a TileDB task graph.

    ``builder.Node``s themselves are inert; they only represent the steps that
    will be taken by an Executor implementation to run the task graph. They
    should be treated as opaque and immutable; the Executor's node objects
    are the ones that can be interacted with to get status and results.
    """

    def __init__(
        self,
        name: Optional[str],
        deps: Iterable["Node"],
        *,
        fallback_name: Optional[str] = None,
    ):
        self.id = uuid.uuid4()
        """A unique ID for this node."""
        self.name = name
        """The name of the node. If present, the node is unnamed."""
        self.deps: AbstractSet[Node] = ordered.FrozenSet(deps)
        """The nodes that this node depends upon directly."""
        self._fallback_name = fallback_name or type(self).__name__
        """A string to use to generate a display name if the node is unnamed."""

    @property
    def display_name(self) -> str:
        """A friendly name for the Node."""
        if self.name is not None:
            return self.name
        id_clip = str(self.id)[-12:]
        return f"{self._fallback_name} ({id_clip})"

    def __repr__(self):
        return f"<{type(self).__name__} {self.display_name}>"

    def _tdb_to_json(self) -> types.RegisteredArg:
        """Converts this to the format that will be used in parameter lists.

        This is used when a Node is used as an input to another Node::

            child = dag.udf(..., types.args(parent_node))
        """
        return {
            "__tdbudf__": "node_output",
            "client_node_id": str(self.id),
        }

    @abc.abstractmethod
    def to_registration_json(self) -> Dict[str, Any]:
        """Converts this node to the form used when registering the graph.

        This is the form of the Node that will be used to represent it in the
        ``RegisteredTaskGraph`` object, i.e. a ``RegisteredTaskGraphNode``.
        """
        return {
            "client_node_id": str(self.id),
            "name": self.name,
        }


class _ParameterEscaper(_codec.Escaper):
    """Converts Python arguments passed into Nodes into serializable format.

    The input to this ``Escaper`` is a ``NativeValue``, i.e. any Python value.
    The output is a ``RegisteredArg``, used to serialize the Node's arguments
    for registration or passing to an Executor.
    """

    def __init__(self):
        super().__init__()
        self.seen_nodes = ordered.Set[Node]()
        """The Nodes we have found when visiting our input(s)."""

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if isinstance(arg, Node):
            self.seen_nodes.add(arg)
        return super().maybe_replace(arg)

    def arguments_to_json(self, arg: types.Arguments) -> types.RegisteredArg:
        arg_outputs = [{"value": self.visit(val)} for val in arg.args]
        kwarg_outputs = [
            {"name": name, "value": self.visit(value)}
            for (name, value) in arg.kwargs.items()
        ]
        return arg_outputs + kwarg_outputs
