"""An asset may be an array or a group."""

from functools import partial
from typing import Union

import tiledb.cloud  # type: ignore
from tiledb.cloud.rest_api.models import ArrayInfo  # type: ignore
from tiledb.cloud.rest_api.models import GroupInfo  # type: ignore


def delete(uri: str, recursive: bool = False) -> None:
    """Deregister the asset and remove its physical groups and arrays from storage.

    :param uri: URI of the asset.
    :return: None.
    """
    delete_map = {
        "array": tiledb.cloud.array.delete_array,
        "group": partial(tiledb.cloud.groups.delete, recursive=recursive),
    }
    asset_type = tiledb.object_type(uri, ctx=tiledb.cloud.Ctx())
    func = delete_map[asset_type]
    return func(uri)


def info(uri: str) -> Union[ArrayInfo, GroupInfo]:
    """Information about an asset.

    :param uri: URI of the asset.
    :return: ArrayInfo or GroupInfo.
    """
    # Note: the URI can be either of the two forms, yes?
    # tiledb://namespace/name or tiledb://namespace/UUID.
    info_map = {"array": tiledb.cloud.array.info, "group": tiledb.cloud.groups.info}
    asset_type = tiledb.object_type(uri, ctx=tiledb.cloud.Ctx())
    func = info_map[asset_type]
    return func(uri)
