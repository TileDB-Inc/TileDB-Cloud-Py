from typing import Dict, List, Optional, Tuple

import tiledb.cloud.array
import tiledb.cloud.client as cloud_client
import tiledb.cloud.rest_api as rest_api
import tiledb.cloud.rest_api.models as models
import tiledb.cloud.tiledb_cloud_error as tiledb_cloud_error
import tiledb.cloud.utils


def get_group(uri: str) -> models.group_info.GroupInfo:
    """
    Returns the cloud metadata

    :return: metadata object
    """
    (namespace, group_name) = tiledb.cloud.utils.split_uri(uri)
    api_instance = cloud_client.client.groups_api

    try:
        return api_instance.get_group(namespace, group_name)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def delete_group_recursively(
    uri: str, dry_run: bool = False, verbose: bool = False
) -> None:
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

    (namespace, group_name) = tiledb.cloud.utils.split_uri(uri)

    # Get all members before deleting any, since we don't want to be deleting
    # things we're iterating over.
    (
        array_element_tiledb_uris,
        group_element_tiledb_uris,
    ) = _get_group_element_tiledb_uris(uri)

    for e in array_element_tiledb_uris:
        if verbose:
            print("DELETE ARRAY", e)
        if not dry_run:
            tiledb.cloud.array.delete_array(e)
    for e in group_element_tiledb_uris:
        # Depth-first traversal
        delete_group_recursively(e, dry_run=dry_run, verbose=verbose)
        if verbose:
            print("DELETE GROUP", e)
        if not dry_run:
            delete_group(e)


def delete_group(uri: str) -> None:
    """
    Deletes the group. The assets are not deleted nor are not relocated to any other group.

    You probably want `delete_group_recursively`.

    :param uri: TileDB Cloud URI of the group to be deleted
    """
    (namespace, group_name) = tiledb.cloud.utils.split_uri(uri)
    api_instance = cloud_client.client.groups_api
    try:
        return api_instance.delete_group(namespace, group_name)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def _get_group_element_tiledb_uris(uri: str) -> Tuple[List[str], List[str]]:
    """
    Given a TileDB Cloud group URI, returns a listing of array-element URIs,
    and group-element URIs. This is intended as an auxiliary helper method
    for `delete_group_recursively`.
    """

    (namespace, group_name) = tiledb.cloud.utils.split_uri(uri)
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
        return (array_tiledb_uris, group_tiledb_uris)

    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None
