"""The actual implementation of the client executor.

Ordinarily you should just import this via its alias in `client_executor`.
"""

import queue
import threading
import traceback
import uuid
import warnings
from typing import Any, Callable, Dict, Optional, Type, TypeVar

from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud._common import futures
from tiledb.cloud._common import ordered
from tiledb.cloud._common import utils
from tiledb.cloud.taskgraphs import executor
from tiledb.cloud.taskgraphs.client_executor import _base
from tiledb.cloud.taskgraphs.client_executor import array_node
from tiledb.cloud.taskgraphs.client_executor import input_node
from tiledb.cloud.taskgraphs.client_executor import sql_node
from tiledb.cloud.taskgraphs.client_executor import udf_node

InvalidStateError = futures.InvalidStateError
Status = _base.Status
_T = TypeVar("_T")
Node = _base.Node["LocalExecutor", _T]

_API_STATUSES = {
    Status.SUCCEEDED: rest_api.TaskGraphLogStatus.SUCCEEDED,
    Status.FAILED: rest_api.TaskGraphLogStatus.FAILED,
    Status.CANCELLED: rest_api.TaskGraphLogStatus.CANCELLED,
}

_REPORT_TIMEOUT_SECS = 10
"""The maximum request time when submitting non-essential log information."""


class LocalExecutor(_base.IClientExecutor):
    """Coordinates the execution of a task graph locally."""

    def __init__(
        self,
        graph: executor.GraphStructure,
        namespace: Optional[str] = None,
        *,
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
        self._name = name or self._graph_json.get("name")
        self._namespace = namespace
        self._event_queue: queue.Queue[Callable[[], None]] = queue.Queue()
        """Event queue used by the main loop.

        All events dispatched in the queue will be executed with
        ``_done_condition`` held.
        """
        self._inputs: Dict[uuid.UUID, Any] = {}
        self._client = api_client or client.client

        self._event_loop_thread = threading.Thread(
            name=self._prefix + "-executor",
            target=self._run,
            daemon=True,
        )
        self._pool = futures.ThreadPoolExecutor(
            max_workers=parallel_server_tasks,
            thread_name_prefix=self._prefix + "-worker",
        )

        self._done_condition = threading.Condition(threading.Lock())
        """Guards lifecycle events and is notified when the graph is done.

        The guarded state includes everything below here. All the state is owned
        by the event loop thread, but the lock must be held when modifying it
        in an externally-visible manner.
        """
        self._status: Status = Status.WAITING
        self._server_graph_uuid = None

        self._active_deps = self._deps.copy()
        """The dependency graph of not-yet-complete nodes.

        This includes both currently-running and to-be-executed Nodes.
        """
        self._unstarted_nodes = ordered.Set(self._deps)
        self._running_nodes = ordered.Set[Node]()
        self._failed_nodes = ordered.Set[Node]()
        self._succeeded_nodes = ordered.Set[Node]()

        self._exception: Optional[Exception] = None
        """The first exception that was raised by a failed Node."""
        self._internal_exception: Optional[Exception] = None
        """An exception raised in the event loop causing it to permafail.

        This should never happen; it indicates an internal logic error, but we
        keep it around to ensure that users don't block forever on failed tasks.
        """

        self._has_status_updates = False
        """True when a Node has status updates since the last callback."""
        self._callback_runner = futures.CallbackRunner(self)

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, new_name: Optional[str]) -> None:
        with self._done_condition:
            if self._status is not Status.WAITING:
                raise futures.InvalidStateError("cannot rename a running graph")
            self._name = new_name

    @property
    def namespace(self) -> str:
        return self._namespace or client.default_charged_namespace(
            required_action=rest_api.NamespaceActions.RUN_JOB
        )

    @namespace.setter
    def namespace(self, new_namespace: Optional[str]) -> None:
        with self._done_condition:
            if self._status is not Status.WAITING:
                raise futures.InvalidStateError(
                    "cannot change namespace of a running graph"
                )
            self._namespace = new_namespace

    @property
    def status(self) -> Status:
        with self._done_condition:
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

        with self._done_condition:
            if self._status is not Status.WAITING:
                raise InvalidStateError(f"Cannot execute a graph in {self._status}")

            self._inputs = inputs_by_id
            self._status = Status.RUNNING

        try:
            result = self._client.build(
                rest_api.TaskGraphLogsApi
            ).create_task_graph_log(
                namespace=self.namespace,
                log=self._build_log_structure(),
            )
        except rest_api.ApiException as apix:
            # There was a problem submitting the task graph for logging.
            # This should not abort the task graph.
            warnings.warn(UserWarning(f"Could not submit logging metadata: {apix}"))
        else:
            try:
                with self._done_condition:
                    self._server_graph_uuid = uuid.UUID(hex=result.uuid)
            except ValueError as ve:
                warnings.warn(
                    UserWarning(f"Server-provided graph ID was invalid: {ve}")
                )

        self._event_loop_thread.start()

    def cancel(self) -> bool:
        with self._done_condition:
            if self._status in (Status.SUCCEEDED, Status.FAILED):
                return False
            self._status = Status.CANCELLED
        return True

    def wait(self, timeout: Optional[float] = None) -> None:
        with self._done_condition:

            def is_done():
                return self._status in (
                    Status.CANCELLED,
                    Status.FAILED,
                    Status.SUCCEEDED,
                )

            futures.wait_for(self._done_condition, is_done, timeout)

    @property
    def server_graph_uuid(self):
        with self._done_condition:
            return self._server_graph_uuid

    def _make_node(
        self,
        uid: uuid.UUID,
        name: Optional[str],
        node_json: Dict[str, Any],
    ) -> Node:
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
        with self._done_condition:
            self._start_ready_nodes()
        just_reported_completion = False
        try:
            while self._active_deps:
                # The main loop continues to run until all nodes are finalized
                # (i.e., there are no failures or cancellations left).
                just_reported_completion = False
                event = self._event_queue.get()
                with self._done_condition:
                    event()
                    self._start_ready_nodes()
                    if self._running_nodes:
                        # Update ourselves to no longer be done if we still have
                        # nodes that are running.
                        if self._status is not Status.RUNNING:
                            self._status = Status.RUNNING
                            self._done_condition.notify_all()
                    else:
                        just_reported_completion = True
                        self._report_completion()
        except Exception as ex:
            # This means an exception has occurred on the event loop.
            # This should never happen, but to be safe we record our own
            # cancellation and permafail.
            with self._done_condition:
                self._exception = self._exception or ex
                self._internal_exception = ex
            just_reported_completion = False
            raise
        finally:
            if not just_reported_completion:
                with self._done_condition:
                    self._report_completion()
            self._pool.shutdown()

    def _enqueue_done_node(self, node: Node) -> None:
        """Called by a Node when it is about to be done.

        This should be called while the node's lifecycle lock is held, but
        about to be released so that all the invariants of a completed node
        are held, to guarantee that waiters are woken up only *after* the node
        is put onto the event queue.
        """
        self._event_queue.put(lambda: self._handle_node_done(node))

    def _handle_node_done(self, node: Node) -> None:
        assert threading.current_thread() is self._event_loop_thread
        # The node may not be running, e.g. if it was cancelled.
        # That's fine.
        self._running_nodes.discard(node)
        # We're guaranteed that the post-completion status of the node will not
        # change here because the only thread allowed to  reset a node back to
        # an incomplete state is this event loop.
        if node.status is Status.SUCCEEDED:
            # Only remove successful nodes from the "active deps" list
            # to support retrying failed/cancelled nodes.
            self._active_deps.remove(node)
            self._succeeded_nodes.add(node)
        else:
            self._failed_nodes.add(node)
            try:
                nex = node.exception()
            except Exception as exc_exc:
                nex = exc_exc
            self._exception = self._exception or nex
            self._failed_nodes.add(node)
            pfe = node._parent_failed_error()

            for child in self._deps.children_of(node):
                child._set_parent_failed(pfe)

    def _start_ready_nodes(self) -> None:
        """Starts all nodes that are ready to run."""
        if self._status is Status.CANCELLED:
            return
        # Using an explicit annotation here because, while collections.abc–based
        # sets accept any iterable in __and__, that can't be reflected in
        # typeshed because the `set` builtin does not do so.
        eligible: ordered.Set[Node] = self._unstarted_nodes & self._active_deps.roots()  # type: ignore[assignment,operator] # noqa: E501
        for node in eligible:
            self._maybe_start(node)

    def _maybe_start(self, node: Node) -> None:
        parents = {n.id: n for n in self._deps.parents_of(node)}
        if not all(p.status is Status.SUCCEEDED for p in parents.values()):
            return
        self._unstarted_nodes.discard(node)
        self._running_nodes.add(node)
        self._pool.submit(
            lambda: node._exec(
                parents=parents,
                input_value=self._inputs.get(node.id, _base.NOTHING),
                default_download_results=self._should_download_results(node),
            )
        )

    def _should_download_results(self, node: Node) -> bool:
        children = self._deps.children_of(node)
        if not children:
            # Always download terminal nodes by default.
            return True
        return any(
            child._run_location() != rest_api.TaskGraphLogRunLocation.SERVER
            for child in self._deps.children_of(node)
        )

    def retry(self, node: Node) -> bool:
        ft: "futures.Future[bool]" = futures.Future()
        self._event_queue.put(lambda: self._do_retry(node, ft))
        return ft.result()

    def _do_retry(self, node: Node, ft: "futures.Future[bool]") -> None:
        try:
            ft.set_result(self._retry_one(node))
        except Exception as e:
            ft.set_exception(e)
            raise

    def _retry_one(self, node: Node) -> bool:
        st = node.status
        if st not in (Status.FAILED, Status.CANCELLED):
            # We only actually retry nodes that failed (or were cancelled)
            # themselves. Parent-failed (or active) nodes cannot be retried.
            return False
        node._prepare_to_retry()
        self._failed_nodes.remove(node)
        self._unstarted_nodes.add(node)

        to_visit = ordered.Set(self._deps.children_of(node))
        # We use an ordered set as a queue, since we only want to visit a node
        # once while it's in the queue (e.g. if it was touched by both A and B,
        # while in the queue, we only need to visit it once) but we may still
        # need to visit a node multiple times (e.g. if a node is touched by A,
        # leaves the queue, then is later touched by B).

        while to_visit:
            visiting = to_visit.popleft()
            parents = self._deps.parents_of(visiting)
            failed_parents = tuple(
                p
                for p in parents
                if p.status in (Status.FAILED, Status.CANCELLED, Status.PARENT_FAILED)
            )
            if failed_parents:
                first = failed_parents[0]
                visiting._set_parent_failed(
                    first._parent_failed_error(), overwrite=True
                )
            elif visiting.status is Status.PARENT_FAILED:
                # If a node was manually cancelled, don't prepare it to be restarted.
                visiting._prepare_to_retry()
                self._failed_nodes.remove(visiting)
                self._unstarted_nodes.add(visiting)
            # Only continue on to visit parent-failed nodes.
            to_visit.update(self._deps.children_of(visiting))
        return True

    def retry_all(self) -> None:
        ft: "futures.Future[None]" = futures.Future()
        self._event_queue.put(lambda: self._do_retry_all(ft))
        return ft.result()

    def _do_retry_all(self, ft: "futures.Future[None]") -> None:
        try:
            all_failures = self._failed_nodes.copy()
            for n in all_failures:
                self._retry_one(n)
        except Exception as exc:
            ft.set_exception(exc)
            traceback.print_exc()
            raise
        ft.set_result(None)

    def _notify_node_status_change(self) -> None:
        """Called when a Node's status changes.

        THE NODE CALLS THIS WHILE ITS LOCK IS HELD. This function must not do
        any major work of its own; instead it should dispatch to another thread.
        """
        with self._update_callbacks_lock:
            self._callback_runner.run_callbacks(self._update_callbacks)

    #
    # Logging
    #

    def _build_log_structure(self) -> rest_api.TaskGraphLog:
        return rest_api.TaskGraphLog(
            name=self.name,
            namespace=self.namespace,
            nodes=[n._to_log_metadata(self._deps.parents_of(n)) for n in self._deps],
        )

    def _report_completion(self) -> None:
        if self._status is not Status.CANCELLED:
            if self._failed_nodes:
                self._status = Status.FAILED
            else:
                self._status = Status.SUCCEEDED
        self._report_server_completion()
        self._done_condition.notify_all()

    def _report_server_completion(self) -> None:
        if not self._server_graph_uuid:
            return
        st = self._status
        try:
            api_st = _API_STATUSES[st]
        except KeyError:
            warnings.warn(UserWarning(f"Task graph ended in invalid state {st!r}"))
            return

        do_update = utils.ephemeral_thread(
            client.build(rest_api.TaskGraphLogsApi).update_task_graph_log,
            name=self._prefix + "-reporter",
        )
        do_update(
            id=str(self._server_graph_uuid),
            namespace=self.namespace,
            log=rest_api.TaskGraphLog(status=api_st),
            _request_timeout=_REPORT_TIMEOUT_SECS,
        )

    @property
    def _prefix(self) -> str:
        return f"task-graph-{self.name}" if self.name else repr(self)
