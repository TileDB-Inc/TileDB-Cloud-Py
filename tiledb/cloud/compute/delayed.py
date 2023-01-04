import abc
import functools
import inspect
import uuid
import warnings
from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
)

import attrs

from tiledb.cloud import array
from tiledb.cloud import rest_api
from tiledb.cloud import sql
from tiledb.cloud import utils
from tiledb.cloud._common import futures
from tiledb.cloud._common import ordered
from tiledb.cloud._common import visitor
from tiledb.cloud.taskgraphs import builder
from tiledb.cloud.taskgraphs import client_executor
from tiledb.cloud.taskgraphs import depgraph
from tiledb.cloud.taskgraphs import executor
from tiledb.cloud.taskgraphs import registration
from tiledb.cloud.taskgraphs import types


class ParentFailedError(futures.CancelledError):
    """Raised when the parent of a :class:`_DelayedNode` fails.

    This is separate from :class:`executor.ParentFailedError` because that type
    is specific to :class:`executor.Node`s.
    """

    def __init__(self, cause: Exception, node: Optional["_DelayedNode"]):
        node_str = f"node {node}" if node else "unknown node"
        super().__init__(f"{cause} on {node_str}")
        self.cause = cause
        self.node = node


class _DelayedGraph:
    def __init__(self):
        self._deps = depgraph.DepGraph[_DelayedNode]()
        self._builder: Optional[builder.TaskGraphBuilder] = None
        self._execution: Optional[client_executor.LocalExecutor] = None
        self._exec_to_node: Dict[executor.Node, "_DelayedNode"] = {}

    def _absorb(self, other: "_DelayedGraph") -> None:
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
        # TODO: address name conflicts (reject? rename?)

    def _add(self, n: "_DelayedNode", *, parents: Iterable["_DelayedNode"]) -> None:
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

    def _exec_node(self, n: "_DelayedNode") -> executor.Node:
        """Gets the execution node associated with the given Delayed node."""
        exec = self._get_execution()
        bn = n._builder_node
        assert bn, "node must be built if executing"
        return exec.node(bn)

    def _delayed_node(self, n: executor.Node) -> Optional["_DelayedNode"]:
        """Gets the DelayedNode associated with a certain executed Node."""
        return self._exec_to_node.get(n)

    def _add_dep(self, *, parent: "_DelayedNode", child: "_DelayedNode") -> None:
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
        self._execution = None
        for node in self._deps:
            node._builder_node = None

    def _build(self) -> Tuple[builder.TaskGraphBuilder, client_executor.LocalExecutor]:
        """Transforms this graph into its TaskGraphBuilder (if needed)."""
        if not self._builder:
            bld = builder.TaskGraphBuilder()
            for node in self._deps:
                node._to_builder_node(bld)
                child_in = node._input_dep_node()

                # Include parent–child relationships that are not specified
                # by the params.
                for parent in self._deps.parents_of(node):
                    assert parent._builder_node
                    built_parent = parent._builder_node
                    bld.add_dep(parent=built_parent, child=child_in)
            self._builder = bld
            self._execution = client_executor.LocalExecutor(bld)
        assert self._execution
        return self._builder, self._execution

    def _register(self, name: str, *, namespace: Optional[str] = None) -> None:
        bld, _ = self._build()
        registration.register(bld, name, namespace=namespace)

    def _visualize(self):
        self._build()
        return self._get_execution().visualize()

    def _start(
        self,
        *,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
    ) -> None:
        """Starts execution of this graph (if not yet started)."""
        _, exec = self._build()
        if exec.status is not executor.Status.WAITING:
            return
        if name:
            exec.name = name
        # We're allowed to assign an Optional[str] here.
        exec.namespace = namespace  # type: ignore[assignment]
        exec.execute()
        # Ensure that all the ``done_callback``s that were registered before
        # starting the graph are executed.
        for node in self._deps:
            exec_node = self._exec_node(node)
            self._exec_to_node[exec_node] = node
            for cb in node._pre_start_callbacks:
                exec_node.add_done_callback(cb)


