# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import tiledb.cloud.rest_api_v2
from tiledb.cloud.rest_api_v2.models.tile_db_config import TileDBConfig  # noqa: E501
from tiledb.cloud.rest_api_v2.rest import ApiException

class TestTileDBConfig(unittest.TestCase):
    """TileDBConfig unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TileDBConfig
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = tiledb.cloud.rest_api_v2.models.tile_db_config.TileDBConfig()  # noqa: E501
        if include_optional :
            return TileDBConfig(
                entries = [
                    tiledb.cloud.rest_api_v2.models.tile_db_config_entries.TileDBConfig_entries(
                        key = '0', 
                        value = '0', )
                    ]
            )
        else :
            return TileDBConfig(
        )

    def testTileDBConfig(self):
        """Test TileDBConfig"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
