# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.1.1
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import rest_api
from tiledb.cloud.rest_api.api.udf_api import UdfApi  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestUdfApi(unittest.TestCase):
    """UdfApi unit test stubs"""

    def setUp(self):
        self.api = tiledb.cloud.rest_api.api.udf_api.UdfApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_udf_info(self):
        """Test case for delete_udf_info"""
        pass

    def test_get_udf_info(self):
        """Test case for get_udf_info"""
        pass

    def test_get_udf_info_list(self):
        """Test case for get_udf_info_list"""
        pass

    def test_get_udf_info_sharing_policies(self):
        """Test case for get_udf_info_sharing_policies"""
        pass

    def test_register_udf_info(self):
        """Test case for register_udf_info"""
        pass

    def test_share_udf_info(self):
        """Test case for share_udf_info"""
        pass

    def test_submit_generic_udf(self):
        """Test case for submit_generic_udf"""
        pass

    def test_submit_udf(self):
        """Test case for submit_udf"""
        pass

    def test_update_udf_info(self):
        """Test case for update_udf_info"""
        pass


if __name__ == "__main__":
    unittest.main()
