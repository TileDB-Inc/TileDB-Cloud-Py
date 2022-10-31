import uuid
from typing import Any, Dict, Optional, TypeVar

from tiledb.cloud import rest_api
from tiledb.cloud.taskgraphs.client_executor import _base
from tiledb.cloud.taskgraphs.client_executor import _replacers

_T = TypeVar("_T")


class ArrayNode(_base.Node[_base.ET, _T]):
    """A node representing a read from a TileDB Array.

    This node is not executed by itself; instead, it only appears as an input
    to TileDB UDF nodes.
    """

    def __init__(
        self,
        uid: uuid.UUID,
        owner: _base.ET,
        name: Optional[str],
        json_data: Dict[str, Any],
    ):
        super().__init__(uid, owner, name)
        self._array_data = json_data["array_node"]
        self._details: Optional[Dict[str, Any]] = None

    def _exec_impl(
        self,
        parents: Dict[uuid.UUID, _base.Node],
        input_value: Any,
        default_download_results: bool,
    ) -> None:
        del default_download_results  # Unused.
        assert input_value is _base.NOTHING
        uri = self._array_data["uri"]
        ranges = self._array_data.get("ranges")
        buffers = self._array_data.get("buffers")
        if parents:
            replacer = _replacers.NodeOutputValueReplacer(parents)
            uri = replacer.visit(uri)
            ranges = replacer.visit(ranges)
            buffers = replacer.visit(buffers)
        # Fix needed to work around deserialization problems on the server side.
        # TODO: remove this.
        ranges["ranges"] = ranges.get("ranges") or []
        self._details = dict(
            parameter_id=str(self.id),
            uri=uri,
            ranges=ranges,
            buffers=buffers,
        )

    def task_id(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        return None

    def _result_impl(self):
        raise TypeError("ArrayNode is a virtual node and does not have results.")

    def _udf_array_details(self) -> Dict[str, Any]:
        self._assert_succeeded()
        assert self._details
        return self._details

    def _encode_for_param(self, mode: _base.ParamFormat):
        del mode  # unused
        self._assert_succeeded()
        return {
            "__tdbudf__": "udf_array_details",
            "udf_array_details": self._udf_array_details(),
        }

    def _run_location(self) -> str:
        return rest_api.TaskGraphLogRunLocation.VIRTUAL
