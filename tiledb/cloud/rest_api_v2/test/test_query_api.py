# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import tiledb.cloud.rest_api_v2
from tiledb.cloud.rest_api_v2.api.query_api import QueryApi  # noqa: E501
from tiledb.cloud.rest_api_v2.rest import ApiException


class TestQueryApi(unittest.TestCase):
    """QueryApi unit test stubs"""

    def setUp(self):
        self.api = tiledb.cloud.rest_api_v2.api.query_api.QueryApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_submit_query(self):
        """Test case for submit_query

        """
        pass


if __name__ == '__main__':
    unittest.main()
