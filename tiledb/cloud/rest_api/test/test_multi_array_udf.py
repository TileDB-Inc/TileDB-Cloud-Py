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
from tiledb.cloud.rest_api.models.multi_array_udf import MultiArrayUDF  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestMultiArrayUDF(unittest.TestCase):
    """MultiArrayUDF unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test MultiArrayUDF
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.multi_array_udf.MultiArrayUDF()  # noqa: E501
        if include_optional:
            return MultiArrayUDF(
                udf_info_name="TileDB-Inc/quickstart_median",
                language="python",
                version="0",
                image_name="0",
                _exec="0",
                exec_raw="0",
                result_format="native",
                task_name="0",
                argument="0",
                stored_param_uuids=["0"],
                store_results=True,
                dont_download_results=True,
                ranges=tiledb.cloud.rest_api.models.query_ranges.QueryRanges(
                    layout="row-major",
                    ranges=[[1.337]],
                ),
                subarray=tiledb.cloud.rest_api.models.udf_subarray.UDFSubarray(
                    layout="row-major",
                    ranges=[
                        tiledb.cloud.rest_api.models.udf_subarray_range.UDFSubarrayRange(
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
                    ],
                ),
                buffers=["0"],
                arrays=[
                    tiledb.cloud.rest_api.models.udf_array_details.UDFArrayDetails(
                        uri="0",
                        ranges=tiledb.cloud.rest_api.models.query_ranges.QueryRanges(
                            layout="row-major",
                        ),
                        buffers=["0"],
                    )
                ],
                timeout=56,
            )
        else:
            return MultiArrayUDF()

    def testMultiArrayUDF(self):
        """Test MultiArrayUDF"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
