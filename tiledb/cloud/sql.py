from . import rest_api
from . import config
from . import client
from . import cloudarray
from . import tasks
from . import tiledb_cloud_error
from .rest_api import ApiException as GenApiException
from .rest_api import rest

import tiledb
import time

last_sql_task_id = None


def exec(
    query,
    output_uri=None,
    output_schema=None,
    namespace=None,
    task_name=None,
    output_array_name=None,
):
    """
  Run a sql query
  :param str query: query to run
  :param str output_uri: optional array to store results to, must be a tiledb:// registered array
  :param str namespace: optional namespace to charge the query to
  :param task_name: optional name to assign the task for logging and audit purposes
  """

    # Make sure the output_uri is remote array
    if not output_uri is None:
        cloudarray.split_uri(output_uri)

    # If the namespace is not set, we will default to the user's namespace
    if namespace is None:
        # Fetch the client profile for username if it is not already cached
        if config.user is None:
            config.user = client.user_profile()

        namespace = config.user.username

    api_instance = client.get_sql_api()

    # If the user passes an output schema create the output array
    if output_schema is not None and output_uri is not None:
        # Create the (empty) output array in the service
        tiledb.Array.create(output_uri, output_schema, ctx=client.Ctx())

        timeout = time.time() + 10  # 10 second timeout
        arrays_api = client.get_array_api()
        (array_namespace, array_name) = cloudarray.split_uri(output_uri)
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
            array_api = client.get_array_api()
            array_api.update_array_metadata(
                namespace=namespace,
                output_uri=output_uri,
                array_metadata=rest_api.models.ArrayMetadataUpdate(
                    name=output_array_name
                ),
            )

    try:

        response = api_instance.run_sql(
            namespace=namespace,
            sql=rest_api.models.SQLParameters(
                name=task_name, query=query, output_uri=output_uri
            ),
            _preload_content=False,
        )
        response = rest.RESTResponse(response)

        global last_sql_task_id
        last_sql_task_id = response.getheader(client.TASK_ID_HEADER)

        if response.status >= 200 and response.status < 300:
            return None

        return response.data
    except GenApiException as exc:
        raise tiledb_cloud_error.check_sql_exc(exc) from None


def exec_and_fetch(
    query,
    output_uri,
    output_schema=None,
    namespace=None,
    task_name=None,
    output_array_name=None,
):
    """
  Run a sql query, results are not stored
  :param str query: query to run
  :param str output_uri: array to store results to, must be either a tiledb:// for an already registered array or a s3:// if passing a new schema to create new output array
  :param tiledb.ArraySchema output_schema: array schema to create output array with
  :param str namespace: optional namespace to charge the query to
  :param str task_name: optional name to assign the task for logging and audit purposes
  :param str output_array_name: optional name for registering new output array if output_schema schema is passed

  :return: TileDB Array with results
  """

    # If the namespace is not set, we will default to the user's namespace
    if namespace is None:
        # Fetch the client profile for username if it is not already cached
        if config.user is None:
            config.user = client.user_profile()

        namespace = config.user.username

    # Execute the sql query
    try:
        exec(
            query=query,
            output_uri=output_uri,
            output_schema=output_schema,
            namespace=namespace,
            task_name=task_name,
            output_array_name=output_array_name,
        )

        # Fetch output schema to check if its sparse or dense
        schema = tiledb.ArraySchema.load(output_uri, ctx=client.Ctx())

        if schema.sparse:
            return tiledb.SparseArray(output_uri, ctx=client.Ctx())

        return tiledb.DenseArray(output_uri, ctx=client.Ctx())

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None
