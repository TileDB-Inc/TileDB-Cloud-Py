from typing import Optional

import requests

from tiledb.cloud import config
from tiledb.cloud._common import utils
from tiledb.services import errors
from tiledb.services.http_actions import AllowedMethods
from tiledb.services.http_actions import perform_request

HOST = config.config.host
ARRAYS_V1_URL = f"{HOST}/v1/arrays"


def deregister(uri: str, *, request_session: Optional[requests.Session] = None) -> int:
    """
    Deregister a TileDB Array.

    :param uri: A TileDB Array URI.
    :param request_session: A requests.Session, defaults to None
    :return int: Expected status code
    """
    namespace, name = utils.split_uri(uri)
    try:
        response = perform_request(
            method=AllowedMethods.DELETE,
            url=f"{ARRAYS_V1_URL}/{namespace}/{name}/deregister",
            request_session=request_session,
        )

        return response.status_code
    except requests.HTTPError as exc:
        if exc.response.status_code == 401:
            raise errors.Unauthorized(
                "You are not authorized to delete this resource"
            ) from exc
        if exc.response.status_code == 404:
            raise errors.NotFound(f"Array '{uri}' does not exist")
        raise errors.TileDBCloudError() from exc
