import uuid
from typing import AbstractSet, Any, Dict, List, Optional, Sequence, TypeVar

import urllib3

from tiledb.cloud import rest_api
from tiledb.cloud import utils
from tiledb.cloud._common import json_safe
from tiledb.cloud._common import ordered
from tiledb.cloud._results import results
from tiledb.cloud.taskgraphs import _codec
from tiledb.cloud.taskgraphs.client_executor import _base
from tiledb.cloud.taskgraphs.client_executor import _replacers
from tiledb.cloud.taskgraphs.client_executor import array_node

_T = TypeVar("_T")


class UDFNode(_base.Node[_base.ET, _T]):
    """A Node that will actually execute a UDF."""

    def __init__(
        self,
        uid: uuid.UUID,
        owner: _base.ET,
        name: Optional[str],
        json_data: Dict[str, Any],
    ):
        super().__init__(uid, owner, name)
        udf_data: Dict[str, Any] = json_data["udf_node"]
        self._udf_data = udf_data
        """The UDF details, in JSON dict format."""
        self._registered_udf_name: Optional[str] = udf_data.get("registered_udf_name")
        """The UDF name, used to give this node a fallback name."""
        self._task_id: Optional[uuid.UUID] = None
        """The server-side task ID for this node's execution."""
        self._result: Optional[_codec.BinaryResult] = None
        """The bytes of the result, as returned from the server."""

    @property
    def fallback_name(self) -> str:
        if self._registered_udf_name:
            return f"UDF {self._registered_udf_name}"
        return super().fallback_name

    def task_id(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        self.wait(timeout)
        return self._task_id

    def _exec_impl(
        self, parents: Dict[uuid.UUID, _base.Node], input_value: Any
    ) -> None:
        assert input_value is _base.NOTHING

        # Parse the arguments.
        raw_args: List[Any] = self._udf_data["arguments"] or []
        stored_param_ids: AbstractSet[uuid.UUID]
        arrays: Sequence[Dict[str, Any]]
        if parents:
            replacer = _replacers.UDFParamReplacer(
                parents, _base.ParamFormat.STORED_PARAMS
            )
            replaced_args = replacer.visit(raw_args)
            stored_param_ids = ordered.FrozenSet(
                filter(None, (n.task_id() for n in replacer.seen_nodes))
            )
            arrays = tuple(
                n._udf_array_details()
                for n in replacer.seen_nodes
                if isinstance(n, array_node.ArrayNode)
            )
        else:
            # If there are no parents, then we only have the existing args.
            replaced_args = raw_args
            stored_param_ids = frozenset()
            arrays = []

        # Set up the basics of the call.
        udf_call = rest_api.MultiArrayUDF(
            task_name=self.display_name,
            stored_param_uuids=json_safe.Value([str(uid) for uid in stored_param_ids]),
            arrays=json_safe.Value(arrays),
            arguments_json=json_safe.Value(replaced_args),
            store_results=True,
            result_format=self._udf_data.get("result_format") or "python_pickle",
            client_node_uuid=str(self.id),
            task_graph_uuid=str(self.owner._server_graph_uuid),
            # This is for reference only.
            exec_raw=self._udf_data.get("source_text"),
        )

        # Set up the environment. The default value of everything in the
        # udf_call object is `None`, so setting it to None is equivalent to
        # leaving it unset.
        env: Dict[str, str] = self._udf_data.get("environment", {})
        udf_call.image_name = env.get("image_name")
        udf_call.language = env.get("language")
        udf_call.version = env.get("language_version")

        # Executable code.
        exec_code = self._udf_data.get("executable_code")
        if exec_code:
            udf_call._exec = exec_code
        else:
            try:
                udf_call.udf_info_name = self._udf_data["registered_udf_name"]
                # TEMPORARY FIX: The server is not properly extracting the
                # language/version information from registered UDFs.
                # Include the current language/version here until that's fixed.
                udf_call.language = "python"
                udf_call.version = utils.PYTHON_VERSION
            except KeyError as ke:
                raise AssertionError("Neither executable code nor UDF name set") from ke

        # Actually make the call.
        api = self.owner._client.udf_api
        try:
            resp: urllib3.HTTPResponse = api.submit_multi_array_udf(
                namespace=self.owner._namespace,
                udf=udf_call,
                _preload_content=False,
            )
        except rest_api.ApiException as exc:
            self._task_id = results.extract_task_id(exc)
            if "RETRY_WITH_PARAMS" not in exc.body:
                raise
        else:
            self._task_id = results.extract_task_id(resp)
            self._result = _codec.BinaryResult.from_response(resp)
            return

        # Our first request failed with a "RETRY_WITH_PARAMS" error.
        # Retry, but substitute in all stored parameters.
        values_replacer = _replacers.UDFParamReplacer(parents, _base.ParamFormat.VALUES)

        udf_call.stored_param_uuids = []
        udf_call.arguments_json = values_replacer.visit(raw_args)
        try:
            resp = api.submit_generic_udf(
                namespace=self.owner._namespace,
                udf=udf_call,
                _preload_content=False,
            )
        except rest_api.ApiException as exc:
            self._task_id = results.extract_task_id(exc)
            raise
        self._task_id = results.extract_task_id(resp)
        self._result = _codec.BinaryResult.from_response(resp)

    def _result_impl(self):
        return self._result.decode()

    def _encode_for_param(self, mode: _base.ParamFormat):
        self._assert_succeeded()
        if mode is _base.ParamFormat.STORED_PARAMS:
            if self._task_id is not None:
                return {
                    _codec.SENTINEL_KEY: "stored_param",
                    "task_id": str(self.task_id()),
                }
        assert self._result
        return self._result._tdb_to_json()
