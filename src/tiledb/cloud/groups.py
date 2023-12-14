"""Functions for managing TileDB Cloud groups."""

import posixpath
import urllib.parse
from typing import Iterable, Optional, Tuple, Union

import tiledb.cloud.tiledb_cloud_error as tce
from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud._common import api_v2
from tiledb.cloud._common import utils


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

    array_api = client.build(rest_api.ArrayApi)
    groups_api = client.build(api_v2.GroupsApi)
    groups_api_v1 = client.build(rest_api.GroupsApi)
    if recursive:
        while True:
            contents: rest_api.GroupContents = groups_api_v1.get_group_contents(
                group_namespace=namespace,
                group_name=name,
                page=1,
                per_page=100,
            )
            pm: rest_api.PaginationMetadata = contents.pagination_metadata
            if not pm.total_items:
                break  # Zero total items remain -> we're done.
            members: Iterable[rest_api.GroupEntry] = contents.entries
            for m in members:
                if m.array:
                    arr: rest_api.ArrayInfo = m.array
                    array_api.deregister_array(
                        namespace=arr.namespace,
                        array=arr.id,
                    )
                elif m.group:
                    grp: rest_api.GroupInfo = m.group
                    deregister(grp.tiledb_uri, recursive=recursive)
                else:
                    raise tce.TileDBCloudError("unexpected group member type")
    groups_api.deregister_group(group_namespace=namespace, group_name=name)


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
    path = path or (principal.default_s3_path + "/groups")
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
