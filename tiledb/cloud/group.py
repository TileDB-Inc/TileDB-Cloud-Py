from typing import Dict, List

from tiledb.cloud import client
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud import utils
from tiledb.cloud.array import delete_array
from tiledb.cloud.rest_api import ApiException as GenApiException

# Re-export for compatibility.
split_uri = utils.split_uri


def get_group(uri):
    """
    Returns the cloud metadata

    :return: metadata object
    """
    (namespace, group_name) = split_uri(uri)
    api_instance = client.client.groups_api

    try:
        return api_instance.get_group(namespace, group_name, async_req=async_req)
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def delete_group_recursively(uri, dry_run=False, verbose=False):
    """
    Deletes the group object, after recursively deregistering/deleting child array elemens
    and deleting child group elements.

    :param uri: TileDB Cloud URI of the group to be deleted

    :param dry_run: If true, print what would be deleted without doing the deletion.

    :param verbose: If true, print what is being deleted. The `dry_run` flag
    implies `verbose`.

    :return success or error
    """

    if dry_run:
        verbose = True

    (namespace, group_name) = split_uri(uri)

    # Get all members before deleting any, since we don't want to be deleting
    # things we're iterating over.
    group_element_tiledb_uris = _get_group_element_tiledb_uris(uri)

    for e in group_element_tiledb_uris["arrays"]:
        if verbose:
            print("DELETE ARRAY", e)
        if not dry_run:
            delete_array(e)
    for e in group_element_tiledb_uris["groups"]:
        # Depth-first traversal
        delete_group_recursively(e, dry_run=dry_run, verbose=verbose)
        if verbose:
            print("DELETE GROUP", e)
        if not dry_run:
            delete_group(e)


def delete_group(uri: str) -> None:
    """
    Deletes the group. The assets are not deleted nor are not relocated to any other group.
    This method makes a synchronous HTTP request by default.

    You probably want `delete_group_recursively`.

    :param uri: TileDB Cloud URI of the group to be deleted
    """
    (namespace, group_name) = split_uri(uri)
    api_instance = client.client.groups_api
    try:
        return api_instance.delete_group(namespace, group_name)
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def _get_group_element_tiledb_uris(uri: str) -> Dict[str, List[str]]:
    """
    Given a TileDB Cloud group URI, returns a listing of array-element URIs,
    and group-element URIs. This is intended as an auxiliary helper method
    for `delete_group_recursively`.
    """

    (namespace, group_name) = split_uri(uri)
    api_instance = client.client.groups_api

    try:
        array_tiledb_uris = []
        group_tiledb_uris = []
        page_index = 1
        while True:
            page = api_instance.get_group_contents(
                namespace, group_name, page=page_index
            )
            for e in page.entries:
                # Do not do:
                #   array_tiledb_uris.append(e.array.tiledb_uri)
                # This is because if we have two groups like
                #   tiledb://username/soma1
                #   tiledb://username/soma2
                # each with an array element 'obs' then e.array.tiledb_uri for those will be
                #   tiledb://username/soma1/obs
                #   tiledb://username/soma2/obs
                # which are non-unique.
                #
                # Instead, we replace the last component with its ID which *is* unique.
                if e.array is not None:
                    array_tiledb_uris.append(
                        f"tiledb://{e.array.namespace}/{e.array.id}"
                    )
                elif e.group is not None:
                    group_tiledb_uris.append(
                        f"tiledb://{e.group.namespace}/{e.group.id}"
                    )
            if len(page.entries) == 0:
                break
            page_index += 1
        return {"arrays": array_tiledb_uris, "groups": group_tiledb_uris}

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None
