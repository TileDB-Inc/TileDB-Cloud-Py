import uuid
from typing import Any, Dict, Optional, TypeVar

from ... import rest_api
from ..._results import tiledb_json
from . import _base

_T = TypeVar("_T")


class InputNode(_base.Node[_base.ET, _T]):
    def __init__(
        self,
        uid: uuid.UUID,
        owner: _base.ET,
        name: Optional[str],
        json_data: Dict[str, Any],
    ):
        super().__init__(uid, owner, name)
        input_data = json_data["input_node"]
        self._default_value_encoded = input_data.get("default_value", _base.NOTHING)
        self._value: Any = _base.NOTHING
        self._value_encoded: Any = _base.NOTHING

    def has_default(self):
        return self._default_value_encoded is not _base.NOTHING

    def _exec_impl(
        self,
        *,
        parents: Dict[uuid.UUID, _base.Node],
        input_value: Any,
        default_download_results: bool,
    ) -> None:
        del default_download_results  # Unused.
        assert not parents, "InputNode cannot depend on anything"
        if input_value is _base.NOTHING:
            self._value_encoded = self._default_value_encoded
            self._value = tiledb_json.Decoder().visit(self._value_encoded)
        else:
            self._value = input_value
            self._value_encoded = tiledb_json.Encoder().visit(input_value)

        if self._value_encoded is _base.NOTHING:
            raise KeyError(f"Input {self.name!r} must be provided")

    def task_id(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        return None

    def _result_impl(self):
        return self._value

    def _encode_for_param(self, mode: _base.ParamFormat):
        del mode  # unused
        self._assert_succeeded()
        return self._value_encoded

    def _run_location(self) -> str:
        return rest_api.TaskGraphLogRunLocation.VIRTUAL
