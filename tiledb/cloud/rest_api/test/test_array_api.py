"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


import unittest

import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api.array_api import ArrayApi  # noqa: E501


class TestArrayApi(unittest.TestCase):
    """ArrayApi unit test stubs"""

    def setUp(self):
        self.api = ArrayApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_array_activity_log(self):
        """Test case for array_activity_log"""
        pass

    def test_arrays_browser_owned_get(self):
        """Test case for arrays_browser_owned_get"""
        pass

    def test_arrays_browser_owned_sidebar_get(self):
        """Test case for arrays_browser_owned_sidebar_get"""
        pass

    def test_arrays_browser_public_get(self):
        """Test case for arrays_browser_public_get"""
        pass

    def test_arrays_browser_public_sidebar_get(self):
        """Test case for arrays_browser_public_sidebar_get"""
        pass

    def test_arrays_browser_shared_get(self):
        """Test case for arrays_browser_shared_get"""
        pass

    def test_arrays_browser_shared_sidebar_get(self):
        """Test case for arrays_browser_shared_sidebar_get"""
        pass

    def test_arrays_namespace_array_end_timestamps_get(self):
        """Test case for arrays_namespace_array_end_timestamps_get"""
        pass

    def test_consolidate_array(self):
        """Test case for consolidate_array"""
        pass

    def test_create_array(self):
        """Test case for create_array"""
        pass

    def test_delete_array(self):
        """Test case for delete_array"""
        pass

    def test_deregister_array(self):
        """Test case for deregister_array"""
        pass

    def test_get_activity_log_by_id(self):
        """Test case for get_activity_log_by_id"""
        pass

    def test_get_all_array_metadata(self):
        """Test case for get_all_array_metadata"""
        pass

    def test_get_array(self):
        """Test case for get_array"""
        pass

    def test_get_array_max_buffer_sizes(self):
        """Test case for get_array_max_buffer_sizes"""
        pass

    def test_get_array_meta_data_json(self):
        """Test case for get_array_meta_data_json"""
        pass

    def test_get_array_metadata(self):
        """Test case for get_array_metadata"""
        pass

    def test_get_array_metadata_capnp(self):
        """Test case for get_array_metadata_capnp"""
        pass

    def test_get_array_non_empty_domain(self):
        """Test case for get_array_non_empty_domain"""
        pass

    def test_get_array_non_empty_domain_json(self):
        """Test case for get_array_non_empty_domain_json"""
        pass

    def test_get_array_sample_data(self):
        """Test case for get_array_sample_data"""
        pass

    def test_get_array_sharing_policies(self):
        """Test case for get_array_sharing_policies"""
        pass

    def test_get_arrays_in_namespace(self):
        """Test case for get_arrays_in_namespace"""
        pass

    def test_get_fragment_end_timestamp(self):
        """Test case for get_fragment_end_timestamp"""
        pass

    def test_get_last_accessed_arrays(self):
        """Test case for get_last_accessed_arrays"""
        pass

    def test_register_array(self):
        """Test case for register_array"""
        pass

    def test_share_array(self):
        """Test case for share_array"""
        pass

    def test_update_array_metadata(self):
        """Test case for update_array_metadata"""
        pass

    def test_update_array_metadata_capnp(self):
        """Test case for update_array_metadata_capnp"""
        pass

    def test_vacuum_array(self):
        """Test case for vacuum_array"""
        pass


if __name__ == "__main__":
    unittest.main()
