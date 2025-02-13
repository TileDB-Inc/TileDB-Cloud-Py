"""Tests of the tiledb.cloud.asset module."""

import time
import unittest
from unittest import mock

import pytest

from tiledb.cloud import asset  # type: ignore
from tiledb.cloud import client
from tiledb.cloud import groups
from tiledb.cloud import rest_api
from tiledb.cloud._common import testonly
from tiledb.cloud.rest_api.models import ArrayInfo  # type: ignore
from tiledb.cloud.rest_api.models import ArraySharing  # type: ignore
from tiledb.cloud.rest_api.models import GroupInfo  # type: ignore
from tiledb.cloud.rest_api.models import GroupSharing  # type: ignore

TRIES = 5


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


@pytest.mark.xfail(reason="Server error 610")
def test_public_array_sharing():
    """Get a public production array's sharing policies."""
    sharing = asset.list_shared_with(
        "tiledb://TileDB-Inc/cd89a0d6-c262-4729-9e75-d942879e1d7d"
    )
    assert len(sharing) == 2
    assert "public" in set(policy.namespace for policy in sharing)


def test_public_group_sharing():
    """Get a public production group's sharing policies."""
    sharing = asset.list_shared_with(
        "tiledb://TileDB-Inc/52165567-040c-4e75-bb89-a3d06017f650"
    )
    assert len(sharing) == 1
    assert sharing[0].namespace == "public"


@mock.patch("tiledb.object_type", return_value="array")
@mock.patch("tiledb.cloud.array.update_info")
def test_asset_update_info_array_dispatch(update_array, object_type):
    """Dispatch to array.update_info when URI is an array."""
    asset.update_info("a", description="new description")
    update_array.assert_called_once_with(
        "a",
        array_name=None,
        description="new description",
        access_credentials_name=None,
        tags=None,
    )


@mock.patch("tiledb.object_type", return_value="group")
@mock.patch("tiledb.cloud.groups.update_info")
def test_asset_update_info_group_dispatch(update_group, object_type):
    """Dispatch to groups.update_info when URI is a group."""
    asset.update_info("g", description="new description")
    update_group.assert_called_once_with(
        "g", name=None, description="new description", tags=None
    )


@mock.patch("tiledb.object_type", return_value="array")
@mock.patch("tiledb.cloud.array.register_array")
def test_asset_register_array_dispatch(register_array, object_type):
    """Dispatch to array.register_array when URI is an array."""
    asset.register("a", "array", name="foo", credentials_name="bar")
    register_array.assert_called_once_with(
        "a",
        namespace=None,
        array_name="foo",
        access_credentials_name="bar",
        dest_uri=None,
    )


@mock.patch("tiledb.object_type", return_value="group")
@mock.patch("tiledb.cloud.groups.register")
def test_asset_register_group_dispatch(register_group, object_type):
    """Dispatch to groups.register when URI is a group."""
    asset.register("a", "group", name="foo", credentials_name="bar")
    register_group.assert_called_once_with(
        "a",
        name="foo",
        namespace=None,
        credentials_name="bar",
        parent_uri=None,
        dest_uri=None,
    )


@mock.patch("tiledb.object_type", return_value="array")
@mock.patch("tiledb.cloud.array.deregister_array")
def test_asset_deregister_array_dispatch(deregister_array, object_type):
    """Dispatch to array.deregister_array when URI is an array."""
    asset.deregister("a")
    deregister_array.assert_called_once_with("a")


@mock.patch("tiledb.object_type", return_value="group")
@mock.patch("tiledb.cloud.groups.deregister")
def test_asset_deregister_group_dispatch(deregister_group, object_type):
    """Dispatch to groups.deregister when URI is a group."""
    asset.deregister("g")
    deregister_group.assert_called_once_with("g", recursive=False)


@mock.patch("tiledb.object_type", return_value="group")
@mock.patch("tiledb.cloud.groups.deregister")
def test_asset_deregister_group_recursive_dispatch(deregister_group, object_type):
    """Dispatch to groups.deregister when URI is a group."""
    asset.deregister("g", recursive=True)
    deregister_group.assert_called_once_with("g", recursive=True)


class ListingTest(unittest.TestCase):
    @pytest.mark.udf
    def test_list(self) -> None:
        # Ensure that we have at least one asset registered (a UDF)
        with testonly.register_udf(lambda: 1, func_name="some_lambda"):
            result = asset.list(page=1, per_page=2)
        self.assertGreater(result.pagination_metadata.total_items, 0)

    def test_list_public(self) -> None:
        result = asset.list_public(page=1, per_page=2)
        self.assertGreater(result.pagination_metadata.total_items, 0)

    def test_canonicalize_csv(self) -> None:
        in_out = (
            ("", None),
            ("a,b", "a,b"),
            (("a", "b"), "a,b"),
            ([""], None),
            ((), None),
            (None, None),
        )
        for inp, outp in in_out:
            self.assertEqual(outp, asset._canonicalize_csv(inp))


class RegistrationTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.namespace, storage_path, _ = groups._default_ns_path_cred()
        self.test_path = storage_path + "/" + testonly.random_name("groups_test")

    def assert_group_exists(self, name):
        """Asserts that a group exists, and gives it a few tries."""
        api = client.build(rest_api.GroupsApi)
        for _ in range(TRIES):
            try:
                api.get_group_contents(group_namespace=self.namespace, group_name=name)
                return
            except rest_api.ApiException:
                pass  # try again
            time.sleep(1)
        self.fail(f"group {self.namespace}/{name} does not exist")

    def assert_group_not_exists(self, name):
        """Asserts that a group does not exist, giving it a few tries to go."""
        api = client.build(rest_api.GroupsApi)
        for _ in range(TRIES):
            try:
                api.get_group_contents(group_namespace=self.namespace, group_name=name)
            except rest_api.ApiException as apix:
                if apix.status in (400, 404):
                    return
            time.sleep(1)
        self.fail(f"group {self.namespace}/{name} still exists")

    def test_create_deregister(self):
        # TODO: This test leaves detritus around.
        # Once we get true delete functions, clean that up.
        outer_name = testonly.random_name("outer")
        outer_storage_name = testonly.random_name(outer_name)
        outer_storage_path = f"{self.test_path}/{outer_storage_name}"
        outer_uri = f"tiledb://{self.namespace}/{outer_name}"
        groups.create(outer_name, storage_uri=outer_storage_path)
        self.assert_group_exists(outer_name)

        asset.deregister(outer_uri)
        self.assert_group_not_exists(outer_name)

        asset.register(outer_storage_path, "group", name=outer_name)
        self.assert_group_exists(outer_name)
        inner_name = testonly.random_name("inner")
        groups.create(inner_name, parent_uri=outer_uri)
        self.assert_group_exists(inner_name)
        for _ in range(TRIES):
            try:
                asset.deregister(outer_uri, recursive=True)
                break
            except Exception:
                time.sleep(2)
        self.assert_group_not_exists(outer_name)
        self.assert_group_not_exists(inner_name)


def test_failure_bogus_uri():
    """Raise ValueError."""
    with pytest.raises(ValueError):
        asset.info("bogus")
