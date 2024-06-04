import posixpath
import urllib.parse
from typing import Optional, Tuple

import requests

import tiledb.cloud.tiledb_cloud_error as tce
from tiledb.cloud import config
from tiledb.cloud._common import utils
from tiledb.services import errors
from tiledb.services.api_v1 import arrays as v1_arrays
from tiledb.services.api_v1 import groups as v1_groups
from tiledb.services.api_v1 import users as v1_users
from tiledb.services.http_actions import AllowedMethods
from tiledb.services.http_actions import perform_request

HOST = config.config.host
GROUPS_V2_URL = f"{HOST}/v2/groups"


# ============================
#      Auxiliary Methods
# ============================
def _add_to(
    *,
    namespace: str,
    name: str,
    parent_uri: str,
    credentials_name: str,
    request_session: Optional[requests.Session] = None,
) -> dict:
    parent_ns, parent_name = utils.split_uri(parent_uri)
    return update_group_contents(
        group_namespace=parent_ns,
        group_name=parent_name,
        group_update_contents={
            "group_changes": {
                "members_to_add": [
                    {
                        "name": name,
                        "uri": f"tiledb://{namespace}/{name}",
                        "type": "GROUP",
                    }
                ]
            }
        },
        credentials_name=credentials_name,
        request_session=request_session,
    )


def _default_ns_path_cred(
    namespace: Optional[str] = None,
    request_session: Optional[requests.Session] = None,
) -> Tuple[str, str, str]:
    if namespace:
        user = v1_users.get_user_with_username(namespace, request_session)
        # TODO: Missing `get_organization` in case of error.
    else:
        user = v1_users.get_user()
        namespace = user.username
        assert namespace

    return (
        namespace,
        f"{user.default_s3_path}/groups",
        user.default_s3_path_credentials_name,
    )


# ============================
#         API Methods
# ============================
def create(
    name: str,
    *,
    namespace: Optional[str] = None,
    parent_uri: Optional[str] = None,
    storage_uri: Optional[str] = None,
    credentials_name: Optional[str] = None,
) -> int:
    """Creates a new TileDB Cloud group.

    :param name: The name of the group to create.
    :param namespace: The namespace to create the group in.
        If not provided, the current logged-in user will be used.
    :param parent_uri: The parent URI to add the group to, if desired.
    :param storage_uri: The backend URI where the group will be stored.
        If not provided, uses the namespace's default storage path for groups.
    :param credentials_name: The name of the storage credential to use for
        creating the group. If not provided, uses the namespace's default
        credential for groups.
    :return int: Expected status code
    """
    with requests.session() as session:
        if not (namespace and storage_uri and credentials_name):
            namespace, default_path, default_cred = _default_ns_path_cred(
                namespace, session
            )
            storage_uri = storage_uri or (default_path + "/" + name)
            credentials_name = credentials_name or default_cred

        try:
            response = perform_request(
                method=AllowedMethods.POST,
                url=f"{GROUPS_V2_URL}/{namespace}",
                acn=credentials_name,
                body={
                    "group_details": {
                        "name": name,
                        "uri": storage_uri,
                    }
                },
                request_session=session,
            )

            if parent_uri:
                _add_to(
                    namespace=namespace,
                    name=name,
                    parent_uri=parent_uri,
                    credentials_name=credentials_name,
                    request_session=session,
                )

            return response.status_code
        except requests.HTTPError as exc:
            raise errors.TileDBCloudError() from exc


def delete(uri: str, *, recursive: bool = False) -> int:
    """
    Deletes a TileDB Group given it's URI.

    :param uri: TileDB Group URI.
    :param recursive: Flag to delete the Group's contents,
        defaults to False
    :return int: Expected Status Code.
    """
    namespace, name = utils.split_uri(uri)
    try:
        response = perform_request(
            method=AllowedMethods.DELETE,
            url=f"{GROUPS_V2_URL}/{namespace}/{name}/delete",
            params={"recursive": recursive},
        )

        return response.status_code
    except requests.HTTPError as exc:
        raise errors.TileDBCloudError() from exc


