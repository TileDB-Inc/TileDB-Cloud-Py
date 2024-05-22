"""An asset may be an array or a group."""

from functools import partial

import tiledb.cloud  # type: ignore


def info(uri: str) -> object:
    """Information about an asset.

    :param uri: URI of the asset.
    :return: object.
    """
    # Note: the URI can be either of the two forms, yes?
    # tiledb://namespace/name or tiledb://namespace/UUID.
    info_map = {"array": tiledb.cloud.array.info, "group": tiledb.cloud.groups.info}
    ctx = tiledb.cloud.Ctx()
    func = info_map[tiledb.object_type(uri, ctx=ctx)]
    return func(uri)


def delete(uri: str, recursive: bool = False) -> None:
    """Deregister the asset and remove its physical groups and arrays from storage.

    :param uri: URI of the asset.
    :return: None.
    """
    delete_map = {
        "array": tiledb.cloud.array.delete_array,
        "group": partial(tiledb.cloud.groups.delete, recursive=recursive),
    }
    ctx = tiledb.cloud.Ctx()
    func = delete_map[tiledb.object_type(uri, ctx=ctx)]
    return func(uri)
