import base64
import uuid
from typing import AbstractSet, Any, Dict, List, Optional, Sequence, TypeVar

import cloudpickle
import urllib3

from ... import rest_api
from ..._common import json_safe
from ..._common import ordered
from ..._common import utils
from ..._results import codecs
from ..._results import results
from ..._results import tiledb_json
from .. import _results as tg_results
from . import _base
from . import _replacers
from . import array_node

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
        self._environment: Dict[str, Any] = udf_data.get("environment", {})
        """Information about the environment where this UDF will run."""
        self._executable_code: Optional[str] = udf_data.get("executable_code")
        """The base64 pickle of the code to be executed, if present."""
        self._registered_udf_name: Optional[str] = udf_data.get("registered_udf_name")
        """The name of the registered UDF to execute, if present."""
        self._arguments: List[_replacers.UDFArgument] = udf_data.get("arguments", [])
        """The RegisteredArg-formatted args that will be passed to this UDF."""
        self._source_text: Optional[str] = udf_data.get("source_text")
        """The source text of the function, for reference only."""
        self._result_format: str = udf_data.get("result_format") or "python_pickle"
        """The format results should be returned in."""
        self._download_results: Optional[bool] = udf_data.get("download_results")
        """The override of the default result-downlaind behavior, if set."""

        self._task_id: Optional[uuid.UUID] = None
        """The server-side task ID for this node's execution."""
        self._result: Optional[tg_results.Result] = None
        """The bytes of the result, as returned from the server."""

    @property
    def fallback_name(self) -> str:
        if self._registered_udf_name:
            return f"UDF {self._registered_udf_name}"
        return super().fallback_name

    def task_id(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        self.wait(timeout)
        return self._task_id

    def _is_local(self) -> bool:
        return bool(self._environment.get("run_client_side"))

    def _exec_impl(
        self,
        *,
        parents: Dict[uuid.UUID, _base.Node],
        input_value: Any,
        default_download_results: bool,
    ) -> None:
        assert input_value is _base.NOTHING

        if self._is_local():
            self._exec_local(parents)
            # TODO: Add a way that users can specify that they want to retry
            # a local UDF remotely.
        else:
            self._exec_remote(
                parents, default_download_results=default_download_results
            )

    def _exec_local(self, parents: Dict[uuid.UUID, _base.Node]) -> None:
        lang = self._environment.get("language")
        if lang != "python":
            # Since we're Python, we can only execute more Python.
            raise RemoteOnlyError(f"Can't execute {lang!r} UDF locally.")
        if not self._executable_code:
            raise RemoteOnlyError(
                f"Can't execute registered UDF {self._registered_udf_name!r} locally."
            )

        # An Arguments whose entries are RegisteredArgs.
        registered_args_args = _replacers.parse_json_args(self._arguments)
        replacer = _replacers.NodeOutputValueReplacer(parents)
        try:
            udf_pkl = base64.b64decode(self._executable_code)
            udf = cloudpickle.loads(udf_pkl)
            real_args = _replacers.visit_args(replacer, registered_args_args)
        except Exception as e:
            raise RemoteOnlyError(e) from e

        output = real_args.apply(udf)
        self._result = codecs.BinaryBlob.of(output)
        # TODO: Report local execution success to the server.

    def _exec_remote(
        self, parents: Dict[uuid.UUID, _base.Node], *, default_download_results: bool
    ) -> None:
        # Parse the arguments.
        stored_param_ids: AbstractSet[uuid.UUID]
        arrays: Sequence[Dict[str, Any]]
        if parents:
            replacer = _replacers.UDFParamReplacer(
                parents, _base.ParamFormat.STORED_PARAMS
            )
            replaced_args = replacer.visit(self._arguments)
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
            replaced_args = self._arguments
            stored_param_ids = frozenset()
            arrays = []

        download_results = (
            default_download_results
            if self._download_results is None
            else self._download_results
        )

        # Set up the basics of the call.
        # The default value of everything in MultiArrayUDF is None, so values
        # that were already None are equivalent to leaving them unset.
        udf_call = rest_api.MultiArrayUDF(
            _exec=self._executable_code,
            udf_info_name=self._registered_udf_name,
            task_name=self.display_name,
            stored_param_uuids=json_safe.Value([str(uid) for uid in stored_param_ids]),
            arrays=json_safe.Value(arrays),
            arguments_json=json_safe.Value(replaced_args),
            store_results=True,
            result_format=self._result_format,
            client_node_uuid=str(self.id),
            task_graph_uuid=str(self.owner._server_graph_uuid),
            exec_raw=self._source_text,  # For reference only.
            image_name=self._environment.get("image_name"),
            language=self._environment.get("language"),
            version=self._environment.get("language_version"),
            timeout=self._environment.get("timeout"),
            resource_class=self._environment.get("resource_class"),
            dont_download_results=not download_results,
        )

        if not (self._executable_code or self._registered_udf_name):
            raise ValueError("Neither executable code nor UDF name set")

        # Actually make the call.
        api = self.owner._client.build(rest_api.UdfApi)
        try:
            resp: urllib3.HTTPResponse = api.submit_multi_array_udf(
                namespace=self._environment.get("namespace") or self.owner.namespace,
                udf=udf_call,
                _preload_content=False,
            )
        except rest_api.ApiException as exc:
            self._task_id = results.extract_task_id(exc)
            if "RETRY_WITH_PARAMS" not in exc.body:
                raise
        else:
            self._set_result(resp, download_results=download_results)
            return

        # Our first request failed with a "RETRY_WITH_PARAMS" error.
        # Retry, but substitute in all stored parameters.
        values_replacer = _replacers.UDFParamReplacer(parents, _base.ParamFormat.VALUES)

        udf_call.stored_param_uuids = []
        udf_call.arguments_json = values_replacer.visit(self._arguments)
        try:
            resp = api.submit_generic_udf(
                namespace=self.owner.namespace,
                udf=udf_call,
                _preload_content=False,
            )
        except rest_api.ApiException as exc:
            self._task_id = results.extract_task_id(exc)
            raise
        self._set_result(resp, download_results=download_results)

    def _set_result(
        self, resp: urllib3.HTTPResponse, *, download_results: bool
    ) -> None:
        """Handles all the internals of setting result information.

        This includes draining and releasing the HTTP connection.
        """
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

    def _encode_for_param(self, mode: _base.ParamFormat):
        self._assert_succeeded()
        if mode is _base.ParamFormat.STORED_PARAMS:
            if self._task_id is not None:
                return {
                    tiledb_json.SENTINEL_KEY: "stored_param",
                    "task_id": str(self.task_id()),
                }
        assert self._result
        return self._result._tdb_to_json()

    def _run_location(self) -> str:
        if self._is_local():
            return rest_api.TaskGraphLogRunLocation.CLIENT
        return rest_api.TaskGraphLogRunLocation.SERVER


class RemoteOnlyError(RuntimeError):
    """Raised when a UDF can only be executed server-side."""
