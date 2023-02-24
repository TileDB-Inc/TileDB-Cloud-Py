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
from tiledb.cloud.rest_api.models.udf_subarray_range import (  # noqa: E501
    UDFSubarrayRange,
)
from tiledb.cloud.rest_api.rest import ApiException


class TestUDFSubarrayRange(unittest.TestCase):
    """UDFSubarrayRange unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test UDFSubarrayRange
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.udf_subarray_range.UDFSubarrayRange()  # noqa: E501
        if include_optional:
            return UDFSubarrayRange(
                dimension_id=56,
                range_start=tiledb.cloud.rest_api.models.dimension_coordinate.DimensionCoordinate(
                    int8=56,
                    uint8=56,
                    int16=56,
                    uint16=56,
                    int32=56,
                    uint32=56,
                    int64=56,
                    uint64=56,
                    float32=1.337,
                    float64=1.337,
                ),
                range_end=tiledb.cloud.rest_api.models.dimension_coordinate.DimensionCoordinate(
                    int8=56,
                    uint8=56,
                    int16=56,
                    uint16=56,
                    int32=56,
                    uint32=56,
                    int64=56,
                    uint64=56,
                    float32=1.337,
                    float64=1.337,
                ),
            )
        else:
            return UDFSubarrayRange()

    def testUDFSubarrayRange(self):
        """Test UDFSubarrayRange"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()