import collections
import datetime
import itertools
import json
import numbers
import threading
import time
import uuid
import warnings
from typing import (
    Any,
    Callable,
    Counter,
    Deque,
    Dict,
    FrozenSet,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
)

from .. import array
from .. import client
from .. import rest_api
from .. import tiledb_cloud_error as tce
from .. import udf
from .._common import functions
from .._common import futures
from .._common import utils
from .._common import visitor
from .._results import codecs
from .._results import results
from .._results import stored_params
from .._results import tiledb_json
from .._results import types
from ..rest_api import models
from ..sql import _execution as _sql_exec
from ..taskgraphs import _results as _tg_results
from . import status as st
from . import visualization as viz
from .mode import Mode

Status = st.Status  # Re-export for compabitility.
_T = TypeVar("_T")
# Special string included in server errors when there is a problem loading
# stored parameters.
_RETRY_MSG = "RETRY_WITH_PARAMS"

_REPORT_TIMEOUT_SECS = 10
"""The maximum request time when submitting non-essential log information."""

_SKIP_BATCH_UDF_KWARGS = [
    "image_name",
    "timeout",
    "result_format",
    "retry_strategy",
    "deadline",
    "access_credentials_name",
]

_TASK_GRAPH_LOG_STATUS_TO_STATUS_MAP = {
    models.TaskGraphLogStatus.SUBMITTED: Status.NOT_STARTED,
    models.TaskGraphLogStatus.RUNNING: Status.RUNNING,
    models.TaskGraphLogStatus.IDLE: Status.NOT_STARTED,
    models.TaskGraphLogStatus.ABANDONED: Status.CANCELLED,
    models.TaskGraphLogStatus.SUCCEEDED: Status.COMPLETED,
    models.TaskGraphLogStatus.FAILED: Status.FAILED,
    models.TaskGraphLogStatus.CANCELLED: Status.CANCELLED,
}

_ARRAY_TASK_STATUS_TO_STATUS_MAP = {
    models.ArrayTaskStatus.QUEUED: Status.NOT_STARTED,
    models.ArrayTaskStatus.FAILED: Status.FAILED,
    models.ArrayTaskStatus.COMPLETED: Status.COMPLETED,
    models.ArrayTaskStatus.RUNNING: Status.RUNNING,
    models.ArrayTaskStatus.RESOURCES_UNAVAILABLE: Status.FAILED,
    models.ArrayTaskStatus.UNKNOWN: Status.FAILED,
    models.ArrayTaskStatus.CANCELLED: Status.CANCELLED,
    models.ArrayTaskStatus.DENIED: Status.FAILED,
}


class ParentFailedError(futures.CancelledError):
    def __init__(self, cause: BaseException, node: "Node"):
        super().__init__(f"node {node} failed: {cause}")
        self.node = node
        self.cause = cause


