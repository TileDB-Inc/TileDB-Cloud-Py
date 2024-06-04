from typing import Optional

import requests

from tiledb.cloud import config
from tiledb.services import errors
from tiledb.services.api_v1.models.users import User
from tiledb.services.http_actions import AllowedMethods
from tiledb.services.http_actions import perform_request

HOST = config.config.host
USER_V1_URL = f"{HOST}/v1/user"
USERS_V1_URL = f"{HOST}/v1/users"


def get_user(request_session: Optional[requests.Session] = None) -> User:
    try:
        response = perform_request(
            method=AllowedMethods.GET,
            url=USER_V1_URL,
            request_session=request_session,
        )
    except requests.HTTPError as exc:
        if exc.response.status_code == 401:
            raise errors.Unauthorized(
                "You are not authorized to access this resource"
            ) from exc
        raise errors.TileDBCloudError() from exc

    return User.model_validate(response.json())


def get_user_with_username(
    username: str, request_session: Optional[requests.Session] = None
) -> User:
    try:
        response = perform_request(
            method=AllowedMethods.GET,
            url=f"{USERS_V1_URL}/{username}",
            request_session=request_session,
        )
    except requests.HTTPError as exc:
        if exc.response.status_code == 401:
            raise errors.Unauthorized(
                "You are not authorized to access this resource"
            ) from exc
        if exc.response.status_code == 404:
            raise errors.NotFound(f"User with Username '{username}' not found") from exc
        raise errors.TileDBCloudError() from exc

    return User.model_validate(response.json())
