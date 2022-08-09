"""Classes that implement delayed UDFs."""

import functools
from typing import Any, Callable, Dict, Generic, NoReturn, Optional, Tuple, TypeVar

from tiledb.cloud import utils
from tiledb.cloud.taskgraphs import builder
from tiledb.cloud.taskgraphs import types
from tiledb.cloud.taskgraphs.delayed import _graph
from tiledb.cloud.taskgraphs.delayed import _nodes

_T = TypeVar("_T")


class DelayedFunction(Generic[_T]):
    """The wrapper around a function that makes it delayed-callable."""

    def __init__(self, fn: utils.Funcable[_T], kwargs: Dict[str, Any]):
        """Initializes a new DelayedFunction.

        Users should never have to call this directly.
        """

        self._fn = fn
        self._node_args = kwargs

    @classmethod
    def create(
        cls,
        __fn: utils.Funcable[_T],
        *,
        result_format: Optional[str] = _graph.NOTHING,
        image_name: Optional[str] = _graph.NOTHING,
        name: Optional[str] = _graph.NOTHING,
    ) -> "DelayedFunction[_T]":
        """Wraps the given function to later call it in a delayed task graph.

        All parameters that you provide to this function configure properties
        about the UDF node that will be executed. You then ``__call__`` the
        returned :class:`DelayedFunction` with the parameters that will be
        passed to your UDF at execution time. The return value of *that* call
        is a :class:`DelayedCall` which is used to build a task graph::

            # Creates a DelayedFunction:
            delayed_fn = delayed.udf(my_fn, name="call_my_fn")
            # Calling the DelayedFunction gives you a DelayedCall.
            # The parameters here are as if you were calling `my_fn`.
            node = delayed_fn(my_params, ...)

        :param __fn: The function to call. This may be a Python callable or
            the name of a registered UDF.
        :param result_format: The format to return results in.
        :param image_name: If specified, will execute the UDF within
            the specified image rather than the default image for its language.
        :param name: If specified, the name of this node within the graph.
            If provided, this must be unique.
        """
        # NOTE: Parameters here are repeated from builder.TaskGraphBuilder.udf
        # for good developer experience when reading documentation / using
        # autocomplete.

        # Create a kwargs dict with only the explicitly-set arguments,
        # so that the default values of the named arguments to
        # `TaskGraphBuilder.udf` are used if unset rather than having to keep
        # them in sync.
        return cls(
            __fn,
            dict(
                result_format=result_format,
                image_name=image_name,
                name=name,
            ),
        )

    def set(self, **updates: Any) -> "DelayedFunction[_T]":
        """Returns a new DelayedFunction with the given argument updates.

        Arguments are the same as :meth:`create` (i.e. the `Delayed` function).
        """
        new_args = dict(self._node_args)
        new_args.update(updates)
        return DelayedFunction(self._fn, new_args)

    def __call__(self, *args, **kwargs) -> "DelayedCall[_T]":
        """Sets up the actual function call with your given parameters.

        Parameters can be provided either as raw values or as the results of
        previous delayed nodes (whether delayed UDFs, arrays, or SQL queries).
        The previous nodes' output values will be substituted into the
        actual parameter list when your UDF is called.
        """
        return DelayedCall._create(self, args, kwargs)

    def __repr__(self) -> str:
        return f"<delayed {utils.func_name(self._fn)}>"


class DelayedCall(_graph.Node[_T]):
    """A node in a delayed task graph that represents a UDF call.

    Once executed, this node acts like a Future, and its results can be accessed
    with the usual methods. A user should never have to directly instantiate
    a DelayedCall; it is created by ``__call__``ing a :class:`DelayedFunction`.
    """

    def __init__(
        self,
        owner: _graph.DelayedGraph,
        fn: DelayedFunction[_T],
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
        *,
        has_node_args: bool,
    ):
        """Initializes this DelayedCall.

        Users should never call this directly.
        """
        super().__init__(owner)
        self._fn = fn
        self._args = args
        self._kwargs = kwargs
        self._has_node_args = has_node_args

    @classmethod
    def _create(
        cls,
        fn: DelayedFunction[_T],
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
    ) -> "DelayedCall[_T]":
        """Factory function for a DelayedCall.

        Users should never call this directly.
        """
        merger = _graph.Merger()
        merger.visit((args, kwargs))
        owner = merger.merge_visited()

        dc = DelayedCall(owner, fn, args, kwargs, has_node_args=merger.has_nodes)
        owner._add(dc, parents=merger.unexecuted_nodes)
        return dc

    def _to_builder_node_impl(self, grf: builder.TaskGraphBuilder) -> builder.Node[_T]:
        if self._has_node_args:
            bnr = _graph.BuilderNodeReplacer(self._owner)
            args, kwargs = bnr.visit((self._args, self._kwargs))
            arguments = types.Arguments(args, kwargs)
        else:
            arguments = types.Arguments(self._args, self._kwargs)
        return grf.udf(
            self._fn._fn, arguments, **_graph.filter_dict(self._fn._node_args)
        )

    def __call__(self, *args, **kwargs) -> NoReturn:
        del args, kwargs
        raise TypeError("This is already a Delayed call; it cannot be called again")

    def __repr__(self) -> str:
        return f"<{self._fn}(...) {id(self):x}>"


def array_udf(
    uri: _graph.ValOrNode[str],
    func: utils.Funcable[_T],
    *,
    raw_ranges: Optional[_graph.ValOrNodeSeq] = _graph.NOTHING,
    buffers: Optional[_graph.ValOrNodeSeq[str]] = _graph.NOTHING,
    **delayed_func_kwargs,
) -> Callable[..., DelayedCall]:
    """Shortcut to build a UDF whose first parameter is a TileDB Array.

    This is a combination of the ``Delayed`` and ``DelayedArray`` function.
    When you call it, you get a delayed callable that is equivalent to a
    :class:`DelayedFunction` with its first parameter pre-populated as a TileDB
    Array::

        d_arr_udf = DelayedArrayUDF(
            "tiledb://some/array",
            my_func,
            raw_ranges=[[0, 10], []],
            buffers=["x", "y", "height"],
            image_name="example-image",
        )
        output = d_arr_udf("topological", colors=["orange", "purple"])
        # The UDF that is executed will be:
        #   my_func(some_array, "topological", colors=["orange", "purple"])

    For a detailed description of the parameters to this function, see
    :meth:`_nodes.Array.create` and :meth:`DelayedFunction.create`.
    """
    arr_node = _nodes.Array.create(
        uri,
        raw_ranges=raw_ranges,
        buffers=buffers,
    )
    fn = DelayedFunction.create(func, **delayed_func_kwargs)
    return functools.partial(fn, arr_node)
