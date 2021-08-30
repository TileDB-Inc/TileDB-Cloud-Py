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
from tiledb.cloud.rest_api.models.last_accessed_array import (  # noqa: E501
    LastAccessedArray,
)
from tiledb.cloud.rest_api.rest import ApiException


class TestLastAccessedArray(unittest.TestCase):
    """LastAccessedArray unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test LastAccessedArray
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.last_accessed_array.LastAccessedArray()  # noqa: E501
        if include_optional:
            return LastAccessedArray(
                array_id="00000000-0000-0000-0000-000000000000",
                array_name="array1",
                namespace="mockuser",
                accessed_time=1540471791873,
                access_type="read_schema",
            )
        else:
            return LastAccessedArray()

    def testLastAccessedArray(self):
        """Test LastAccessedArray"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
