# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import rest_api
from tiledb.cloud.rest_api.api.stats_api import StatsApi  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestStatsApi(unittest.TestCase):
    """StatsApi unit test stubs"""

    def setUp(self):
        self.api = tiledb.cloud.rest_api.api.stats_api.StatsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_tiledb_stats(self):
        """Test case for get_tiledb_stats

        """
        pass


if __name__ == "__main__":
    unittest.main()
