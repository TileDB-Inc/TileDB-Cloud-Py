"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.model.array_info import ArrayInfo
from tiledb.cloud.rest_api.model.pagination_metadata import PaginationMetadata

globals()["ArrayInfo"] = ArrayInfo
globals()["PaginationMetadata"] = PaginationMetadata
from tiledb.cloud.rest_api.model.array_favorites_data import ArrayFavoritesData


class TestArrayFavoritesData(unittest.TestCase):
    """ArrayFavoritesData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testArrayFavoritesData(self):
        """Test ArrayFavoritesData"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ArrayFavoritesData()  # noqa: E501
        pass


if __name__ == "__main__":
    unittest.main()