def update_group_contents(
    group_namespace: str,
    group_name: str,
    group_update_contents: dict,
    credentials_name: str,
    request_session: Optional[requests.Session] = None,
) -> Tuple[int, Optional[dict]]:
    try:
        response = perform_request(
            method=AllowedMethods.PATCH,
            url=f"{GROUPS_V2_URL}/{group_namespace}/{group_name}",
            acn=credentials_name,
            body=group_update_contents,
            request_session=request_session,
        )

        return response.status_code, response.json()
    except requests.HTTPError as exc:
        raise errors.TileDBCloudError() from exc
    except requests.JSONDecodeError:
        # Status 204 case
        return response.status_code, None


def register(
    storage_uri: str,
    *,
    name: Optional[str] = None,
    namespace: Optional[str] = None,
    parent_uri: Optional[str] = None,
    credentials_name: Optional[str] = None,
) -> int:
    """
    Registers a pre-existing group.

    :param storage_uri: The backend URI where the Group is stored.
    :param name: The name to register the Group as, defaults to None
    :param namespace: The namespace to register the group in.
        If not provided, the current logged-in user will be used.
    :param parent_uri: The parent URI to add the group to, if desired.
    :param credentials_name: The name of the storage credential to use for
        creating the group. If not provided, uses the namespace's default
        credential for groups.
    :return int: Expected status code
    """
    if not name:
        # Extract the basename from the storage URI and use it for the name.
        parsed_uri = urllib.parse.urlparse(storage_uri)
        name = posixpath.basename(parsed_uri.path)

    with requests.session() as session:
        if not (namespace and credentials_name):
            namespace, _, default_cred = _default_ns_path_cred(namespace, session)
            credentials_name = credentials_name or default_cred

        try:
            response = perform_request(
                method=AllowedMethods.PUT,
                url=f"{GROUPS_V2_URL}/{namespace}",
                acn=credentials_name,
                body={
                    "group_details": {
                        "name": name,
                        "uri": storage_uri,
                        "access_credentials_name": credentials_name,
                        "parent": parent_uri,
                    }
                },
                request_session=session,
            )

            if parent_uri:
                _add_to(
                    namespace=namespace,
                    name=name,
                    parent_uri=parent_uri,
                    credentials_name=credentials_name,
                    request_session=session,
                )

            return response.status_code
        except requests.HTTPError as exc:
            raise errors.TileDBCloudError() from exc


def deregister(
    uri: str,
    *,
    recursive: bool = False,
    credentials_name: Optional[str] = None,
    request_session: Optional[requests.Session] = None,
) -> int:
    """
    De-registers the given group from TileDB Cloud.

    :param uri: The URI of the group to deregister.
    :param recursive: If true, deregister the group recursively by de-registering
        all of the elements of the group (and all elements of those groups,
        recursively) before de-registering the group itself.
    :param credentials_name: The name of the storage credential to use for
        de-registering the group. If not provided, uses the namespace's default
        credential for groups.
    :return int: Expected status code
    """
    namespace, name = utils.split_uri(uri)
    session = request_session or requests.session()

    if not credentials_name:
        _, _, credentials_name = _default_ns_path_cred(namespace, session)

    if recursive:
        group_contents = v1_groups.get_group_contents(uri, request_session=session)
        pm = group_contents.get("pagination_metadata", {})
        while pm.get("total_items", 0) > 0:
            for member in group_contents.get("entries", []):
                if member.get("array", None):
                    array = member["array"]
                    try:
                        v1_arrays.deregister(uri=array["uri"], request_session=session)
                    except Exception:
                        # TODO: Add some logging
                        continue
                elif member.get("group", None):
                    group = member["group"]
                    deregister(
                        uri=group["tiledb_uri"], recursive=True, request_session=session
                    )
                else:
                    raise tce.TileDBCloudError("unexpected group member type")

    try:
        response = perform_request(
            method=AllowedMethods.DELETE,
            url=f"{GROUPS_V2_URL}/{namespace}/{name}",
            acn=credentials_name,
            # TODO: [DISCUSSION] Since v2 expects a "recursive" param,
            #       it must be able to do the recursive de-registering
            #       instead of doing it manually as we do above.
            params={"recursive": recursive},
            request_session=session,
        )

        return response.status_code
    except requests.HTTPError as exc:
        raise errors.TileDBCloudError() from exc
