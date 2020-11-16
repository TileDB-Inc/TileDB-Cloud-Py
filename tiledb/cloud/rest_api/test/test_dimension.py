# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.1.1
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import rest_api
from tiledb.cloud.rest_api.models.dimension import Dimension  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException

class TestDimension(unittest.TestCase):
    """Dimension unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Dimension
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = tiledb.cloud.rest_api.models.dimension.Dimension()  # noqa: E501
        if include_optional :
            return Dimension(
                name = 'row', 
                type = 'INT32', 
                domain = tiledb.cloud.rest_api.models.domain_array.DomainArray(
                    int8 = [
                        56
                        ], 
                    uint8 = [
                        56
                        ], 
                    int16 = [
                        56
                        ], 
                    uint16 = [
                        56
                        ], 
                    int32 = [
                        56
                        ], 
                    uint32 = [
                        56
                        ], 
                    int64 = [
                        56
                        ], 
                    uint64 = [
                        56
                        ], 
                    float32 = [
                        1.337
                        ], 
                    float64 = [
                        1.337
                        ], ), 
                null_tile_extent = True, 
                tile_extent = tiledb.cloud.rest_api.models.dimension_tile_extent.Dimension_tileExtent(
                    int8 = 56, 
                    uint8 = 56, 
                    int16 = 56, 
                    uint16 = 56, 
                    int32 = 56, 
                    uint32 = 56, 
                    int64 = 56, 
                    uint64 = 56, 
                    float32 = 56, 
                    float64 = 56, ), 
                filter_pipeline = tiledb.cloud.rest_api.models.filter_pipeline.FilterPipeline(
                    filters = [
                        tiledb.cloud.rest_api.models.filter.Filter(
                            type = 'FILTER_NONE', 
                            data = tiledb.cloud.rest_api.models.filter_data.Filter_data(
                                int8 = 56, 
                                uint8 = 56, 
                                int16 = 56, 
                                uint16 = 56, 
                                int32 = 56, 
                                uint32 = 56, 
                                int64 = 56, 
                                uint64 = 56, 
                                float32 = 56, 
                                float64 = 56, ), )
                        ], )
            )
        else :
            return Dimension(
                type = 'INT32',
                domain = tiledb.cloud.rest_api.models.domain_array.DomainArray(
                    int8 = [
                        56
                        ], 
                    uint8 = [
                        56
                        ], 
                    int16 = [
                        56
                        ], 
                    uint16 = [
                        56
                        ], 
                    int32 = [
                        56
                        ], 
                    uint32 = [
                        56
                        ], 
                    int64 = [
                        56
                        ], 
                    uint64 = [
                        56
                        ], 
                    float32 = [
                        1.337
                        ], 
                    float64 = [
                        1.337
                        ], ),
                null_tile_extent = True,
        )

    def testDimension(self):
        """Test Dimension"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
