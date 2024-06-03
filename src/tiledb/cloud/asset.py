"""An asset may be an array or a group."""

from functools import partial
from typing import Callable, Mapping, Union

import tiledb  # type: ignore

from . import array  # type: ignore
from . import groups  # type: ignore
from .rest_api.models import ArrayInfo  # type: ignore
from .rest_api.models import GroupInfo  # type: ignore


def delete(uri: str, recursive: bool = False) -> None:
    """Deregister the asset and remove its physical groups and arrays from storage.

    :param uri: tiledb URI of the asset.
    :return: None.
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
    :return: ArrayInfo or GroupInfo.
    """
    # Note: the URI can be either of the two forms, yes?
    # tiledb://namespace/name or tiledb://namespace/UUID.
    info_map: Mapping[str, Callable] = {"array": array.info, "group": groups.info}
    asset_type: str = tiledb.object_type(uri, ctx=tiledb.cloud.Ctx())
    func = info_map[asset_type]
    return func(uri)
