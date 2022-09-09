"""Tools for visualizing TileDB Cloud task graphs."""

# This module should never be eagerly imported by TileDB Cloud code; it relies
# on packages we do not depend on by default. It should only be imported by
# user code or lazily imported when the user calls a task graph object method.


import json
from typing import Any, Dict, Tuple

import networkx
from networkx.drawing import nx_pydot

from tiledb.cloud.taskgraphs import executor


class TileDBVisualizer:
    def __init__(
        self,
        graph: executor.Executor,
        positions: Dict[str, Tuple[float, float]],
    ):
        from tiledb.plot import widget

        self._graph = graph
        self._nodes = tuple(str(n.id) for n in self._graph._deps)
        self._edges = tuple(
            (str(e.parent.id), str(e.child.id)) for e in self._graph._deps.edges()
        )
        self._positions = positions

        self.widget = widget.Visualize(data=self._to_json())

    @classmethod
    def create(cls, graph: executor.Executor) -> "TileDBVisualizer":
        positions = _position_nodes(graph)
        viz = cls(graph, positions)
        viz._start_updates()
        return viz

    def _start_updates(self) -> None:
        self._graph.add_update_callback(self._do_update)

    def _do_update(self, grf: executor.Executor) -> None:
        assert self._graph is grf, "Somehow got passed the wrong graph???"
        self.widget.setData(self._to_json())

    def _node_details(self) -> Dict[str, Dict[str, Any]]:
        return {
            str(n.id): dict(
                name=n.name,
                status=n.status.friendly_name(),
            )
            for n in self._graph._deps
        }

    def _to_json(self) -> str:
        return json.dumps(
            dict(
                nodes=self._nodes,
                edges=self._edges,
                positions=self._positions,
                node_details=self._node_details(),
            )
        )


def visualize(graph: executor.Executor) -> Any:
    ver = TileDBVisualizer.create(graph)
    return ver.widget


def _position_nodes(graph: executor.Executor) -> Dict[str, Tuple[float, float]]:
    net = _to_networkx(graph)
    return nx_pydot.pydot_layout(net, prog="dot")


def _to_networkx(graph: executor.Executor) -> networkx.DiGraph:
    nxgraph = networkx.DiGraph()
    nxgraph.add_nodes_from(
        (str(n.id) for n in graph.nodes_by_name().values()),
        label="",
        height=0.5,
        width=0.5,
    )
    nxgraph.add_edges_from(
        (str(e.parent.id), str(e.child.id)) for e in graph._deps.edges()
    )

    return nxgraph
