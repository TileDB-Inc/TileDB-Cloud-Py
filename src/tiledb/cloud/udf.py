import base64
import uuid
import warnings
from typing import Any, Callable, Iterable, Optional, Union

import cloudpickle

from . import array
from . import client
from . import rest_api
from . import tiledb_cloud_error
from ._common import functions
from ._common import json_safe
from ._common import utils
from ._common import visitor
from ._results import decoders
from ._results import results
from ._results import sender
from ._results import stored_params
from ._results import tiledb_json
from ._results import types
from .rest_api import ApiException as GenApiException
from .rest_api import models

# Deprecated; re-exported for backwards compatibility.
tiledb_cloud_protocol = utils.TILEDB_CLOUD_PROTOCOL


def exec_base(
    func: Union[str, Callable, Any],
    *args: Any,
    name: Optional[str] = None,
    namespace: Optional[str] = None,
    image_name: str = "default",
    http_compressor: Optional[str] = "deflate",
    include_source_lines: bool = True,
    task_name: Optional[str] = None,
    result_format: str = "tiledb_json",
    result_format_version=None,
    store_results: bool = False,
    stored_param_uuids: Iterable[uuid.UUID] = (),
    timeout: int = None,
    resource_class: Optional[str] = None,
    _download_results: bool = True,
    _server_graph_uuid: Optional[uuid.UUID] = None,
    _client_node_uuid: Optional[uuid.UUID] = None,
    access_credentials_name: Optional[str] = None,
    **kwargs,
) -> "results.RemoteResult":
    """Run a user defined function, returning the result and metadata.

    :param func: The function to call, either as a callable function, or as
        the name of a registered user-defined function. (If ``name`` is set,
        this is instead prepended to ``args`` for backwards compatibility.)
    :param args: The arguments to pass to the function.
    :param name: DEPRECATED. If present, the name of the user-defined function
        to run.
    :param namespace: namespace to run udf under
    :param image_name: udf image name to use, useful for testing beta features
    :param http_compressor: set http compressor for results
    :param include_source_lines: True to send the source code of your UDF to
        the server with your request. (This means it can be shown to you
        in stack traces if an error occurs.) False to send only compiled Python
        bytecode.
    :param str task_name: optional name to assign the task
        for logging and audit purposes
    :param ResultFormat result_format: result serialization format
    :param str result_format_version: Deprecated and ignored.
    :param store_results: True to temporarily store results on the server side
        for later retrieval (in addition to downloading them).
    :param timeout: Timeout for UDF in seconds
    :param resource_class: The name of the resource class to use. Resource classes
        define maximum limits for cpu and memory usage.
    :param _download_results: True to download and parse results eagerly.
        False to not download results by default and only do so lazily
        (e.g. for an intermediate node in a graph).
    :param _server_graph_uuid: If this function is being executed within a DAG,
        the server-generated ID of the graph's log. Otherwise, None.
    :param _client_node_uuid: If this function is being executed within a DAG,
        the ID of this function's node within the graph. Otherwise, None.
    :param kwargs: named arguments to pass to function
    """

    if result_format_version:
        warnings.warn(DeprecationWarning("result_format_version is unused."))

    api_instance = client.build(rest_api.UdfApi)

    namespace = namespace or client.default_charged_namespace(
        required_action=rest_api.NamespaceActions.RUN_JOB
    )

    user_func: Union[str, Callable]
    if name:
        warnings.warn(
            DeprecationWarning(
                "Use of `name` to set a function name is deprecated. "
                "Pass the function name in `func` instead."
            )
        )
        if type(name) is not str:
            raise TypeError("`name` (if used) must be the name of a function.")
        args = (func,) + args
        user_func = name
    else:
        if not callable(func) and type(func) is not str:
            raise TypeError(
                "`func` must be either a callable function "
                f"or the name of a registered UDF as a str, not {type(func)}"
            )
        user_func = func

    udf_model = models.MultiArrayUDF(
        language=models.UDFLanguage.PYTHON,
        result_format=result_format,
        store_results=store_results,
        version=utils.PYTHON_VERSION,
        image_name=image_name,
        task_name=task_name,
        stored_param_uuids=list(str(uuid) for uuid in stored_param_uuids),
        resource_class=resource_class,
        dont_download_results=not _download_results,
        task_graph_uuid=_server_graph_uuid and str(_server_graph_uuid),
        client_node_uuid=_client_node_uuid and str(_client_node_uuid),
        access_credentials_name=access_credentials_name,
    )

    if timeout is not None:
        udf_model.timeout = timeout

    if callable(user_func):
        udf_model._exec = utils.b64_pickle(user_func)
        if include_source_lines:
            udf_model.exec_raw = functions.getsourcelines(user_func)
    else:
        udf_model.udf_info_name = user_func

    arguments = types.Arguments(args, kwargs)
    udf_model.arguments_json = json_safe.Value(
        _StoredParamJSONer().encode_arguments(arguments)
    )

    submit_kwargs = dict(namespace=namespace, udf=udf_model)
    if http_compressor:
        submit_kwargs["accept_encoding"] = http_compressor

    return sender.send_udf_call(
        api_instance.submit_generic_udf,
        submit_kwargs,
        decoders.Decoder(result_format),
        id_callback=array._maybe_set_last_udf_id,
        results_stored=store_results,
        results_downloaded=_download_results,
    )


