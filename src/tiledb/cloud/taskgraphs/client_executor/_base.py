"""Base types and functions for the client executor."""

import abc
import enum
import uuid
from typing import Any, Dict, Iterable, Optional, TypeVar

import attrs

from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud._common import futures
from tiledb.cloud.taskgraphs import executor

Status = executor.Status
NOTHING = attrs.make_class("Nothing", (), frozen=True, slots=True)()
"""Sentinel value to distinguish missing values from None."""


class IClientExecutor(executor.Executor["Node"], metaclass=abc.ABCMeta):
    """Executor sub-interface adding type information used by Nodes."""

    _client: client.Client
    _server_graph_uuid: Optional[uuid.UUID]

    @abc.abstractmethod
    def _enqueue_done_node(self, node: "Node") -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def _notify_node_status_change(self) -> None:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def namespace(self) -> str:
        raise NotImplementedError()


ET = TypeVar("ET", bound=IClientExecutor)
_T = TypeVar("_T")


class ParamFormat(enum.Enum):
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


class Node(executor.Node[ET, _T], metaclass=abc.ABCMeta):
    """Base class for Nodes to be executed locally.

    All public-facing methods MUST be thread-safe.
    """

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self._status: Status = Status.WAITING
        self._result_exception: Optional[Exception] = None
        """An exception that was raised when executing the Node."""
        self._lifecycle_exception: Optional[futures.CancelledError] = None
        """An exception that was set on the node by a lifecycle event.

        This is distinct from ``_result_exception`` because it will be RAISED
        by methods like `.exception()` rather than returned.
        """
        self._callback_runner = futures.CallbackRunner(self)

    #
    # External API.
    #

    def result(self, timeout: Optional[float] = None) -> _T:
        with self._lifecycle_condition:
            futures.wait_for(self._lifecycle_condition, self._done, timeout)
            exc = self._lifecycle_exception or self._result_exception
            if exc:
                raise exc
            return self._result_impl()

    def exception(self, timeout: Optional[float] = None) -> Optional[Exception]:
        with self._lifecycle_condition:
            futures.wait_for(self._lifecycle_condition, self._done, timeout)
            if self._lifecycle_exception:
                raise self._lifecycle_exception
            return self._result_exception

    def cancel(self) -> bool:
        with self._lifecycle_condition:
            cancelled = self._set_status_if_can_start(Status.CANCELLED)
            if not cancelled:
                return cancelled
            self._lifecycle_exception = futures.CancelledError()
            self._lifecycle_condition.notify_all()
            self.owner._enqueue_done_node(self)
            cbs = self._callbacks()
        if cancelled:
            self._callback_runner.run_callbacks(cbs)
        return cancelled

    def wait(self, timeout: Optional[float] = None) -> None:
        with self._lifecycle_condition:
            futures.wait_for(self._lifecycle_condition, self._done, timeout)

    #
    # Abstract methods to be implemented by subclasses to do the work of a Node.
    #

    @abc.abstractmethod
    def _exec_impl(
        self,
        *,
        parents: Dict[uuid.UUID, "Node"],
        input_value: Any,
        default_download_results: bool,
    ) -> None:
        """The type-specific behavior of executing a Node."""
        raise NotImplementedError()

    @abc.abstractmethod
    def _result_impl(self) -> _T:
        """Returns the result of this node's execution, if applicable.

        This will only ever be called after ``_event`` is set and the state is
        ``SUCCEEDED``. It should only ever be called inside ``result()``.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _encode_for_param(self, mode: ParamFormat) -> Any:
        """Encodes the result of this node for use in a JSON parameter list.

        This is used to pass the output of this Node into the parameters of a
        following Node.
        """
        raise NotImplementedError()

    #
    # Execution internals
    #

    def _status_impl(self) -> Status:
        return self._status

    def _exec(
        self,
        *,
        parents: Dict[uuid.UUID, "Node"],
        input_value: Any,
        default_download_results: bool,
    ) -> None:
        """The boilerplate for the ``_exec`` implementation for local Nodes.

        This handles all the lifecycle management for Node execution. It should
        only ever be called by the Executor. Subclasses should instead implement
        ``_exec_impl``, which contains the type-specific behavior.
        """
        with self._lifecycle_condition:
            # Make sure we're still in a runnable state (weren't just cancelled)
            if not self._set_status_if_can_start(Status.RUNNING):
                return

        try:
            self._exec_impl(
                parents=parents,
                input_value=input_value,
                default_download_results=default_download_results,
            )
        except Exception as ex:
            with self._lifecycle_condition:
                self._set_status_notify(Status.FAILED)
                self._result_exception = ex
                self.owner._enqueue_done_node(self)
                cbs = self._callbacks()
            raise
        else:
            with self._lifecycle_condition:
                self._set_status_notify(Status.SUCCEEDED)
                self._result_exception = None
                self.owner._enqueue_done_node(self)
                cbs = self._callbacks()
        finally:
            self._callback_runner.run_callbacks(cbs)

    #
    # Lifecycle-management internals.
    #

    def _assert_succeeded(self) -> None:
        if self._status is not Status.SUCCEEDED:
            raise AssertionError("_encoded_result is only valid for successful nodes")

    def _set_ready(self) -> None:
        with self._lifecycle_condition:
            self._set_status_if_can_start(Status.READY)

    def _set_status_if_can_start(self, status: Status) -> bool:
        """If this node is allowed to start, updates its status.

        Updates the status of this node, but only if it's unstarted (and is able
        to be started). Used to implement both :meth:`cancel` and the equivalent
        of ``Future.set_running_or_notify_cancel``.

        ``_lifecycle_condition`` must be held.
        """
        if self._status in (Status.WAITING, Status.READY):
            self._set_status_notify(status)
            return True
        return False

    def _set_status_notify(self, status: Status) -> None:
        """Sets the Node's status and notifies waiters.

        ``_lifecycle_condition`` must be held.
        """
        if self._status is status:
            return
        self._status = status
        self._lifecycle_condition.notify_all()
        self.owner._notify_node_status_change()

    def _set_parent_failed(
        self,
        pfe: executor.ParentFailedError,
        *,
        overwrite: bool = False,
    ) -> None:
        with self._lifecycle_condition:
            could_set = self._set_status_if_can_start(Status.PARENT_FAILED)
            if not could_set:
                return
            updated = False
            if overwrite or not self._lifecycle_exception:
                if self._lifecycle_exception is not pfe:
                    updated = True
                self._lifecycle_exception = pfe
            if not updated:
                return
            self.owner._enqueue_done_node(self)
            cbs = self._callbacks()

        self._callback_runner.run_callbacks(cbs)

    def _parent_failed_error(self) -> executor.ParentFailedError:
        """Returns the PFE that should be associated with this Node.

        If this node is the one that failed (or was cancelled), then returns
        a PFE corresponding to this node. If this node has a parent-failed
        status, returns the PFE that caused it.
        """
        with self._lifecycle_condition:
            st = self._status
            if st is Status.FAILED:
                assert self._result_exception
                return executor.ParentFailedError(self._result_exception, self)
            if st is Status.CANCELLED:
                assert self._lifecycle_exception
                return executor.ParentFailedError(self._lifecycle_exception, self)
            if st is Status.PARENT_FAILED:
                assert isinstance(self._lifecycle_exception, executor.ParentFailedError)
                return self._lifecycle_exception
        raise AssertionError(
            f"Accessing {self}._parent_failed_error() with status {st}"
        )

    def _prepare_to_retry(self) -> None:
        with self._lifecycle_condition:
            assert self._status in (
                Status.FAILED,
                Status.CANCELLED,
                Status.PARENT_FAILED,
            )
            self._set_status_notify(Status.WAITING)
            self._lifecycle_exception = None
            self._result_exception = None

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

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.display_name!r}>"
