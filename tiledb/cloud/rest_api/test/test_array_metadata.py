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
from tiledb.cloud.rest_api.models.array_metadata import ArrayMetadata  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestArrayMetadata(unittest.TestCase):
    """ArrayMetadata unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ArrayMetadata
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.array_metadata.ArrayMetadata()  # noqa: E501
        if include_optional:
            return ArrayMetadata(
                entries=[
                    tiledb.cloud.rest_api.models.array_metadata_entry.ArrayMetadataEntry(
                        key="",
                        type="",
                        value_num=56,
                        value=[56],
                        _del=True,
                    )
                ]
            )
        else:
            return ArrayMetadata()

    def testArrayMetadata(self):
        """Test ArrayMetadata"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
