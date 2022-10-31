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
from tiledb.cloud.rest_api.models.asset_locations import AssetLocations  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestAssetLocations(unittest.TestCase):
    """AssetLocations unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AssetLocations
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.asset_locations.AssetLocations()  # noqa: E501
        if include_optional:
            return AssetLocations(
                arrays=tiledb.cloud.rest_api.models.storage_location.StorageLocation(
                    path="0",
                    credentials_name="0",
                ),
                files=tiledb.cloud.rest_api.models.storage_location.StorageLocation(
                    path="0",
                    credentials_name="0",
                ),
                groups=tiledb.cloud.rest_api.models.storage_location.StorageLocation(
                    path="0",
                    credentials_name="0",
                ),
                ml_models=tiledb.cloud.rest_api.models.storage_location.StorageLocation(
                    path="0",
                    credentials_name="0",
                ),
                notebooks=tiledb.cloud.rest_api.models.storage_location.StorageLocation(
                    path="0",
                    credentials_name="0",
                ),
                task_graphs=tiledb.cloud.rest_api.models.storage_location.StorageLocation(
                    path="0",
                    credentials_name="0",
                ),
                udfs=tiledb.cloud.rest_api.models.storage_location.StorageLocation(
                    path="0",
                    credentials_name="0",
                ),
            )
        else:
            return AssetLocations()

    def testAssetLocations(self):
        """Test AssetLocations"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
