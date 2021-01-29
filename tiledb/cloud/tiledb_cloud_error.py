import json
from . import sql
from . import client
from . import array
from tiledb import TileDBError


class TileDBCloudError(TileDBError):
    pass


def check_exc(exc):
    internal_err_msg = (
        "[InternalError: failed to parse or message missing from ApiException]"
    )

    if not isinstance(exc, BaseException):
        raise Exception(internal_err_msg)

    if exc.status == 404 and len(exc.body) == 0:
        return TileDBCloudError("Array or Namespace Not found")

    try:
        body = json.loads(exc.body)
        new_exc = TileDBCloudError(
            "{} - Code: {}".format(body["message"], body["code"])
        )
    except:
        raise Exception(internal_err_msg) from exc

    return new_exc


def check_sql_exc(exc):
    internal_err_msg = (
        "[InternalError: failed to parse or message missing from ApiException]"
    )

    if not isinstance(exc, BaseException):
        raise Exception(internal_err_msg)

    try:
        if client.TASK_ID_HEADER in exc.headers:
            sql.last_sql_task_id = exc.headers[client.TASK_ID_HEADER]
        body = json.loads(exc.body)
        new_exc = TileDBCloudError(
            "{} - Code: {}".format(body["message"], body["code"])
        )
    except:
        raise Exception(internal_err_msg) from exc

    return new_exc


def check_udf_exc(exc):
    internal_err_msg = (
        "[InternalError: failed to parse or message missing from ApiException]"
    )

    if not isinstance(exc, BaseException):
        raise Exception(internal_err_msg)

    try:
        if client.TASK_ID_HEADER in exc.headers:
            array.last_udf_task_id = exc.headers[client.TASK_ID_HEADER]
        body = json.loads(exc.body)
        new_exc = TileDBCloudError(
            "{} - Code: {}".format(body["message"], body["code"])
        )
    except:
        raise Exception(internal_err_msg) from exc

    return new_exc
