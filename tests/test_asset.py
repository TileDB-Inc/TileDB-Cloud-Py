"""Tests of the tiledb.cloud.asset module."""

from unittest import mock

import tiledb
import tiledb.cloud


@mock.patch("tiledb.object_type")
@mock.patch("tiledb.cloud.array.info")
def test_asset_info_array(array_info, object_type):
    """Dispatch to array.info when URI is an array."""
    object_type.return_value = "array"
    array_info.return_value = {"tiledb_uri": "tiledb://a"}

    def info(uri):
        asset_map = {"array": tiledb.cloud.array, "group": tiledb.cloud.groups}
        mod = asset_map[tiledb.object_type(uri)]
        return getattr(mod, "info")(uri)

    assert info("a") == {"tiledb_uri": "tiledb://a"}


@mock.patch("tiledb.object_type")
@mock.patch("tiledb.cloud.groups.info")
def test_asset_info_group(groups_info, object_type):
    """Dispatch to groups.info when URI is a group."""
    object_type.return_value = "group"
    groups_info.return_value = {"tiledb_uri": "tiledb://g"}

    def info(uri):
        asset_map = {"array": tiledb.cloud.array, "group": tiledb.cloud.groups}
        mod = asset_map[tiledb.object_type(uri)]
        return getattr(mod, "info")(uri)

    assert info("g") == {"tiledb_uri": "tiledb://g"}
