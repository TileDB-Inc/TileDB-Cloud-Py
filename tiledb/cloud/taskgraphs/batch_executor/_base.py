"""Base types and functions for the server-side batch executor."""

import abc
import threading
import uuid
from typing import Callable, Optional, TypeVar

import attrs

from tiledb.cloud import client
from tiledb.cloud._common import futures
from tiledb.cloud.rest_api import models
from tiledb.cloud.taskgraphs import builder
from tiledb.cloud.taskgraphs import executor

Status = executor.Status
NOTHING = attrs.make_class("Nothing", (), frozen=True, slots=True)()
"""Sentinel value to distinguish missing values from None."""


class IBatchExecutor(executor.Executor["Node"], metaclass=abc.ABCMeta):
    """Executor sub-interface adding type information used by Nodes."""

    _client: client.Client
    _server_graph_uuid: Optional[uuid.UUID]


ET = TypeVar("ET", bound=IBatchExecutor)
_T = TypeVar("_T")

_Self = TypeVar("_Self", bound="Node")
"""Type for self-annotations where needed"""


class Node(executor.Node[ET, _T], builder.Node[_T], metaclass=abc.ABCMeta):
    """Base class for Nodes to be executed in batch mode.

    All public-facing methods MUST be thread-safe.
    """

    def __init__(
        self,
        uid: uuid.UUID,
        owner: ET,
        name: Optional[str],
        api_client: client.Client,
    ):
        super().__init__(uid, owner, name)
        self._client = api_client
        self._status: Status = Status.WAITING
        self._execution_id: uuid = None

    def set_execution_id(self, execution_id: uuid) -> None:
        self._execution_id = execution_id

    def set_status_notify(self, status: Status) -> None:
        """Sets the Node's status and notifies waiters."""
        with self._lifecycle_condition:
            if self._status is status:
                return
            self._status = status
            if self._done():
                futures.execute_callbacks(self, self._callbacks())
            self._lifecycle_condition.notify_all()

    def _status_impl(self) -> Status:
        return self._status


def array_task_status_to_executor_status(st: models.ArrayTaskStatus) -> Status:
    if st == models.ArrayTaskStatus.QUEUED:
        return Status.WAITING
    elif st == models.ArrayTaskStatus.FAILED:
        return Status.FAILED
    elif st == models.ArrayTaskStatus.COMPLETED:
        return Status.SUCCEEDED
    elif st == models.ArrayTaskStatus.RUNNING:
        return Status.RUNNING
    elif st == models.ArrayTaskStatus.RESOURCES_UNAVAILABLE:
        return Status.FAILED
    elif st == models.ArrayTaskStatus.UNKNOWN:
        return Status.FAILED
    elif st == models.ArrayTaskStatus.CANCELLED:
        return Status.CANCELLED
    elif st == models.ArrayTaskStatus.DENIED:
        return Status.FAILED
    else:
        return Status.WAITING


def task_graph_log_status_to_executor_status(st: models.TaskGraphLogStatus) -> Status:
    if st == models.TaskGraphLogStatus.SUBMITTED:
        return Status.WAITING
    elif st == models.TaskGraphLogStatus.RUNNING:
        return Status.RUNNING
    elif st == models.TaskGraphLogStatus.IDLE:
        return Status.SUCCEEDED
    elif st == models.TaskGraphLogStatus.ABANDONED:
        return Status.FAILED
    elif st == models.TaskGraphLogStatus.SUCCEEDED:
        return Status.SUCCEEDED
    elif st == models.TaskGraphLogStatus.FAILED:
        return Status.FAILED
    elif st == models.TaskGraphLogStatus.CANCELLED:
        return Status.CANCELLED
    else:
        return Status.WAITING


def wait_for(
    cond: threading.Condition,
    pred: Callable[[], bool],
    timeout: Optional[float],
) -> None:
    """Waits for the given condition variable, with a timeout.

    Condition's ``wait_for`` method will return after the given amount of time,
    even if the condition was not met, rather than raising a timeout (as one
    might expect). This corrects that expectation to raise that timeout.
    """
    if not cond.wait_for(pred, timeout):
        raise futures.TimeoutError(f"timed out after {timeout} sec")