class Node(futures.FutureLike[_T]):
    def __init__(
        self,
        func: Callable[..., _T],
        *args: Any,
        name: Optional[str] = None,
        dag: Optional["DAG"] = None,
        mode: Mode = Mode.REALTIME,
        expand_node_output: Optional["Node"] = None,
        _download_results: Optional[bool] = None,
        _internal_prewrapped_func: Callable[..., "results.Result[_T]"] = None,
        _internal_accepts_stored_params: bool = True,
        **kwargs,
    ):
        """
        Node is a class that represents a function to run in a DAG
        :param func: function to run
        :param args: tuple of arguments to run
        :param name: optional name of dag
        :param dag: dag this node is associated with
        :param mode: Mode the node is to run in.
        :param _download_results: An optional boolean to override default
            result-downloading behavior. If True, will always download the
            results of the function immediately upon completion.
            If False, will not download the results of the function immediately,
            but will be downloaded when ``.result()`` is called.
        :param _prewrapped_func: For internal use only. A function that returns
            something that is already a Result, which does not require wrapping.
            We assume that all prewrapped functions make server calls.
        :param _accepts_stored_params: For internal use only.
            Applies only when ``_prewrapped_func`` is used.
            ``True`` if ``_prewrapped_func`` can accept stored parameters.
            ``False`` if it cannot, and all parameters must be serialized.
        :param kwargs: dictionary for keyword arguments
        """
        self.id = uuid.uuid4()
        self._name = name

        self._lifecycle_condition = threading.Condition(threading.Lock())
        self._status = Status.NOT_STARTED
        self._starting = False
        self._result: Optional[results.Result[_T]] = None
        self._lazy_result: Optional[_tg_results.LazyResult] = None
        self._lifecycle_exception: Optional[Exception] = None
        self._exception: Optional[Exception] = None
        self._cb_list: List[Callable[["Node[_T]"], None]] = []

        self.dag = dag
        self.mode: Mode = mode
        self._expand_node_output: Optional[Node] = expand_node_output

        self._resource_class = kwargs.pop("resource_class", None)
        self._resources = kwargs.pop("resources", None)

        self._wrapped_func: Callable[..., "results.Result[_T]"]

        if _internal_prewrapped_func:
            self._wrapped_func = _internal_prewrapped_func
            self._was_prewrapped = True
            args = (func,) + args
        else:
            if func is not None and not callable(func):
                raise TypeError("func argument to `Node` must be callable!")
            self._wrapped_func = results.LocalResult.wrap(func)
            self._was_prewrapped = False

        # True if this function is one of the XXX_base functions.
        # This means we can pass arguments as StoredParams.
        self._uses_stored_params = all(
            (
                _internal_accepts_stored_params,
                self._was_prewrapped,
                self.mode == Mode.REALTIME,
            )
        )
        self._download_results = _download_results

        self.parents: Dict[uuid.UUID, Node] = {}
        self.children: Dict[uuid.UUID, Node] = {}

        self._has_node_args = False
        self.args: Tuple[Any, ...] = args
        self.kwargs: Dict[str, Any] = kwargs
        self._check_resources_and_mode()
        self._find_deps()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def __ne__(self, other):
        return not (self == other)

    @property
    def name(self) -> str:
        return self._name or str(self.id)

    @name.setter
    def name(self, to: Optional[str]) -> None:
        self._name = to

    def _check_resources_and_mode(self):
        """
        Check if the user has set the resource options correctly for the mode
        """

        resources_set = self._resources is not None
        if self.mode == Mode.BATCH:
            if self._resource_class:
                if resources_set:
                    raise tce.TileDBCloudError(
                        "Only one of `resources` and `resource_class`"
                        " may be set when running a task graph node."
                    )
            elif not resources_set:
                self._resource_class = "standard"
        elif resources_set:
            raise tce.TileDBCloudError(
                "Cannot set resources for REALTIME task graphs,"
                ' please use "resource_class" to set a predefined option'
                ' for "standard" or "large"'
            )
        elif self.mode is Mode.LOCAL and self._resource_class:
            raise tce.TileDBCloudError(
                "Resource class cannot be set for locally-executed nodes."
            )

    def _find_deps(self):
        """Finds Nodes this depends on and adds them to our dependency list."""
        parents = _find_parent_nodes((self.args, self.kwargs))
        for dep in parents:
            self._has_node_args = True
            if dep.dag is self.dag:
                # This is the expected case: where the node we're adding
                # is part of the same DAG as we are.
                self.depends_on(dep)
            else:
                # This is the less-common case: where the node we're adding
                # is part of a previous DAG. We can only support when the
                # previous DAG has already completed execution.
                try:
                    dep.future.result(0)
                except Exception as e:
                    raise tce.TileDBCloudError(
                        "Nodes from a previous DAG may only be used as inputs"
                        " in a subsequent DAG if they are already complete."
                    ) from e

    def depends_on(self, node: "Node"):
        """
        Create dependency chain for node, useful when there is a dependency
        that does not rely directly on passing results from one to another
        :param node: node to mark as a dependency of this node
        :return:
        """
        with self._lifecycle_condition:
            if self._status is not Status.NOT_STARTED:
                raise RuntimeError("Cannot add dependency to an already-started node.")
            self.parents[node.id] = node
            node.children[self.id] = self

            if self.dag is None and node.dag is not None:
                self.dag = node.dag

    # FutureLike methods.

    def cancel(self) -> bool:
        with self._lifecycle_condition:
            if self._status is not Status.NOT_STARTED:
                return False
            self._update_status(Status.CANCELLED)
            self._lifecycle_exception = futures.CancelledError()
            cbs = self._callbacks()
        futures.execute_callbacks(self, cbs)
        return True

    def done(self) -> bool:
        with self._lifecycle_condition:
            return self._done()

    def cancelled(self) -> bool:
        with self._lifecycle_condition:
            return self._status is Status.CANCELLED

    def running(self) -> bool:
        with self._lifecycle_condition:
            return self._status is Status.RUNNING

    def result(self, timeout: Optional[float] = None) -> _T:
        if self.mode == Mode.BATCH:
            with self._lifecycle_condition:
                self._wait(timeout)
                to_raise = self._error()
                if to_raise:
                    raise to_raise
                result = self._lazy_result
            assert result
            return result.decode()

        else:
            with self._lifecycle_condition:
                self._wait(timeout)
                to_raise = self._error()
                if to_raise:
                    raise to_raise
                result = self._result
            assert result
            return result.get()

    def exception(self, timeout: Optional[float] = None) -> Optional[BaseException]:
        with self._lifecycle_condition:
            self._wait(timeout)
            if self._lifecycle_exception:
                raise self._lifecycle_exception
            return self._exception

    def add_done_callback(self, fn: Callable[["Node[_T]"], None]) -> None:
        with self._lifecycle_condition:
            self._cb_list.append(fn)
            if not self._done():
                return
        try:
            fn(self)
        except Exception:
            pass

    # Bonus public methods.

    finished = done  # Alias.

    @property
    def future(self) -> futures.FutureLike[_T]:
        """Returns something that pretends to be a Future."""
        return self

    @property
    def status(self) -> st.Status:
        with self._lifecycle_condition:
            return self._status

    @property
    def error(self) -> Optional[Exception]:
        return self._error()

    def retry(self) -> bool:
        if not self.dag:
            return False
        with self._lifecycle_condition:
            if not self._reset_internal():
                return False
        self.dag._submit_retry(self)
        return True

    def task_id(self) -> Optional[uuid.UUID]:
        """Gets the server-side Task ID of this node.

        Returns None if this has no task ID (as it was run on the client side).
        """
        try:
            with self._lifecycle_condition:
                if not self._result:
                    return None
                res = self._result
            sp = res.to_stored_param()
        except TypeError:
            # Run client-side; can't be converted to a stored param.
            return None
        return sp.task_id

    def wait(self, timeout: Optional[float] = None):
        """
        Wait for node to be completed
        :param timeout: optional timeout in seconds to wait for DAG to be completed
        :return: None or raises TimeoutError if timeout occurs
        """
        with self._lifecycle_condition:
            self._wait(timeout)

    # Things for internal use and use by the DAG.

    def _error(self) -> Optional[Exception]:
        return self._lifecycle_exception or self._exception

    def _reset_internal(self) -> bool:
        """Prepares this Node to be retried if it failed."""
        if self._status not in (Status.FAILED, Status.CANCELLED, Status.PARENT_FAILED):
            return False
        self._starting = False
        self._result = None
        self._lifecycle_exception = None
        self._exception = None
        self._update_status(Status.NOT_STARTED)
        return True

    def _callbacks(self):
        return tuple(self._cb_list)

    def _wait(self, timeout: Optional[float]):
        futures.wait_for(self._lifecycle_condition, self._done, timeout)

    def _done(self) -> bool:
        return self._status in (
            Status.CANCELLED,
            Status.COMPLETED,
            Status.FAILED,
            Status.PARENT_FAILED,
        )

    def _maybe_start(self, namespace: Optional[str]) -> bool:
        """Maybe starts this node, if possible.

        Returns True if the node is queued to start. This is called by the DAG
        while it holds its own lock, so we can't call back into it on this
        thread since it's in a transitional state.
        """
        assert self.dag
        with self._lifecycle_condition:
            if self._status is Status.PARENT_FAILED:
                self._reset_internal()
            if self._starting:
                # We're already starting.
                return False
            parents = self.parents.values()
            self._starting = any(
                p.status in {Status.CANCELLED, Status.FAILED, Status.PARENT_FAILED}
                for p in parents
            ) or all(p.status is Status.COMPLETED for p in parents)
            if not self._starting:
                return False
        self.dag._node_executor.submit(self._dag_exec, namespace)
        return True

    def _dag_exec(self, namespace: Optional[str]) -> None:
        with self._lifecycle_condition:
            if self._status is Status.CANCELLED:
                # We may have been cancelled between the time that we were
                # enqueued and the time that we ran.
                return
            for p in self.parents.values():
                if p.status in (Status.CANCELLED, Status.FAILED, Status.PARENT_FAILED):
                    # Take the first parent that failed
                    try:
                        exc = p.exception(0)
                    except Exception as e:
                        exc = e
                    if isinstance(exc, ParentFailedError):
                        self._lifecycle_exception = exc
                    else:
                        assert exc
                        self._lifecycle_exception = ParentFailedError(exc, p)
                    self._update_status(Status.PARENT_FAILED)
            if self._lifecycle_exception:
                cbs = self._callbacks()
            else:
                cbs = None
                self._update_status(Status.RUNNING)

        if cbs is not None:
            futures.execute_callbacks(self, cbs)
            return
        assert self.dag
        self.dag._report_node_status_update()
        # We have to make a shallow copy of kwargs here.
        # Since we modify the kwargs dictionary here before passing it
        # to the wrapped function, we need to ensure that the arguments
        # that we add are not reused across retries.
        raw_kwargs = dict(self.kwargs)

        if self._has_node_args:
            if self._uses_stored_params:
                # Stored parameters work only on remote functions.
                (args, kwargs), param_ids = _replace_nodes_with_stored_params(
                    (self.args, raw_kwargs)
                )

                if param_ids:
                    kwargs["stored_param_uuids"] = param_ids

            else:
                # For functions that run locally, give them the results as normal.
                args, kwargs = _replace_nodes_with_results((self.args, raw_kwargs))
        else:
            args, kwargs = self.args, raw_kwargs

        # Delayed functions bypass all our nice assumptions about how we set up
        # a task graph and are not themselves "prewrapped nodes", so we have to
        # separately check whether a node is remote (i.e., it executes on the
        # server side period) and whether it is prewrapped (i.e., it is a
        # whatever_base function that supports the download_results calls etc).
        if self.mode == Mode.REALTIME:
            # If it's `Mode.REALTIME`, we assume that the function is either
            # prewrapped or it was created with `Delayed`, so the function
            # itself is one of the `submit_xxx` (but not `_base`) functions.
            self.dag.initial_setup()
            kwargs.update(
                _server_graph_uuid=self.dag.server_graph_uuid,
                _client_node_uuid=self.id,
                resource_class=self._resource_class,
            )
            if self._name:
                kwargs.setdefault("task_name", self._name)
            if namespace:
                kwargs["namespace"] = namespace

        if self._was_prewrapped:
            # Prewrapped functions support special result handling.
            if self._download_results is None:
                # If the user didn't explicitly choose, set a download behavior:
                if self.children:
                    # If this is an intermediate node, download results only if
                    # there is a child node which runs locally.
                    download_results = any(
                        child.mode == Mode.LOCAL for child in self.children.values()
                    )
                else:
                    # If this is a terminal node, always download results.
                    download_results = True
            else:
                download_results = self._download_results
            kwargs["_download_results"] = download_results

        sp_future = self.dag._udf_executor.submit(self._wrapped_func, *args, **kwargs)
        try:
            result = sp_future.result()
        except Exception as exc:
            # We don't need to worry about cancellation exceptions here, because
            # we're the only ones who hold onto this future and we never cancel.
            exc_msg = exc.args and exc.args[0]
            if not isinstance(exc_msg, str) or _RETRY_MSG not in exc_msg:
                # This is not a missing-stored-param error. Don't retry.
                with self._lifecycle_condition:
                    self._exception = exc
                    self._update_status(Status.FAILED)
                    cbs = self._callbacks()
                futures.execute_callbacks(self, cbs)
                return
            # Otherwise, fall through to _replace_nodes_with_results below.
        else:
            # We succeeded!
            with self._lifecycle_condition:
                self._result = result
                self._update_status(Status.COMPLETED)
                cbs = self._callbacks()
            futures.execute_callbacks(self, cbs)
            return

        args, kwargs = _replace_nodes_with_results((self.args, self.kwargs))
        raw_future = self.dag._udf_executor.submit(self._wrapped_func, *args, **kwargs)
        try:
            result = raw_future.result()
        except Exception as exc:
            with self._lifecycle_condition:
                self._exception = exc
                self._update_status(Status.FAILED)
                cbs = self._callbacks()
            futures.execute_callbacks(self, cbs)
        else:
            with self._lifecycle_condition:
                self._result = result
                self._update_status(Status.COMPLETED)
                cbs = self._callbacks()
            futures.execute_callbacks(self, cbs)

    def _update_status(self, st: Status) -> None:
        if self._status is st:
            return
        self._status = st
        self._lifecycle_condition.notify_all()

    def _to_log_metadata(self) -> rest_api.TaskGraphNodeMetadata:
        return rest_api.TaskGraphNodeMetadata(
            client_node_uuid=str(self.id),
            name=self.name,
            depends_on=[str(dep) for dep in self.parents],
            run_location=(
                rest_api.TaskGraphLogRunLocation.CLIENT
                if self.mode == Mode.LOCAL
                else rest_api.TaskGraphLogRunLocation.SERVER
            ),
        )


