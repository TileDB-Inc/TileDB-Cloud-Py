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
from tiledb.cloud.rest_api.models.writer import Writer  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestWriter(unittest.TestCase):
    """Writer unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Writer
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.writer.Writer()  # noqa: E501
        if include_optional:
            return Writer(
                check_coord_dups=True,
                check_coord_oob=True,
                dedup_coords=True,
                subarray_ranges=tiledb.cloud.rest_api.models.subarray.Subarray(
                    layout="row-major",
                    ranges=[
                        tiledb.cloud.rest_api.models.subarray_ranges.SubarrayRanges(
                            type="INT32",
                            has_default_range=True,
                            buffer=[56],
                            buffer_sizes=[56],
                            buffer_start_sizes=[56],
                        )
                    ],
                ),
                subarray=tiledb.cloud.rest_api.models.domain_array.DomainArray(
                    int8=[56],
                    uint8=[56],
                    int16=[56],
                    uint16=[56],
                    int32=[56],
                    uint32=[56],
                    int64=[56],
                    uint64=[56],
                    float32=[1.337],
                    float64=[1.337],
                ),
            )
        else:
            return Writer()

    def testWriter(self):
        """Test Writer"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
