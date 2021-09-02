# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import datetime
import unittest

import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.models.favorite import Favorite  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestFavorite(unittest.TestCase):
    """Favorite unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Favorite
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.favorite.Favorite()  # noqa: E501
        if include_optional:
            return Favorite(
                id="0",
                object_type="ARRAY",
                namespace="0",
                name="0",
                created_at=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
            )
        else:
            return Favorite()

    def testFavorite(self):
        """Test Favorite"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
