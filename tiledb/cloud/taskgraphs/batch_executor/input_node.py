import uuid
from typing import Any, Dict, Optional, TypeVar, Set

from tiledb.cloud import client
from tiledb.cloud.taskgraphs import _codec
from tiledb.cloud.taskgraphs.batch_executor import _base

_T = TypeVar("_T")


class InputNode(_base.Node[_base.ET, _T]):
    def __init__(
        self,
        uid: uuid.UUID,
        owner: _base.ET,
        name: Optional[str],
        api_client: client.Client,
        json_data: Dict[str, Any],
    ):
        super().__init__(uid, owner, name, api_client)
        input_data = json_data["input_node"]
        self._default_value_encoded = input_data.get("default_value", _base.NOTHING)
        self._default_value = _codec.Unescaper().visit(self._default_value_encoded)
        self._value: Any = _base.NOTHING
        self._value_encoded: Any = _base.NOTHING

    def wait(self, timeout: Optional[float] = None) -> None:
        return

    def result(self, timeout: Optional[float] = None) -> _T:
        return self._value

    def exception(self, timeout: Optional[float] = None) -> Optional[Exception]:
        return None

    def cancel(self) -> bool:
        raise ValueError("Input nodes can't be cancelled")

    def task_id(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        return None

    def has_default(self):
        return self._default_value_encoded is not _base.NOTHING

    def set_value(
        self,
        input_value: Any,
    ) -> None:
        if input_value is _base.NOTHING:
            self._value = self._default_value
            self._value_encoded = self._default_value_encoded
        else:
            self._value = input_value
            self._value_encoded = _codec.Escaper().visit(input_value)
        if self._value_encoded is _base.NOTHING:
            raise KeyError(f"Input {self.name!r} must be provided")

    def to_registration_json(self, existing_names: Set[str]) -> Dict[str, Any]:
        ret = super().to_registration_json(existing_names)
        input_node = {}
        if self._default_value_encoded is not _base.NOTHING:
            input_node["default_value"] = self._default_value_encoded
        if self._value_encoded is not _base.NOTHING:
            input_node["value"] = self._value_encoded
        ret["input_node"] = input_node
        return ret
