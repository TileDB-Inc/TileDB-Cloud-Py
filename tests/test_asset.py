"""Tests of the tiledb.cloud.asset module."""

from unittest import mock

from tiledb.cloud import asset  # type: ignore
from tiledb.cloud.rest_api.models import ArrayInfo  # type: ignore
from tiledb.cloud.rest_api.models import ArraySharing  # type: ignore
from tiledb.cloud.rest_api.models import GroupInfo  # type: ignore
from tiledb.cloud.rest_api.models import GroupSharing  # type: ignore


@mock.patch("tiledb.object_type", return_value="array")
@mock.patch("tiledb.cloud.array.delete_array")
def test_asset_delete_array_dispatch(delete_array, object_type):
    """Dispatch to array.array_delete when URI is an array."""
    asset.delete("a")
    # Since asset.delete() doesn't return a value, we assert on the implementation.
    delete_array.assert_called_once_with("a")


@mock.patch("tiledb.object_type", return_value="group")
@mock.patch("tiledb.cloud.groups.delete")
def test_asset_delete_group_dispatch(delete_group, object_type):
    """Dispatch to groups.delete when URI is a group."""
    asset.delete("g")
    delete_group.assert_called_once_with("g", recursive=False)


@mock.patch("tiledb.object_type", return_value="group")
@mock.patch("tiledb.cloud.groups.delete")
def test_asset_delete_group_recursive(delete_group, object_type):
    """Dispatch to groups.delete, recursively, when URI is a group."""
    asset.delete("g", recursive=True)
    delete_group.assert_called_once_with("g", recursive=True)


@mock.patch("tiledb.object_type", return_value="array")
@mock.patch("tiledb.cloud.array.info", return_value=ArrayInfo(tiledb_uri="tiledb://a"))
def test_asset_info_array_dispatch(array_info, object_type):
    """Dispatch to array.info when URI is an array."""
    info = asset.info("a")
    assert isinstance(info, ArrayInfo)
    assert info.tiledb_uri == "tiledb://a"


@mock.patch("tiledb.object_type", return_value="group")
@mock.patch("tiledb.cloud.groups.info", return_value=GroupInfo(tiledb_uri="tiledb://g"))
def test_asset_info_group_dispatch(group_info, object_type):
    """Dispatch to groups.info when URI is a group."""
    info = asset.info("g")
    assert isinstance(info, GroupInfo)
    assert info.tiledb_uri == "tiledb://g"


def test_public_array_asset_info():
    """Get info about a public production array."""
    info = asset.info("tiledb://TileDB-Inc/cd89a0d6-c262-4729-9e75-d942879e1d7d")
    assert info.name == "documents"
    assert info.type == "sparse"


def test_public_group_asset_info():
    """Get info about a public production group."""
    info = asset.info("tiledb://TileDB-Inc/52165567-040c-4e75-bb89-a3d06017f650")
    assert info.name == "langchain_documentation_huggingface"


@mock.patch("tiledb.object_type", return_value="array")
@mock.patch("tiledb.cloud.array.share_array")
def test_asset_share_array_dispatch(share_array, object_type):
    """Dispatch to array.share_array when URI is an array."""
    asset.share("a", "public", "read")
    share_array.assert_called_once_with("a", "public", "read")


@mock.patch("tiledb.object_type", return_value="group")
@mock.patch("tiledb.cloud.groups.share_group")
def test_asset_share_group_dispatch(share_group, object_type):
    """Dispatch to groups.share when URI is a group."""
    asset.share("g", "public", "read")
    share_group.assert_called_once_with("g", "public", "read")


@mock.patch("tiledb.object_type", return_value="group")
@mock.patch("tiledb.cloud.groups.share_group")
def test_asset_unshare_group_dispatch(share_group, object_type):
    """Dispatch to groups.share when URI is a group."""
    asset.unshare("g", "public")
    share_group.assert_called_once_with("g", "public", [])


@mock.patch("tiledb.object_type", return_value="array")
@mock.patch(
    "tiledb.cloud.array.list_shared_with", return_value=[ArraySharing(namespace="foo")]
)
def test_asset_list_shared_with_array_dispatch(array_sharing, object_type):
    """Dispatch to array.list_shared_with when URI is an array."""
    sharing = asset.list_shared_with("a")
    assert isinstance(sharing[0], ArraySharing)
    assert sharing[0].namespace == "foo"


@mock.patch("tiledb.object_type", return_value="group")
@mock.patch(
    "tiledb.cloud.groups.list_shared_with", return_value=[GroupSharing(namespace="bar")]
)
def test_asset_list_shared_with_group_dispatch(group_sharing, object_type):
    """Dispatch to groups.info when URI is a group."""
    sharing = asset.list_shared_with("g")
    assert isinstance(sharing[0], GroupSharing)
    assert sharing[0].namespace == "bar"


def test_public_array_sharing():
    """Get a public production array's sharing policies."""
    sharing = asset.list_shared_with(
        "tiledb://TileDB-Inc/cd89a0d6-c262-4729-9e75-d942879e1d7d"
    )
    assert len(sharing) == 2
    assert sharing[0].namespace == "public"


def test_public_group_sharing():
    """Get a public production group's sharing policies."""
    sharing = asset.list_shared_with(
        "tiledb://TileDB-Inc/52165567-040c-4e75-bb89-a3d06017f650"
    )
    assert len(sharing) == 1
    assert sharing[0].namespace == "public"
