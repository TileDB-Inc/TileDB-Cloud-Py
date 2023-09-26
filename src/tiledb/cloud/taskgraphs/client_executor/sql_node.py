import uuid
from typing import Any, Dict, Optional, TypeVar

from ... import rest_api
from ..._common import utils
from ..._results import codecs
from ..._results import results
from ..._results import tiledb_json
from .. import _results as tg_results
from . import _base
from . import _replacers

_T = TypeVar("_T")


class SQLNode(_base.Node[_base.ET, _T]):
    """A Node that executes a TileDB SQL query."""

    def __init__(
        self,
        uid: uuid.UUID,
        owner: _base.ET,
        name: Optional[str],
        json_data: Dict[str, Any],
    ):
        super().__init__(uid, owner, name)
        self._sql_data = json_data["sql_node"]
        self._task_id: Optional[uuid.UUID] = None
        """The server-side task ID for this node's execution."""
        self._result: Optional[tg_results.Result] = None
        """The bytes of the result, as returned from the server."""

    def task_id(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        self.wait(timeout)
        return self._task_id

    def _exec_impl(
        self,
        *,
        parents: Dict[uuid.UUID, _base.Node],
        input_value: Any,
        default_download_results: bool,
    ) -> None:
        assert input_value is _base.NOTHING

        raw_parameters = self._sql_data.get("parameters") or []
        if parents:
            replacer = _replacers.NodeOutputValueReplacer(parents)
            parameters = replacer.visit(raw_parameters)
        else:
            parameters = raw_parameters

        namespace = self._sql_data.get("namespace") or self.owner.namespace

        download_override = self._sql_data.get("download_results")
        download_results = (
            default_download_results if download_override is None else download_override
        )

        try:
            resp = self.owner._client.build(rest_api.SqlApi).run_sql(
                namespace=namespace,
                sql=rest_api.SQLParameters(
                    name=self.display_name,
                    query=self._sql_data["query"],
                    init_commands=self._sql_data.get("init_commands"),
                    parameters=parameters,
                    result_format=self._sql_data["result_format"],
                    store_results=True,
                    client_node_uuid=str(self.id),
                    task_graph_uuid=str(self.owner._server_graph_uuid),
                    dont_download_results=not download_results,
                ),
                _preload_content=False,
            )
        except rest_api.ApiException as apix:
            self._task_id = results.extract_task_id(apix)
            raise
        try:
            self._task_id = results.extract_task_id(resp)
            if download_results or not self._task_id:
                self._result = codecs.BinaryBlob.from_response(resp)
            else:
                self._result = tg_results.LazyResult(self.owner._client, self._task_id)
        finally:
            utils.release_connection(resp)

    def _result_impl(self):
        assert self._result
        return self._result.decode()

    def _encode_for_param(self, mode: _base.ParamFormat) -> Dict[str, Any]:
        self._assert_succeeded()
        if mode is _base.ParamFormat.STORED_PARAMS:
            if self._task_id:
                return {
                    tiledb_json.SENTINEL_KEY: "stored_param",
                    "task_id": str(self._task_id),
                }
        assert self._result
        return self._result._tdb_to_json()