class _DelayedNode(futures.FutureLike, metaclass=abc.ABCMeta):
    def __init__(self, owner: _DelayedGraph, name: Optional[str]):
        self.timeout: Optional[float] = None
        """Maximum time to wait for results when calling ``compute``.

        This will not cut off execution.
        """
        self._owner = owner
        """The graph that this Node belongs to.

        This may change during the building process, but is fixed once execution
        starts.
        """
        self._builder_node: Optional[builder.Node] = None
        """The builder node that this represents when the graph is built/run.

        This is used both in the process of building the graph using the
        :class:`builder.TaskGraphBuilder` (as the node to build, and as the
        input to downstream nodes) and during execution as a way to get the
        :class:`executor.Node` which represents what is actually happening.

        This is only set up when the graph is actually built for either
        registration or startup.
        """
        self._pre_start_callbacks: List[Callable[[_DelayedNode], Any]] = []
        """``done_callback``s that were added before this Node was started."""

        self._name: Optional[str] = name

    @property
    def name(self) -> str:
        try:
            name = self._exec_node().name
        except futures.InvalidStateError:
            pass
        else:
            name = self._name
        return name or repr(self)

    @name.setter
    def name(self, to: Optional[str]) -> None:
        if self._finalized():
            raise futures.InvalidStateError("cannot set a name after starting a node")
        self._name = to

    def depends_on(self, other: "_DelayedNode") -> None:
        self._owner._absorb(other._owner)
        self._owner._add_dep(parent=other, child=self)

    def set_timeout(self, value: Optional[float]) -> None:
        """Sets the max time to wait for results."""
        self.timeout = value

    def compute(
        self, namespace: Optional[str] = None, name: Optional[str] = None
    ) -> Any:
        self._owner._start(namespace=namespace, name=name)
        return self.result(self.timeout)

    # Future-like methods

    def result(self, timeout: Optional[float] = None) -> Any:
        try:
            return self._exec_node().result(timeout)
        except executor.ParentFailedError as pfe:
            raise self._replace_pfe_node(pfe) from pfe

    def exception(self, timeout: Optional[float] = None) -> Optional[Exception]:
        exc = self._exec_node().exception(timeout)
        if isinstance(exc, executor.ParentFailedError):
            return self._replace_pfe_node(exc)
        return exc

    def cancel(self) -> bool:
        return self._exec_node().cancel()

    def done(self) -> bool:
        try:
            return self._exec_node().done()
        except futures.InvalidStateError:
            return False

    def cancelled(self) -> bool:
        try:
            return self._exec_node().done()
        except futures.InvalidStateError:
            return False

    def running(self) -> bool:
        try:
            return self._exec_node().running()
        except futures.InvalidStateError:
            return False

    def add_done_callback(self, fn: Callable[["_DelayedNode"], None]) -> None:
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

        if self._finalized():
            self._exec_node().add_done_callback(proxy)
        else:
            self._pre_start_callbacks.append(proxy)

    # Extra methods

    finished = done  # Alias.

    @property
    def future(self) -> futures.FutureLike:
        return self

    def retry(self) -> bool:
        return self._exec_node().retry()

    def retry_all(self) -> None:
        return self._owner._get_execution().retry_all()

    @property
    def status(self) -> executor.Status:
        try:
            return self._exec_node().status
        except futures.InvalidStateError:
            return executor.Status.WAITING

    @property
    def error(self) -> Optional[Exception]:
        try:
            return self.exception(0)
        except (futures.InvalidStateError, futures.TimeoutError):
            return None
        except Exception as exc:
            return exc

    def task_id(self) -> Optional[uuid.UUID]:
        try:
            return self._exec_node().task_id(0)
        except futures.TimeoutError:
            return None

    def wait(self, timeout: Optional[float] = None) -> None:
        self._exec_node().wait(timeout)

    def visualize(self):
        return self._owner._visualize()

    @staticmethod
    def all(futures: Sequence["_DelayedNode"], namespace: Optional[str] = None) -> list:
        if not futures:
            return []
        first = futures[0]
        for other in futures[1:]:
            first._owner._absorb(other._owner)
        return [ft.compute(namespace=namespace) for ft in futures]

    def _replace_pfe_node(self, pfe: executor.ParentFailedError) -> ParentFailedError:
        return ParentFailedError(pfe.cause, self._owner._delayed_node(pfe.node))

    def _finalized(self) -> bool:
        return bool(self._owner._execution)

    def _exec_node(self) -> executor.Node:
        return self._owner._exec_node(self)

    def _to_builder_node(self, grf: builder.TaskGraphBuilder) -> builder.Node:
        """Builds this node into the provided graph and returns the result."""
        self._builder_node = self._to_builder_node_impl(grf)
        return self._builder_node

    @abc.abstractmethod
    def _to_builder_node_impl(self, grf: builder.TaskGraphBuilder) -> builder.Node:
        """The type-specific implementation that builds a builder Node."""
        raise NotImplementedError()

    def _input_dep_node(self) -> builder.Node:
        assert self._builder_node
        return self._builder_node


