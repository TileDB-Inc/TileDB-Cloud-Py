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

import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.models.pagination_metadata import (
    PaginationMetadata,
)  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestPaginationMetadata(unittest.TestCase):
    """PaginationMetadata unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PaginationMetadata
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.pagination_metadata.PaginationMetadata()  # noqa: E501
        if include_optional:
            return PaginationMetadata(
                page=1.0, per_page=10.0, total_pages=14.0, total_items=138.0
            )
        else:
            return PaginationMetadata()

    def testPaginationMetadata(self):
        """Test PaginationMetadata"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
