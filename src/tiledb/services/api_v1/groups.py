from dataclasses import asdict
from typing import List, Optional

import requests

from tiledb.cloud import config
from tiledb.cloud._common import utils
from tiledb.services import errors
from tiledb.services.api_v1 import models
from tiledb.services.http_actions import AllowedMethods
from tiledb.services.http_actions import perform_request

HOST = config.config.host
GROUPS_V1_URL = f"{HOST}/v1/groups"


def get_group_contents(
    uri: str,
    *,
    page: int = 1,
    per_page: int = 100,
    request_session: Optional[requests.Session] = None,
) -> dict:
    namespace, name = utils.split_uri(uri)
    try:
        response = perform_request(
            method=AllowedMethods.GET,
            url=f"{GROUPS_V1_URL}/{namespace}/{name}/contents",
            params={
                "page": page,
                "per_page": per_page,
            },
            request_session=request_session,
        )

        return response.json()
    except requests.HTTPError as exc:
        if exc.response.status_code == 400:
            raise errors.BadRequest(str(exc))
        if exc.response.status_code == 401:
            raise errors.Unauthorized(
                "You are not authorized to delete this resource"
            ) from exc
        if exc.response.status_code == 404:
            raise errors.NotFound(f"Group '{uri}' does not exist")
        raise errors.TileDBCloudError() from exc


def update_info(
    uri: str,
    *,
    description: Optional[str] = None,
    name: Optional[str] = None,
    logo: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> int:
    """
    Update Group Attributes

    :param uri: URI of the group in the form 'tiledb://<namespace>/<group>'
    :param description: Group description, defaults to None
    :param name: Group's name, defaults to None
    :param logo: Group's logo, defaults to None
    :param tags: Group tags, defaults to None
    :return: None
    """
    namespace, group_name = utils.split_uri(uri)
    info = models.groups.GroupUpdateInfo(description, name, logo, tags)
    info = asdict(
        info, dict_factory=lambda item: {k: v for (k, v) in item if v is not None}
    )
    try:
        response = perform_request(
            method=AllowedMethods.PATCH,
            url=f"{GROUPS_V1_URL}/{namespace}/{group_name}",
            body=info,
        )
        return response.status_code
    except requests.HTTPError as exc:
        if exc.response.status_code == 404:
            raise errors.NotFound(f"Group '{uri}' does not exist") from exc
        raise errors.TileDBCloudError() from exc


def info(uri: str) -> dict:
    """
    Fetches metadata for a TileDB Group.

    :param uri: TileDB Group URI.
    :return dict: Group Metadata
    """
    namespace, name = utils.split_uri(uri)
    try:
        response = perform_request(
            method=AllowedMethods.GET, url=f"{GROUPS_V1_URL}/{namespace}/{name}"
        )
        return response.json()
    except requests.HTTPError as exc:
        if exc.response.status_code == 404:
            raise errors.NotFound(f"Group '{uri}' does not exist") from exc
        raise errors.TileDBCloudError() from exc
