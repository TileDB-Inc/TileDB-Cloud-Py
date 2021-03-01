from . import rest_api
from . import array
from . import client
from .rest_api import ApiException as GenApiException
from . import tiledb_cloud_error
from . import config
from . import utils

import cloudpickle

tiledb_cloud_protocol = 4

import base64
import sys


def exec_async(
    *args,
    func=None,
    name=None,
    namespace=None,
    image_name=None,
    http_compressor="deflate",
    include_source_lines=True,
    task_name=None,
    result_format=rest_api.models.UDFResultType.NATIVE,
    result_format_version=None,
    **kwargs
):
    """
     Run a user defined function


    :param args: arguments to pass to function
    :param func: user function to run
    :param name: registered function name
    :param namespace: namespace to run udf under
    :param image_name: udf image name to use, useful for testing beta features
    :param http_compressor: set http compressor for results
    :param include_source_lines: disables sending sources lines of function along with udf
    :param str task_name: optional name to assign the task for logging and audit purposes
    :param UDFResultType result_format: result serialization format
    :param str result_format_version: set a format version for cloudpickle or arrow IPC
    :param kwargs: named arguments to pass to function
    :return: UDFResult object which is a future containing the results of the UDF
    """

    api_instance = client.client.udf_api

    # If the namespace is not set, we will default to the user's namespace
    if namespace is None:
        # Fetch the client profile for username if it is not already cached
        if config.user is None:
            config.user = client.user_profile()

        namespace = client.find_organization_or_user_for_default_charges(config.user)

    if func is not None and not callable(func):
        raise TypeError("func argument to `exec` must be callable!")
    elif func is None and name is None or name == "":
        if args is not None and len(args) > 0:
            if callable(args[0]):
                func = args[0]
                args = args[1:]
        if func is None:
            raise TypeError(
                "name argument to `exec` must be set if no function is passed"
            )

    pickledUDF = None
    source_lines = None
    if func is not None:
        source_lines = utils.getsourcelines(func) if include_source_lines else None
        pickledUDF = cloudpickle.dumps(func, protocol=tiledb_cloud_protocol)
        pickledUDF = base64.b64encode(pickledUDF).decode("ascii")

    arguments = None
    if (args is not None and len(args) > 0) or (kwargs is not None and len(kwargs) > 0):
        arguments = []
        if len(args) > 0:
            arguments.append(args)
        if len(kwargs) > 0:
            arguments.append(kwargs)
        arguments = tuple(arguments)
        arguments = cloudpickle.dumps(arguments, protocol=tiledb_cloud_protocol)
        arguments = base64.b64encode(arguments).decode("ascii")

    if image_name is None:
        image_name = "default"
    try:

        kwargs = {"_preload_content": False, "async_req": True}
        if http_compressor is not None:
            kwargs["accept_encoding"] = http_compressor

        udf_model = rest_api.models.GenericUDF(
            language=rest_api.models.UDFLanguage.PYTHON,
            argument=arguments,
            result_format=result_format,
            result_format_version=result_format_version,
            version="{}.{}.{}".format(
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
            ),
            image_name=image_name,
            task_name=task_name,
        )

        if pickledUDF is not None:
            udf_model._exec = pickledUDF
        elif name is not None:
            udf_model.udf_info_name = name

        if source_lines is not None:
            udf_model.exec_raw = source_lines

        # _preload_content must be set to false to avoid trying to decode binary data
        response = api_instance.submit_generic_udf(
            namespace=namespace, udf=udf_model, **kwargs
        )

        return array.UDFResult(response, result_format=result_format)

    except GenApiException as exc:
        raise tiledb_cloud_error.check_sql_exc(exc) from None


def exec(
    *args,
    func=None,
    name=None,
    namespace=None,
    image_name=None,
    http_compressor="deflate",
    include_source_lines=True,
    task_name=None,
    result_format=rest_api.models.UDFResultType.NATIVE,
    result_format_version=None,
    **kwargs
):
    """
     Run a user defined function


    :param args: arguments to pass to function
    :param func: user function to run
    :param namespace: namespace to run udf under
    :param image_name: udf image name to use, useful for testing beta features
    :param http_compressor: set http compressor for results
    :param include_source_lines: disables sending sources lines of function along with udf
    :param str task_name: optional name to assign the task for logging and audit purposes
    :param UDFResultType result_format: result serialization format
    :param str result_format_version: set a format version for cloudpickle or arrow IPC
    :param kwargs: named arguments to pass to function
    :return: UDFResult object which is a future containing the results of the UDF
    """
    return exec_async(
        *args,
        func=func,
        name=name,
        namespace=namespace,
        image_name=image_name,
        http_compressor=http_compressor,
        include_source_lines=include_source_lines,
        task_name=task_name,
        result_format=result_format,
        result_format_version=result_format_version,
        **kwargs,
    ).get()


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

        pickledUDF = cloudpickle.dumps(func, protocol=tiledb_cloud_protocol)
        pickledUDF = base64.b64encode(pickledUDF).decode("ascii")

        source_lines = utils.getsourcelines(func) if include_source_lines else None

        udf_model = rest_api.models.UDFInfoUpdate(
            name=name,
            language=rest_api.models.UDFLanguage.PYTHON,
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
        type=rest_api.models.UDFType.GENERIC,
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
        type=rest_api.models.UDFType.SINGLE_ARRAY,
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

        pickledUDF = cloudpickle.dumps(func, protocol=tiledb_cloud_protocol)
        pickledUDF = base64.b64encode(pickledUDF).decode("ascii")

        source_lines = utils.getsourcelines(func) if include_source_lines else None

        update_udf_name = name
        if update_name is not None and update_name != "":
            update_udf_name = update_name

        udf_model = rest_api.models.UDFInfoUpdate(
            name=update_udf_name,
            language=rest_api.models.UDFLanguage.PYTHON,
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
        type=rest_api.models.UDFType.GENERIC,
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
        type=rest_api.models.UDFType.SINGLE_ARRAY,
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
            udf_sharing=rest_api.models.UDFSharing(
                namespace=namespace, actions=[rest_api.models.UDFActions.FETCH_UDF]
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
            udf_sharing=rest_api.models.UDFSharing(namespace=namespace),
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
