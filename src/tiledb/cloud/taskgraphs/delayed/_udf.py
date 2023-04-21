"""Classes that implement delayed UDFs."""

import datetime
from typing import Any, Dict, Generic, NoReturn, Optional, Tuple, TypeVar, Union

import attrs

from tiledb.cloud._common import functions
from tiledb.cloud.taskgraphs import builder
from tiledb.cloud.taskgraphs import types
from tiledb.cloud.taskgraphs.delayed import _graph

_T = TypeVar("_T")

_NOTHING: Any = attrs.make_class("Nothing", (), frozen=True, slots=True)()
"""Sentinel value to distinguish an unset parameter from None."""


class DelayedFunction(Generic[_T]):
    """The wrapper around a function that makes it delayed-callable."""

    def __init__(self, fn: functions.Funcable[_T], kwargs: Dict[str, Any]):
        """Initializes a new DelayedFunction.

        Users should never have to call this directly.
        """

        self._fn = fn
        self._node_args = kwargs

    @classmethod
    def create(
        cls,
        __fn: functions.Funcable[_T],
        *,
        result_format: Optional[str] = _NOTHING,
        local: bool = _NOTHING,
        image_name: Optional[str] = _NOTHING,
        timeout: Union[datetime.timedelta, int, None] = _NOTHING,
        resource_class: Optional[str] = _NOTHING,
        name: Optional[str] = _NOTHING,
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
        :param local: If set to True, will execute the function on the local
            machine rather than in TileDB Cloud.
        :param image_name: If specified, will execute the UDF within
            the specified image rather than the default image for its language.
        :param timeout: If specified, the length of time after which the UDF
            will be terminated on the server side. If specified as a number,
            a number of seconds. If zero or unset, the UDF will run until
            the server’s configured maximum. Unlike the ``timeout`` parameter to
            Future-like objects, this sets a limit on actual execution time,
            rather than just a limit on how long to wait.
        :param resource_class: If specified, the container resource class
            that this UDF will be executed in.
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
        raw_kwargs = dict(
            result_format=result_format,
            local=local,
            image_name=image_name,
            timeout=timeout,
            resource_class=resource_class,
            name=name,
        )
        node_kwargs = {k: v for k, v in raw_kwargs.items() if v is not _NOTHING}
        return cls(__fn, node_kwargs)

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
        return f"<delayed {functions.full_name(self._fn)}>"


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
        return grf.udf(self._fn._fn, arguments, **self._fn._node_args)

    def __call__(self, *args, **kwargs) -> NoReturn:
        del args, kwargs
        raise TypeError("This is already a Delayed call; it cannot be called again")

    def __repr__(self) -> str:
        return f"<{self._fn}(...) {id(self):x}>"
