"""Simpler nodes for Delayed task graphs.

Unlike the UDF node, these nodes are "static" once created.
"""

from typing import Any, Dict, Iterable, Optional

from tiledb.cloud.taskgraphs import builder
from tiledb.cloud.taskgraphs import types
from tiledb.cloud.taskgraphs.delayed import _graph


class Array(_graph.Node[types.ArrayMultiIndex]):
    """Used as an input parameter to a UDF node."""

    def __init__(
        self,
        owner: _graph.DelayedGraph,
        uri: _graph.ValOrNode[str],
        nodeable_kwargs: Dict[str, Any],
        *,
        name: Optional[str],
        has_node_args: bool,
    ):
        """Initializer. Users should never call this directly."""
        super().__init__(owner)
        self._uri = uri
        """The URI to visit (may be a node)"""
        self._nodeable_kwargs = nodeable_kwargs
        """The kwargs to pass to ``array_node`` (which may be nodes)"""
        self._name = name
        """A name (also to pass to ``array_node``, but cannot be a node)"""
        self._has_node_args = has_node_args
        """True if we found any Nodes in node_kwargs."""

    @classmethod
    def create(
        cls,
        uri: _graph.ValOrNode[str],
        *,
        raw_ranges: Optional[_graph.ValOrNodeSeq] = _graph.NOTHING,
        buffers: Optional[_graph.ValOrNodeSeq[str]] = _graph.NOTHING,
        name: Optional[str] = _graph.NOTHING,
    ) -> "Array":
        """Creates an array parameter that can be used as an input to a UDF.

        This allows you to specify an array to be used as an input to a UDF
        executed on TileDB Cloud. Arrays can be provided as a parameter to UDFs
        and appear just like any other parameter to the UDF::

            result = Delayed(my_function, name="process array data")(
                first_param,
                DelayedArray("tiledb://some/array", raw_ranges=[[10, 20], [30, 50]]),
                more,
                params,
            )

        Most inputs can be provided as either direct values, or as upstream
        nodes, so you can dynamically specify, for instance, which array
        to read from::

            which_array = Delayed(pick_array)(param)
            result = Delayed(my_function, name="process array data")(
                source=DelayedArray(which_array, raw_ranges=[[1, 7, 99, 650]),
            )

        Further details about the parameters can be found on
        :meth:`builder.TaskGraphBuilder.array_read`.

        :param uri: The ``tiledb://`` URI of the array to be queried.
        :param raw_ranges: The ranges to read. Each dimension is provided as
            a list of `[lo1, hi1, lo2, hi2, ...]` (both inclusive) pairs.
            To read values 3–5 and 20–29 on the only dimension, you would
            provide `[[3, 5, 20, 29]]` as the value.
        :param buffers: The names of the dimensions and attributes to read from.
        :param name: An optional name for reference in the task graph.
            If provided, this must be unique within the graph.
        """
        merger = _graph.Merger()
        merger.visit(uri)
        merger.visit(raw_ranges)
        merger.visit(buffers)
        owner = merger.merge_visited()
        node = cls(
            owner,
            uri,
            dict(
                raw_ranges=raw_ranges,
                buffers=buffers,
            ),
            name=name,
            has_node_args=merger.has_nodes,
        )
        owner._add(node, parents=merger.unexecuted_nodes)
        return node

    def _to_builder_node_impl(
        self,
        grf: builder.TaskGraphBuilder,
    ) -> builder.Node[types.ArrayMultiIndex]:
        if self._has_node_args:
            bnr = _graph.BuilderNodeReplacer(self._owner)
            uri = bnr.visit(self._uri)
            kwargs = _graph.filter_kwargs(
                **bnr.visit(self._nodeable_kwargs),
                name=self._name,
            )
        else:
            uri = self._uri
            kwargs = _graph.filter_kwargs(
                **self._nodeable_kwargs,
                name=self._name,
            )
        return grf.array_read(uri, **kwargs)


class SQL(_graph.Node):
    """A Node that executes a SQL query and returns the results."""

    def __init__(
        self,
        owner: _graph.DelayedGraph,
        query: str,
        parameters: _graph.ValOrNodeSeq,
        kwargs: Dict[str, Any],
        has_node_args: bool = False,
    ):
        """Initializer. Users should not manually call this."""
        super().__init__(owner)
        self._query = query
        self._parameters = parameters
        """The parameters to pass to the query.

        This is the only argument that may contain Nodes as input.
        """
        self._kwargs = kwargs
        """Other kwargs to pass to ``grf.sql()``. May not contain Nodes."""
        self._has_node_args = has_node_args

    @classmethod
    def create(
        cls,
        query: str,
        *,
        init_commands: Iterable[str] = _graph.NOTHING,
        parameters: _graph.ValOrNodeSeq = _graph.NOTHING,
        result_format: str = _graph.NOTHING,
        name: Optional[str] = _graph.NOTHING,
    ) -> "SQL":
        """Creates a delayed TileDB Serverless SQL query.

        Allows you to specify a SQL query to be run in TileDB Cloud.

        For more details about the parameters, see
        :meth:`builder.TaskGraphBuilder.sql`.

        :param query: The SQL query to execute. This must be a static string.
        :param init_commands: A sequence of commands to execute before the
            main SQL query whose results you want is executed.
        :param parameters: The parameters to subsitute into ``?``s in ``query``.
            These may be provided as either direct values or as the output
            of upstream Nodes.
        :param result_format: The format to return results in, either
            ``arrow`` (the default) or ``json``.
        :param name: An optional name for the node. If provided, it must be
            unique within the graph.
        """
        merger = _graph.Merger()
        merger.visit(parameters)
        owner = merger.merge_visited()
        node = cls(
            owner,
            query,
            parameters,
            kwargs=dict(
                init_commands=init_commands,
                result_format=result_format,
                name=name,
            ),
            has_node_args=merger.has_nodes,
        )
        owner._add(node, parents=merger.unexecuted_nodes)
        return node

    def _to_builder_node_impl(self, grf: builder.TaskGraphBuilder) -> builder.Node:
        if self._has_node_args:
            bnr = _graph.BuilderNodeReplacer(self._owner)
            parameters = bnr.visit(self._parameters)
        else:
            parameters = self._parameters

        return grf.sql(
            self._query,
            **_graph.filter_kwargs(
                parameters=parameters,
                **self._kwargs,
            ),
        )
