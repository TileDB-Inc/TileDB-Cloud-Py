import base64
import sys
import uuid
import warnings
from typing import Any, Callable, Iterable, Optional, Union

import cloudpickle

from tiledb.cloud import array
from tiledb.cloud import client
from tiledb.cloud import config
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud import utils
from tiledb.cloud._results import decoders
from tiledb.cloud._results import results
from tiledb.cloud.rest_api import ApiException as GenApiException
from tiledb.cloud.rest_api import models

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
    result_format: str = models.ResultFormat.NATIVE,
    result_format_version=None,
    store_results: bool = False,
    stored_param_uuids: Iterable[uuid.UUID] = (),
    timeout: int = None,
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
    :param kwargs: named arguments to pass to function
    """

    if result_format_version:
        warnings.warn(DeprecationWarning("result_format_version is unused."))

    api_instance = client.client.udf_api

    # If the namespace is not set, we will default to the user's namespace
    if namespace is None:
        # Fetch the client profile for username if it is not already cached
        if config.user is None:
            config.user = client.user_profile()

        namespace = client.find_organization_or_user_for_default_charges(config.user)

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

    udf_model = models.GenericUDF(
        language=models.UDFLanguage.PYTHON,
        result_format=result_format,
        store_results=store_results,
        version="{}.{}.{}".format(
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro,
        ),
        image_name=image_name,
        task_name=task_name,
        stored_param_uuids=list(str(uuid) for uuid in stored_param_uuids),
    )

    if timeout is not None:
        udf_model.timeout = timeout

    if callable(user_func):
        udf_model._exec = utils.b64_pickle(user_func)
        if include_source_lines:
            udf_model.exec_raw = utils.getsourcelines(user_func)
    else:
        udf_model.udf_info_name = user_func

    arguments = tuple(filter(None, [args, kwargs]))
    if arguments:
        udf_model.argument = utils.b64_pickle(arguments)

    submit_kwargs = dict(namespace=namespace, udf=udf_model)
    if http_compressor:
        submit_kwargs["accept_encoding"] = http_compressor

    return client.send_udf_call(
        api_instance.submit_generic_udf,
        submit_kwargs,
        decoders.Decoder(result_format),
        id_callback=array._maybe_set_last_udf_id,
        results_stored=store_results,
    )


@utils.signature_of(exec_base)
def exec(*args, **kwargs) -> Any:
    """Run a user defined function, synchronously, returning only the result.

    Arguments are exactly as in :func:`exec_base`.
    """
    return exec_base(*args, **kwargs).get()


@utils.signature_of(exec_base)
def exec_async(*args, **kwargs) -> Any:
    """Run a user defined function, asynchronously.

    Arguments are exactly as in :func:`exec_base`.
    """
    return client.client.wrap_async_base_call(exec_base, *args, **kwargs)


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
    :param include_source_lines: disables sending sources lines of function along with udf
    :param async_req: return future instead of results for async support
    :return:
    """

    try:
        api_instance = client.client.udf_api

        # If the namespace is not set, we will default to the user's namespace
        if namespace is None:
            # Fetch the client profile for username if it is not already cached
            if config.user is None:
                config.user = client.user_profile()

            namespace = config.user.username

        if not callable(func):
            raise TypeError("First argument to `exec` must be callable!")

        pickledUDF = cloudpickle.dumps(func, protocol=utils.TILEDB_CLOUD_PROTOCOL)
        pickledUDF = base64.b64encode(pickledUDF).decode("ascii")

        source_lines = utils.getsourcelines(func) if include_source_lines else None

        udf_model = models.UDFInfoUpdate(
            name=name,
            language=models.UDFLanguage.PYTHON,
            version="{}.{}.{}".format(
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
            ),
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
    :param include_source_lines: disables sending sources lines of function along with udf
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
    :param include_source_lines: disables sending sources lines of function along with udf
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
    :param update_name: new name for udf - physical folder will not be renamed, just the registered array name
    :param image_name: optional image name
    :param type: type of udf, generic or single_array
    :param license_id: license id for udf according to https://spdx.org/licenses/
    :param license_text: text of license for udf
    :param readme: readme of udf
    :param include_source_lines: disables sending sources lines of function along with udf
    :param async_req: return future instead of results for async support
    :return:
    """

    try:
        api_instance = client.client.udf_api

        # If the namespace is not set, we will default to the user's namespace
        if namespace is None:
            # Fetch the client profile for username if it is not already cached
            if config.user is None:
                config.user = client.user_profile()

            namespace = config.user.username

        if not callable(func):
            raise TypeError("First argument to `exec` must be callable!")

        pickledUDF = cloudpickle.dumps(func, protocol=utils.TILEDB_CLOUD_PROTOCOL)
        pickledUDF = base64.b64encode(pickledUDF).decode("ascii")

        source_lines = utils.getsourcelines(func) if include_source_lines else None

        update_udf_name = name
        if update_name is not None and update_name != "":
            update_udf_name = update_name

        udf_model = models.UDFInfoUpdate(
            name=update_udf_name,
            language=models.UDFLanguage.PYTHON,
            version="{}.{}.{}".format(
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
            ),
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
    :param include_source_lines: disables sending sources lines of function along with udf
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
    :param include_source_lines: disables sending sources lines of function along with udf
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
        api_instance = client.client.udf_api

        if not (
            namespace is not None
            and name is not None
            and namespace != ""
            and name != ""
        ):
            # If the namespace is not set, we will default to the user's namespace
            # Fetch the client profile for username if it is not already cached
            if config.user is None:
                config.user = client.user_profile()

            namespace = config.user.username

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
        # If the namespace is not set, we will default to the user's namespace
        # Fetch the client profile for username if it is not already cached
        if config.user is None:
            config.user = client.user_profile()

        udf_namespace = config.user.username

    try:
        api_instance = client.client.udf_api

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
        # If the namespace is not set, we will default to the user's namespace
        # Fetch the client profile for username if it is not already cached
        if config.user is None:
            config.user = client.user_profile()

        udf_namespace = config.user.username

    try:
        api_instance = client.client.udf_api

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
        api_instance = client.client.udf_api

        return api_instance.delete_udf_info(
            namespace,
            name,
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None
