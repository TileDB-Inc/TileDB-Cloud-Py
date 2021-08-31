import inspect
import time

import tiledb
from tiledb.cloud import array
from tiledb.cloud import client
from tiledb.cloud import config
from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud import utils
from tiledb.cloud.rest_api import models
from tiledb.cloud.results import PandasDecoder

last_sql_task_id = None


class SQLResult(array.TaskResult):
    def __init__(self, response, result_format, result_type="pandas"):
        super().__init__(response, result_format)

        if result_type == "pandas":
            self.decoder = PandasDecoder(result_format)

    def get(self, timeout=None):
        res = super().get(timeout)

        # Set last udf task id
        global last_sql_task_id
        last_sql_task_id = self.task_id

        return res


def exec_async(
    query,
    output_uri=None,
    output_schema=None,
    namespace=None,
    task_name=None,
    output_array_name=None,
    raw_results=False,
    http_compressor="deflate",
    init_commands=None,
    parameters=None,
    result_format=models.ResultFormat.ARROW,
    result_format_version=None,
):
    """
    Run a sql query asynchronous
    :param str query: query to run
    :param str output_uri: optional array to store results to, must be a tiledb:// registered array
    :param tiledb.ArraySchema output_schema: optional schema for creating output array if it does not exist
    :param str namespace: optional namespace to charge the query to
    :param str task_name: optional name to assign the task for logging and audit purposes
    :param str output_array_name: optional array name to set if creating new output array
    :param bool raw_results: optional flag to return raw json bytes of results instead of converting to pandas dataframe
    :param string http_compressor: optional http compression method to use
    :param list init_commands: optional list of sql queries or commands to run before main query
    :param list parameters: optional list of sql parameters for use in query
    :param UDFResultType result_format: result serialization format
    :param str result_format_version: set a format version for cloudpickle or arrow IPC

    :return: A SQLResult object which is a future for a pandas dataframe if no output array is given and query returns results
    """

    # Make sure the output_uri is remote array
    if not output_uri is None:
        array.split_uri(output_uri)

    # If the namespace is not set, we will default to the user's namespace
    if namespace is None:
        # Fetch the client profile for username if it is not already cached
        if config.user is None:
            config.user = client.user_profile()

        namespace = client.find_organization_or_user_for_default_charges(config.user)

    api_instance = client.client.sql_api

    if init_commands is not None and not isinstance(init_commands, list):
        raise Exception("init_commands must be a list of query strings")

    # If the user passes an output schema create the output array
    if output_schema is not None and output_uri is not None:
        # Create the (empty) output array in the service
        tiledb.Array.create(output_uri, output_schema, ctx=client.Ctx())

        timeout = time.time() + 10  # 10 second timeout
        (array_namespace, array_name) = array.split_uri(output_uri)
        while True:
            if time.time() > timeout:
                break

            try:
                res = tiledb.ArraySchema.load(output_uri, ctx=client.Ctx())
                if res is not None:
                    break
            except:
                pass

            # Sleep for 250ms to avoid dosing the server
            time.sleep(0.25)

        # If the user wishes to set a specific array name for the newly registered output array let's update the details
        if output_array_name is not None:
            array_api = client.client.array_api
            array_api.update_array_metadata(
                namespace=namespace,
                output_uri=output_uri,
                array_metadata=rest_api.models.ArrayInfoUpdate(name=output_array_name),
            )

    try:
        kwargs = {"_preload_content": False, "async_req": True}
        if http_compressor is not None:
            kwargs["accept_encoding"] = http_compressor

        response = api_instance.run_sql(
            namespace=namespace,
            sql=rest_api.models.SQLParameters(
                name=task_name,
                query=query,
                output_uri=output_uri,
                init_commands=init_commands,
                parameters=parameters,
                result_format=result_format,
                result_format_version=result_format_version,
            ),
            **kwargs
        )

        return SQLResult(
            response,
            result_format,
            result_type=None if raw_results else "pandas",
        )

    except rest_api.ApiException as exc:
        if exc.headers:
            task_id = exc.headers.get(client.TASK_ID_HEADER)
            if task_id:
                global last_sql_task_id
                last_sql_task_id = task_id
        raise tiledb_cloud_error.check_sql_exc(exc) from None


@utils.signature_of(exec_async)
def exec_and_fetch(*args, **kwargs):
    """
    Run a sql query, results are not stored

    All arguments are exactly as in :func:`exec_async`.

    :return: TileDB Array with results
    """
    my_sig: inspect.Signature = exec_and_fetch.__signature__
    output_uri = my_sig.bind(*args, **kwargs).arguments["output_uri"]

    # Execute the sql query
    try:
        exec(*args, **kwargs)

        # Fetch output schema to check if its sparse or dense
        schema = tiledb.ArraySchema.load(output_uri, ctx=client.Ctx())

        if schema.sparse:
            return tiledb.SparseArray(output_uri, ctx=client.Ctx())

        return tiledb.DenseArray(output_uri, ctx=client.Ctx())

    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


@utils.signature_of(exec_async)
def exec(*args, **kwargs):
    """
    Run a SQL query, synchronously.

    All arguments are exactly as in :func:`exec_async`.
    """
    return exec_async(*args, **kwargs).get()
