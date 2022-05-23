"""A client-side implementation of a task graph Executor.

This module implements a task graph Executor that coordinates the execution of
graph nodes on the client side.
"""

import abc
import enum
import queue
import threading
import uuid
import warnings
from concurrent import futures
from typing import (
    AbstractSet,
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

import urllib3

from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud._common import json_safe
from tiledb.cloud._common import ordered
from tiledb.cloud._common import visitor
from tiledb.cloud._results import results
from tiledb.cloud.rest_api import models
from tiledb.cloud.taskgraphs import _codec
from tiledb.cloud.taskgraphs import executor

Status = executor.Status
_T = TypeVar("_T")
"""Value that a Node yields."""
_NOTHING = object()
"""Sentinel value to distinguish missing values from None."""

if hasattr(futures, "InvalidStateError"):
    InvalidStateError = futures.InvalidStateError  # type: ignore[attr-defined]

else:

    class InvalidStateError(futures._base.Error):  # type: ignore[attr-defined,no-redef]
        """The operation is not allowed in this state."""


class LocalExecutor(executor.Executor["Node"]):
    """Coordinates the execution of a task graph locally."""

    def __init__(
        self,
        graph: executor.GraphStructure,
        namespace: Optional[str] = None,
        api_client: Optional[client.Client] = None,
        name: Optional[str] = None,
        parallel_server_tasks: int = 10,
    ):
        """Sets up a local executor.

        :param graph: The graph to execute, provided either as a JSON result
            or as the Builder object used to create the graph.
        :param namespace: If provided, the namespace to run tasks in.
            If not provided, uses the default namespace.
        :param api_client: An API client object, for using a client other than
            the default.
        :param name: A name to give this execution of your task graph.
        :param parallel_server_tasks: The maximum number of tasks that will be
            run on the server simultaneously.
        """
        super().__init__(graph)
        self.name = name
        self._namespace = namespace or client.default_charged_namespace()
        self._done_node_queue: "queue.Queue[Node]" = queue.Queue()
        """Queue where completed nodes are added as they are done.

        This acts as the event loop for ``_exec_loop.``
        """
        self._inputs: Dict[uuid.UUID, Any] = {}
        self._client = api_client or client.client

        self._active_deps = self._deps.copy()
        """The dependency graph of not-yet-complete nodes.

        This includes both currently-running and to-be-executed Nodes.
        """
        self._running_nodes = ordered.Set[Node]()
        self._failed_nodes = ordered.Set[Node]()
        self._succeeded_nodes = ordered.Set[Node]()

        self._lifecycle_lock = threading.Lock()
        self._status: Status = Status.WAITING
        self._server_graph_uuid: Optional[uuid.UUID] = None

        if self.name:
            prefix = f"task-graph-{self.name}"
        else:
            prefix = repr(self)
        self._event_loop_thread = threading.Thread(
            name=prefix + "-executor",
            target=self._run,
            daemon=True,
        )
        self._pool = futures.ThreadPoolExecutor(
            max_workers=parallel_server_tasks,
            thread_name_prefix=prefix + "-worker",
        )
        self._done_event = threading.Event()
        self._exception: Optional[BaseException] = None

    @property
    def status(self) -> Status:
        with self._lifecycle_lock:
            return self._status

    def execute(self, **inputs: Any) -> None:
        provided_names = frozenset(inputs)
        input_nodes = {
            name: node
            for (name, node) in self._by_name.items()
            if isinstance(node, InputNode)
        }
        try:
            inputs_by_id = {
                input_nodes[name].id: value for (name, value) in inputs.items()
            }
        except KeyError:
            extras = list(provided_names.difference(input_nodes))
            raise TypeError(f"execute() got unexpected arguments {extras}")

        required_names = frozenset(
            name for (name, node) in input_nodes.items() if not node.has_default()
        )
        missing_names = required_names - provided_names
        if missing_names:
            raise TypeError(
                f"execute() missing {len(missing_names)} required keyword-only "
                f"argument(s): {list(missing_names)}"
            )

        with self._lifecycle_lock:
            if self._status is not Status.WAITING:
                raise InvalidStateError(f"Cannot execute a graph in {self._status}")

            self._inputs = inputs_by_id
            self._status = Status.RUNNING

        try:
            result = self._client.task_graph_logs_api.create_task_graph_log(
                namespace=self._namespace,
                log=self._build_log_structure(),
            )
        except rest_api.ApiException as apix:
            # There was a problem submitting the task graph for logging.
            # This should not abort the task graph.
            warnings.warn(UserWarning(f"Could not submit logging metadata: {apix}"))
        else:
            try:
                with self._lifecycle_lock:
                    self._server_graph_uuid = uuid.UUID(hex=result.uuid)
            except ValueError as ve:
                warnings.warn(
                    UserWarning(f"Server-provided graph ID was invalid: {ve}")
                )

        self._event_loop_thread.start()

    def cancel(self) -> bool:
        with self._lifecycle_lock:
            if self._status in (Status.SUCCEEDED, Status.FAILED):
                return False
            self._status = Status.CANCELLED
        return True

    def wait(self, timeout: Optional[float] = None) -> None:
        _wait_for(self._done_event, timeout)

    @property
    def server_graph_uuid(self):
        with self._lifecycle_lock:
            return self._server_graph_uuid

    def _make_node(
        self,
        uid: uuid.UUID,
        name: Optional[str],
        node_json: Dict[str, Any],
    ) -> "Node":
        cls: Type[Node]
        if "array_node" in node_json:
            cls = ArrayNode
        elif "input_node" in node_json:
            cls = InputNode
        elif "sql_node" in node_json:
            cls = SQLNode
        elif "udf_node" in node_json:
            cls = UDFNode
        else:
            raise ValueError("Could not determine node type")
        return cls(uid, self, name, node_json)

    def _run(self):
        """The main event loop of this Executor."""
        try:
            self._start_ready_nodes()
            while self._running_nodes:
                node = self._done_node_queue.get()
                self._handle_node_done(node)
                self._start_ready_nodes()
        except Exception as ex:
            # This means an exception has occurred on the event loop.
            # This should never happen, but to be safe we record our own
            # cancellation.
            self._exception = ex
            for node in self._by_id.values():
                if node.cancel():
                    self._failed_nodes[node.id] = node
        finally:
            with self._lifecycle_lock:
                if self._status is not Status.CANCELLED:
                    if self._failed_nodes:
                        self._status = Status.FAILED
                    else:
                        self._status = Status.SUCCEEDED
            self._done_event.set()
            self._pool.shutdown()
            self._report_server_completion()

    def _handle_node_done(self, node: "Node") -> None:
        assert threading.current_thread() is self._event_loop_thread
        self._running_nodes.discard(node)
        self._active_deps.remove(node)
        if node.status is Status.SUCCEEDED:
            self._succeeded_nodes.add(node)
        else:
            self._exception = self._exception or node._exception
            self._failed_nodes.add(node)

    def _start_ready_nodes(self):
        """Starts all nodes that are ready to run."""
        for node in self._active_deps.roots():
            if node in self._running_nodes:
                continue
            node._set_ready()
            self._running_nodes.add(node)
            node.add_done_callback(self._done_node_queue.put)
            self._pool.submit(self._exec_one_node, node)

    def _exec_one_node(self, node: "Node") -> None:
        """Handles the execution of exactly one Node."""
        if self.status == Status.CANCELLED:
            node.cancel()
            return
        parents = {n.id: n for n in self._deps.parents_of(node)}
        if not all(p.status is Status.SUCCEEDED for p in parents.values()):
            node.cancel()
            return
        else:
            node._exec(parents, self._inputs.get(node.id, _NOTHING))

    def _build_log_structure(self) -> rest_api.TaskGraphLog:
        return rest_api.TaskGraphLog(
            name=self.name,
            namespace=self._namespace,
            nodes=[n._to_log_metadata(self._deps.parents_of(n)) for n in self._deps],
        )

    def _report_server_completion(self) -> None:
        if not self.server_graph_uuid:
            return
        try:
            api_st = _API_STATUSES[self.status]
        except KeyError as ke:
            raise ValueError(
                f"Task graph ended in invalid state {self.status!r}"
            ) from ke
        try:
            client.client.task_graph_logs_api.update_task_graph_log(
                id=str(self.server_graph_uuid),
                namespace=self._namespace,
                log=rest_api.TaskGraphLog(status=api_st),
            )
        except rest_api.ApiException as apix:
            warnings.warn(UserWarning(f"Error reporting graph completion: {apix}"))


_API_STATUSES = {
    Status.SUCCEEDED: rest_api.TaskGraphLogStatus.SUCCEEDED,
    Status.FAILED: rest_api.TaskGraphLogStatus.FAILED,
    Status.CANCELLED: rest_api.TaskGraphLogStatus.CANCELLED,
}


class _ParamFormat(enum.Enum):
    """The format used to encode the result of a parent node for a child."""

    STORED_PARAMS = enum.auto()
    """The node result is encoded in ``CallArgStoredParams`` format.

    Rather than including the actual value in the UDF's parameter list sent to
    the server, this will (when possible) provide the result ID to be
    substituted in server-side. If the node is purely local (e.g., an input),
    this will encode the value itself.
    """
    VALUES = enum.auto()
    """The node result is encoded directly, in ``CallArg`` format.

    This will include the actual result of the node in the parameter list,
    without the need for any server-side processing.
    """


class Node(executor.Node[LocalExecutor, _T], metaclass=abc.ABCMeta):
    """Base class for Nodes to be executed locally.

    All public-facing methods MUST be thread-safe.
    """

    def __init__(self, *args):
        super().__init__(*args)
        self._event = threading.Event()
        self._status: Status = Status.WAITING
        self._exception: Optional[Exception] = None

    # External API

    def result(self, timeout: Optional[float] = None) -> _T:
        self.wait(timeout)
        # Because it's guaranteed that `exception` will *never be written to*
        # after the `_event` is set, we don't need to hold a lock here.
        if self._exception:
            raise self._exception
        return self._result_impl()

    def exception(self, timeout: Optional[float] = None) -> Optional[Exception]:
        self.wait(timeout)
        if self._status is Status.CANCELLED:
            raise futures.CancelledError()
        return self._exception

    def cancel(self) -> bool:
        cancelled = self._set_status_if_can_start(Status.CANCELLED)
        if cancelled:
            # If we were successful at cancelling this Node, we effectively
            # "own" the result fields on this thread. We can set them safely
            # ourselves before firing the Event.
            self._exception = futures.CancelledError()
            self._event.set()
            self._do_callbacks()
        return cancelled

    def wait(self, timeout: Optional[float] = None) -> None:
        _wait_for(self._event, timeout)

    # Internals

    def _status_impl(self) -> Status:
        return self._status

    def _exec(self, parents: Dict[uuid.UUID, "Node"], input_value: Any) -> None:
        """The boilerplate for the ``_exec`` implementation for local Nodes.

        This handles all the lifecycle management for Node execution. It should
        only ever be called by the Executor. Subclasses should instead implement
        ``_exec_impl``, which contains the type-specific behavior.
        """
        if not self._set_status_if_can_start(Status.RUNNING):
            return

        try:
            self._exec_impl(parents, input_value)
        except Exception as ex:
            with self._lifecycle_lock:
                self._status = Status.FAILED
                self._exception = ex
            raise
        else:
            with self._lifecycle_lock:
                self._status = Status.SUCCEEDED
        finally:
            self._event.set()
            self._do_callbacks()

    @abc.abstractmethod
    def _exec_impl(self, parents: Dict[uuid.UUID, "Node"], input_value: Any) -> None:
        """The type-specific behavior of executing a Node."""
        raise NotImplementedError()

    @abc.abstractmethod
    def _result_impl(self) -> _T:
        """Returns the result of this node's execution, if applicable.

        This will only ever be called after ``_event`` is set and the state is
        ``SUCCEEDED``. It should only ever be called inside ``result()``.
        """
        raise NotImplementedError()

    def _assert_succeeded(self) -> None:
        if self._status is not Status.SUCCEEDED:
            raise AssertionError("_encoded_result is only valid for successful nodes")

    def _set_ready(self) -> None:
        self._set_status_if_can_start(Status.READY)

    def _set_status_if_can_start(self, status: Status) -> bool:
        """If this node is allowed to start, updates its status.

        Updates the status of this node, but only if it's unstarted (and is able
        to be started). Used to implement both :meth:`cancel` and the equivalent
        of ``Future.set_running_or_notify_cancel``.
        """
        with self._lifecycle_lock:
            if self._status in (Status.WAITING, Status.READY):
                self._status = status
                return True
            return False

    @abc.abstractmethod
    def _encode_for_param(self, mode: _ParamFormat) -> Any:
        """Encodes the result of this node for use in a JSON parameter list.

        This is used to pass the output of this Node into the parameters of a
        following Node.
        """
        raise NotImplementedError()

    def _to_log_metadata(
        self,
        deps: Iterable["Node"],
    ) -> rest_api.TaskGraphNodeMetadata:
        """Builds the entry that will be used to include in the logs."""
        return rest_api.TaskGraphNodeMetadata(
            client_node_uuid=str(self.id),
            name=self.display_name,
            run_location=self._run_location(),
            depends_on=[str(dep.id) for dep in deps],
        )

    def _run_location(self) -> str:
        """The location where this node will be executed."""
        return rest_api.TaskGraphLogRunLocation.SERVER

    def task_id(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        """The task ID that was returned from the server, if applicable.

        If this was executed on the server side, this should return the UUID of
        the actual execution of this task. If it was purely client-side, or the
        server did not return a UUID, this should return None.
        """
        return None


class ArrayNode(Node):
    """A node representing a read from a TileDB Array.

    This node is not executed by itself; instead, it only appears as an input
    to TileDB UDF nodes.
    """

    def __init__(
        self,
        uid: uuid.UUID,
        owner: LocalExecutor,
        name: Optional[str],
        json_data: Dict[str, Any],
    ):
        super().__init__(uid, owner, name)
        self._array_data = json_data["array_node"]
        array_data = json_data["array_node"]
        self._parameter_id = array_data["parameter_id"]
        self._details: Optional[Dict[str, Any]] = None

    def _exec_impl(self, parents: Dict[uuid.UUID, Node], input_value: Any) -> None:
        assert input_value is _NOTHING
        uri = self._array_data["uri"]
        ranges = self._array_data.get("ranges")
        buffers = self._array_data.get("buffers")
        if parents:
            replacer = _NodeOutputValueReplacer(parents)
            uri = replacer.visit(uri)
            ranges = replacer.visit(ranges)
            buffers = replacer.visit(buffers)
        self._details = dict(
            parameter_id=self._parameter_id,
            uri=uri,
            # TODO: Eliminate the `or []` once we fix the server.
            ranges={"ranges": (ranges or [])},
            buffers=buffers,
        )

    def _result_impl(self):
        raise TypeError("ArrayNode is a virtual node and does not have results.")

    def _udf_array_details(self) -> Dict[str, Any]:
        self._assert_succeeded()
        assert self._details
        return self._details

    def _encode_for_param(self, mode: _ParamFormat):
        del mode  # unused
        self._assert_succeeded()
        return {
            "__tdbudf__": "udf_array_details",
            "udf_array_details": self._udf_array_details(),
        }

    def _run_location(self) -> str:
        return rest_api.TaskGraphLogRunLocation.VIRTUAL


class InputNode(Node):
    def __init__(
        self,
        uid: uuid.UUID,
        owner: LocalExecutor,
        name: Optional[str],
        json_data: Dict[str, Any],
    ):
        super().__init__(uid, owner, name)
        input_data = json_data["input_node"]
        self._default_value_encoded = input_data.get("default_value", _NOTHING)
        self._value: Any = _NOTHING
        self._value_encoded: Any = _NOTHING

    def has_default(self):
        return self._default_value_encoded is not _NOTHING

    def _exec_impl(
        self,
        parents: Dict[uuid.UUID, Node],
        input_value: Any,
        server_graph_uuid: Optional[uuid.UUID] = None,
    ) -> None:
        del server_graph_uuid  # Unused.
        assert not parents, "InputNode cannot depend on anything"
        if input_value is _NOTHING:
            self._value_encoded = self._default_value_encoded
            self._value = _codec.Unescaper().visit(self._value_encoded)
        else:
            self._value = input_value
            self._value_encoded = _codec.Escaper().visit(input_value)

        if self._value_encoded is _NOTHING:
            raise KeyError(f"Input {self.name!r} must be provided")

    def _result_impl(self):
        return self._value

    def _encode_for_param(self, mode: _ParamFormat):
        del mode  # unused
        self._assert_succeeded()
        return self._value_encoded

    def _run_location(self) -> str:
        return rest_api.TaskGraphLogRunLocation.VIRTUAL


class SQLNode(Node):
    """A Node that executes a TileDB SQL query."""

    def __init__(
        self,
        uid: uuid.UUID,
        owner: LocalExecutor,
        name: Optional[str],
        json_data: Dict[str, Any],
    ):
        super().__init__(uid, owner, name)
        self._sql_data = json_data["sql_node"]
        self._task_id: Optional[uuid.UUID] = None
        """The server-side task ID for this node's execution."""
        self._result: Optional[_codec.BinaryResult] = None
        """The bytes of the result, as returned from the server."""

    def task_id(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        self.wait(timeout)
        return self._task_id

    def _exec_impl(self, parents: Dict[uuid.UUID, Node], input_value: Any) -> None:
        assert input_value is _NOTHING

        raw_parameters = self._sql_data.get("parameters") or []
        if parents:
            replacer = _NodeOutputValueReplacer(parents)
            parameters = replacer.visit(raw_parameters)
        else:
            parameters = raw_parameters

        try:
            resp = self.owner._client.sql_api.run_sql(
                namespace=self.owner._namespace,
                sql=models.SQLParameters(
                    name=self.display_name,
                    query=self._sql_data["query"],
                    init_commands=self._sql_data.get("init_commands"),
                    parameters=parameters,
                    result_format=self._sql_data["result_format"],
                    store_results=True,
                    client_node_uuid=str(self.id),
                    task_graph_uuid=str(self.owner._server_graph_uuid),
                ),
                _preload_content=False,
            )
        except rest_api.ApiException as apix:
            self._task_id = results.extract_task_id(apix)
            raise
        self._task_id = results.extract_task_id(resp)
        self._result = _codec.BinaryResult.from_response(resp)

    def _result_impl(self):
        return self._result.decode()

    def _encode_for_param(self, mode: _ParamFormat) -> Dict[str, Any]:
        self._assert_succeeded()
        if mode is _ParamFormat.STORED_PARAMS:
            if self._task_id:
                return {
                    _codec.SENTINEL_KEY: "stored_param",
                    "task_id": str(self._task_id),
                }
        assert self._result
        return self._result._tdb_to_json()


class UDFNode(Node):
    """A Node that will actually execute a UDF."""

    def __init__(
        self,
        uid: uuid.UUID,
        owner: LocalExecutor,
        name: Optional[str],
        json_data: Dict[str, Any],
    ):
        super().__init__(uid, owner, name)
        udf_data: Dict[str, Any] = json_data["udf_node"]
        self._udf_data = udf_data
        """The UDF details, in JSON dict format."""
        self._registered_udf_name: Optional[str] = udf_data.get("registered_udf_name")
        """The UDF name, used to give this node a fallback name."""
        self._task_id: Optional[uuid.UUID] = None
        """The server-side task ID for this node's execution."""
        self._result: Optional[_codec.BinaryResult] = None
        """The bytes of the result, as returned from the server."""

    @property
    def fallback_name(self) -> str:
        if self._registered_udf_name:
            return f"UDF {self._registered_udf_name}"
        return super().fallback_name

    def task_id(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        self.wait(timeout)
        return self._task_id

    def _exec_impl(self, parents: Dict[uuid.UUID, "Node"], input_value: Any) -> None:
        assert input_value is _NOTHING

        # Parse the arguments.
        raw_args: List[Any] = self._udf_data["arguments"] or []
        stored_param_ids: AbstractSet[uuid.UUID]
        arrays: Sequence[Dict[str, Any]]
        if parents:
            replacer = _UDFParamReplacer(parents, _ParamFormat.STORED_PARAMS)
            replaced_args = replacer.visit(raw_args)
            stored_param_ids = ordered.FrozenSet(
                filter(None, (n.task_id() for n in replacer.seen_nodes))
            )
            arrays = tuple(
                n._udf_array_details()
                for n in replacer.seen_nodes
                if isinstance(n, ArrayNode)
            )
        else:
            # If there are no parents, then we only have the existing args.
            replaced_args = raw_args
            stored_param_ids = frozenset()
            arrays = []

        # Set up the basics of the call.
        udf_call = models.MultiArrayUDF(
            task_name=self.display_name,
            stored_param_uuids=json_safe.Value([str(uid) for uid in stored_param_ids]),
            arrays=json_safe.Value(arrays),
            arguments_json=json_safe.Value(replaced_args),
            store_results=True,
            result_format=self._udf_data.get("result_format") or "python_pickle",
            client_node_uuid=str(self.id),
            task_graph_uuid=str(self.owner._server_graph_uuid),
        )

        # Executable code.
        exec_code = self._udf_data.get("executable_code")
        if exec_code:
            udf_call._exec = exec_code
        else:
            try:
                udf_call.udf_info_name = self._udf_data["registered_udf_name"]
            except KeyError as ke:
                raise AssertionError("Neither executable code nor UDF name set") from ke

        # Set up the environment. The default value of everything in the
        # udf_call object is `None`, so setting it to None is equivalent to
        # leaving it unset.
        env: Dict[str, str] = self._udf_data.get("environment", {})
        udf_call.image_name = env.get("image_name")
        udf_call.language = env.get("language")
        udf_call.version = env.get("language_version")

        # Actually make the call.
        api = self.owner._client.udf_api
        try:
            resp: urllib3.HTTPResponse = api.submit_multi_array_udf(
                namespace=self.owner._namespace,
                udf=udf_call,
                _preload_content=False,
            )
        except rest_api.ApiException as exc:
            self._task_id = results.extract_task_id(exc)
            if "RETRY_WITH_PARAMS" not in exc.body:
                raise
        else:
            self._task_id = results.extract_task_id(resp)
            self._result = _codec.BinaryResult.from_response(resp)
            return

        # Our first request failed with a "RETRY_WITH_PARAMS" error.
        # Retry, but substitute in all stored parameters.
        values_replacer = _UDFParamReplacer(parents, _ParamFormat.VALUES)

        udf_call.stored_param_uuids = []
        udf_call.arguments_json = values_replacer.visit(raw_args)
        try:
            resp = api.submit_generic_udf(
                namespace=self.owner._namespace,
                udf=udf_call,
                _preload_content=False,
            )
        except rest_api.ApiException as exc:
            self._task_id = results.extract_task_id(exc)
            raise
        self._task_id = results.extract_task_id(resp)
        self._result = _codec.BinaryResult.from_response(resp)

    def _result_impl(self):
        return self._result.decode()

    def _encode_for_param(self, mode: _ParamFormat):
        self._assert_succeeded()
        if mode is _ParamFormat.STORED_PARAMS:
            if self._task_id is not None:
                return {
                    _codec.SENTINEL_KEY: "stored_param",
                    "task_id": str(self.task_id()),
                }
        assert self._result
        return self._result._tdb_to_json()


class _NodeOutputValueReplacer(_codec.Unescaper):
    """An Unescaper for when the output value of a node must be used locally.

    For Nodes where non–UDF-parameter inputs may be Nodes (e.g. array query
    ranges), this replaces the node's input with the actual value output by
    the previous node.
    """

    def __init__(self, nodes: Dict[uuid.UUID, Node]):
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


class _UDFParamReplacer(visitor.ReplacingVisitor):
    # This isn't an Unescaper since we don't want to unescape non-JSON values,
    # we only want to replace parent nodes with their data.

    def __init__(
        self,
        nodes: Dict[uuid.UUID, Node],
        mode: _ParamFormat,
    ):
        super().__init__()
        self._nodes = nodes
        self._mode = mode
        self.seen_nodes: ordered.Set[Node] = ordered.Set()
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


def _wait_for(evt: threading.Event, timeout: Optional[float]) -> None:
    if not evt.wait(timeout):
        raise futures.TimeoutError(f"timed out after {timeout} sec")
