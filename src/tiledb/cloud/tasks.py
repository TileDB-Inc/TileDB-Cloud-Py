import datetime
import uuid
from typing import TYPE_CHECKING, Any, Optional

from tiledb.cloud import array
from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud import sql
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud._common import utils
from tiledb.cloud._results import decoders
from tiledb.cloud._results import results
from tiledb.cloud.rest_api import ApiException as GenApiException
from tiledb.cloud.rest_api import models

if TYPE_CHECKING:
    import pandas


def task(id, async_req=False):
    """
    Fetch a single array task
    :param str id: id to lookup
    :param async_req: return future instead of results for async support
    :return task : object with task details
    """

    if id is None:
        raise Exception("id parameter can not be empty")

    api_instance = client.build(rest_api.TasksApi)

    try:
        return api_instance.task_id_get(id=id, async_req=async_req)

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def tasks(
    namespace=None,
    array=None,
    start=None,
    end=datetime.datetime.utcnow(),
    status=None,
    page=None,
    per_page=None,
    async_req=False,
):
    """
    Fetch all tasks a user has access too
    :param str namespace: optional filter by namespace
    :param str array: optional limit tasks to specific array
    :param datetime start: optional start time for listing of tasks,
        defaults to 7 days ago
    :param datetime end: optional end time for listing of tasks defaults to now
    :param str status: optional filter on status can be one of
        ['FAILED', 'RUNNING', 'COMPLETED']
    :param int page: optional page for pagenating results
    :param int per_page: optional records to return per page
    :param async_req: return future instead of results for async support
    :return:
    """
    api_instance = client.build(rest_api.TasksApi)

    if end is not None:
        if not isinstance(end, datetime.datetime):
            raise Exception("end must be datetime object")
        end = datetime.datetime.timestamp(end)

    if start is not None:
        if not isinstance(start, datetime.datetime):
            raise Exception("start must be datetime object")
        start = datetime.datetime.timestamp(start)

    if (
        status is not None
        and status != "FAILED"
        and status != "RUNNING"
        and status != "COMPLETED"
    ):
        raise Exception("status must be one of ['FAILED', 'RUNNING', 'COMPLETED']")

    if array is not None:
        (namespace, array) = utils.split_uri(array)

    try:
        args = {"async_req": async_req}
        if namespace is not None:
            args["namespace"] = namespace
        if array is not None:
            args["array"] = array
        if start is not None:
            args["start"] = int(start)
        if end is not None:
            args["end"] = int(end)
        if status is not None:
            args["status"] = status
        if page is not None:
            args["page"] = page
        if per_page is not None:
            args["per_page"] = per_page

        return api_instance.tasks_get(**args)

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def last_sql_task():
    """
    Fetch the last run sql array task
    :return task : object with task details
    """

    if sql.last_sql_task_id is None:
        raise Exception("There is no last run sql task in current python session")

    return task(id=sql.last_sql_task_id)


def last_udf_task():
    """
    Fetch the last run udf task
    :return task : object with task details
    """

    if array.last_udf_task_id is None:
        raise Exception("There is no last run udf task in current python session")

    return task(id=array.last_udf_task_id)


def fetch_results(
    task_id: uuid.UUID,
    *,
    result_format: Optional[str] = None,
) -> Any:
    """Fetches the results of a previously-executed UDF or SQL query."""
    decoder = None if result_format is None else decoders.Decoder(result_format)
    return results.fetch_remote(task_id, decoder)


def fetch_results_pandas(
    task_id: uuid.UUID,
    *,
    result_format: str = models.ResultFormat.NATIVE,
) -> "pandas.DataFrame":
    """Fetches the results of a previously-executed UDF or SQL query."""
    return results.fetch_remote(task_id, decoders.PandasDecoder(result_format))