class DAG:
    def __init__(
        self,
        max_workers: Optional[int] = None,
        use_processes: bool = False,
        done_callback: Optional[Callable[["DAG"], None]] = None,
        update_callback: Optional[Callable[["DAG"], None]] = None,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        mode: Mode = Mode.REALTIME,
        retry_strategy: Optional[models.RetryStrategy] = None,
        workflow_retry_strategy: Optional[models.RetryStrategy] = None,
        deadline: Optional[int] = None,
    ):
        """
        DAG is a class for creating and managing direct acyclic graphs
        :param max_workers: how many workers should be used to execute the dag
        :param use_processes: if true will use processes instead of threads,
            defaults to threads
        :param done_callback: optional call back function to register for
            when dag is completed. Function will be passed reference to this dag
        :param update_callback: optional call back function to register for
            when dag status is updated. Function will be passed reference to this dag
        :param namespace: optional namespace to use for all tasks in DAG
        :param name: A human-readable name used to identify this task graph
            in logs. Does not need to be unique.
        :param mode: Mode the DAG is to run in, valid options are
            Mode.REALTIME, Mode.BATCH
        :param retry_strategy: RetryStrategy to be applied on every node of the DAG.
        :param workflow_retry_strategy: RetryStrategy to use to retry the entire DAG.
        :param deadline: Duration in seconds relative to the workflow start time
            which the workflow is allowed to run before it gets terminated.
        """
        self.id = uuid.uuid4()
        self.nodes: Dict[uuid.UUID, Node] = {}
        self.nodes_by_name: Dict[str, Node] = {}

        self.namespace = namespace or client.default_charged_namespace(
            required_action=rest_api.NamespaceActions.RUN_JOB
        )
        self.name = name
        self.server_graph_uuid: Optional[uuid.UUID] = None
        self.max_workers = max_workers
        self.retry_strategy = retry_strategy
        self.workflow_retry_strategy = workflow_retry_strategy
        self.deadline = deadline

        self._update_batch_status_thread: Optional[threading.Thread] = None
        """The thread that is updating the status of Batch execution."""
        self.mode: Mode = mode

        """The server-generated UUID of this graph, used for logging.

        Will be ``None`` until :meth:`initial_setup` is called. If submitting
        the log works, will be the UUID; otherwise, will be None.
        """

        self.visualization = None

        self._udf_executor: futures.Executor
        """The executor that is used to make server calls and run local UDFs."""
        if use_processes:
            self._udf_executor = futures.ProcessPoolExecutor(max_workers=max_workers)
        else:
            self._udf_executor = futures.ThreadPoolExecutor(
                thread_name_prefix=f"dag-{self.name or self.id}-worker",
                max_workers=max_workers,
            )
        self._node_executor = futures.ThreadPoolExecutor(
            thread_name_prefix=f"dag-{self.name or self.id}-nodes",
            max_workers=max_workers,
        )
        """The thread pool that is used to execute nodes' exec functions."""

        self._lifecycle_condition = threading.Condition(threading.Lock())

        self.completed_nodes: Dict[uuid.UUID, Node] = {}
        self.failed_nodes: Dict[uuid.UUID, Node] = {}
        self.running_nodes: Dict[uuid.UUID, Node] = {}
        self.not_started_nodes: Dict[uuid.UUID, Node] = {}
        self.cancelled_nodes: Dict[uuid.UUID, Node] = {}

        self._status = st.Status.NOT_STARTED

        self._done_callbacks = []
        if callable(done_callback):
            self._done_callbacks.append(done_callback)

        self._update_callbacks = []
        if callable(update_callback):
            self._update_callbacks.append(update_callback)

        self._tried_setup: bool = False

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def __ne__(self, other):
        return not (self == other)

    @property
    def status(self):
        with self._lifecycle_condition:
            return self._status

    def initial_setup(self):
        """Performs one-time server-side setup tasks.

        Can safely be called multiple times.
        """
        with self._lifecycle_condition:
            if not self._tried_setup:
                log_structure = self._build_log_structure()
                try:
                    result = client.build(
                        rest_api.TaskGraphLogsApi
                    ).create_task_graph_log(
                        namespace=self.namespace,
                        log=log_structure,
                    )
                except rest_api.ApiException as apix:
                    # There was a problem submitting the task graph for logging.
                    # This should not abort the task graph.

                    warnings.warn(
                        UserWarning(f"Could not submit logging metadata: {apix}")
                    )
                else:
                    try:
                        self.server_graph_uuid = uuid.UUID(hex=result.uuid)
                    except ValueError as ve:
                        warnings.warn(
                            UserWarning(f"Server-provided graph ID was invalid: {ve}")
                        )
                self._tried_setup = True

        return self.server_graph_uuid

    def add_update_callback(self, func):
        """
        Add a callback for when DAG status is updated
        :param func: Function to call when DAG status is updated.
            The function will be passed reference to this dag
        :return:
        """
        if not callable(func):
            raise TypeError("func to add_update_callback must be callable")

        with self._lifecycle_condition:
            self._update_callbacks.append(func)

    def add_done_callback(self, func):
        """
        Add a callback for when DAG is completed
        :param func: Function to call when DAG status is updated.
            The function will be passed reference to this dag
        :return:
        """
        if not callable(func):
            raise TypeError("func to add_done_callback must be callable")

        with self._lifecycle_condition:
            self._done_callbacks.append(func)
            if not self._done():
                return
        try:
            func(self)
        except Exception:
            pass

    def _submit_retry(self, node: Node) -> None:
        with self._lifecycle_condition:
            self.failed_nodes.pop(node.id, None)
            self.cancelled_nodes.pop(node.id, None)
            self.not_started_nodes[node.id] = node
            self._maybe_exec(node)
            if self.running_nodes:
                self._set_status(Status.RUNNING)
            # TODO: We currently don't immediately propagate the change in
            # PARENT_FAILED status to child nodes.

    def _report_node_status_update(self):
        """Updates the state of callbacks from the node."""
        with self._lifecycle_condition:
            cbs = tuple(self._update_callbacks)
        futures.execute_callbacks(self, cbs)

    def _report_server_completion(self, status: Status) -> None:
        if not self.server_graph_uuid:
            return
        try:
            api_st = _API_STATUSES[status]
        except KeyError as ke:
            raise AssertionError(f"Task graph ended in invalid state {status}") from ke
        do_update = utils.ephemeral_thread(
            client.build(rest_api.TaskGraphLogsApi).update_task_graph_log
        )
        do_update(
            id=str(self.server_graph_uuid),
            namespace=self.namespace,
            log=rest_api.TaskGraphLog(status=api_st),
            _request_timeout=_REPORT_TIMEOUT_SECS,
        )

    def _done(self):
        return self._status in (
            st.Status.FAILED,
            st.Status.CANCELLED,
            st.Status.COMPLETED,
        )

    def done(self) -> bool:
        with self._lifecycle_condition:
            return self._done()

    def add_node_obj(self, node):
        """
        Add node to DAG
        :param node: to add to dag
        :return: node
        """
        with self._lifecycle_condition:
            return self._add_node_internal(node)

    def _add_node_internal(self, node: Node) -> Node:
        """Add node implementation. Must hold lifecycle condition."""
        if self._status is not Status.NOT_STARTED:
            raise RuntimeError("Cannot add nodes to a running graph")
        self.nodes[node.id] = node
        self.nodes_by_name[str(node.name)] = node
        self.not_started_nodes[node.id] = node
        # If you add a Node that you already cancelled, this will deadlock.
        # Also there is absolutely no good reason to do that.
        node.add_done_callback(self.report_node_complete)
        return node

    def add_node(self, func_exec, *args, name=None, local_mode=True, **kwargs):
        """
        Create and add a node.

        DEPRECATED. Use `submit_local` instead.

        :param func_exec: function to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        mode = Mode.LOCAL if local_mode else Mode.REALTIME

        return self._add_raw_node(
            func_exec,
            *args,
            name=name,
            mode=mode,
            **kwargs,
        )

    def _suffix_name(self, name: str) -> str:
        if name not in self.nodes_by_name:
            return name
        for i in itertools.count(1):
            suffixed = f"{name} ({i})"
            if suffixed not in self.nodes_by_name:
                return suffixed
        assert False, "It is impossible to get here."

    def _add_raw_node(
        self,
        func_exec,
        *args,
        name: Optional[str] = None,
        _fallback_name: Optional[str] = None,
        **kwargs,
    ):
        """Adds a generic (usually local) node to the graph."""
        with self._lifecycle_condition:
            if name is None and _fallback_name is not None:
                # If the node is unnamed, generate a name to give to it,
                # without trampling on the user's selected name.
                name = self._suffix_name(_fallback_name)
            node = Node(func_exec, *args, name=name, dag=self, **kwargs)
            return self._add_node_internal(node)

    def _add_prewrapped_node(
        self,
        func_exec,
        *args,
        name=None,
        _fallback_name: Optional[str] = None,
        store_results=True,
        expand_node_output: Optional[Node] = None,
        **kwargs,
    ):
        with self._lifecycle_condition:
            if name is None and _fallback_name is not None:
                # If the node is unnamed, generate a name to give to it,
                # without trampling on the user's selected name.
                name = self._suffix_name(_fallback_name)

            if "local_mode" in kwargs and kwargs["local_mode"]:
                # Check for deprecated local_mode parameter
                kwargs["mode"] = Mode.LOCAL

            if self.mode == Mode.BATCH:
                if kwargs.get("mode") is not None and kwargs.get("mode") != Mode.BATCH:
                    raise tce.TileDBCloudError(
                        "BATCH mode DAG can only execute BATCH mode Nodes."
                    )
                kwargs["mode"] = Mode.BATCH
            elif "local_mode" in kwargs and kwargs["local_mode"]:
                # Check for deprecated local_mode parameter
                kwargs["mode"] = Mode.LOCAL
            else:
                kwargs["mode"] = Mode.REALTIME
                kwargs["store_results"] = store_results

            node = Node(
                *args,
                _internal_prewrapped_func=func_exec,
                dag=self,
                name=name,
                expand_node_output=expand_node_output,
                **kwargs,
            )
            return self._add_node_internal(node)

    def submit_array_udf(self, func, *args, **kwargs):
        """
        Submit a function that will be executed in the cloud serverlessly
        :param func: function to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self._add_prewrapped_node(
            array.apply_base,
            func,
            *args,
            _fallback_name=functions.full_name(func),
            **kwargs,
        )

    def submit_local(self, func, *args, **kwargs):
        """
        Submit a function that will run locally
        :param func: function to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        kwargs.setdefault("name", functions.full_name(func))
        return self._add_raw_node(func, *args, mode=Mode.LOCAL, **kwargs)

    def submit_udf(self, func, *args, **kwargs):
        """
        Submit a function that will be executed in the cloud serverlessly
        :param func: function to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """

        if "local_mode" in kwargs:
            if kwargs.get("local_mode") or kwargs.get("mode") == Mode.LOCAL:
                # Drop kwarg
                kwargs.pop("local_mode", None)
                kwargs.pop("mode", None)
                return self.submit_local(func, *args, **kwargs)

            del kwargs["local_mode"]

        return self._add_prewrapped_node(
            udf.exec_base,
            func,
            *args,
            _fallback_name=functions.full_name(func),
            **kwargs,
        )

    submit = submit_udf

    def submit_udf_stage(
        self, func, *args, expand_node_output: Optional[Node] = None, **kwargs
    ):
        """
        Submit a function that will be executed in the cloud serverlessly
        :param func: function to execute
        :param args: arguments for function execution
        :param expand_node_output: the Node that we want to expand the output of.
            The output of the node should be a JSON encoded list.
        :param name: name
        :return: Node that is created
        """

        if "local_mode" in kwargs or self.mode != Mode.BATCH:
            raise tce.TileDBCloudError(
                "Stage nodes are only supported for BATCH mode DAGs."
            )

        return self._add_prewrapped_node(
            udf.exec_base,
            func,
            *args,
            _fallback_name=functions.full_name(func),
            expand_node_output=expand_node_output,
            **kwargs,
        )

    def submit_sql(self, *args, **kwargs):
        """
        Submit a sql query to run serverlessly in the cloud
        :param sql: query to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self._add_prewrapped_node(
            _sql_exec.exec_base,
            *args,
            _internal_accepts_stored_params=False,
            _fallback_name="SQL query",
            **kwargs,
        )

    def report_node_status_change(self, node: Node, new_status: Status):
        self.completed_nodes.pop(node.id, None)
        self.failed_nodes.pop(node.id, None)
        self.running_nodes.pop(node.id, None)
        self.not_started_nodes.pop(node.id, None)
        self.cancelled_nodes.pop(node.id, None)
        with node._lifecycle_condition:
            node._update_status(new_status)

        if new_status is Status.COMPLETED:
            self.completed_nodes[node.id] = node
        elif new_status is Status.FAILED:
            self.failed_nodes[node.id] = node
        elif new_status is Status.PARENT_FAILED:
            self.failed_nodes[node.id] = node
        elif new_status is Status.RUNNING:
            self.running_nodes[node.id] = node
        elif new_status is Status.NOT_STARTED:
            self.not_started_nodes[node.id] = node
        elif new_status is Status.CANCELLED:
            self.cancelled_nodes[node.id] = node

    def report_node_complete(self, node: Node):
        """
        Report a node as complete
        :param node: to mark as complete
        :return
        """
        to_report: Optional[str] = None
        """The client-side event to report to the server, if needed.

        For nodes that do not run because of a client-side event (e.g. they're
        cancelled, they are run only on the client side, they crashed before
        being sent to the server), we want to report an empty ArrayTask so that
        the graph information on the server can know about these failed nodes
        even though there will be no ArrayTask for them in our database.
        """
        with self._lifecycle_condition:
            # A node may be either "running" or "not started" depending upon
            # whether it failed or was cancelled.
            self.running_nodes.pop(node.id, None)
            self.not_started_nodes.pop(node.id, None)

            if node.status is st.Status.COMPLETED:
                self.completed_nodes[node.id] = node
                if node.mode == Mode.LOCAL:
                    to_report = models.ArrayTaskStatus.COMPLETED
            elif node.status is Status.CANCELLED:
                self.cancelled_nodes[node.id] = node
                to_report = models.ArrayTaskStatus.CANCELLED
            elif node.status is Status.PARENT_FAILED:
                # If the parent failed, put this back onto the "unstarted" pile.
                self.not_started_nodes[node.id] = node
                to_report = None
            elif node.status is Status.FAILED:
                self.failed_nodes[node.id] = node
                if node.mode == Mode.LOCAL:
                    to_report = models.ArrayTaskStatus.FAILED
            else:
                raise AssertionError(f"Unknown node status {node.status}")

            if self.mode != Mode.BATCH:
                for child in node.children.values():
                    self._maybe_exec(child)

            if self._status is not Status.CANCELLED:
                if self.failed_nodes or self.cancelled_nodes:
                    self._set_status(Status.FAILED)
                elif self.running_nodes or self.not_started_nodes:
                    self._set_status(Status.RUNNING)
                else:
                    self._set_status(Status.COMPLETED)

            # If we're done, we're going to need to report that.
            done_cbs = (
                None if self._status is Status.RUNNING else tuple(self._done_callbacks)
            )
            status = self._status

            update_cbs = tuple(self._update_callbacks)

        # First, execute callbacks...
        futures.execute_callbacks(self, update_cbs)
        if done_cbs is not None:
            futures.execute_callbacks(self, done_cbs)

        # ...and only when that's done, report things to the server.
        if self.mode != Mode.BATCH and self.server_graph_uuid:
            # Only report client-side events to the server if we've submitted
            # the structure of the graph.
            if to_report:
                do_report = utils.ephemeral_thread(
                    client.build(rest_api.TaskGraphLogsApi).report_client_node
                )
                do_report(
                    id=str(self.server_graph_uuid),
                    namespace=self.namespace,
                    report=models.TaskGraphClientNodeStatus(
                        client_node_uuid=str(node.id),
                        status=to_report,
                    ),
                    _request_timeout=_REPORT_TIMEOUT_SECS,
                )

            if done_cbs is not None:
                try:
                    api_st = _API_STATUSES[status]
                except KeyError as ke:
                    raise AssertionError(f"Invalid end state {status}") from ke
                do_update = utils.ephemeral_thread(
                    client.build(rest_api.TaskGraphLogsApi).update_task_graph_log
                )
                do_update(
                    id=str(self.server_graph_uuid),
                    namespace=self.namespace,
                    log=rest_api.TaskGraphLog(status=api_st),
                    _request_timeout=_REPORT_TIMEOUT_SECS,
                )

    def _set_status(self, st: Status) -> None:
        if self._status is st:
            return
        self._status = st
        self._lifecycle_condition.notify_all()

    def _find_root_nodes(self):
        """
        Find all root nodes
        :return: list of root nodes
        """
        roots = []
        for node in self.nodes.values():
            if node.parents is None or len(node.parents) == 0:
                roots.append(node)

        return roots

    def compute(self):
        """
        Start the DAG by executing root nodes
        :return:
        """
        with self._lifecycle_condition:
            if self._status is not Status.NOT_STARTED:
                return
            if self.mode == Mode.REALTIME:
                roots = self._find_root_nodes()
                if len(roots) == 0:
                    raise tce.TileDBCloudError(
                        "DAG is circular, there are no root nodes"
                    )
                self._status = Status.RUNNING

                for node in roots:
                    self._maybe_exec(node)
            elif self.mode == Mode.BATCH:
                try:
                    self._batch_taskgraph = self._build_batch_taskgraph()
                    api_client = client.build(rest_api.TaskGraphsApi)
                    submission = api_client.create_task_graph(
                        namespace=self.namespace, graph=self._batch_taskgraph
                    )
                    execution = api_client.submit_task_graph(
                        namespace=self.namespace, id=submission.uuid
                    )
                    self.server_graph_uuid = execution.uuid
                except rest_api.ApiException:
                    raise
                self._update_batch_status_thread = threading.Thread(
                    name=f"dag-{self.name}-update-status",
                    target=self._update_status,
                    daemon=True,
                )
                self._update_batch_status_thread.start()

    def _maybe_exec(self, node: Node):
        did_start = node._maybe_start(self.namespace)
        if did_start:
            self.running_nodes[node.id] = node
            del self.not_started_nodes[node.id]

    def wait(self, timeout: Optional[float] = None) -> None:
        """
        Wait for DAG to be completed
        :param timeout: optional timeout in seconds to wait for DAG to be completed
        :return: None or raises TimeoutError if timeout occurs
        """

        if timeout is not None and not isinstance(timeout, numbers.Number):
            raise TypeError(
                "timeout must be numeric value representing seconds to wait"
            )

        with self._lifecycle_condition:
            futures.wait_for(self._lifecycle_condition, self._done, timeout)

        # in case of failure reraise the first failed node exception
        if self.status == st.Status.FAILED:
            exc = next(iter(self.failed_nodes.values())).error
            assert exc
            raise exc

    def cancel(self):
        if self.mode == Mode.BATCH:
            client.build(rest_api.TaskGraphLogsApi).stop_task_graph_execution(
                namespace=self.namespace, id=self.server_graph_uuid
            )
            with self._lifecycle_condition:
                self._set_status(Status.CANCELLED)
        else:
            with self._lifecycle_condition:
                if self._status not in (Status.RUNNING, Status.NOT_STARTED):
                    return
                self._set_status(Status.CANCELLED)
                to_cancel = tuple(self.not_started_nodes.values())

            for n in to_cancel:
                n.cancel()

    def retry_all(self) -> None:
        """Retries all failed and cancelled nodes."""
        if self.mode == Mode.BATCH:
            for node in frozenset(self.failed_nodes.values()).union(
                self.cancelled_nodes.values()
            ):
                self.report_node_status_change(node, Status.NOT_STARTED)

            if self._status is Status.CANCELLED or self._status is Status.FAILED:
                client.build(rest_api.TaskGraphLogsApi).retry_task_graph_execution(
                    namespace=self.namespace,
                    id=self.server_graph_uuid,
                )

            with self._lifecycle_condition:
                self._set_status(Status.RUNNING)
            if not self._update_batch_status_thread.is_alive():
                self._update_batch_status_thread = threading.Thread(
                    name=f"dag-{self.name}-update-status",
                    target=self._update_status,
                    daemon=True,
                )
                self._update_batch_status_thread.start()

        else:
            with self._lifecycle_condition:
                # Assume that we want to un-cancel.
                if self._status is Status.CANCELLED:
                    self._set_status(Status.RUNNING)
                to_retry = frozenset(self.failed_nodes.values()).union(
                    self.cancelled_nodes.values()
                )
            for n in to_retry:
                n.retry()

    def find_end_nodes(self):
        """
        Find all end nodes
        :return: list of end nodes
        """
        end = []
        for node in self.nodes.values():
            if node.children is None or len(node.children) == 0:
                end.append(node)

        return end

    def stats(self):
        return {
            "percent_complete": len(self.completed_nodes) / len(self.nodes) * 100,
            "running": len(self.running_nodes),
            "failed": len(self.failed_nodes),
            "completed": len(self.completed_nodes),
            "cancelled": len(self.cancelled_nodes),
            "not_started": len(self.not_started_nodes),
            "total_count": len(self.nodes),
        }

    def networkx_graph(self):
        import networkx as nx

        graph = nx.DiGraph()

        for n in self.nodes.values():
            graph.add_node(str(n.id), label=n.name)
        for n in self.nodes.values():
            for child in n.children.values():
                graph.add_edge(str(n.id), str(child.id))

        return graph

    def get_tiledb_plot_node_details(self):
        """
        Build list of details needed for tiledb node graph
        :return:
        """
        node_details = {}

        for node in self.nodes.values():
            node_details[str(node.id)] = dict(name=node.name, status=str(node.status))

        return node_details

    def _build_log_structure(self) -> rest_api.TaskGraphLog:
        """Builds the structure of this graph for logging."""
        nodes = [n._to_log_metadata() for n in self.nodes.values()]
        return rest_api.TaskGraphLog(
            name=self.name,
            namespace=self.namespace,
            nodes=_topo_sort(nodes),
        )

    @staticmethod
    def _update_dag_tiledb_graph(graph):
        graph.visualization["node_details"] = graph.get_tiledb_plot_node_details()
        viz.update_tiledb_graph(
            graph.visualization["nodes"],
            graph.visualization["edges"],
            graph.visualization["node_details"],
            graph.visualization["positions"],
            graph.visualization["fig"],
        )

    @staticmethod
    def _update_dag_plotly_graph(graph):
        viz.update_plotly_graph(
            graph.visualization["nodes"], graph.visualization["fig"]
        )

    def visualize(self, notebook=True, auto_update=True, force_plotly=False):
        """
        Build and render a tree diagram of the DAG.
        :param notebook: Is the visualization inside a jupyter notebook?
            If so we'll use a widget
        :param auto_update: Should the diagram be auto updated with each status change
        :param force_plotly: Force the use of plotly graphs instead of
            TileDB Plot Widget
        :return: returns figure
        """
        if not notebook or force_plotly:
            return self._visualize_plotly(notebook=notebook, auto_update=auto_update)

        try:
            return self._visualize_tiledb(auto_update=auto_update)
        except ImportError:
            return self._visualize_plotly(notebook=notebook, auto_update=auto_update)

    def _visualize_tiledb(self, auto_update=True):
        """
        Create graph visualization with tiledb.plot.widget
        :param auto_update: Should the diagram be auto updated with each status change
        :return: figure
        """

        import tiledb.plot.widget

        graph = self.networkx_graph()
        nodes = list(graph.nodes())
        edges = list(graph.edges())
        node_details = self.get_tiledb_plot_node_details()
        positions = viz.build_visualization_positions(graph)

        self.visualization = {
            "nodes": nodes,
            "edges": edges,
            "node_details": node_details,
            "positions": positions,
        }
        fig = tiledb.plot.widget.Visualize(data=json.dumps(self.visualization))
        self.visualization["fig"] = fig

        if auto_update:
            self.add_update_callback(self._update_dag_tiledb_graph)

        return fig

    def _visualize_plotly(self, notebook=True, auto_update=True):
        """

        :param notebook: Is the visualization inside a jupyter notebook?
            If so we'll use a widget
        :param auto_update: Should the diagram be auto updated with each status change
        :return: figure
        """
        import plotly.graph_objects as go

        graph = self.networkx_graph()
        pos = viz.build_visualization_positions(graph)

        # Convert to plotly scatter plot
        edge_x = []
        edge_y = []
        for edge in graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=0.5, color="#888"),
            hoverinfo="none",
            mode="lines",
        )

        # Build node x,y and also build a mapping of the graph market numbers
        # to actual node objects so we can fetch status.
        # The graph ends up with each marker on a list, so we need to map
        # from this list's order to actual nodes so we can look things up.
        node_x = []
        node_y = []
        nodes = []
        for node_id in graph.nodes():
            x, y = pos[node_id]
            node_x.append(x)
            node_y.append(y)
            nodes.append(self.nodes[uuid.UUID(node_id)])

        # Build node scatter plot
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            hoverinfo="text",
            marker=dict(size=15, line_width=2),
        )

        (node_trace.marker.color, node_trace.text) = viz.build_graph_node_details(nodes)

        fig_obj = go.Figure
        if notebook:
            fig_obj = go.FigureWidget
        # Create plot
        fig = fig_obj(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                # title="Status",
                # titlefont_size=16,
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[
                    dict(showarrow=True, xref="paper", yref="paper", x=0.005, y=-0.002)
                ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            ),
        )

        self.visualization = dict(fig=fig, network=graph, nodes=nodes)

        if auto_update:
            self.add_update_callback(self._update_dag_plotly_graph)

        return fig

    def end_nodes(self):
        """
        Find all ends nodes

        dag = DAG()
        dag.add_node(Node())

        end_nodes = dag.end_nodes()

        :return: list of root nodes
        """
        ends = []
        for node in self.nodes.values():
            if node.children is None or len(node.children) == 0:
                ends.append(node)

        return ends

    def end_results(self):
        """
        Get all end results, will block if all results are not ready

        dag = DAG()
        dag.add_node(Node())

        end_results = dag.end_results()

        :return: map of results by node ID
        """

        results = {}
        for node in self.end_nodes():
            results[node.id] = node.result()

        return results

    def end_results_by_name(self):
        """
        Get all end results, will block if all results are not ready

        dag = DAG()
        dag.add_node(Node())

        end_results = dag.end_results_by_name()

        :return: map of results by node name
        """

        results = {}
        for node in self.end_nodes():
            results[node.name] = node.result()

        return results

    def _build_batch_taskgraph(self):
        """
        Builds the batch taskgraph model for submission
        """

        # We need to guarantee that the existing node names are maintained.
        topo_sorted_nodes = _topo_sort_nodes(self.nodes)
        node_jsons = []
        for node in topo_sorted_nodes:
            kwargs = {}
            node_args = list(node.args)
            # XXX: This is subtly different from the way functions are handled
            # when coordinated locally ("realtime").
            if callable(node_args[0]):
                func = node_args.pop(0)
                kwargs["executable_code"] = codecs.PickleCodec.encode_base64(func)
                kwargs["source_text"] = functions.getsourcelines(func)
            if type(node.args[0]) == str:
                func = node_args.pop(0)
                kwargs["registered_udf_name"] = func

            filtered_node_kwargs = {
                name: val
                for name, val in node.kwargs.items()
                if name not in _SKIP_BATCH_UDF_KWARGS
            }

            all_args = types.Arguments(node_args, filtered_node_kwargs)
            encoder = _BatchArgEncoder(input_is_expanded=bool(node._expand_node_output))
            kwargs["arguments"] = encoder.encode_arguments(all_args)

            env_dict = {
                "language": models.UDFLanguage.PYTHON,
                "language_version": utils.PYTHON_VERSION,
                "run_client_side": False,
            }
            if "image_name" in node.kwargs:
                env_dict["image_name"] = node.kwargs["image_name"]

            if "timeout" in node.kwargs:
                env_dict["timeout"] = node.kwargs["timeout"]

            if "access_credentials_name" in node.kwargs:
                env_dict["access_credentials_name"] = node.kwargs[
                    "access_credentials_name"
                ]

            if node._resource_class:
                env_dict["resource_class"] = node._resource_class

            if node._resources:
                env_dict["resources"] = models.TGUDFEnvironmentResources(
                    **node._resources
                )

            # Don't let each task set a namespace, use the DAG's namespace
            # if "namespace" in node.kwargs:
            #     env_dict["namespace"] = node.kwargs["namespace"]
            env_dict["namespace"] = self.namespace

            kwargs["environment"] = models.TGUDFEnvironment(**env_dict)
            kwargs["result_format"] = node.kwargs.get(
                "result_format", models.ResultFormat.NATIVE
            )
            expand_node_output = ""
            if node._expand_node_output:
                expand_node_output = str(node._expand_node_output.id)

            retry_strategy = None
            if "retry_strategy" in node.kwargs:
                retry_strategy = node.kwargs["retry_strategy"]

            deadline = None
            if "deadline" in node.kwargs:
                deadline = node.kwargs["deadline"]

            task_graph_node = models.TaskGraphNode(
                client_node_id=str(node.id),
                name=node.name,
                depends_on=[str(parent) for parent in node.parents],
                expand_node_output=expand_node_output,
                retry_strategy=retry_strategy,
                deadline=deadline,
                udf_node=models.TGUDFNodeData(**kwargs),
            )
            node_jsons.append(task_graph_node)
        return dict(
            name=self.name,
            parallelism=self.max_workers,
            retry_strategy=self.retry_strategy,
            workflow_retry_strategy=self.workflow_retry_strategy,
            deadline=self.deadline,
            nodes=node_jsons,
        )

    def _update_status(self) -> None:
        while True:
            time.sleep(2)
            if self._done():
                return

            try:
                result: models.TaskGraphLog = client.build(
                    rest_api.TaskGraphLogsApi
                ).get_task_graph_log(
                    namespace=self.namespace, id=self.server_graph_uuid
                )
            except rest_api.ApiException:
                raise
            else:
                for new_node in result.nodes or ():
                    assert isinstance(new_node, models.TaskGraphNodeMetadata)
                    node_uuid = uuid.UUID(new_node.client_node_uuid)
                    node = self.nodes[node_uuid]
                    new_node_status = array_task_status_to_status(new_node.status)
                    if node.status != new_node_status:
                        if new_node_status in (
                            Status.FAILED,
                            Status.CANCELLED,
                            Status.COMPLETED,
                        ):
                            if new_node.executions:
                                execution_id = new_node.executions[
                                    len(new_node.executions) - 1
                                ].id
                                node._lazy_result = _tg_results.LazyResult(
                                    client, execution_id
                                )
                                if new_node_status == Status.FAILED:
                                    try:
                                        e = node._lazy_result.decode()
                                        if isinstance(e, Exception):
                                            node._exception = e
                                    except Exception as e:
                                        node._exception = e

                            else:
                                raise RuntimeError("No executions found for done Node.")
                            self.report_node_status_change(node, new_node_status)
                            self.report_node_complete(node)
                        else:
                            self.report_node_status_change(node, new_node_status)
                new_workflow_status = task_graph_log_status_to_status(result.status)
                if self._status != new_workflow_status:
                    with self._lifecycle_condition:
                        self._set_status(new_workflow_status)


