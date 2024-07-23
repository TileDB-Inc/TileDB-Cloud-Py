"""Functions for managing TileDB Cloud groups."""

import inspect
import posixpath
import urllib.parse
from typing import List, Optional, Tuple, Union

from . import client
from . import rest_api
from . import tiledb_cloud_error
from ._common import api_v2
from ._common import utils
from .rest_api import ApiException as GenApiException
from .rest_api import models
from .rest_api.models import group_update

split_uri = utils.split_uri


def create(
    name: str,
    *,
    namespace: Optional[str] = None,
    parent_uri: Optional[str] = None,
    storage_uri: Optional[str] = None,
    credentials_name: Optional[str] = None,
) -> None:
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
    """
    if not (namespace and storage_uri and credentials_name):
        namespace, default_path, default_cred = _default_ns_path_cred(namespace)
        storage_uri = storage_uri or (default_path + "/" + name)
        credentials_name = credentials_name or default_cred

    groups_client = client.build(api_v2.GroupsApi)
    groups_client.create_group(
        group_namespace=namespace,
        x_tiledb_cloud_access_credentials_name=credentials_name,
        group_creation=api_v2.GroupCreationRequest(
            group_details=api_v2.GroupCreationRequestGroupDetails(
                name=name,
                uri=storage_uri,
            )
        ),
    )
    if parent_uri:
        _add_to(namespace=namespace, name=name, parent_uri=parent_uri)


def register(
    storage_uri: str,
    *,
    name: Optional[str] = None,
    namespace: Optional[str] = None,
    credentials_name: Optional[str] = None,
    parent_uri: Optional[str] = None,
):
    """Registers a pre-existing group."""
    if not (namespace and credentials_name):
        namespace, _, default_cred = _default_ns_path_cred(namespace)
        credentials_name = credentials_name or default_cred

    if not name:
        # Extract the basename from the storage URI and use it for the name.
        parsed_uri = urllib.parse.urlparse(storage_uri)
        name = posixpath.basename(parsed_uri.path)
    groups_client = client.build(api_v2.GroupsApi)
    groups_client.register_group(
        group_namespace=namespace,
        x_tiledb_cloud_access_credentials_name=credentials_name,
        group_registration=api_v2.GroupRegistrationRequest(
            group_details=api_v2.GroupRegistrationRequestGroupDetails(
                name=name,
                uri=storage_uri,
                access_credentials_name=credentials_name,
                parent=parent_uri,
            )
        ),
    )
    if parent_uri:
        _add_to(namespace=namespace, name=name, parent_uri=parent_uri)


def info(uri: str) -> object:
    """Gets metadata about the named TileDB Cloud group."""
    namespace, group_name = utils.split_uri(uri)
    groups_client = client.build(rest_api.GroupsApi)
    return groups_client.get_group(group_namespace=namespace, group_name=group_name)


def update_info(
    uri: str,
    *,
    description: Optional[str] = None,
    name: Optional[str] = None,
    logo: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> None:
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
    groups_v1_client = client.build(rest_api.GroupsApi)
    info = {}
    for kw, arg in inspect.signature(update_info).parameters.items():
        if arg.kind != inspect.Parameter.KEYWORD_ONLY:
            # Skip every non-keyword-only argument
            continue

        value = locals()[kw]
        if value is None:
            # Explicitly update metadata
            continue
        info[kw] = value

    info = group_update.GroupUpdate(**info)
    try:
        return groups_v1_client.update_group(namespace, group_name, group_update=info)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc)


def deregister(
    uri: str,
    *,
    recursive: bool = False,
) -> None:
    """Deregisters the given group from TileDB Cloud.

    :param uri: The URI of the group to deregister.
    :param recursive: If true, deregister the group recursively by deregistering
        all of the elements of the group (and all elements of those groups,
        recursively) before deregistering the group itself.
    """
    namespace, name = utils.split_uri(uri)
    groups_api = client.build(api_v2.GroupsApi)
    # Server expects recursive: "true"/"false".
    groups_api.deregister_group(
        group_namespace=namespace,
        group_name=name,
        recursive=str(bool(recursive)).lower(),
    )


def delete(uri: str, recursive: bool = False) -> None:
    """
    Deletes a group.

    :param uri: TileDB Group URI.
    :param recursive: Delete all off the group's contents, defaults to False
    """
    namespace, group_name = utils.split_uri(uri)
    groups_api = client.build(api_v2.GroupsApi)
    # Server expects recursive: "true"/"false".
    groups_api.delete_group(
        group_namespace=namespace,
        group_name=group_name,
        recursive=str(bool(recursive)).lower(),
    )


def _default_ns_path_cred(namespace: Optional[str] = None) -> Tuple[str, str, str]:
    principal: Union[rest_api.User, rest_api.Organization]
    if namespace:
        try:
            principal = client.build(rest_api.UserApi).get_user_with_username(namespace)
        except rest_api.ApiException:
            try:
                principal = client.build(rest_api.OrganizationApi).get_organization(
                    namespace
                )
            except rest_api.ApiException:
                raise ValueError(f"Could not find namespace {namespace!r}.")
    else:
        principal = client.default_user()
        namespace = principal.username
        assert namespace

    locs: Optional[rest_api.AssetLocations] = principal.asset_locations
    # Weird structure to silence mypy complaints.
    storage: Optional[rest_api.StorageLocation] = locs.groups if locs else None

    path: Optional[str] = None
    cred_name: Optional[str] = None
    if storage:
        path = storage.path
        cred_name = storage.credentials_name
    if not path and not principal.default_s3_path:
        raise ValueError("No storage provider configured.")
    # Sanitize any extra trailing "/"
    path = path or (principal.default_s3_path.rstrip("/") + "/groups")
    cred_name = cred_name or principal.default_s3_path_credentials_name
    return namespace, path, cred_name


def _add_to(*, namespace: str, name: str, parent_uri: str) -> None:
    parent_ns, parent_name = utils.split_uri(parent_uri)
    client.build(api_v2.GroupsApi).update_group_contents(
        group_namespace=parent_ns,
        group_name=parent_name,
        group_update_contents=api_v2.GroupContentsChangesRequest(
            group_changes=api_v2.GroupContentsChangesRequestGroupChanges(
                members_to_add=[
                    api_v2.GroupMember(
                        name=name,
                        uri=f"tiledb://{namespace}/{name}",
                        type="GROUP",
                    ),
                ],
            ),
        ),
    )


def list_shared_with(uri, async_req=False):
    """List a group's sharing policies.

    :param str uri: tiledb URI of the asset.
    :param async_req: return future instead of results for async support.
    :return: a list of GroupSharing objects.
    """
    (group_namespace, group_name) = split_uri(uri)
    api_instance = client.build(rest_api.GroupsApi)

    try:
        return api_instance.get_group_sharing_policies(
            group_namespace=group_namespace, group_name=group_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def share_group(uri, namespace, permissions, async_req=False):
    """Shares group with given namespace and permissions.

    :param str uri: tiledb URI of the asset.
    :param str namespace:
    :param list(str) permissions:
    :param async_req: return future instead of results for async support.
    :return: None.
    """

    if not isinstance(permissions, list):
        permissions = [permissions]

    if set([perm.lower() for perm in permissions]) - {
        models.GroupActions.READ,
        models.GroupActions.WRITE,
    }:
        raise Exception("Only read or write permissions are accepted")

    (group_namespace, group_name) = split_uri(uri)
    api_instance = client.build(rest_api.GroupsApi)

    try:
        return api_instance.share_group(
            group_namespace=group_namespace,
            group_name=group_name,
            group_sharing_request=models.GroupSharingRequest(
                namespace=namespace,
                group_actions=permissions,
                array_actions=permissions,
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def unshare_group(uri, namespace, async_req=False):
    """
    Removes sharing of a group from given namespace

    :param str namespace: namespace to remove shared access to the group
    :param async_req: return future instead of results for async support
    :return:
    :raises: :py:exc:
    """
    return share_group(uri, namespace, list(), async_req=async_req)
