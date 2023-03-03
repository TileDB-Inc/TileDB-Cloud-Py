import json

from tiledb import TileDBError
from tiledb.cloud import rest_api


class TileDBCloudError(TileDBError):
    pass


def check_exc(exc):
    internal_err_msg = (
        "[InternalError: failed to parse or message missing from ApiException]"
    )

    # Make sure exc.status and exc.body exist before dereferncing them.
    if not isinstance(exc, rest_api.ApiException):
        # If this isn't an ApiException, something non–API-related happened.
        # We shouldn't try to wrap it.
        #
        # Bare "raise" here is OK because this function is already called from
        # within an exception handler.
        raise

    if exc.status == 404 and len(exc.body) == 0:
        return TileDBCloudError("Array or Namespace Not found")

    try:
        body = json.loads(exc.body)
        new_exc = TileDBCloudError(
            "{} - Code: {}".format(body["message"], body["code"])
        )
    except Exception:
        raise TileDBCloudError(internal_err_msg) from exc

    return new_exc