def list_logs(
    *,
    namespace: Optional[str] = None,
    created_by: Optional[str] = None,
    search: Optional[str] = None,
    start_time: Optional[datetime.datetime] = None,
    end_time: Optional[datetime.datetime] = None,
    page: int = 1,
    per_page: int = 10,
) -> models.TaskGraphLogsData:
    """Retrieves the list of task graph logs you can view.

    The returned graph logs will be "light" versions, meaning they will not
    include any details about the execution state of an individual DAG.
    To retrieve those, pass the ID to :func:`server_logs`.

    :param namespace: If present, include logs for only this namespace.
        If absent, include logs for all namespaces you have access to.
    :param created_by: Include only logs from this user (if present).
    :param search: A search string for the name of the task graph.
    :param start_time: Include logs created after this time.
    :param end_time: Include logs created before this time.
    :param page: The page number to use, starting from 1.
    :param per_page: The number of items per page.
    """
    return client.build(rest_api.TaskGraphLogsApi).list_task_graph_logs(
        namespace=namespace,
        created_by=created_by,
        search=search,
        start_time=start_time,
        end_time=end_time,
        page=page,
        per_page=per_page,
    )


def server_logs(
    dag_or_id: Union[DAG, models.TaskGraphLog, uuid.UUID, str],
    namespace: Optional[str] = None,
) -> Optional[models.TaskGraphLog]:
    """Retrieves the full server-side logs for the given DAG.

    The DAG can be provided as a DAG object, or the server-provided UUID of a
    DAG's execution log in either :class:`uuid.UUID` or string form.
    This can be used to access both completed DAGs and in-progress DAGs.
    The returned DAGs will include full data

    Will return None if called with a DAG object that has no server-side nodes.
    """
    if isinstance(dag_or_id, DAG):
        the_id = dag_or_id.server_graph_uuid
    elif isinstance(dag_or_id, models.TaskGraphLog):
        the_id = uuid.UUID(hex=dag_or_id.uuid)
    elif isinstance(dag_or_id, str):
        the_id = uuid.UUID(hex=dag_or_id)
    else:
        the_id = dag_or_id

    if not the_id:
        return None

    namespace = namespace or client.default_charged_namespace(
        required_action=rest_api.NamespaceActions.RUN_JOB
    )

    return client.build(rest_api.TaskGraphLogsApi).get_task_graph_log(
        namespace=namespace,
        id=str(the_id),
    )


