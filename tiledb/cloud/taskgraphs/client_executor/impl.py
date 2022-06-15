"""The actual implementation of the client executor.

Ordinarily you should just import this via its alias in `client_executor`.
"""

import queue
import threading
import uuid
import warnings
from concurrent import futures
from typing import Any, Dict, Optional, Type, TypeVar

from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud._common import ordered
from tiledb.cloud.taskgraphs import executor
from tiledb.cloud.taskgraphs.client_executor import _base
from tiledb.cloud.taskgraphs.client_executor import array_node
from tiledb.cloud.taskgraphs.client_executor import input_node
from tiledb.cloud.taskgraphs.client_executor import sql_node
from tiledb.cloud.taskgraphs.client_executor import udf_node

# Define InvalidStateError if it hasn't been defined yet.
if hasattr(futures, "InvalidStateError"):
    InvalidStateError = futures.InvalidStateError  # type: ignore[attr-defined]

else:

    class InvalidStateError(futures._base.Error):  # type: ignore[attr-defined,no-redef]
        """The operation is not allowed in this state."""


Status = _base.Status
_T = TypeVar("_T")
Node = _base.Node["LocalExecutor", _T]

_API_STATUSES = {
    Status.SUCCEEDED: rest_api.TaskGraphLogStatus.SUCCEEDED,
    Status.FAILED: rest_api.TaskGraphLogStatus.FAILED,
    Status.CANCELLED: rest_api.TaskGraphLogStatus.CANCELLED,
}


class LocalExecutor(_base.IClientExecutor):
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
        self._done_node_queue: queue.Queue[Node] = queue.Queue()
        """Queue where completed nodes are added as they are done.

        This acts as the event loop for ``_exec_loop.``
        """
        for n in self._deps:
            n.add_done_callback(self._done_node_queue.put)
        self._inputs: Dict[uuid.UUID, Any] = {}
        self._client = api_client or client.client

        self._active_deps = self._deps.copy()
        """The dependency graph of not-yet-complete nodes.

        This includes both currently-running and to-be-executed Nodes.
        """
        self._unstarted_nodes = ordered.Set(self._deps)
        self._running_nodes = ordered.Set[Node]()
        self._failed_nodes = ordered.Set[Node]()
        self._succeeded_nodes = ordered.Set[Node]()

        self._lifecycle_lock = threading.Lock()
        self._status: Status = Status.WAITING
        self._server_graph_uuid = None

        if self.name:
            self._prefix = f"task-graph-{self.name}"
        else:
            self._prefix = repr(self)
        self._event_loop_thread = threading.Thread(
            name=self._prefix + "-executor",
            target=self._run,
            daemon=True,
        )
        self._pool = futures.ThreadPoolExecutor(
            max_workers=parallel_server_tasks,
            thread_name_prefix=self._prefix + "-worker",
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
            if isinstance(node, input_node.InputNode)
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
        _base.wait_for(self._done_event, timeout)

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
            cls = array_node.ArrayNode
        elif "input_node" in node_json:
            cls = input_node.InputNode
        elif "sql_node" in node_json:
            cls = sql_node.SQLNode
        elif "udf_node" in node_json:
            cls = udf_node.UDFNode
        else:
            raise ValueError("Could not determine node type")
        return cls(uid, self, name, node_json)  # type: ignore[misc] # false alarm

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
        finally:
            with self._lifecycle_lock:
                if self._status is not Status.CANCELLED:
                    if self._failed_nodes:
                        self._status = Status.FAILED
                    else:
                        self._status = Status.SUCCEEDED
            self._report_server_completion()
            self._done_event.set()
            self._pool.shutdown()

    def _handle_node_done(self, node: "Node") -> None:
        assert threading.current_thread() is self._event_loop_thread
        # The node may not be running, e.g. if it was cancelled.
        # That's fine.
        self._running_nodes.discard(node)
        if node.status is Status.SUCCEEDED:
            # Only remove successful nodes from the "active deps" list
            # to support retrying failed/cancelled nodes.
            self._active_deps.remove(node)
            self._succeeded_nodes.add(node)
        else:
            self._exception = self._exception or node._exception
            self._failed_nodes.add(node)

    def _start_ready_nodes(self):
        """Starts all nodes that are ready to run."""
        if self.status is Status.CANCELLED:
            return
        # Using an explicit annotation here because, while collections.abc–based
        # sets accept any iterable in __and__, that can't be reflected in
        # typeshed because the `set` builtin does not do so.
        eligible: ordered.Set[Node] = self._unstarted_nodes & self._active_deps.roots()
        for node in eligible:
            self._start_one_node(node)

    def _start_one_node(self, node: Node) -> None:
        """Handles the execution of exactly one Node."""
        parents = {n.id: n for n in self._deps.parents_of(node)}
        if not all(p.status is Status.SUCCEEDED for p in parents.values()):
            return
        self._unstarted_nodes.discard(node)
        self._running_nodes.add(node)
        self._pool.submit(node._exec, parents, self._inputs.get(node.id, _base.NOTHING))

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
        except KeyError:
            warnings.warn(
                UserWarning(f"Task graph ended in invalid state {self.status!r}")
            )

        # Kick off a non-daemonic thread to report completion so that we don't
        # block on the server call when reporting doneness to the caller,
        # but also we don't let the process terminate while we're still
        # reporting.
        #
        # ┄: blocked, ═: running, •: synchronization point, ×: termination
        # [d] = daemon thread
        #
        # main:  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄╒══════×
        # worker[d]:     ══════•══×              │      ┊
        # event loop[d]: ┄┄┄┄┄┄╘═══════•═╕┄┄┄┄╒══•══×   main terminates
        # reporter:            ┊       ┊ ┊   ═•══╪═══════════×
        #         last node done       ┊ ┊    ┊  ┊           ┊
        #                 start reporter ┊    ┊  ┊           reporter terminates
        #            reporter_running.wait    ┊  ┊
        #                  reporter_running.set  ┊
        #                         self._done_event
        #
        # Without this non-daemon reporter, the Python interpreter could stop
        # as soon as main terminates, meaning that the reporter might not
        # get the chance to report graph completion to the server.
        # With the non-daemon reporter, the interpreter remains running until
        # the reporting thread completes.
        #
        # The reporter_running event is needed because otherwise it's possible
        # for self._done_event to be set and main to terminate before the
        # reporter thread even has time to get started.
        reporter_running = threading.Event()

        def report_completion():
            reporter_running.set()
            try:
                client.client.task_graph_logs_api.update_task_graph_log(
                    id=str(self.server_graph_uuid),
                    namespace=self._namespace,
                    log=rest_api.TaskGraphLog(status=api_st),
                )
            except rest_api.ApiException as apix:
                warnings.warn(UserWarning(f"Error reporting graph completion: {apix}"))

        threading.Thread(
            target=report_completion,
            name=self._prefix + "-reporter",
            daemon=False,
        ).start()
        reporter_running.wait()
