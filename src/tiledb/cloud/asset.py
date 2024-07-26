"""An asset may be an array or a group."""

from functools import partial
from typing import Callable, List, Mapping, Optional, Union

import tiledb  # type: ignore

from . import array  # type: ignore
from . import groups  # type: ignore
from .rest_api.models import ArrayInfo  # type: ignore
from .rest_api.models import GroupInfo  # type: ignore


def register(
    storage_uri: str,
    type: str,
    *,
    name: Optional[str] = None,
    namespace: Optional[str] = None,
    credentials_name: Optional[str] = None,
    parent_uri: Optional[str] = None,
) -> None:
    """
    Register stored objects as an asset.

    :param storage_uri: S3, for example, URI of the data to be registered.
    :type uri: str
    :param type: The type of asset, "array" or "group".
    :type type: str
    :param namespace: The user or organization to register the asset
        under. If unset will default to the logged-in user's namespace.
    :type namespace: str
    :param name: Name of asset.
    :type name: str
    :param description: Optional description.
    :type description: str
    :param credentials_name: Optional name of access credentials to use.
        If omitted, the default for namespace will be used.
    :type credentials_name: str
    :param parent_uri: Optional parent URI for group type assets.
    :type parent_uri: str

    For example, to register an array stored on S3 in a bucket named
    'your-bucket' with a prefix 'prefix' to your own namespace:

    >>> from tiledb.cloud import asset
    >>> asset.register(
    ...     "s3://your-bucket/prefix",
    ...     "array",
    ...     name="new-array",
    ... )
    """
    if type == "array":
        array.register_array(
            storage_uri,
            namespace=namespace,
            array_name=name,
            access_credentials_name=credentials_name,
        )
    elif type == "group":
        groups.register(
            storage_uri,
            name=name,
            namespace=namespace,
            credentials_name=credentials_name,
            parent_uri=parent_uri,
        )
    else:
        raise tiledb.TileDBError(f"Invalid asset type '{type}'")


def deregister(uri: str, *, recursive: Optional[bool] = False) -> None:
    """Deregister an asset.

    :param uri: tiledb URI of the asset.
    :type uri: str
    :param recursive: if True, contents of an asset will be recursively
        deregistered Default: False.
    :type recursive: bool
    """
    deregister_map: Mapping[str, Callable] = {
        "array": array.deregister_array,
        "group": partial(groups.deregister, recursive=recursive),
    }
    asset_type: str = tiledb.object_type(uri, ctx=tiledb.cloud.Ctx())
    func = deregister_map[asset_type]
    return func(uri)


def delete(uri: str, *, recursive: Optional[bool] = False) -> None:
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


def update_info(
    uri: str,
    *,
    description: Optional[str] = None,
    name: Optional[str] = None,
    tags: Optional[List[str]] = None,
    access_credentials_name: Optional[str] = None,
) -> None:
    """
    Update asset info settings.

    :param uri: tiledb URI of the asset.
    :type uri: str
    :param description: Asset description, defaults to None
    :type description: str
    :param name: Asset name, defaults to None
    :type name: str
    :param tags: Asset tags, defaults to None
    :type tags: List[str]

    For example, to update only the description of an asset, call update_info()
    with only a 'description' keyword argument:

    >>> from tiledb.cloud import asset
    >>> asset.update_info(
    ...     "tiledb://your-namespace/your-asset",
    ...     description="This is a new description"
    ... )
    """
    # Note: logo not yet supported.
    asset_type: str = tiledb.object_type(uri, ctx=tiledb.cloud.Ctx())
    if asset_type == "array":
        return array.update_info(
            uri,
            array_name=name,
            description=description,
            access_credentials_name=access_credentials_name,
            tags=tags,
        )
    elif asset_type == "group":
        return groups.update_info(uri, description=description, name=name, tags=tags)
    else:
        raise tiledb.TileDBError(f"Invalid asset type '{asset_type}'")


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
    uri: str, namespace: str, permissions: Optional[Union[str, List[str]]] = "read"
) -> None:
    """Give another namespace permission to access an asset.

    :param uri: tiledb URI of the asset.
    :type uri: str
    :param namespace: the target namespace.
    :type namespace: str
    :param permissions: 'read', 'write', or ['read', 'write'].
    :type permissions: str or List[str]

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
