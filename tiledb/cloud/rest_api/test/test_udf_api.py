# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 1.4.0
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

    def test_submit_udf(self):
        """Test case for submit_udf

        """
        pass


if __name__ == "__main__":
    unittest.main()
