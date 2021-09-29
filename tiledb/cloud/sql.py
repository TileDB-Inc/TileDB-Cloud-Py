import inspect
import time
import uuid
import warnings
from typing import Any, Optional, Sequence

import tiledb
from tiledb.cloud import array
from tiledb.cloud import client
from tiledb.cloud import config
from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud import utils
from tiledb.cloud._results import decoders
from tiledb.cloud._results import results
from tiledb.cloud.rest_api import models

last_sql_task_id: Optional[str] = None


def exec_base(
    query: str,
    output_uri: Optional[str] = None,
    output_schema: Optional[tiledb.ArraySchema] = None,
    namespace: Optional[str] = None,
    task_name: Optional[str] = None,
    output_array_name: Optional[str] = None,
    raw_results: bool = False,
    http_compressor: Optional[str] = "deflate",
    init_commands: Optional[Sequence[str]] = None,
    parameters: Optional[Sequence[str]] = None,
    result_format: str = models.ResultFormat.ARROW,
    result_format_version=None,
    store_results: bool = False,
) -> "results.RemoteResult":
    """Run a Serverless SQL query, returning both the result and metadata.

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
    :param str result_format_version: Deprecated and ignored.
    :param store_results: True to temporarily store results on the server side
        for later retrieval (in addition to downloading them).
    """

    if result_format_version:
        warnings.warn(DeprecationWarning("result_format_version is unused."))

    # Make sure the output_uri is remote array
    if output_uri:
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

    kwargs = dict(
        namespace=namespace,
        sql=rest_api.models.SQLParameters(
            name=task_name,
            query=query,
            output_uri=output_uri,
            init_commands=init_commands,
            parameters=parameters,
            result_format=result_format,
            store_results=store_results,
        ),
    )
    if http_compressor is not None:
        kwargs["accept_encoding"] = http_compressor

    decoder_cls = decoders.Decoder if raw_results else decoders.PandasDecoder
    decoder = decoder_cls(result_format)

    return client.send_udf_call(
        api_instance.run_sql,
        kwargs,
        decoder,
        id_callback=_maybe_set_last_task_id,
        results_stored=store_results,
    )


@utils.signature_of(exec_base)
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


@utils.signature_of(exec_base)
def exec(*args, **kwargs) -> Any:
    """Run a SQL query, synchronously.

    All arguments are exactly as in :func:`exec_base`.
    """
    return exec_base(*args, **kwargs).get()


@utils.signature_of(exec_base)
def exec_async(*args, **kwargs) -> "results.AsyncResult":
    """Run a SQL query, asynchronously.

    All arguments are exactly as in :func:`exec_base`. Returns an AsyncResponse,
    a Future-like object.
    """
    return client.client.wrap_async_base_call(exec_base, *args, **kwargs)


def _maybe_set_last_task_id(task_id: Optional[uuid.UUID]):
    global last_sql_task_id
    if task_id:
        last_sql_task_id = str(task_id)