_C = TypeVar("_C", bound=Callable)


def _add_all_attr(t: _C) -> _C:
    @functools.wraps(t)
    def call(*args, **kwargs):
        return t(*args, **kwargs)

    call.all = _DelayedNode.all  # type: ignore[attr-defined]
    return call  # type: ignore[return-value]


class _DelayedCall(_DelayedNode):

    _RESERVED_KWARGS = frozenset(
        (
            "namespace",
            "image_name",
            "http_compressor",
            "include_source_lines",
            "task_name",
            "result_format",
            "result_format_version",
            "store_results",
            "stored_param_uuids",
            "timeout",
            "resource_class",
            "_download_results",
            "dag",
        )
    )

    @classmethod
    @_add_all_attr
    def create(
        cls,
        func_exec: utils.Funcable,
        *args,
        name: Optional[str] = None,
        task_name: Optional[str] = None,
        local: bool = False,
        local_mode: bool = False,
        **kwargs,
    ) -> "_DelayedCall":
        reserved_kw = _pop_keys(kwargs, cls._RESERVED_KWARGS)

        merger = _Merger()
        merger.visit(args)
        merger.visit(kwargs)
        owner = merger.merge_visited()
        result = cls(
            owner,
            name or task_name,
            reserved_kw,
            func_exec,
            args,
            kwargs,
            local=local or local_mode,
            has_node_args=merger.has_nodes,
        )
        owner._add(result, parents=merger.unexecuted_nodes)
        return result

    def __init__(
        self,
        owner: _DelayedGraph,
        name: Optional[str],
        reserved_kwargs: Dict[str, Any],
        fn: utils.Funcable,
        user_args: Tuple[Any, ...],
        user_kwargs: Dict[str, Any],
        *,
        local: bool,
        has_node_args: bool,
    ):
        super().__init__(owner, name)
        self._reserved_kwargs = reserved_kwargs
        self._fn = fn
        self._user_args = user_args
        self._user_kwargs = user_kwargs
        self._local = local
        self._has_node_args = has_node_args

    def __call__(self, *args, **kwargs) -> "_DelayedCall":
        """Adds more arguments to this call."""
        self._owner._invalidate_builder()

        reserved_kw = _pop_keys(kwargs, self._RESERVED_KWARGS)
        self._reserved_kwargs.update(reserved_kw)
        merger = _Merger()
        merger.visit(args)
        merger.visit(kwargs)
        merger.merge_into(self._owner)
        for other in merger.unexecuted_nodes:
            self.depends_on(other)
        self._user_args += args
        self._user_kwargs.update(kwargs)
        self._has_node_args = self._has_node_args or merger.has_nodes
        return self

    def _to_builder_node_impl(self, grf: builder.TaskGraphBuilder) -> builder.Node:
        bnr = _BuilderNodeReplacer(self._owner)
        user_args, user_kwargs = self._user_args, dict(self._user_kwargs)
        if self._has_node_args:
            user_args, user_kwargs = bnr.visit((user_args, user_kwargs))
        arguments = types.Arguments(user_args, user_kwargs)

        kwargs: Dict[str, Any] = {}

        if self._local:
            kwargs["local"] = self._local
            pass

        name = self._reserved_kwargs.get("task_name", self._name)
        if name is not None:
            kwargs["name"] = name

        include_source = self._reserved_kwargs.get("include_source_lines")
        if include_source is not None:
            kwargs["include_source"] = include_source

        # TODO: _download_results

        copy_keys = (
            "image_name",
            "layout",
            "name",
            "namespace",
            "resource_class",
            "result_format",
            "timeout",
        )
        for k in copy_keys:
            try:
                kwargs[k] = self._reserved_kwargs[k]
            except KeyError:
                pass
        return grf.udf(self._fn, arguments, **kwargs)


Delayed = _DelayedCall.create