@functions.signature_of(exec_base)
def exec(*args, **kwargs) -> Any:
    """Run a user defined function, synchronously, returning only the result.

    Arguments are exactly as in :func:`exec_base`.
    """
    return exec_base(*args, **kwargs).get()


@functions.signature_of(exec_base)
def exec_async(*args, **kwargs) -> Any:
    """Run a user defined function, asynchronously.

    Arguments are exactly as in :func:`exec_base`.
    """
    return sender.wrap_async_base_call(exec_base, *args, **kwargs)


def register_udf(
    func,
    name,
    namespace=None,
    image_name=None,
    type=None,
    include_source_lines=True,
    async_req=False,
):
    """

    :param func: function to register
    :param name: name of udf to register
    :param namespace: namespace to register in
    :param image_name: optional image name
    :param type: type of udf, generic or single_array
    :param include_source_lines: disables sending sources lines of function
        along with udf
    :param async_req: return future instead of results for async support
    :return:
    """

    try:
        api_instance = client.build(rest_api.UdfApi)

        namespace = namespace or client.default_user().username

        if not callable(func):
            raise TypeError("First argument to `exec` must be callable!")

        pickledUDF = cloudpickle.dumps(func, protocol=utils.TILEDB_CLOUD_PROTOCOL)
        pickledUDF = base64.b64encode(pickledUDF).decode("ascii")

        source_lines = functions.getsourcelines(func) if include_source_lines else None

        udf_model = models.UDFInfoUpdate(
            name=name,
            language=models.UDFLanguage.PYTHON,
            version=utils.PYTHON_VERSION,
            image_name=image_name,
            type=type,
            _exec=pickledUDF,
            exec_raw=None,
        )

        if source_lines is not None:
            udf_model.exec_raw = source_lines

        api_instance.register_udf_info(
            namespace=namespace, name=name, udf=udf_model, async_req=async_req
        )

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def register_generic_udf(
    func,
    name,
    namespace=None,
    image_name=None,
    include_source_lines=True,
    async_req=False,
):
    """

    :param func: function to register
    :param name: name of udf to register
    :param namespace: namespace to register in
    :param image_name: optional image name
    :param include_source_lines: disables sending sources lines of function
        along with udf
    :param async_req: return future instead of results for async support
    :return:
    """
    return register_udf(
        func=func,
        name=name,
        namespace=namespace,
        image_name=image_name,
        type=models.UDFType.GENERIC,
        include_source_lines=include_source_lines,
        async_req=async_req,
    )


def register_single_array_udf(
    func,
    name,
    namespace=None,
    image_name=None,
    include_source_lines=True,
    async_req=False,
):
    """

    :param func: function to register
    :param name: name of udf to register
    :param namespace: namespace to register in
    :param image_name: optional image name
    :param include_source_lines: disables sending sources lines of function
        along with udf
    :param async_req: return future instead of results for async support
    :return:
    """
    return register_udf(
        func=func,
        name=name,
        namespace=namespace,
        image_name=image_name,
        type=models.UDFType.SINGLE_ARRAY,
        include_source_lines=include_source_lines,
        async_req=async_req,
    )


def register_multi_array_udf(
    func,
    name,
    namespace=None,
    image_name=None,
    include_source_lines=True,
    async_req=False,
):
    """

    :param func: function to register
    :param name: name of udf to register
    :param namespace: namespace to register in
    :param image_name: optional image name
    :param include_source_lines: disables sending sources lines of function
        along with udf
    :param async_req: return future instead of results for async support
    :return:
    """
    return register_udf(
        func=func,
        name=name,
        namespace=namespace,
        image_name=image_name,
        type=models.UDFType.MULTI_ARRAY,
        include_source_lines=include_source_lines,
        async_req=async_req,
    )