_API_STATUSES: Dict[st.Status, str] = {
    st.Status.COMPLETED: rest_api.TaskGraphLogStatus.SUCCEEDED,
    st.Status.FAILED: rest_api.TaskGraphLogStatus.FAILED,
    st.Status.CANCELLED: rest_api.TaskGraphLogStatus.CANCELLED,
}


def replace_stored_params(tree, loader: stored_params.ParamLoader) -> Any:
    """Descends into data structures and replaces Stored Params with results."""

    return _StoredParamReplacer(loader).visit(tree)


def _replace_nodes_with_results(tree):
    """Descends into data structures and replaces Node IDs with their values."""

    return _NodeResultReplacer().visit(tree)


def _find_parent_nodes(tree) -> Tuple[Node, ...]:
    df = _DepFinder()
    df.visit(tree)
    return tuple(df.nodes.values())


def _replace_nodes_with_stored_params(tree: _T) -> Tuple[_T, FrozenSet[uuid.UUID]]:
    """Descends into data structures and replaces Nodes with StoredParams.

    If a Node cannot be used as a StoredParam, replaces it with the value.
    Returns the replaced tree and the IDs that we saw.
    """
    nspr = _NodeToStoredParamReplacer()
    result = nspr.visit(tree)
    return result, frozenset(nspr.ids)


