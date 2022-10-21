import uuid
import warnings
from typing import Any, Callable, Iterable, Optional, Sequence, Union

from tiledb.cloud import client
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud import utils
from tiledb.cloud._common import json_safe
from tiledb.cloud._results import decoders
from tiledb.cloud._results import results
from tiledb.cloud._results import sender
from tiledb.cloud.rest_api import ApiException as GenApiException
from tiledb.cloud.rest_api import models

# Re-export for compatibility.
split_uri = utils.split_uri

def info(uri, async_req=False):
    """
    Returns the cloud metadata

    :param async_req: return future instead of results for async support

    :return: metadata object
    """
    (namespace, group_name) = split_uri(uri)
    api_instance = client.client.groups_api

    try:
        return api_instance.get_group_metadata(
            namespace=namespace, group=group_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def list_shared_with(uri, async_req=False):
    """Return group sharing policies"""
    (namespace, group_name) = split_uri(uri)
    api_instance = client.client.groups_api

    try:
        return api_instance.get_group_sharing_policies(
            namespace=namespace, group=group_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def share_group(uri, namespace, group_permissions, content_permissions, async_req=False):
    """
    Shares group with give namespace and permissions

    :param str namespace:
    :param list(str) group_permissions: The permissions of the group itself, can a user add/remove things from the group?
    :param list(str) content_permissions: The permissions for all assets in the group. Can a user read/write arrays inside the group?
    :param async_req: return future instead of results for async support
    :return:
    """

    if not isinstance(permissions, list):
        permissions = [permissions]

    for perm in permissions:
        if (
            not perm.lower() == models.GroupActions.READ
            and not perm.lower() == models.GroupActions.WRITE
        ):
            raise Exception("Only read or write permissions are accepted")

    (group_namespace, group_name) = split_uri(uri)
    api_instance = client.client.groups_api

    try:
        return api_instance.share_group(
            namespace=group_namespace,
            group=group_name,
            group_sharing=models.GroupSharing(namespace=namespace, array_actions=content_permissions, group_actions=permissions),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def unshare_group(uri, namespace, async_req=False):
    """
    Removes sharing of an group from given namespace

    :param str namespace: namespace to remove shared access to the group
    :param async_req: return future instead of results for async support
    :return:
    :raises: :py:exc:
    """
    return share_group(uri, namespace, list(), list(), async_req=async_req)


def update_info(
    uri,
    group_name=None,
    description=None,
    access_credentials_name=None,
    tags=None,
    async_req=False,
):
    """
    Update an group's info
    :param str namespace: optional username or organization group should be registered under. If unset will default to the user
    :param str group_name: name of group to rename to
    :param str description: optional description
    :param str access_credentials_name: optional name of access credentials to use, if left blank default for namespace will be used
    :param list tags: to update to
    :param str file_type: group represents give file type
    :param str file_properties: set file properties on group
    :param async_req: return future instead of results for async support
    """
    api_instance = client.client.groups_api
    (namespace, current_group_name) = split_uri(uri)

    try:
        return api_instance.update_group_metadata(
            namespace=namespace,
            group=current_group_name,
            group_metadata=models.GroupInfo(
                description=description,
                name=group_name,
                uri=uri,
                access_credentials_name=access_credentials_name,
                tags=tags,
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None

def register_group(
    uri,
    namespace=None,
    group_name=None,
    description=None,
    access_credentials_name=None,
    async_req=False,
):
    """
    Register this group with the tiledb cloud service
    :param str namespace: optional username or organization group should be registered under. If unset will default to the user
    :param str group_name: name of group
    :param str description: optional description
    :param str access_credentials_name: optional name of access credentials to use, if left blank default for namespace will be used
    :param async_req: return future instead of results for async support
    """
    api_instance = client.client.groups_api

    namespace = namespace or client.default_user().username

    try:
        return api_instance.register_group(
            namespace=namespace,
            group=uri,
            group_metadata=models.GroupInfoUpdate(
                description=description,
                name=group_name,
                uri=uri,
                access_credentials_name=access_credentials_name,
            ),
            async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def deregister_group(uri, async_req=False):
    """
    Deregister the from the tiledb cloud service. This does not physically delete the group, it will remain
    in your bucket. All access to the group and cloud metadata will be removed.

    :param async_req: return future instead of results for async support

    :return success or error
    """
    (namespace, group_name) = split_uri(uri)

    api_instance = client.client.groups_api

    try:
        return api_instance.deregister_group(
            namespace=namespace, group=group_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None
