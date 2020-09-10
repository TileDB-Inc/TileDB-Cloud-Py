from . import client
from . import tiledb_cloud_error
from .array import split_uri
from . import cloudarray
from . import sql
from .rest_api import ApiException as GenApiException

import datetime


def task(id):
    """
    Fetch a single array task
    :param str id: id to lookup, if unset will use the id of the last array task run in the current python session
    :return task : object with task details
    """

    if id is None:
        raise Exception("id parameter can not be empty")

    api_instance = client.client.tasks_api

    try:
        return api_instance.task_id_get(id=id)

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
        args = {}
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

    if cloudarray.last_udf_task_id is None:
        raise Exception("There is no last run udf task in current python session")

    return task(id=cloudarray.last_udf_task_id)
