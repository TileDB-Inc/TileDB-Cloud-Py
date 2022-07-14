from typing import List, Tuple

from tiledb.cloud import array
from tiledb.cloud import client as cloud_client
from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud import utils
from tiledb.cloud.rest_api import models


def get_group(uri: str) -> models.GroupInfo:
    """
    Returns the cloud metadata

    :return: metadata object
    """
    namespace, group_name = utils.split_uri(uri)
    api_instance = cloud_client.client.groups_api

    try:
        return api_instance.get_group(namespace, group_name)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def delete_group_recursively(
    uri: str, *, dry_run: bool = False, verbose: bool = False
) -> None:
    """
    Deletes the group object, after recursively deregistering/deleting child array
    elements and deleting child group elements.

    :param uri: TileDB Cloud URI of the group to be deleted

    :param dry_run: If true, print what would be deleted without doing the deletion.

    :param verbose: If true, print what is being deleted. The ``dry_run`` flag
    implies ``verbose``.
    """

    if dry_run:
        verbose = True

    # Get all members before deleting any, since we don't want to be deleting
    # things we're iterating over.
    array_uris, group_uris = _get_group_element_tiledb_uris(uri)

    for arr in array_uris:
        if verbose:
            print("DELETE ARRAY", arr)
        if not dry_run:
            array.delete_array(arr)
    for grp in group_uris:
        # Depth-first traversal
        delete_group_recursively(grp, dry_run=dry_run, verbose=verbose)
        if verbose:
            print("DELETE GROUP", grp)
        if not dry_run:
            delete_group(grp)


def delete_group(uri: str) -> None:
    """
    Deletes the group. The assets are not deleted nor relocated to any other group.

    You probably want :func:`delete_group_recursively`.

    :param uri: TileDB Cloud URI of the group to be deleted
    """
    namespace, group_name = utils.split_uri(uri)
    api_instance = cloud_client.client.groups_api
    try:
        return api_instance.delete_group(namespace, group_name)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def _get_group_element_tiledb_uris(uri: str) -> Tuple[List[str], List[str]]:
    """
    Given a TileDB Cloud group URI, returns a listing of array-element URIs,
    and group-element URIs. This is intended as an auxiliary helper method
    for :func:`delete_group_recursively`.
    """

    namespace, group_name = utils.split_uri(uri)
    api_instance = cloud_client.client.groups_api

    try:
        array_tiledb_uris = []
        group_tiledb_uris = []
        page_index = 1
        while True:
            page = api_instance.get_group_contents(
                namespace,
                group_name,
                page=page_index,
                per_page=20,
            )
            for e in page.entries:
                # Do not do:
                #   array_tiledb_uris.append(e.array.tiledb_uri)
                # This is because if we have two groups like
                #   tiledb://username/soma1
                #   tiledb://username/soma2
                # each with an array element 'obs', then both will have
                # an array.tiledb_uri that looks like:
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
        return (array_tiledb_uris, group_tiledb_uris)

    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None
