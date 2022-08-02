import base64
import datetime
import multiprocessing
import uuid
from typing import AbstractSet, Any, Dict, List, Optional, Sequence, TypeVar

import attrs
import cloudpickle
import urllib3

from tiledb.cloud import rest_api
from tiledb.cloud._common import json_safe
from tiledb.cloud._common import ordered
from tiledb.cloud._results import results
from tiledb.cloud.taskgraphs import _codec
from tiledb.cloud.taskgraphs import types
from tiledb.cloud.taskgraphs.client_executor import _base
from tiledb.cloud.taskgraphs.client_executor import _replacers
from tiledb.cloud.taskgraphs.client_executor import array_node

_T = TypeVar("_T")

_DEFAULT_LOCAL_TIMEOUT = datetime.timedelta(hours=1)
"""The default maximum amout of time we allow a local UDF to run."""


_MP_CTX = multiprocessing.get_context("spawn")


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

    def _is_local(self) -> bool:
        return bool(self._environment.get("run_client_side"))

    def _exec_impl(
        self, parents: Dict[uuid.UUID, _base.Node], input_value: Any
    ) -> None:
        assert input_value is _base.NOTHING

        if self._is_local():
            self._exec_local(parents)
            # TODO: Add a way that users can specify that they want to retry
            # a local UDF remotely.
            return
        self._exec_remote(parents)

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
        upr = _replacers.UDFParamReplacer(parents, _base.ParamFormat.VALUES)
        # An Arguments whose entries are CallArgs. These are not fully decoded
        # to native values since we need to pass them to our worker process
        # while still CloudPickle-encoded (since regular Pickle may not handle
        # them correctly).
        call_args_args = _replacers.visit_args(upr, registered_args_args)

        # Use an 'or' rather than `.get("timeout", default)` since we want to
        # use the default timeout if it is set to zero.
        udf_timeout: Optional[int] = self._environment.get("timeout")
        actual_timeout = udf_timeout or _DEFAULT_LOCAL_TIMEOUT.total_seconds()

        # TODO: Have the executor own a process pool and execute on that.
        q = _MP_CTX.SimpleQueue()
        p = _MP_CTX.Process(
            name=f"{self.display_name} worker process",
            target=_run_udf,
            args=(self._executable_code, call_args_args, q),
        )
        p.start()
        try:
            p.join(actual_timeout)
            p.terminate()  # No-op if the process already completed.
            if p.exitcode != 0:
                # The built-in TimeoutError is NOT a futures.TimeoutError
                # and represents a different outcome.
                raise TimeoutError(
                    f"{self.display_name} terminated with code {p.exitcode}"
                )
        finally:
            p.join(1)
            # Python 3.6 doesn't have process.Close; sub in a no-op if needed.
            getattr(p, "close", lambda: None)()
        result: _RunResult = q.get()
        if result.internal_exception:
            roe = RemoteOnlyError(result.internal_exception)
            raise roe from result.internal_exception
        if result.user_exception:
            raise result.user_exception
        assert result.result
        self._result = result.result
        # TODO: Report local execution success to the server.

    def _exec_remote(self, parents: Dict[uuid.UUID, _base.Node]) -> None:
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
        )

        if not (self._executable_code or self._registered_udf_name):
            raise ValueError("Neither executable code nor UDF name set")

        # Actually make the call.
        api = self.owner._client.udf_api
        try:
            resp: urllib3.HTTPResponse = api.submit_multi_array_udf(
                namespace=self._environment.get("namespace") or self.owner._namespace,
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
        udf_call.arguments_json = values_replacer.visit(self._arguments)
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

    def _run_location(self) -> str:
        if self._is_local():
            return rest_api.TaskGraphLogRunLocation.CLIENT
        return rest_api.TaskGraphLogRunLocation.SERVER


def _run_udf(
    exec_data: str, encoded_args: types.Arguments, ret: multiprocessing.SimpleQueue
) -> None:
    unesc = _replacers.NodeOutputValueReplacer({})
    try:
        udf_pkl = base64.b64decode(exec_data)
        udf = cloudpickle.loads(udf_pkl)
        real_args = _replacers.visit_args(unesc, encoded_args)
    except Exception as e:
        ret.put(_RunResult(internal_exception=e))
        return

    try:
        result = real_args.apply(udf)
    except Exception as e:
        ret.put(_RunResult(user_exception=e))
        return
    try:
        bin_result = _codec.BinaryResult.of(result)
    except Exception as e:
        ret.put(_RunResult(internal_exception=e))
    else:
        ret.put(_RunResult(result=bin_result))


@attrs.define(frozen=True, slots=True)
class _RunResult:
    result: Optional[_codec.BinaryResult] = None
    internal_exception: Optional[Exception] = None
    user_exception: Optional[Exception] = None


class RemoteOnlyError(RuntimeError):
    """Raised when a UDF can only be executed server-side."""
