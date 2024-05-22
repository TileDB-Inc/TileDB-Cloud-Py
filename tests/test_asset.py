"""Tests of the tiledb.cloud.asset module."""

from unittest import mock

from tiledb.cloud import asset


@mock.patch("tiledb.object_type")
@mock.patch("tiledb.cloud.array.info")
def test_asset_info_array(array_info, object_type):
    """Dispatch to array.info when URI is an array."""
    object_type.return_value = "array"
    array_info.return_value = {"tiledb_uri": "tiledb://a"}

    assert asset.info("a") == {"tiledb_uri": "tiledb://a"}
    array_info.assert_called_once_with("a")


@mock.patch("tiledb.object_type")
@mock.patch("tiledb.cloud.groups.info")
def test_asset_info_group(groups_info, object_type):
    """Dispatch to groups.info when URI is a group."""
    object_type.return_value = "group"
    groups_info.return_value = {"tiledb_uri": "tiledb://g"}

    assert asset.info("g") == {"tiledb_uri": "tiledb://g"}
    groups_info.assert_called_once_with("g")


def test_prod_group_asset_info():
    """Get info about a production group."""
    info = asset.info("tiledb://TileDB-Inc/d185ecf1-4572-45f8-81a7-b02e907657dd")
    assert info.name == "cmu1_small"
    assert info.group_type == "bioimg"


def test_prod_array_asset_info():
    """Get info about a production array."""
    info = asset.info("tiledb://TileDB-Inc/886afe8c-c055-4569-9644-351d8e72f098")
    assert info.name == "l_0.tdb"
    assert info.type == "dense"


@mock.patch("tiledb.object_type")
@mock.patch("tiledb.cloud.array.delete_array")
def test_asset_delete_array(delete_array, object_type):
    """Dispatch to array.array_delete when URI is an array."""
    object_type.return_value = "array"

    asset.delete("a")
    delete_array.assert_called_once_with("a")


@mock.patch("tiledb.object_type")
@mock.patch("tiledb.cloud.groups.delete")
def test_asset_delete_group(delete, object_type):
    """Dispatch to groups.delete when URI is a group."""
    object_type.return_value = "group"

    asset.delete("g")
    delete.assert_called_once_with("g", recursive=False)


@mock.patch("tiledb.object_type")
@mock.patch("tiledb.cloud.groups.delete")
def test_asset_delete_group_recursive(delete, object_type):
    """Dispatch to groups.delete when URI is a group."""
    object_type.return_value = "group"

    asset.delete("g", recursive=True)
    delete.assert_called_once_with("g", recursive=True)