class _DelayedSQL(_DelayedNode):

    _SIGNATURE = inspect.signature(sql.exec_base)

    @classmethod
    @_add_all_attr
    def create(
        cls,
        *args,
        name: Optional[str] = None,
        **kwargs,
    ) -> "_DelayedSQL":
        owner = _DelayedGraph()
        result = cls(owner, name, args, kwargs)
        owner._add(result, parents=())
        return result

    def __init__(
        self,
        owner: _DelayedGraph,
        name: Optional[str],
        args: tuple,
        kwargs: Dict[str, Any],
    ):
        super().__init__(owner, name)
        self._args = args
        self._kwargs = kwargs
        self._sql_node: Optional[builder.Node] = None
        """Separate storage for the SQL node if we have to convert to Pandas."""

    def __call__(self, *args, **kwargs) -> "_DelayedSQL":
        self._args += args
        self._kwargs.update(kwargs)
        return self

    def _to_builder_node_impl(self, grf: builder.TaskGraphBuilder) -> builder.Node:
        resolved = self._SIGNATURE.bind(*self._args, **self._kwargs)
        resolved.apply_defaults()
        bound = resolved.arguments
        result_format = bound["result_format"] or "arrow"

        self._sql_node = grf.sql(
            bound["query"],
            name=bound["task_name"] or self._name,
            namespace=bound["namespace"],
            init_commands=bound["init_commands"] or (),
            parameters=bound["parameters"] or (),
            result_format=result_format,
            # TODO: resource_class, store_results
        )

        if bound.get("raw_results"):
            return self._sql_node

        def pandas_convert(data):
            import pandas as pd
            import pyarrow as pa

            if result_format == "arrow":
                assert isinstance(data, pa.Table)
                return data.to_pandas()
            if result_format == "json":
                return pd.DataFrame(data)

        return grf.udf(pandas_convert, types.args(self._sql_node))

    def _input_dep_node(self) -> builder.Node:
        assert self._sql_node
        return self._sql_node


DelayedSQL = _DelayedSQL.create


_DAC_T = TypeVar("_DAC_T", bound="_DelayedArrayCommon")


class _DelayedArrayCommon(_DelayedNode, metaclass=abc.ABCMeta):
    """Common implementation stuff for the Delayed(Multi)ArrayUDFs."""

    _SIGNATURE: inspect.Signature

    def __init__(
        self,
        owner: _DelayedGraph,
        name: Optional[str],
        args: tuple,
        kwargs: Dict[str, Any],
        *,
        has_node_args: bool,
    ):
        super().__init__(owner, name)
        self._args = args
        self._kwargs = kwargs
        self._has_node_args = has_node_args

    @classmethod
    @_add_all_attr
    def create(
        cls: Type[_DAC_T],
        *args,
        name: Optional[str] = None,
        **kwargs,
    ) -> _DAC_T:
        merger = _Merger()
        merger.visit(args)
        merger.visit(kwargs)
        owner = merger.merge_visited()
        result = cls(owner, name, args, kwargs, has_node_args=merger.has_nodes)
        owner._add(result, parents=merger.unexecuted_nodes)
        return result

    def __call__(self: _DAC_T, *args, **kwargs) -> _DAC_T:
        merger = _Merger()
        merger.visit(args)
        merger.visit(kwargs)
        merger.merge_into(self._owner)
        for other in merger.unexecuted_nodes:
            self.depends_on(other)
        self._args += args
        self._kwargs.update(kwargs)
        self._has_node_args = self._has_node_args or merger.has_nodes
        return self


class _DelayedArrayUDF(_DelayedArrayCommon):

    _SIGNATURE = inspect.signature(array.apply_base)

    def _to_builder_node_impl(self, grf: builder.TaskGraphBuilder) -> builder.Node:
        bound = self._SIGNATURE.bind(*self._args, **self._kwargs)
        bound.apply_defaults()
        arg_dict: Dict[str, Any] = bound.arguments
        if self._has_node_args:
            bnr = _BuilderNodeReplacer(self._owner)
            arg_dict = bnr.visit(arg_dict)

        ranges = array.parse_ranges(arg_dict["ranges"])
        array_node = grf.array_read(
            arg_dict["uri"],
            raw_ranges=ranges.value,
            buffers=arg_dict.get("buffers"),
            layout=arg_dict.get("layout"),
        )
        node: builder.Node = grf.udf(
            arg_dict["func"],
            types.args(array_node, **arg_dict["kwargs"]),
            name=arg_dict.get("task_name", self._name),
            result_format=arg_dict["result_format"],
            include_source=arg_dict["include_source_lines"],
            resource_class=arg_dict["resource_class"],
            image_name=arg_dict["image_name"],
            timeout=arg_dict["timeout"],
            namespace=arg_dict["namespace"],
            # TODO: store_results
        )
        return node


