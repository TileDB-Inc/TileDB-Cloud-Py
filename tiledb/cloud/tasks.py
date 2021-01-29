from . import client
from . import tiledb_cloud_error
from .array import split_uri
from . import sql
from . import array
from .rest_api import ApiException as GenApiException
from .rest_api.models import ArrayTaskType

import datetime


def task(id, async_req=False):
    """
    Fetch a single array task
    :param str id: id to lookup
    :param async_req: return future instead of results for async support
    :return task : object with task details
    """

    if id is None:
        raise Exception("id parameter can not be empty")

    api_instance = client.client.tasks_api

    try:
        return api_instance.task_id_get(id=id, async_req=async_req)

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def retry(id, async_req=False, raw_results=False, http_compressor="deflate"):
    """
    Retry a single task
    :param str id: id to retry
    :param async_req: return future instead of results for async support
    :param bool raw_results: optional flag for sql tasks to return raw json bytes of results instead of converting to pandas dataframe
    :param string http_compressor: optional http compression method to use
    :return results or future if async
    """

    if id is None:
        raise Exception("id parameter can not be empty")

    t = task(id)

    api_instance = client.client.tasks_api

    try:
        kwargs = {"_preload_content": False, "async_req": True}
        if http_compressor is not None:
            kwargs["accept_encoding"] = http_compressor
        response = api_instance.task_id_retry_post(id=id, **kwargs)

        if t.type == ArrayTaskType.GENERIC_UDF or t.type == ArrayTaskType.UDF:
            response = array.UDFResult(response)
        elif t.type == ArrayTaskType.SQL:
            response = sql.SQLResults(response, raw_results)

        if not async_req:
            return response.get()

        return response

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
    :param datetime start: optional start time for listing of tasks, defaults to 7 days ago
    :param datetime end: optional end time for listing of tasks defaults to now
    :param str status: optional filter on status can be one of ['FAILED', 'RUNNING', 'COMPLETED']
    :param int page: optional page for pagenating results
    :param int per_page: optional records to return per page
    :param async_req: return future instead of results for async support
    :return:
    """
    api_instance = client.client.tasks_api

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
        (namespace, array) = split_uri(array)

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
