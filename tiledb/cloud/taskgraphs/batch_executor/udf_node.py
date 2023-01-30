import uuid
from typing import Any, Dict, Optional, Set, TypeVar

from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud.taskgraphs import _codec
from tiledb.cloud.taskgraphs import executor
from tiledb.cloud.taskgraphs.batch_executor import _base

_T = TypeVar("_T")
Status = executor.Status


class UDFNode(_base.Node[_base.ET, _T]):
    def __init__(
        self,
        uid: uuid.UUID,
        owner: _base.ET,
        name: Optional[str],
        api_client: client.Client,
        json_data: Dict[str, Any],
    ):
        super().__init__(uid, owner, name, api_client)
        self._json_data = json_data

    def wait(self, timeout: Optional[float] = None) -> None:
        pass

    def result(self, timeout: Optional[float] = None) -> _T:
        with self._lifecycle_condition:
            _base.wait_for(self._lifecycle_condition, self._done, timeout)
        if self._status_impl() in (
            Status.FAILED,
            Status.CANCELLED,
            Status.PARENT_FAILED,
        ):
            raise RuntimeError("Workflow execution failed.")
        try:
            return _codec.LazyResult(self._client, self._execution_id).decode()
        except rest_api.ApiException as apix:
            self.set_status_notify(Status.FAILED)
            raise

    def exception(self, timeout: Optional[float] = None) -> Optional[Exception]:
        with self._lifecycle_condition:
            _base.wait_for(self._lifecycle_condition, self._done, timeout)
        if self._status_impl() != Status.FAILED:
            return None
        try:
            e = _codec.LazyResult(self._client, self._execution_id).decode()
            if isinstance(e, Exception):
                return e
            else:
                return rest_api.ApiException("Failed node result is not an Exception")
        except rest_api.ApiException as apix:
            self.set_status_notify(Status.FAILED)
            return apix

    def cancel(self) -> bool:
        self.owner.cancel()

    def task_id(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        pass

    def to_registration_json(self, existing_names: Set[str]) -> Dict[str, Any]:
        return self._json_data
