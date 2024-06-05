"""An asset may be an array or a group."""

from functools import partial
from typing import Callable, Mapping, Union

import tiledb  # type: ignore

from . import array  # type: ignore
from . import groups  # type: ignore
from .rest_api.models import ArrayInfo  # type: ignore
from .rest_api.models import GroupInfo  # type: ignore


def delete(uri: str, recursive: bool = False) -> None:
    """Deregister an asset and remove its objects from storage.

    :param uri: tiledb URI of the asset.
    :type uri: str
    :param recursive: if True, contents of an asset will be recursively
        deleted. Default: False.
    :type recursive: bool
    """
    delete_map: Mapping[str, Callable] = {
        "array": array.delete_array,
        "group": partial(groups.delete, recursive=recursive),
    }
    asset_type: str = tiledb.object_type(uri, ctx=tiledb.cloud.Ctx())
    func = delete_map[asset_type]
    return func(uri)


def info(uri: str) -> Union[ArrayInfo, GroupInfo]:
    """Retrieve information about an asset.

    :param uri: tiledb URI of the asset.
    :type uri: str
    :return: ArrayInfo or GroupInfo.
    """
    # Note: the URI can be either of the two forms, yes?
    # tiledb://namespace/name or tiledb://namespace/UUID.
    info_map: Mapping[str, Callable] = {"array": array.info, "group": groups.info}
    asset_type: str = tiledb.object_type(uri, ctx=tiledb.cloud.Ctx())
    func = info_map[asset_type]
    return func(uri)


def list_shared_with(uri: str) -> None:
    """List an asset's sharing policies.

    :param uri: tiledb URI of the asset.
    :type uri: str
    :return: a list of ArraySharing or GroupSharing objects.
    """
    sharing_map: Mapping[str, Callable] = {
        "array": array.list_shared_with,
        "group": groups.list_shared_with,
    }
    asset_type: str = tiledb.object_type(uri, ctx=tiledb.cloud.Ctx())
    func = sharing_map[asset_type]
    return func(uri)


def share(
    uri: str, namespace: str, permissions: Union[str, list[str]] = "read"
) -> None:
    """Give another namespace permission to access an asset.

    :param uri: tiledb URI of the asset.
    :type uri: str
    :param namespace: the target namespace.
    :type namespace: str
    :param permissions: 'read', 'write', or ['read', 'write'].
    :type permissions: str or list[str]

    For example, to make an asset readable by all, share it with the
    "public" namespace:

    >>> from tiledb.cloud import asset
    >>> asset.share("tiledb://your-namespace/your-asset", "public", "read")

    """
    share_map: Mapping[str, Callable] = {
        "array": array.share_array,
        "group": groups.share_group,
    }
    asset_type: str = tiledb.object_type(uri, ctx=tiledb.cloud.Ctx())
    func = share_map[asset_type]
    return func(uri, namespace, permissions)


def unshare(uri: str, namespace: str) -> None:
    """Remove access permissions for another namespace.

    :param uri: tiledb URI of the asset.
    :type uri: str
    :param namespace: the target namespace.
    :type namespace: str

    For example:

    >>> from tiledb.cloud import asset
    >>> asset.unshare("tiledb://your-namespace/your-asset", "guest")

    """
    share(uri, namespace, [])