class _DepFinder(visitor.ReplacingVisitor):
    """Locates :class:`Node`s in the input. Never replaces anything."""

    def __init__(self):
        super().__init__()
        self.nodes: Dict[uuid.UUID, Node] = {}

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if isinstance(arg, Node):
            self.nodes[arg.id] = arg
        return None


class _NodeToStoredParamReplacer(visitor.ReplacingVisitor):
    """Replaces Nodes with :class:`stored_param.StoredParam`s (if possible).

    If it cannot replace a Node with a StoredParam, it replaces it
    with the Node's value.
    """

    def __init__(self):
        super().__init__()
        # A collection of the UUIDs we saw.
        self.ids: Set[uuid.UUID] = set()

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if not isinstance(arg, Node):
            # Not a node, just use it as-is.
            return None
        try:
            assert arg._result
            sp = arg._result.to_stored_param()
        except (TypeError, ValueError):
            # Can't make a StoredParam out of it.
            # Treat it like any other Node.
            pass
        else:
            self.ids.add(sp.task_id)
            return visitor.Replacement(sp)
        return visitor.Replacement(arg.result())


class _BatchArgEncoder(tiledb_json.Encoder):
    """Encodes arguments with the special format used by batch graphs."""

    def __init__(self, input_is_expanded: bool) -> None:
        self._input_is_expanded = input_is_expanded
        super().__init__()

    def maybe_replace(self, arg: object) -> Optional[visitor.Replacement]:
        if isinstance(arg, Node):
            if self._input_is_expanded:
                return visitor.Replacement("{{inputs.parameters.partId}}")
            return visitor.Replacement(
                {"__tdbudf__": "node_output", "client_node_id": str(arg.id)}
            )
        return super().maybe_replace(arg)


