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
from tiledb.cloud.rest_api.models.array_info_update import ArrayInfoUpdate  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestArrayInfoUpdate(unittest.TestCase):
    """ArrayInfoUpdate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ArrayInfoUpdate
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.array_info_update.ArrayInfoUpdate()  # noqa: E501
        if include_optional:
            return ArrayInfoUpdate(
                description="0",
                name="myarray1",
                uri="s3://bucket/array",
                file_type="notebook",
                file_properties={"key": "0"},
                access_credentials_name="0",
                logo="0",
                tags=["0"],
                license_id="0",
                license_text="0",
                read_only=True,
            )
        else:
            return ArrayInfoUpdate()

    def testArrayInfoUpdate(self):
        """Test ArrayInfoUpdate"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
