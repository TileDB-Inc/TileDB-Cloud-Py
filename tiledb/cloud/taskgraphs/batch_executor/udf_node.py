import uuid
import warnings
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
        try:
            return _codec.LazyResult(self._client, self._execution_id).decode()
        except rest_api.ApiException as apix:
            self.set_status_notify(Status.FAILED)
            self._result_exception = apix
            raise


    def exception(self, timeout: Optional[float] = None) -> Optional[Exception]:
        try:
            _codec.LazyResult(self._client, self._execution_id).decode()
        except rest_api.ApiException as apix:
            self.set_status_notify(Status.FAILED)
            self._result_exception = apix
        finally:
            return self._result_exception

    def cancel(self) -> bool:
        self.owner.cancel()

    def task_id(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        pass

    def to_registration_json(self, existing_names: Set[str]) -> Dict[str, Any]:
        return self._json_data
