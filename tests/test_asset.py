"""Tests of the tiledb.cloud.asset module."""

from unittest import mock

from tiledb.cloud.asset import delete  # type: ignore
from tiledb.cloud.asset import info  # type: ignore
from tiledb.cloud.rest_api.models import ArrayInfo  # type: ignore
from tiledb.cloud.rest_api.models import GroupInfo  # type: ignore


@mock.patch("tiledb.object_type", return_value="array")
@mock.patch("tiledb.cloud.array.delete_array")
def test_asset_delete_array_dispatch(delete_array, object_type):
    """Dispatch to array.array_delete when URI is an array."""
    delete("a")
    # Since delete() doesn't return a value, we assert on the implementation.
    delete_array.assert_called_once_with("a")


@mock.patch("tiledb.object_type", return_value="group")
@mock.patch("tiledb.cloud.groups.delete")
def test_asset_delete_group_dispatch(delete_group, object_type):
    """Dispatch to groups.delete when URI is a group."""
    delete("g")
    # Since delete() doesn't return a value, we assert on the implementation.
    delete_group.assert_called_once_with("g", recursive=False)


@mock.patch("tiledb.object_type", return_value="group")
@mock.patch("tiledb.cloud.groups.delete")
def test_asset_delete_group_recursive(delete_group, object_type):
    """Dispatch to groups.delete, recursively, when URI is a group."""
    delete("g", recursive=True)
    # Since delete() doesn't return a value, we assert on the implementation.
    delete_group.assert_called_once_with("g", recursive=True)


@mock.patch("tiledb.object_type", return_value="array")
@mock.patch("tiledb.cloud.array.info", return_value=ArrayInfo(tiledb_uri="tiledb://a"))
def test_asset_info_array_dispatch(array_info, object_type):
    """Dispatch to array.info when URI is an array."""
    asset_info = info("a")
    assert isinstance(asset_info, ArrayInfo)
    assert asset_info.tiledb_uri == "tiledb://a"


@mock.patch("tiledb.object_type", return_value="group")
@mock.patch("tiledb.cloud.groups.info", return_value=GroupInfo(tiledb_uri="tiledb://g"))
def test_asset_info_group_dispatch(group_info, object_type):
    """Dispatch to groups.info when URI is a group."""
    asset_info = info("g")
    assert isinstance(asset_info, GroupInfo)
    assert asset_info.tiledb_uri == "tiledb://g"


def test_public_array_asset_info():
    """Get info about a public production array."""
    asset_info = info("tiledb://TileDB-Inc/cd89a0d6-c262-4729-9e75-d942879e1d7d")
    assert asset_info.name == "documents"
    assert asset_info.type == "sparse"


def test_public_group_asset_info():
    """Get info about a public production group."""
    asset_info = info("tiledb://TileDB-Inc/52165567-040c-4e75-bb89-a3d06017f650")
    assert asset_info.name == "langchain_documentation_huggingface"
