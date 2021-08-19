import json
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
