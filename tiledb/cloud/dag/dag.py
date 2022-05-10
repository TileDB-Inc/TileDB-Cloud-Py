import collections
import datetime
import json
import numbers
import threading
import time
import uuid
import warnings
from concurrent import futures
from typing import (
    Any,
    Callable,
    Counter,
    Deque,
    Dict,
    FrozenSet,
    Generic,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
)

from tiledb.cloud import array
from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud import sql
from tiledb.cloud import tiledb_cloud_error as tce
from tiledb.cloud import udf
from tiledb.cloud._common import visitor
from tiledb.cloud._results import results
from tiledb.cloud._results import stored_params
from tiledb.cloud.dag import status as st
from tiledb.cloud.dag import visualization as viz
from tiledb.cloud.rest_api import models

Status = st.Status  # Re-export for compabitility.
_T = TypeVar("_T")
# Special string included in server errors when there is a problem loading
# stored parameters.
_RETRY_MSG = "RETRY_WITH_PARAMS"


class Node(Generic[_T]):
    def __init__(
        self,
        func: Callable[..., _T],
        *args: Any,
        name: Optional[str] = None,
        dag: Optional["DAG"] = None,
        local_mode: bool = False,
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

        self.error: Optional[BaseException] = None
        self.dag = dag
        self.local_mode: bool = local_mode

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
                not self.local_mode,
            )
        )
        self._download_results = _download_results

        self._future: "futures.Future[results.Result[_T]]" = futures.Future()
        """A proxy Future that is used to handle lifecycle events of this Node.

        The actual Future executes and then sends its results here.
        """
        self._future.add_done_callback(self._handle_completed_future)

        self.parents: Dict[uuid.UUID, Node] = {}
        self.children: Dict[uuid.UUID, Node] = {}

        self._has_node_args = False
        self.args: Tuple[Any, ...] = args
        self.kwargs: Dict[str, Any] = kwargs
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

    def _find_deps(self):
        """Finds Nodes this depends on and adds them to our dependency list."""
        parents = _find_parent_nodes((self.args, self.kwargs))
        for dep in parents:
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
        self._has_node_args = bool(parents)

    def depends_on(self, node: "Node"):
        """
        Create dependency chain for node, useful when there is a dependency that does not rely directly on passing
        results from one to another
        :param node: node to mark as a dependency of this node
        :return:
        """
        self.parents[node.id] = node
        node.children[self.id] = self

        if self.dag is None and node.dag is not None:
            self.dag = node.dag

    def cancel(self) -> bool:
        return self._future.cancel()

    def finished(self) -> bool:
        """
        Is the node finished
        :return: True if the node's function is finished
        """
        return self._future.done()

    done = finished

    def exec(self, namespace: Optional[str] = None):
        """
        Execute function for node
        :return: None
        """
        assert self.dag
        # This is the actual Future. After it finishes, we proxy its results
        # back to the proxy we have in `self._future`.
        real_ft = self.dag.executor.submit(self._do_exec, namespace)
        real_ft.add_done_callback(self._forward_to_proxy)

    def _forward_to_proxy(self, real: "futures.Future[results.Result[_T]]") -> None:
        """After the actual Future completes, forwards results to the proxy."""
        try:
            self._future.set_result(real.result())
        except BaseException as exc:
            if not self._future.cancelled():
                self.error = exc
                self._future.set_exception(exc)

    def _do_exec(self, namespace: Optional[str]) -> results.Result[_T]:
        if not self._future.set_running_or_notify_cancel():
            raise futures.CancelledError()
        assert self.dag
        self.dag.execute_update_callbacks()
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
        if not self.local_mode:
            # If it's not `local_mode`, we assume that the function is either
            # prewrapped or it was created with `Delayed`, so the function
            # itself is one of the `submit_xxx` (but not `_base`) functions.
            self.dag.initial_setup()
            kwargs.update(
                _server_graph_uuid=self.dag.server_graph_uuid,
                _client_node_uuid=self.id,
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
                        child.local_mode for child in self.parents.values()
                    )
                else:
                    # If this is a terminal node, always download results.
                    download_results = True
            else:
                download_results = self._download_results
            kwargs["_download_results"] = download_results

        try:
            return self._wrapped_func(*args, **kwargs)
        except tce.TileDBCloudError as exc:
            exc_msg = exc.args and exc.args[0]
            if not isinstance(exc_msg, str) or _RETRY_MSG not in exc_msg:
                # This is not a missing-stored-param error. Don't retry.
                raise

        args, kwargs = _replace_nodes_with_results((self.args, self.kwargs))
        return self._wrapped_func(*args, **kwargs)

    compute = exec

    def _handle_completed_future(self, _) -> None:
        assert self.dag
        self.dag.report_node_complete(self)

    def ready_to_compute(self):
        """
        Is the node ready to execute? Are all dependencies completed?
        :return: True if node is able to be run
        """
        if self.status != st.Status.NOT_STARTED:
            return False

        return all(node.finished() for node in self.parents.values())

    def result(self, timeout: Optional[float] = None) -> Optional[_T]:
        """
        Fetch results of function, block if not complete
        :return:
        """
        return self._future.result(timeout).get()

    @property
    def future(self) -> "futures.Future[_T]":
        # We return an UnwrapperProxy that acts just like a real Future,
        # at least as far as the caller is concerned.
        return results.UnwrapperProxy(self._future)  # type: ignore[return-value]

    @property
    def status(self) -> st.Status:
        ft = self._future
        if ft.running():
            return st.Status.RUNNING
        if ft.done():
            if ft.cancelled():
                return st.Status.CANCELLED
            if ft.exception():
                return st.Status.FAILED
            return st.Status.COMPLETED
        return st.Status.NOT_STARTED

    def task_id(self) -> Optional[uuid.UUID]:
        """Gets the server-side Task ID of this node.

        Returns None if this has no task ID (as it was run on the client side).
        """
        try:
            sp = self._future.result(timeout=0).to_stored_param()
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
        self._future.exception(timeout)

    def _to_log_metadata(self) -> rest_api.TaskGraphNodeMetadata:
        return rest_api.TaskGraphNodeMetadata(
            client_node_uuid=str(self.id),
            name=self.name,
            depends_on=[str(dep) for dep in self.parents],
            run_location=(
                rest_api.TaskGraphLogRunLocation.CLIENT
                if self.local_mode
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
    ):
        """
        DAG is a class for creating and managing direct acyclic graphs
        :param max_workers: how many workers should be used to execute the dag
        :param use_processes: if true will use processes instead of threads, defaults to threads
        :param done_callback: optional call back function to register for when dag is completed. Function will be passed reference to this dag
        :param update_callback: optional call back function to register for when dag status is updated. Function will be passed reference to this dag
        :param namespace: optional namespace to use for all tasks in DAG
        :param name: A human-readable name used to identify this task graph
            in logs. Does not need to be unique.
        """
        self.id = uuid.uuid4()
        self.nodes: Dict[uuid.UUID, Node] = {}
        self.nodes_by_name: Dict[str, Node] = {}
        self.completed_nodes: Dict[uuid.UUID, Node] = {}
        self.failed_nodes: Dict[uuid.UUID, Node] = {}
        self.running_nodes: Dict[uuid.UUID, Node] = {}
        self.not_started_nodes: Dict[uuid.UUID, Node] = {}
        self.cancelled_nodes: Dict[uuid.UUID, Node] = {}
        self.namespace = namespace or client.default_charged_namespace()
        self.name = name
        self.server_graph_uuid: Optional[uuid.UUID] = None
        """The server-generated UUID of this graph, used for logging.

        Will be ``None`` until :meth:`initial_setup` is called. If submitting
        the log works, will be the UUID; otherwise, will be None.
        """

        self.visualization = None

        self.executor: futures.Executor
        if use_processes:
            self.executor = futures.ProcessPoolExecutor(max_workers=max_workers)
        else:
            self.executor = futures.ThreadPoolExecutor(
                thread_name_prefix=f"dag-{self.name or self.id}-worker",
                max_workers=max_workers,
            )

        self.status = st.Status.NOT_STARTED

        self.done_callbacks = []
        self._called_done_callbacks = threading.Semaphore()
        if done_callback is not None and callable(done_callback):
            self.done_callbacks.append(done_callback)

        self.update_callbacks = []
        if update_callback is not None and callable(update_callback):
            self.update_callbacks.append(update_callback)

        self._lifecycle_lock = threading.Lock()
        self._tried_setup: bool = False

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def __ne__(self, other):
        return not (self == other)

    def initial_setup(self):
        """Performs one-time server-side setup tasks.

        Can safely be called multiple times.
        """
        with self._lifecycle_lock:
            if not self._tried_setup:
                log_structure = self._build_log_structure()
                try:
                    result = client.client.task_graph_logs_api.create_task_graph_log(
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
        :param func: Function to call when DAG status is updated. The function will be passed reference to this dag
        :return:
        """
        if not callable(func):
            raise TypeError("func to add_update_callback must be callable")

        self.update_callbacks.append(func)

    def add_done_callback(self, func):
        """
        Add a callback for when DAG is completed
        :param func: Function to call when DAG status is updated. The function will be passed reference to this dag
        :return:
        """
        if not callable(func):
            raise TypeError("func to add_done_callback must be callable")

        self.done_callbacks.append(func)

    def execute_update_callbacks(self):
        """
        Run user specified callbacks for status updates
        :return:
        """
        for func in self.update_callbacks:
            func(self)

    def _report_completion(self) -> None:
        """Reports the completion of the task graph to the server and callbacks."""
        if self._called_done_callbacks.acquire(blocking=False):
            self.executor.shutdown(wait=False)
            self._report_server_completion()
            for func in self.done_callbacks:
                func(self)

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
                namespace=self.namespace,
                log=rest_api.TaskGraphLog(status=api_st),
            )
        except rest_api.ApiException as apix:
            warnings.warn(UserWarning(f"Error reporting graph completion: {apix}"))

    def _update_status(self):
        """Updates the status and sets completion if we're done."""
        if self.running_nodes or self.not_started_nodes:
            return

        # If there is no running nodes we can assume it is complete and check if we should mark as failed or successful
        if len(self.failed_nodes) > 0:
            self.status = st.Status.FAILED
        elif len(self.cancelled_nodes) > 0:
            self.status = st.Status.CANCELLED
        else:
            self.status = st.Status.COMPLETED
        self._report_completion()

    def done(self):
        return self.status in (
            st.Status.FAILED,
            st.Status.CANCELLED,
            st.Status.COMPLETED,
        )

    def add_node_obj(self, node):
        """
        Add node to DAG
        :param node: to add to dag
        :return: node
        """
        self.nodes[node.id] = node
        self.nodes_by_name[str(node.name)] = node
        self.not_started_nodes[node.id] = node
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
        return self._add_raw_node(
            func_exec,
            *args,
            name=name,
            local_mode=local_mode,
            **kwargs,
        )

    def _add_raw_node(self, func_exec, *args, **kwargs):
        """Adds a generic (usually local) node to the graph."""
        node = Node(func_exec, *args, dag=self, **kwargs)
        return self.add_node_obj(node)

    def _add_prewrapped_node(
        self, func_exec, *args, name=None, store_results=True, **kwargs
    ):
        node = Node(
            *args,
            _internal_prewrapped_func=func_exec,
            dag=self,
            name=name,
            store_results=store_results,
            **kwargs,
        )
        return self.add_node_obj(node)

    def submit_array_udf(self, *args, **kwargs):
        """
        Submit a function that will be executed in the cloud serverlessly
        :param func_exec: function to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self._add_prewrapped_node(array.apply_base, *args, **kwargs)

    def submit_udf(self, *args, **kwargs):
        """
        Submit a function that will be executed in the cloud serverlessly
        :param func_exec: function to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self._add_prewrapped_node(udf.exec_base, *args, **kwargs)

    submit = submit_udf

    def submit_sql(self, *args, **kwargs):
        """
        Submit a sql query to run serverlessly in the cloud
        :param sql: query to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self._add_prewrapped_node(
            sql.exec_base,
            *args,
            _internal_accepts_stored_params=False,
            **kwargs,
        )

    def submit_local(self, *args, **kwargs):
        """
        Submit a function that will run locally
        :param func_exec: function to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self._add_raw_node(*args, local_mode=True, **kwargs)

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

        if node.status == st.Status.COMPLETED:
            self.completed_nodes[node.id] = node
            for child in node.children.values():
                self._exec_node(child)
            if node.local_mode:
                to_report = models.ArrayTaskStatus.COMPLETED
        else:
            if node.status == st.Status.CANCELLED:
                self.cancelled_nodes[node.id] = node
                to_report = models.ArrayTaskStatus.CANCELLED
            else:
                self.failed_nodes[node.id] = node
                if not isinstance(node.error, tce.TileDBCloudError) or node.local_mode:
                    to_report = models.ArrayTaskStatus.FAILED
            # Cancel dependents since this node has failed or been cancelled.
            for child in node.children.values():
                child.cancel()

        if self.server_graph_uuid and to_report:
            # Only report client-side events to the server if we've submitted
            # the structure of the graph.
            try:
                client.client.task_graph_logs_api.report_client_node(
                    id=str(self.server_graph_uuid),
                    namespace=self.namespace,
                    report=models.TaskGraphClientNodeStatus(
                        client_node_uuid=str(node.id),
                        status=to_report,
                    ),
                )
            except rest_api.ApiException:
                pass  # If we can't report a node status, don't worry about it.

        self.running_nodes.pop(node.id, None)
        self.not_started_nodes.pop(node.id, None)
        self.execute_update_callbacks()
        self._update_status()

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
        roots = self._find_root_nodes()
        if len(roots) == 0:
            raise tce.TileDBCloudError("DAG is circular, there are no root nodes")

        self.status = st.Status.RUNNING
        for node in roots:
            self._exec_node(node)

    def _exec_node(self, node):
        """
        Execute a node
        :param node: node to execute
        :return:
        """
        if node.ready_to_compute():
            self.running_nodes[node.id] = node
            del self.not_started_nodes[node.id]
            # Execute the node, the node will launch it's task with a worker pool from this dag
            node.exec(namespace=self.namespace)

    def wait(self, timeout=None):
        """
        Wait for DAG to be completed
        :param timeout: optional timeout in seconds to wait for DAG to be completed
        :return: None or raises TimeoutError if timeout occurs
        """

        if timeout is not None and not isinstance(timeout, numbers.Number):
            raise TypeError(
                "timeout must be numeric value representing seconds to wait"
            )

        start_time = time.time()
        end_time = None
        if timeout is not None:
            end_time = start_time + timeout
        while not self.done():
            if end_time is not None and time.time() >= end_time:
                raise futures.TimeoutError(
                    "timeout of {} reached and dag is not complete".format(timeout)
                )
            time.sleep(0.01)

        # in case of failure reraise the first failed node exception
        if self.status == st.Status.FAILED:
            raise next(iter(self.failed_nodes.values())).error

    def cancel(self):
        if self.status not in (st.Status.RUNNING, st.Status.NOT_STARTED):
            return
        for node in list(self.running_nodes.values()):
            node.cancel()
        for node in list(self.not_started_nodes.values()):
            node.cancel()

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
        :param notebook: Is the visualization inside a jupyter notebook? If so we'll use a widget
        :param auto_update: Should the diagram be auto updated with each status change
        :param force_plotly: Force the use of plotly graphs instead of TileDB Plot Widget
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

        :param notebook: Is the visualization inside a jupyter notebook? If so we'll use a widget
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

        # Build node x,y and also build a mapping of the graph market numbers to actual node objects so we can fetch status
        # The graph ends up with each market on a list, so we need to map from this list's order to actual nodes so we can look things up
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
    return client.client.task_graph_logs_api.list_task_graph_logs(
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

    namespace = namespace or client.default_charged_namespace()

    return client.client.task_graph_logs_api.get_task_graph_log(
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
            assert arg._future
            sp = arg._future.result().to_stored_param()
        except (TypeError, ValueError):
            # Can't make a StoredParam out of it.
            # Treat it like any other Node.
            pass
        else:
            self.ids.add(sp.task_id)
            return visitor.Replacement(sp)
        return visitor.Replacement(arg.result())


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