def update_udf(
    func,
    name,
    namespace=None,
    update_name=None,
    image_name=None,
    type=None,
    license_id=None,
    license_text=None,
    readme=None,
    include_source_lines=True,
    async_req=False,
):
    """

    :param func: function to update register
    :param name: name of udf to register
    :param namespace: namespace to register in
    :param update_name: new name for udf - physical folder will not be renamed,
        just the registered array name
    :param image_name: optional image name
    :param type: type of udf, generic or single_array
    :param license_id: license id for udf according to https://spdx.org/licenses/
    :param license_text: text of license for udf
    :param readme: readme of udf
    :param include_source_lines: disables sending sources lines of function
        along with udf
    :param async_req: return future instead of results for async support
    :return:
    """

    try:
        api_instance = client.build(rest_api.UdfApi)

        namespace = namespace or client.default_user().username

        if not callable(func):
            raise TypeError("First argument to `exec` must be callable!")

        pickledUDF = cloudpickle.dumps(func, protocol=utils.TILEDB_CLOUD_PROTOCOL)
        pickledUDF = base64.b64encode(pickledUDF).decode("ascii")

        source_lines = functions.getsourcelines(func) if include_source_lines else None

        update_udf_name = name
        if update_name is not None and update_name != "":
            update_udf_name = update_name

        udf_model = models.UDFInfoUpdate(
            name=update_udf_name,
            language=models.UDFLanguage.PYTHON,
            version=utils.PYTHON_VERSION,
            image_name=image_name,
            license_id=license_text,
            license_text=license_id,
            readme=readme,
            type=type,
            _exec=pickledUDF,
            exec_raw=None,
        )

        if source_lines is not None:
            udf_model.exec_raw = source_lines

        api_instance.update_udf_info(
            namespace=namespace, name=name, udf=udf_model, async_req=async_req
        )

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def update_generic_udf(
    func,
    name,
    namespace=None,
    image_name=None,
    include_source_lines=True,
    async_req=False,
):
    """

    :param func: function to register
    :param name: name of udf to register
    :param namespace: namespace to register in
    :param image_name: optional image name
    :param include_source_lines: disables sending sources lines of function
        along with udf
    :param async_req: return future instead of results for async support
    :return:
    """
    return update_udf(
        func=func,
        name=name,
        namespace=namespace,
        image_name=image_name,
        type=models.UDFType.GENERIC,
        include_source_lines=include_source_lines,
        async_req=async_req,
    )


def update_single_array_udf(
    func,
    name,
    namespace=None,
    image_name=None,
    include_source_lines=True,
    async_req=False,
):
    """

    :param func: function to register
    :param name: name of udf to register
    :param namespace: namespace to register in
    :param image_name: optional image name
    :param include_source_lines: disables sending sources lines of function
        along with udf
    :param async_req: return future instead of results for async support
    :return:
    """
    return update_udf(
        func=func,
        name=name,
        namespace=namespace,
        image_name=image_name,
        type=models.UDFType.SINGLE_ARRAY,
        include_source_lines=include_source_lines,
        async_req=async_req,
    )


def info(namespace=None, name=None, async_req=False):
    """
    Fetch info on a registered udf
    :param namespace: namespace to filter to
    :param name: name of udf to get info
    :param async_req: return future instead of results for async support
    :return: registered udf details
    """
    try:
        api_instance = client.build(rest_api.UdfApi)

        if not (
            namespace is not None
            and name is not None
            and namespace != ""
            and name != ""
        ):
            namespace = client.default_user().username

        return api_instance.get_udf_info(
            namespace=namespace, name=name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


"""
Share a registered udf
"""


def share(name=None, namespace=None, async_req=False):
    """
    Share a registered udf
    :param name: name of udf in "namespace/name" format
    :param namespace: namespace to share array with
    :param async_req: return future instead of results for async support
    :return: registered udf details
    """
    (udf_namespace, udf_name) = name.split("/")

    if not (
        udf_namespace is not None
        and udf_name is not None
        and udf_namespace != ""
        and udf_name != ""
    ):
        udf_namespace = client.default_user().username

    try:
        api_instance = client.build(rest_api.UdfApi)

        return api_instance.share_udf_info(
            udf_namespace,
            udf_name,
            udf_sharing=models.UDFSharing(
                namespace=namespace, actions=[models.UDFActions.FETCH_UDF]
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def unshare(name=None, namespace=None, async_req=False):
    """
    Share a registered udf
    :param name: name of udf in "namespace/name" format
    :param namespace: namespace to share array with
    :param async_req: return future instead of results for async support
    :return: registered udf details
    """
    (udf_namespace, udf_name) = name.split("/")

    if not (
        udf_namespace is not None
        and udf_name is not None
        and udf_namespace != ""
        and udf_name != ""
    ):
        udf_namespace = client.default_user().username

    try:
        api_instance = client.build(rest_api.UdfApi)

        return api_instance.share_udf_info(
            udf_namespace,
            udf_name,
            udf_sharing=models.UDFSharing(namespace=namespace),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


"""
Delete a registered udf
"""


def delete(name, namespace, async_req=False):
    """
    Deletes a registered udf
    :param name: name of udf
    :param namespace: namespace the udf belongs to
    :param async_req: return future instead of results for async support
    :return: deleted udf details
    """
    try:
        api_instance = client.build(rest_api.UdfApi)

        return api_instance.delete_udf_info(
            namespace,
            name,
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


class _StoredParamJSONer(tiledb_json.Encoder):
    """Turns parameters passed to the existing UDF APIs into TileDB JSON.

    Existing code needs to maintain the same interface for stored params,
    so to match the behavior of the Pickle-based argument encoding,
    we still accept ``StoredParam`` objects as parameters to the various UDF
    execution functions.
    """

    def maybe_replace(self, arg: object) -> Optional[visitor.Replacement]:
        if isinstance(arg, stored_params.StoredParam):
            return visitor.Replacement(
                {
                    tiledb_json.SENTINEL_KEY: "stored_param",
                    "task_id": str(arg.task_id),
                    # Because the decoder may contain special logic apart from
                    # "just read in the tdbjson-serialized object", we need to
                    # specify the exact Decoder object we will use.
                    "python_decoder": self.visit(arg.decoder),
                }
            )
        return super().maybe_replace(arg)