DelayedArrayUDF = _DelayedArrayUDF.create


class _DelayedMultiArrayUDF(_DelayedArrayCommon):

    _SIGNATURE = inspect.signature(array.exec_multi_array_udf_base)

    def _to_builder_node_impl(self, grf: builder.TaskGraphBuilder) -> builder.Node:
        bound = self._SIGNATURE.bind(*self._args, **self._kwargs)
        bound.apply_defaults()
        arg_dict: Dict[str, Any] = bound.arguments
        if self._has_node_args:
            bnr = _BuilderNodeReplacer(self._owner)
            arg_dict = bnr.visit(arg_dict)

        al: array.ArrayList = arg_dict["array_list"]
        arrays = al.get()
        array_args = tuple(_array_details_to_node(arr, grf) for arr in arrays)

        array_node_arg: tuple
        if not array_args:
            array_node_arg = ()
        elif len(array_args) == 1:
            array_node_arg = (array_args[0],)
        else:
            array_node_arg = (array_args,)

        return grf.udf(
            arg_dict["func"],
            types.args(*array_node_arg, **arg_dict["kwargs"]),
            name=arg_dict.get("task_name", self._name),
            result_format=arg_dict["result_format"],
            include_source=arg_dict["include_source_lines"],
            resource_class=arg_dict["resource_class"],
            image_name=arg_dict["image_name"],
            timeout=arg_dict.get("timeout"),
            namespace=arg_dict["namespace"],
            # TODO: store_results
        )


DelayedMultiArrayUDF = _DelayedMultiArrayUDF.create


def _array_details_to_node(
    details: rest_api.UDFArrayDetails, grf: builder.TaskGraphBuilder
) -> builder.Node:
    return grf.array_read(
        details.uri,
        # details.ranges.ranges is a json_safe.Value.
        raw_ranges=details.ranges.ranges.value,
        buffers=details.buffers,
        layout=details.ranges.layout,
    )


class _Merger(visitor.ReplacingVisitor):
    """Crawls data structures to find parent delayed Nodes to merge together."""

    def __init__(self):
        super().__init__()
        self.has_nodes = False
        """Has this visitor seen any parent Nodes?

        Both unexecuted and executed Nodes are included in this set, since
        previously-executed nodes must still have their results substituted in
        at execution time.
        """

        self.unexecuted_nodes = ordered.Set[_DelayedNode]()
        """All the nodes seen by this visitor from not-yet-executed graphs.

        Nodes that are not part of graphs that are being executed can have their
        graph structure (and what graph they are a part of) changed at will.
        Nodes that are part of graphs that have been executed are finalized and
        cannot have their structure changed; instead they must be treated as
        regular input data.
        """

    def merge_visited(self) -> _DelayedGraph:
        """Merges all unexecuted Nodes into the same DelayedGraph, returning it.

        The DelayedGraph returned by this method is used as the owner of the
        newly-built Node.
        """
        new_owner: Optional[_DelayedGraph] = None
        for parent in self.unexecuted_nodes:
            if new_owner is None:
                new_owner = parent._owner
            else:
                new_owner._absorb(parent._owner)
        return new_owner or _DelayedGraph()

    def merge_into(self, owner: _DelayedGraph) -> None:
        for parent in self.unexecuted_nodes:
            owner._absorb(parent._owner)

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if isinstance(arg, _DelayedNode):
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


class _BuilderNodeReplacer(visitor.ReplacingVisitor):
    """Replaces delayed Nodes with builder Nodes for building a task graph."""

    def __init__(self, dg: _DelayedGraph):
        super().__init__()
        self._dg = dg

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if isinstance(arg, _DelayedNode):
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


_NOTHING: Any = attrs.make_class("Nothing", (), frozen=True, slots=True)()


def _pop_keys(source: Dict[str, Any], keys: Collection[str]) -> Dict[str, Any]:
    popseq = ((k, source.pop(k, _NOTHING)) for k in keys)
    return {k: v for k, v in popseq if v is not _NOTHING}
