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
        groups.deregister(outer_uri, recursive=True)
        self.assert_group_not_exists(outer_name)
        self.assert_group_not_exists(inner_name)

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
