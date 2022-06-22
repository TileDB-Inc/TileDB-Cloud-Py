"""Classes that descend into things and do replacements."""

import uuid
from typing import Any, Dict, Optional

from tiledb.cloud._common import ordered
from tiledb.cloud._common import visitor
from tiledb.cloud.taskgraphs import _codec
from tiledb.cloud.taskgraphs.client_executor import _base


class NodeOutputValueReplacer(_codec.Unescaper):
    """An Unescaper for when the output value of a node must be used locally.

    For Nodes where non–UDF-parameter inputs may be Nodes (e.g. array query
    ranges), this replaces the node's input with the actual value output by
    the previous node.
    """

    def __init__(self, nodes: Dict[uuid.UUID, _base.Node]):
        super().__init__()
        self._nodes = nodes

    def _replace_sentinel(
        self,
        kind: str,
        value: Dict[str, Any],
    ) -> Optional[visitor.Replacement]:
        if kind == "node_output":
            node = self._nodes[uuid.UUID(hex=value["client_node_id"])]
            return visitor.Replacement(node.result())
        return super()._replace_sentinel(kind, value)


class UDFParamReplacer(visitor.ReplacingVisitor):
    # This isn't an Unescaper since we don't want to unescape non-JSON values,
    # we only want to replace parent nodes with their data.

    def __init__(
        self,
        nodes: Dict[uuid.UUID, _base.Node],
        mode: _base.ParamFormat,
    ):
        super().__init__()
        self._nodes = nodes
        self._mode = mode
        self.seen_nodes = ordered.Set[_base.Node]()
        """All the Nodes that we have actually seen while visiting.

        This allows us to avoid passing unnecessary dependencies to the server.
        """

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if not isinstance(arg, dict):
            return None

        try:
            kind = arg[_codec.SENTINEL_KEY]
        except KeyError:
            return None

        # The current value is a __tdbudf__ dictionary.

        if kind == _codec.ESCAPE_CODE:
            # If we have an escaped dictionary, descend into it.
            escaped: Dict[str, Any] = arg[_codec.ESCAPE_CODE]
            return visitor.Replacement(
                {
                    _codec.SENTINEL_KEY: _codec.ESCAPE_CODE,
                    _codec.ESCAPE_CODE: {
                        k: self.visit(v) for (k, v) in escaped.items()
                    },
                }
            )
        if kind == "node_output":
            node = self._nodes[uuid.UUID(hex=arg["client_node_id"])]
            result = visitor.Replacement(node._encode_for_param(self._mode))
            self.seen_nodes.add(node)
            return result

        # If it was neither an escape sequence or a node output,
        # do not dig further into the value.
        return visitor.Replacement(arg)