class _NodeResultReplacer(visitor.ReplacingVisitor):
    """Replaces :class:`Node`s with their results."""

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if isinstance(arg, Node):
            return visitor.Replacement(arg.result())
        return None


class _StoredParamReplacer(visitor.ReplacingVisitor):
    """Replaces stored parameters with their values."""

    def __init__(self, loader: stored_params.ParamLoader):
        super().__init__()
        self._loader = loader

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if isinstance(arg, stored_params.StoredParam):
            return visitor.Replacement(self._loader.load(arg))
        return None


def _topo_sort(
    lst: Sequence[rest_api.TaskGraphNodeMetadata],
) -> Sequence[rest_api.TaskGraphNodeMetadata]:
    """Topologically sorts the list of node metadatas."""
    by_uuid: Dict[str, rest_api.TaskGraphNodeMetadata] = {
        node.client_node_uuid: node for node in lst
    }
    in_degrees: Counter[str] = collections.Counter()
    # We reverse the input list so that when we reverse the output,
    # it's in an order kind of close to what we were given.
    for node in reversed(lst):
        # Ensure that we have an entry in the counter even for root nodes.
        in_degrees[node.client_node_uuid] += 0
        for dep_id in node.depends_on:
            if dep_id not in by_uuid:
                raise ValueError(
                    f"Node {node.client_node_uuid!r} depends upon"
                    f" non-existent node {dep_id!r}"
                )
            in_degrees[dep_id] += 1
    output: List[rest_api.TaskGraphNodeMetadata] = []
    queue: Deque[str] = collections.deque()
    for uid, degree in in_degrees.items():
        if degree == 0:
            queue.append(uid)

    while queue:
        nid = queue.popleft()
        node = by_uuid[nid]
        for dep_id in node.depends_on:
            in_degrees[dep_id] -= 1
            if in_degrees[dep_id] == 0:
                queue.append(dep_id)
        output.append(node)
    if sum(in_degrees.values()):
        participating = [uid for (uid, deg) in in_degrees.items() if deg]
        raise ValueError(f"The task graph contains a cycle involving {participating}")
    output.reverse()
    return output


