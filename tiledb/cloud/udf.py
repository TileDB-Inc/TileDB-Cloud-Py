from . import rest_api
from . import array
from . import client
from .rest_api import ApiException as GenApiException
from . import tiledb_cloud_error
from . import config

import cloudpickle

tiledb_cloud_protocol = 4

import base64
import sys

last_udf_task_id = None


def exec_async(
    func, arguments=None, namespace=None, image_name=None, http_compressor="deflate",
):
    """
     Run a user defined function


    :param func: user function to run
    :param arguments: arguments to pass to function
    :param namespace: namespace to run udf under
    :param image_name: udf image name to use, useful for testing beta features
    :param http_compressor: set http compressor for results
    :return: UDFResult object which is a future containing the results of the UDF
    """

    api_instance = client.client.udf_api

    # If the namespace is not set, we will default to the user's namespace
    if namespace is None:
        # Fetch the client profile for username if it is not already cached
        if config.user is None:
            config.user = client.user_profile()

        namespace = config.user.username

    if not callable(func):
        raise TypeError("First argument to `apply` must be callable!")

    pickledUDF = cloudpickle.dumps(func, protocol=tiledb_cloud_protocol)
    pickledUDF = base64.b64encode(pickledUDF).decode("ascii")

    if arguments != None:
        arguments = cloudpickle.dumps(arguments, protocol=tiledb_cloud_protocol)
        arguments = base64.b64encode(arguments).decode("ascii")

    if image_name is None:
        image_name = "default"
    try:

        kwargs = {"_preload_content": False, "async_req": True}
        if http_compressor is not None:
            kwargs["accept_encoding"] = http_compressor

        # _preload_content must be set to false to avoid trying to decode binary data
        response = api_instance.submit_generic_udf(
            namespace=namespace,
            udf=rest_api.models.GenericUDF(
                type=rest_api.models.UDFType.PYTHON,
                _exec=pickledUDF,
                argument=arguments,
                result_format=rest_api.models.UDFResultType.NATIVE,
                version="{}.{}.{}".format(
                    sys.version_info.major,
                    sys.version_info.minor,
                    sys.version_info.micro,
                ),
                image_name=image_name,
            ),
            **kwargs
        )

        return array.UDFResult(response)

    except GenApiException as exc:
        raise tiledb_cloud_error.check_sql_exc(exc) from None


def exec(
    func, arguments=None, namespace=None, image_name=None, http_compressor="deflate",
):
    """
     Run a user defined function


    :param func: user function to run
    :param arguments: arguments to pass to function
    :param namespace: namespace to run udf under
    :param image_name: udf image name to use, useful for testing beta features
    :param http_compressor: set http compressor for results
    :return: UDFResult object which is a future containing the results of the UDF
    """
    return exec_async(
        func=func,
        arguments=arguments,
        namespace=namespace,
        image_name=image_name,
        http_compressor=http_compressor,
    ).get()
