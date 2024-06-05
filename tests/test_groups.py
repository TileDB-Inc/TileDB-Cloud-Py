import time
import unittest

from tiledb.cloud import client
from tiledb.cloud import groups
from tiledb.cloud import rest_api
from tiledb.cloud._common import testonly

TRIES = 5


class GroupsTest(unittest.TestCase):
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

        groups.deregister(outer_uri)
        self.assert_group_not_exists(outer_name)

        groups.register(outer_storage_path, name=outer_name)
        self.assert_group_exists(outer_name)
        inner_name = testonly.random_name("inner")
        groups.create(inner_name, parent_uri=outer_uri)
        self.assert_group_exists(inner_name)
        for _ in range(TRIES):
            try:
                groups.deregister(outer_uri, recursive=True)
                break
            except Exception:
                time.sleep(2)
        self.assert_group_not_exists(outer_name)
        self.assert_group_not_exists(inner_name)

    def test_update_group_info(self):
        group_name = testonly.random_name("test_group_info")
        group_storage_name = testonly.random_name(group_name)
        group_storage_path = f"{self.test_path}/{group_storage_name}"
        group_uri = f"tiledb://{self.namespace}/{group_name}"
        groups.create(group_name, storage_uri=group_storage_path)
        self.assert_group_exists(group_name)

        description = "this is a test description"
        logo = "testLogo"
        tags = ["tag", "othertag"]
        groups.update_info(group_uri, description=description, logo=logo, tags=tags)
        group_info = groups.info(group_uri)

        self.assertEqual(group_info.description, description)
        self.assertEqual(group_info.logo, logo)
        self.assertCountEqual(group_info.tags, tags)

        # Cleanup
        groups.deregister(group_uri)
        self.assert_group_not_exists(group_name)

    def test_group_sharing(self):
        """Share a created group with 'public', unshare, then delete."""
        group_name = testonly.random_name("test_group_sharing")
        group_storage_name = testonly.random_name(group_name)
        group_storage_path = f"{self.test_path}/{group_storage_name}"
        group_uri = f"tiledb://{self.namespace}/{group_name}"
        groups.create(group_name, storage_uri=group_storage_path)
        self.assert_group_exists(group_name)

        groups.share_group(group_uri, "public", "read")
        sharing = groups.list_shared_with(group_uri)
        self.assertEqual(len(sharing), 1)
        self.assertEqual(sharing[0].namespace, "public")
        groups.unshare_group(group_uri, "public")
        sharing = groups.list_shared_with(group_uri)
        self.assertEqual(len(sharing), 0)

        groups.delete(group_uri)