def _topo_sort_nodes(
    by_uuid: Dict[uuid.UUID, Node],
) -> Sequence[Node]:
    """Topologically sorts the list of nodes."""
    in_degrees: Counter[str] = collections.Counter()
    # We reverse the input list so that when we reverse the output,
    # it's in an order kind of close to what we were given.
    for node in reversed(list(by_uuid.values())):
        # Ensure that we have an entry in the counter even for root nodes.
        in_degrees[node.id] += 0
        for dep_id in node.parents:
            if dep_id not in by_uuid:
                raise ValueError(
                    f"Node {node.id!r} depends upon" f" non-existent node {dep_id!r}"
                )
            in_degrees[dep_id] += 1
    output: List[Node] = []
    queue: Deque[str] = collections.deque()
    for uid, degree in in_degrees.items():
        if degree == 0:
            queue.append(uid)

    while queue:
        nid = queue.popleft()
        node = by_uuid[nid]
        for dep_id in node.parents:
            in_degrees[dep_id] -= 1
            if in_degrees[dep_id] == 0:
                queue.append(dep_id)
        output.append(node)
    if sum(in_degrees.values()):
        participating = [uid for (uid, deg) in in_degrees.items() if deg]
        raise ValueError(f"The task graph contains a cycle involving {participating}")
    output.reverse()
    return output


def array_task_status_to_status(status: models.ArrayTaskStatus) -> Status:
    return _ARRAY_TASK_STATUS_TO_STATUS_MAP.get(status, Status.NOT_STARTED)


def task_graph_log_status_to_status(status: models.TaskGraphLogStatus) -> Status:
    return _TASK_GRAPH_LOG_STATUS_TO_STATUS_MAP.get(status, Status.NOT_STARTED)
