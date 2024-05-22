"""An asset may be an array or a group."""

import tiledb.cloud  # type: ignore

asset_type_map = {"array": tiledb.cloud.array, "group": tiledb.cloud.groups}


def info(uri: str) -> object:
    """Information about an asset.

    :param uri: URI of the asset.
    :return: object.
    """
    # Note: the URI can be either of the two forms, yes?
    # tiledb://namespace/name or tiledb://namespace/UUID.
    ctx = tiledb.cloud.Ctx()
    mod = asset_type_map[tiledb.object_type(uri, ctx=ctx)]
    return getattr(mod, "info")(uri)
