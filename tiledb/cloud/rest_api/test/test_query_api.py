# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import rest_api
from tiledb.cloud.rest_api.api.query_api import QueryApi  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestQueryApi(unittest.TestCase):
    """QueryApi unit test stubs"""

    def setUp(self):
        self.api = tiledb.cloud.rest_api.api.query_api.QueryApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_finalize_query(self):
        """Test case for finalize_query"""
        pass

    def test_get_est_result_sizes(self):
        """Test case for get_est_result_sizes"""
        pass

    def test_get_file(self):
        """Test case for get_file"""
        pass

    def test_submit_query(self):
        """Test case for submit_query"""
        pass

    def test_submit_query_json(self):
        """Test case for submit_query_json"""
        pass


if __name__ == "__main__":
    unittest.main()
