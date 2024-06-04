import time
import unittest

from tiledb.cloud._common import testonly
from tiledb.services import errors
from tiledb.services.api_v1 import groups as v1_groups
from tiledb.services.api_v2 import groups as v2_groups

TRIES = 5


class GroupsTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.namespace, storage_path, _ = v2_groups._default_ns_path_cred()
        self.test_path = storage_path + "/" + testonly.random_name("groups_test")

    def assert_group_exists(self, name):
        """Asserts that a group exists, and gives it a few tries."""
        for _ in range(TRIES):
            try:
                v1_groups.get_group_contents(uri=f"tiledb://{self.namespace}/{name}")
                return
            except errors.TileDBCloudError:
                pass  # try again
            time.sleep(1)
        self.fail(f"group {self.namespace}/{name} does not exist")

    def assert_group_not_exists(self, name):
        """Asserts that a group does not exist, giving it a few tries to go."""
        for _ in range(TRIES):
            try:
                v1_groups.get_group_contents(uri=f"tiledb://{self.namespace}/{name}")
            except (errors.BadRequest, errors.NotFound):
                return
            time.sleep(1)
        self.fail(f"group {self.namespace}/{name} still exists")

    def test_create_deregister(self):
        outer_name = testonly.random_name("outer")
        outer_storage_name = testonly.random_name(outer_name)
        outer_storage_path = f"{self.test_path}/{outer_storage_name}"
        outer_uri = f"tiledb://{self.namespace}/{outer_name}"
        v2_groups.create(outer_name, storage_uri=outer_storage_path)
        self.assert_group_exists(outer_name)

        v2_groups.deregister(outer_uri)
        self.assert_group_not_exists(outer_name)

        v2_groups.register(outer_storage_path, name=outer_name)
        self.assert_group_exists(outer_name)
        inner_name = testonly.random_name("inner")
        v2_groups.create(inner_name, parent_uri=outer_uri)
        self.assert_group_exists(inner_name)
        for _ in range(TRIES):
            try:
                v2_groups.deregister(outer_uri, recursive=True)
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
        v2_groups.create(group_name, storage_uri=group_storage_path)
        self.assert_group_exists(group_name)

        description = "this is a test description"
        logo = "testLogo"
        tags = ["tag", "othertag"]
        status_code = v1_groups.update_info(
            group_uri, description=description, logo=logo, tags=tags
        )
        self.assertEqual(status_code, 204)

        group_info = v1_groups.info(group_uri)
        self.assertEqual(group_info.get("description", None), description)
        self.assertEqual(group_info.get("logo", None), logo)
        self.assertCountEqual(group_info.get("tags", []), tags)

        # Cleanup
        v2_groups.deregister(group_uri)
        self.assert_group_not_exists(group_name)
