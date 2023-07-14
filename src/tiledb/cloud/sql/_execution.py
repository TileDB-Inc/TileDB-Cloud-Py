import inspect
import time
import uuid
import warnings
from typing import Any, Optional, Sequence

import tiledb
from tiledb.cloud import array
from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud import sql
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud._common import functions
from tiledb.cloud._results import decoders
from tiledb.cloud._results import results
from tiledb.cloud._results import sender
from tiledb.cloud.rest_api import models


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
    resource_class: Optional[str] = None,
    _download_results: bool = True,
    _server_graph_uuid: Optional[uuid.UUID] = None,
    _client_node_uuid: Optional[uuid.UUID] = None,
) -> "results.RemoteResult":
    """Run a Serverless SQL query, returning both the result and metadata.

    :param str query: query to run
    :param str output_uri: optional array to store results to,
        must be a tiledb:// registered array
    :param tiledb.ArraySchema output_schema: optional schema
        for creating output array if it does not exist
    :param str namespace: optional namespace to charge the query to
    :param str task_name: optional name to assign the task for logging and
        audit purposes
    :param str output_array_name: optional array name to set if creating new
        output array
    :param bool raw_results: optional flag to return raw json bytes of results
        instead of converting to pandas dataframe
    :param string http_compressor: optional http compression method to use
    :param list init_commands: optional list of sql queries or commands to run
        before main query
    :param list parameters: optional list of sql parameters for use in query
    :param UDFResultType result_format: result serialization format
    :param str result_format_version: Deprecated and ignored.
    :param store_results: True to temporarily store results on the server side
        for later retrieval (in addition to downloading them).
    :param resource_class: The name of the resource class to use. Resource classes
        define maximum limits for cpu and memory usage.
    :param _server_graph_uuid: If this function is being executed within a DAG,
        the server-generated ID of the graph's log. Otherwise, None.
    :param _client_node_uuid: If this function is being executed within a DAG,
        the ID of this function's node within the graph. Otherwise, None.
    :param _download_results: True to download and parse results eagerly.
        False to not download results by default and only do so lazily
        (e.g. for an intermediate node in a graph).
    """

    if result_format_version:
        warnings.warn(DeprecationWarning("result_format_version is unused."))

    # Make sure the output_uri is remote array
    if output_uri:
        array.split_uri(output_uri)

    namespace = namespace or client.default_charged_namespace(
        required_action=rest_api.NamespaceActions.RUN_JOB
    )

    api_instance = client.build(rest_api.SqlApi)

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
            except Exception:
                pass

            # Sleep for 250ms to avoid dosing the server
            time.sleep(0.25)

        # If the user wishes to set a specific array name for
        # the newly registered output array let's update the details
        if output_array_name is not None:
            array_api = client.build(rest_api.ArrayApi)
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
            resource_class=resource_class,
            dont_download_results=not _download_results,
            task_graph_uuid=_server_graph_uuid and str(_server_graph_uuid),
            client_node_uuid=_client_node_uuid and str(_client_node_uuid),
        ),
    )
    if http_compressor is not None:
        kwargs["accept_encoding"] = http_compressor

    decoder_cls = decoders.Decoder if raw_results else decoders.PandasDecoder
    decoder = decoder_cls(result_format)

    return sender.send_udf_call(
        api_instance.run_sql,
        kwargs,
        decoder,
        id_callback=_maybe_set_last_task_id,
        results_stored=store_results,
        results_downloaded=_download_results,
    )


@functions.signature_of(exec_base)
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


@functions.signature_of(exec_base)
def exec(*args, **kwargs) -> Any:
    """Run a SQL query, synchronously.

    All arguments are exactly as in :func:`exec_base`.
    """
    return exec_base(*args, **kwargs).get()


@functions.signature_of(exec_base)
def exec_async(*args, **kwargs) -> "results.AsyncResult":
    """Run a SQL query, asynchronously.

    All arguments are exactly as in :func:`exec_base`. Returns an AsyncResponse,
    a Future-like object.
    """
    return sender.wrap_async_base_call(exec_base, *args, **kwargs)


def _maybe_set_last_task_id(task_id: Optional[uuid.UUID]):
    if task_id:
        sql.last_sql_task_id = str(task_id)
