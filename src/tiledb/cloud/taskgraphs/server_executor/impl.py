import abc
import threading
import time
import uuid
from typing import Any, Dict, Optional, TypeVar, Union

import urllib3
from typing_extensions import Self, TypedDict

from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud._common import futures
from tiledb.cloud.taskgraphs import _results
from tiledb.cloud.taskgraphs import executor

_T = TypeVar("_T")


class Node(executor.Node["ServerExecutor", _T], metaclass=abc.ABCMeta):
    """A Node executed on a server-side task graph.

    This can currently only be a UDF node.
    """

    def __init__(self, *args: Any):
        super().__init__(*args)
        self._status: executor.Status = executor.Status.WAITING
        self._result: Optional[_results.LazyResult] = None
        self._exception: Optional[Exception] = None
        self._latest_exec_id: Optional[uuid.UUID] = None
        self._callback_runner = futures.CallbackRunner(self)

    def _status_impl(self) -> executor.Status:
        return self._status

    def wait(self, timeout: Optional[float] = None) -> None:
        self.owner._maybe_start_status_updater()
        with self._lifecycle_condition:
            futures.wait_for(self._lifecycle_condition, self._done, timeout)

    def result(self, timeout: Optional[float] = None) -> _T:
        self.owner._maybe_start_status_updater()
        with self._lifecycle_condition:
            futures.wait_for(self._lifecycle_condition, self._done, timeout)
            if self._status.is_cancellation():
                raise futures.CancelledError()
            if self._exception is not None:
                raise self._exception
            result = self._load_result()
            try:
                decoded = result.decode()
            except Exception as ex:
                self._exception = ex
                raise
            if self._status is executor.Status.SUCCEEDED:
                return decoded
            # Unlike standard UDFs, results from server-side graph executions
            # return their results with a 200 HTTP status code.
            # This means we need to manually raise it ourselves.
            self._exception = _maybe_wrap_exc(decoded)
            raise self._exception

    def exception(self, timeout: Optional[float] = None) -> Optional[Exception]:
        self.owner._maybe_start_status_updater()
        with self._lifecycle_condition:
            futures.wait_for(self._lifecycle_condition, self._done, timeout)
            if self._status.is_cancellation():
                raise futures.CancelledError()
            if self._exception is not None:
                return self._exception
            if self._status is executor.Status.SUCCEEDED:
                return None
            try:
                result = self._load_result()
                decoded = result.decode()
            except rest_api.ApiException as apix:
                self._exception = apix
            else:
                self._exception = _maybe_wrap_exc(decoded)
            return self._exception

    def cancel(self) -> bool:
        """We do not yet support cancelling."""
        return False

    def task_id(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        self.owner._maybe_start_status_updater()
        with self._lifecycle_condition:
            futures.wait_for(
                self._lifecycle_condition,
                lambda: self._latest_exec_id is not None,
                timeout,
            )
            return self._latest_exec_id

    def _update_data(self, received_data: Any) -> bool:
        """Updates the status of this Node from the task graph status output.

        Returns True if anything changed; False if not.
        """
        with self._lifecycle_condition:
            json_status = received_data.get("status") or "UNKNOWN"
            try:
                new_status = executor.Status.from_array_task_status(json_status)
                status_changed = self._status is not new_status
                self._status = new_status
            except (AttributeError, ValueError):
                status_changed = False
            try:
                latest_exec = received_data["executions"][-1]
                exec_id = uuid.UUID(latest_exec["id"])
                exec_id_changed = self._latest_exec_id != exec_id
                self._latest_exec_id = exec_id
            except (KeyError, ValueError, IndexError, AttributeError):
                exec_id_changed = False
            if status_changed or exec_id_changed:
                # If the status changed, then our Result object is invalid.
                self._result = None
                self._exception = None
                self._lifecycle_condition.notify_all()
                self._callback_runner.run_callbacks(self._callbacks())
        return status_changed or exec_id_changed

    def _load_result(self) -> _results.LazyResult:
        """Loads the result of execution from the server."""
        if self._result:
            return self._result
        if not self._latest_exec_id:
            raise futures.InvalidStateError(
                f"{self} is reported complete but does not have an exec ID"
            )
        self._result = _results.LazyResult(self.owner._client, self._latest_exec_id)
        return self._result


class ServerExecutor(executor.Executor["Node"]):
    """Executor that manages server-side execution."""

    def __init__(
        self,
        server_graph: Dict[str, Any],
        *,
        api_client: client.Client = client.client,
    ) -> None:
        """Creates a new ServerExecutor connected to a graph.

        *Currently only supports connecting to existing graphs.*
        """
        super().__init__(server_graph)
        del server_graph  # We only want to access this as _graph_json.
        self._client = api_client
        self._namespace: str = self._graph_json["namespace"]
        self._server_graph_uuid = uuid.UUID(self._graph_json["uuid"])
        self._callback_runner = futures.CallbackRunner(self)
        self._done_condition = threading.Condition(threading.Lock())
        self._status: executor.Status = executor.Status.WAITING
        self._status_updater_thread: Optional[threading.Thread] = None
        self._run_single_update(self._graph_json)

    def _make_node(
        self, uid: uuid.UUID, name: Optional[str], node_json: Dict[str, Any]
    ) -> "Node":
        del node_json
        return Node(uid, self, name)

    @classmethod
    def load(
        cls,
        namespace: Optional[str],
        graph_id: uuid.UUID,
        *,
        api_client: client.Client = client.client,
    ) -> Self:
        return cls(_load_logs(api_client, namespace, graph_id), api_client=api_client)

    def _maybe_start_status_updater(self) -> None:
        with self._done_condition:
            if self._status_updater_thread:
                return
            self._status_updater_thread = threading.Thread(
                name=f"{self} status updater", target=self._status_updater, daemon=True
            )
            self._status_updater_thread.start()

    def _status_updater(self) -> None:
        """Internal thread to fetch graph status from server and update self."""
        # It's OK for us to access self._status outside a lock since we own it
        # and we're not modifying it here.
        while not self._status.is_terminal():
            current_log = _load_logs(
                self._client, self._namespace, self._server_graph_uuid
            )
            with self._done_condition:
                had_update = self._run_single_update(current_log)
                if had_update:
                    self._done_condition.notify_all()
                    with self._update_callbacks_lock:
                        self._callback_runner.run_callbacks(self._update_callbacks)
            time.sleep(1)

    def _run_single_update(self, current_log: Any) -> bool:
        try:
            new_status = executor.Status.from_task_graph_log_status(
                current_log.get("status")
            )
            status_changed = self._status is not new_status
            self._status = new_status
        except (AttributeError, ValueError):
            # If we get a completely unexpected status value,
            # just don't change anything.
            status_changed = False
        nodes = current_log.get("nodes") or ()
        any_node_update = False
        for node_data in nodes:
            node_id = uuid.UUID(node_data["client_node_uuid"])
            local_node = self._by_id[node_id]
            was_updated = local_node._update_data(node_data)
            any_node_update = any_node_update or was_updated
        return status_changed or any_node_update

    def execute(self, **inputs: Any) -> None:
        raise NotImplementedError(
            "The ServerExecutor currently only supports"
            " connecting to an existing execution."
        )

    @property
    def server_graph_uuid(self) -> Optional[uuid.UUID]:
        return self._server_graph_uuid

    @property
    def status(self) -> executor.Status:
        self._maybe_start_status_updater()
        with self._done_condition:
            return self._status

    def wait(self, timeout: Optional[float] = None) -> None:
        self._maybe_start_status_updater()
        with self._done_condition:
            futures.wait_for(self._done_condition, self._status.is_terminal, timeout)

    def __repr__(self) -> str:
        return f"<ServerExecutor for graph {self._server_graph_uuid}>"


class IngestorReturn(TypedDict):
    """Specification for the JSON data returned from ingestor functions:

    ``{"graph_id": "some-graph-uuid", "status": "(we don't use this)"}
    """

    graph_id: str


AnyGraphID = Union[IngestorReturn, str, uuid.UUID]


def connect(
    graph_id: AnyGraphID,
    namespace: Optional[str] = None,
    *,
    api_client: client.Client = client.client,
) -> ServerExecutor:
    """Connects to an existing task graph running server-side.

    :param graph_id: The identifier for a graph. This can be a UUID (either as
        a :class uuid.UUID: object or a string) or the return dictionary from
        an ingestor launcher (``{"graph_id": some_id, ...}``).
    :return: An Executor that can be used to get results from the task graph.
    """
    orig_id = type(graph_id)
    if isinstance(graph_id, dict):
        # We expect this to be the return from an ingestor.
        try:
            graph_id = graph_id["graph_id"]
        except KeyError as ke:
            raise ValueError(
                "input dictionary is not the return from a task graph launcher"
            ) from ke
    if isinstance(graph_id, str):
        try:
            graph_id = uuid.UUID(graph_id)
        except (TypeError, ValueError) as ex:
            raise ValueError(f"{orig_id!r} cannot be converted to a graph ID") from ex
    if isinstance(graph_id, uuid.UUID):
        return ServerExecutor.load(namespace, graph_id, api_client=api_client)
    raise TypeError(f"{type(orig_id)} cannot be converted to a task graph ID")


def _load_logs(
    api_client: client.Client, namespace: Optional[str], graph_id: uuid.UUID
) -> Dict[str, Any]:
    """Loads task graph logs as a JSON object."""
    namespace = namespace or client.default_charged_namespace(
        required_action=rest_api.NamespaceActions.RUN_JOB
    )

    response: urllib3.HTTPResponse = api_client.build(
        rest_api.TaskGraphLogsApi
    ).get_task_graph_log(
        namespace=namespace,
        id=str(graph_id),
        _preload_content=False,
    )

    return response.json()


def _maybe_wrap_exc(value: object) -> Exception:
    if isinstance(value, Exception):
        return value
    return Exception(value)
