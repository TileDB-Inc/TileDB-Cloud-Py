"""The implementation of the batch server-side executor.
"""

import threading
import uuid
import time
import warnings
from typing import Optional, Dict, Any, Type, TypeVar

from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud._common import futures
from tiledb.cloud.taskgraphs import executor
from tiledb.cloud.taskgraphs.executor import Status
from tiledb.cloud.taskgraphs.batch_executor import _base, udf_node, input_node

InvalidStateError = futures.InvalidStateError
_T = TypeVar("_T")
Node = _base.Node["BatchExecutor", _T]


class BatchExecutor(_base.IBatchExecutor):
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
        self._client = api_client or client.client
        super().__init__(graph)
        self._name = name
        self._namespace = namespace
        self._inputs: Dict[uuid.UUID, Any] = {}

        self._done_condition = threading.Condition(threading.Lock())
        """Guards lifecycle events and is notified when the graph is done.

        The guarded state includes everything below here. All the state is owned
        by the event loop thread, but the lock must be held when modifying it
        in an externally-visible manner.
        """
        self._status: Status = Status.WAITING
        self._server_graph_uuid = None

        self._update_status_thread: Optional[threading.Thread] = None
        """The thread that is updating the status of the execution."""
        self._has_status_updates = False
        """True when a Node has status updates since the last callback."""
        self._update_callback_thread: Optional[threading.Thread] = None
        """If present, the thread that is dispatching update callbacks."""

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

        for (name, node) in input_nodes.items():
            node.set_value(input_value=inputs_by_id.get(node.id, _base.NOTHING))
            node._status: Status = Status.SUCCEEDED

        self._graph_json = self._executor_to_json()
        # TODO call the workflow submit API using _graph_json and set the _server_graph_uuid

        self._update_status_thread = threading.Thread(
            name=f"{self._prefix}-update-status",
            target=self._update_status,
            daemon=True,
        )
        self._update_status_thread.start()

    @property
    def status(self) -> Status:
        with self._done_condition:
            return self._status

    def wait(self, timeout: Optional[float] = None) -> None:
        with self._done_condition:
            _base.wait_for(self._done_condition, self._done, timeout)

    @property
    def server_graph_uuid(self) -> Optional[uuid.UUID]:
        pass

    def cancel(self) -> bool:
        return False

    def retry(self, node: _base.Node) -> bool:
        return self.retry_all()

    def retry_all(self) -> None:
        """Retries the workflow"""

        # TODO call workflow retry API and set the new _server_graph_uuid and restart the _update_status_thread
        pass

    def namespace(self) -> str:
        return self._namespace or client.default_charged_namespace()

    def _make_node(
        self,
        uid: uuid.UUID,
        name: Optional[str],
        node_json: Dict[str, Any],
    ) -> _base.Node:
        cls: Type[_base.Node]
        if "udf_node" in node_json:
            cls = udf_node.UDFNode
        elif "input_node" in node_json:
            cls = input_node.InputNode
        elif "array_node" in node_json:
            raise ValueError("Array node is not supported for batch execution")
        elif "sql_node" in node_json:
            raise ValueError("SQL node is not supported for batch execution")
        else:
            raise ValueError("Could not determine node type")
        return cls(uid, self, name, self._client, node_json)  # type: ignore[misc] # false alarm

    def _executor_to_json(self, override_name: Optional[str] = None):
        """Converts this task graph to a registerable/executable format."""
        nodes = self._deps.topo_sorted
        # We need to guarantee that the existing node names are maintained.
        existing_names = set(self._by_name)
        node_jsons = [n.to_registration_json(existing_names) for n in nodes]
        for n, n_json in zip(nodes, node_jsons):
            n_json["depends_on"] = [
                str(parent.id) for parent in self._deps.parents_of(n)
            ]
        return dict(
            name=override_name or self._name,
            nodes=node_jsons,
        )

    def _update_status(self) -> None:
        while True:
            time.sleep(2)
            if self._done():
                return

            try:
                result = self._client.build(
                    rest_api.TaskGraphLogsApi
                ).get_task_graph_log(namespace="TileDB-Inc", id=self._server_graph_uuid)
            except rest_api.ApiException as apix:
                raise
            else:
                for new_node in result.nodes:
                    node = self._by_name[new_node.name]
                    if not isinstance(node, input_node.InputNode):
                        if new_node.executions:
                            node.set_execution_id(
                                new_node.executions[len(new_node.executions) - 1].id
                            )
                        new_node_status = _base.array_task_status_to_executor_status(
                            new_node.status
                        )
                        if node.status != new_node_status:
                            self._has_status_updates = True
                            node.set_status_notify(new_node_status)

                with self._done_condition:
                    new_workflow_status = (
                        _base.task_graph_log_status_to_executor_status(result.status)
                    )
                    if self._status != new_workflow_status:
                        self._has_status_updates = True
                        self._status = new_workflow_status
                        self._done_condition.notify_all()

                self._notify_status_change()

    def _done(self) -> bool:
        return self._status in (
            Status.CANCELLED,
            Status.SUCCEEDED,
            Status.FAILED,
        )

    def _prefix(self) -> str:
        return f"task-graph-{self.name}" if self.name else repr(self)

    def _notify_status_change(self) -> None:
        """Called when updating the status of the execution.

        THE NODE CALLS THIS WHILE ITS LOCK IS HELD. This function must not do
        any major work of its own; instead it should dispatch to another thread.
        """
        with self._update_callbacks_lock:
            if not self._update_callbacks:
                return
            if not self._update_callback_thread:
                self._update_callback_thread = threading.Thread(
                    name=f"{self._prefix}-update-callbacks",
                    target=self._call_update_callbacks,
                )
                self._update_callback_thread.start()

    def _call_update_callbacks(self) -> None:
        while True:
            with self._update_callbacks_lock:
                if not self._has_status_updates:
                    # If there are no updates, then quit.
                    self._update_callback_thread = None
                    return
                self._has_status_updates = False
                cbs = tuple(self._update_callbacks)
            futures.execute_callbacks(self, cbs)
