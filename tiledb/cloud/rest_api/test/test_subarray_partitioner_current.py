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
from tiledb.cloud.rest_api.models.subarray_partitioner_current import SubarrayPartitionerCurrent  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestSubarrayPartitionerCurrent(unittest.TestCase):
    """SubarrayPartitionerCurrent unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SubarrayPartitionerCurrent
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.subarray_partitioner_current.SubarrayPartitionerCurrent()  # noqa: E501
        if include_optional:
            return SubarrayPartitionerCurrent(
                subarray=tiledb.cloud.rest_api.models.subarray.Subarray(
                    layout="row-major",
                    ranges=[
                        tiledb.cloud.rest_api.models.subarray_ranges.SubarrayRanges(
                            type="INT32",
                            has_default_range=True,
                            buffer=[56],
                        )
                    ],
                ),
                start=56,
                end=56,
                split_multi_range=True,
            )
        else:
            return SubarrayPartitionerCurrent()

    def testSubarrayPartitionerCurrent(self):
        """Test SubarrayPartitionerCurrent"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
