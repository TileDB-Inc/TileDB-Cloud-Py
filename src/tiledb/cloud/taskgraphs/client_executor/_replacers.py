"""Classes that descend into things and do replacements."""

import uuid
from typing import Any, Dict, List, Optional

from ..._common import ordered
from ..._common import visitor
from ..._results import tiledb_json
from .. import types
from . import _base


class NodeOutputValueReplacer(tiledb_json.Decoder):
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
    """Converts ``RegisteredArg`` values to ``CallArg``[``StoredParams``]."""

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
            kind = arg[tiledb_json.SENTINEL_KEY]
        except KeyError:
            return None

        # The current value is a __tdbudf__ dictionary.

        if kind == tiledb_json.ESCAPE_CODE:
            # If we have an escaped dictionary, descend into it.
            escaped: Dict[str, Any] = arg[tiledb_json.ESCAPE_CODE]
            return visitor.Replacement(
                {
                    tiledb_json.SENTINEL_KEY: tiledb_json.ESCAPE_CODE,
                    tiledb_json.ESCAPE_CODE: {
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


def visit_args(
    vtor: visitor.ReplacingVisitor, args: types.Arguments
) -> types.Arguments:
    return types.Arguments(
        (vtor.visit(a) for a in args.args),
        {k: vtor.visit(v) for k, v in args.kwargs.items()},
    )


UDFArgument = Dict[str, Any]
"""Marker for a structured dict for an argument, with ``name`` and ``value``."""


def parse_json_args(json_args: List[UDFArgument]) -> types.Arguments:
    """Parses a list of ``UDFArgument``s into an ``Arguments`` instance.

    This takes the ``UDFArgument`` sequence and turns it into its ``args`` and
    ``kwargs`` values, without performing any parsing of the actual values
    inside each of the arguments (that is, it turns the JSON list into a
    list of args and a dict of kwargs, but does not perform further processing).
    """
    # Usually we don't include internal type-checks, but this function is also
    # used on the server-side UDF executor, where we do want to ensure that
    # we don't get the wrong type of data.
    arg_type = type(json_args)
    if arg_type is not list:
        raise ValueError(
            f"Arguments must be a list of TGUDFArgument dicts, not {arg_type}"
        )
    args: List[Any] = []
    kwargs: Dict[str, Any] = {}
    for pos, entry in enumerate(json_args):
        e_type = type(entry)
        if e_type is not dict:
            raise ValueError(
                "Each argument entry must be a TGUDFArgument dict."
                f" Position {pos} was of type {e_type}."
            )
        name = entry.get("name")
        # Go likes to eat `null` and turn it into a missing field, so we have to
        # assume that a missing `value` field means None.
        value = entry.get("value")
        if name is None:
            if kwargs:
                # If 'name' is not present but kwargs already has been set,
                # that means a positional argument appears after a named arg.
                # This is not allowed.
                raise ValueError(
                    "All positional args must appear before all named args."
                    f" Positional arg at index {pos} appears after named args"
                    f" {tuple(kwargs)}."
                )
            args.append(value)
        else:
            if name in kwargs:
                prev = len(args)
                for kw in kwargs:
                    if name == kw:
                        break
                    prev += 1
                raise ValueError(
                    f"Keyword arg {name!r} (at index {pos})"
                    f" has already been used (at index {prev})."
                )
            kwargs[name] = value
    return types.Arguments(args, kwargs)
