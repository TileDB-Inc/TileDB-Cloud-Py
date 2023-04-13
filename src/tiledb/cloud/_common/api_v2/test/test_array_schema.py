# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import datetime
import unittest

import tiledb.cloud._common.api_v2
from tiledb.cloud._common.api_v2.models.array_schema import ArraySchema  # noqa: E501
from tiledb.cloud._common.api_v2.rest import ApiException


class TestArraySchema(unittest.TestCase):
    """ArraySchema unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ArraySchema
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud._common.api_v2.models.array_schema.ArraySchema()  # noqa: E501
        if include_optional:
            return ArraySchema(
                uri="s3://<bucket>/test_array",
                name="0",
                version=[1, 3, 0],
                array_type="dense",
                tile_order="row-major",
                cell_order="row-major",
                capacity=100000,
                coords_filter_pipeline=tiledb.cloud._common.api_v2.models.filter_pipeline.FilterPipeline(
                    filters=[
                        tiledb.cloud._common.api_v2.models.filter.Filter(
                            type="FILTER_NONE",
                            float_scale_config=tiledb.cloud._common.api_v2.models.float_scale_config.FloatScaleConfig(
                                scale=56,
                                offset=56,
                                byte_width=56,
                            ),
                            data=tiledb.cloud._common.api_v2.models.filter_data.Filter_data(
                                text="0",
                                bytes=[56],
                                int8=56,
                                uint8=56,
                                int16=56,
                                uint16=56,
                                int32=56,
                                uint32=56,
                                int64=56,
                                uint64=56,
                                float32=56,
                                float64=56,
                            ),
                        )
                    ],
                ),
                offset_filter_pipeline=tiledb.cloud._common.api_v2.models.filter_pipeline.FilterPipeline(
                    filters=[
                        tiledb.cloud._common.api_v2.models.filter.Filter(
                            type="FILTER_NONE",
                            float_scale_config=tiledb.cloud._common.api_v2.models.float_scale_config.FloatScaleConfig(
                                scale=56,
                                offset=56,
                                byte_width=56,
                            ),
                            data=tiledb.cloud._common.api_v2.models.filter_data.Filter_data(
                                text="0",
                                bytes=[56],
                                int8=56,
                                uint8=56,
                                int16=56,
                                uint16=56,
                                int32=56,
                                uint32=56,
                                int64=56,
                                uint64=56,
                                float32=56,
                                float64=56,
                            ),
                        )
                    ],
                ),
                validity_filter_pipeline=tiledb.cloud._common.api_v2.models.filter_pipeline.FilterPipeline(
                    filters=[
                        tiledb.cloud._common.api_v2.models.filter.Filter(
                            type="FILTER_NONE",
                            float_scale_config=tiledb.cloud._common.api_v2.models.float_scale_config.FloatScaleConfig(
                                scale=56,
                                offset=56,
                                byte_width=56,
                            ),
                            data=tiledb.cloud._common.api_v2.models.filter_data.Filter_data(
                                text="0",
                                bytes=[56],
                                int8=56,
                                uint8=56,
                                int16=56,
                                uint16=56,
                                int32=56,
                                uint32=56,
                                int64=56,
                                uint64=56,
                                float32=56,
                                float64=56,
                            ),
                        )
                    ],
                ),
                domain=tiledb.cloud._common.api_v2.models.domain.Domain(
                    type="INT32",
                    tile_order="row-major",
                    cell_order="row-major",
                    dimensions=[
                        tiledb.cloud._common.api_v2.models.dimension.Dimension(
                            name="row",
                            type="INT32",
                            domain=tiledb.cloud._common.api_v2.models.domain_array.DomainArray(
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
                            null_tile_extent=True,
                            tile_extent=tiledb.cloud._common.api_v2.models.dimension_tile_extent.Dimension_tileExtent(),
                            filter_pipeline=tiledb.cloud._common.api_v2.models.filter_pipeline.FilterPipeline(
                                filters=[
                                    tiledb.cloud._common.api_v2.models.filter.Filter(
                                        type="FILTER_NONE",
                                        float_scale_config=tiledb.cloud._common.api_v2.models.float_scale_config.FloatScaleConfig(
                                            scale=56,
                                            offset=56,
                                            byte_width=56,
                                        ),
                                        data=tiledb.cloud._common.api_v2.models.filter_data.Filter_data(
                                            text="0",
                                            bytes=[56],
                                        ),
                                    )
                                ],
                            ),
                        )
                    ],
                ),
                attributes=[
                    tiledb.cloud._common.api_v2.models.attribute.Attribute(
                        name="attribute1",
                        type="INT32",
                        filter_pipeline=tiledb.cloud._common.api_v2.models.filter_pipeline.FilterPipeline(
                            filters=[
                                tiledb.cloud._common.api_v2.models.filter.Filter(
                                    type="FILTER_NONE",
                                    float_scale_config=tiledb.cloud._common.api_v2.models.float_scale_config.FloatScaleConfig(
                                        scale=56,
                                        offset=56,
                                        byte_width=56,
                                    ),
                                    data=tiledb.cloud._common.api_v2.models.filter_data.Filter_data(
                                        text="0",
                                        bytes=[56],
                                        int8=56,
                                        uint8=56,
                                        int16=56,
                                        uint16=56,
                                        int32=56,
                                        uint32=56,
                                        int64=56,
                                        uint64=56,
                                        float32=56,
                                        float64=56,
                                    ),
                                )
                            ],
                        ),
                        cell_val_num=1,
                        nullable=True,
                        fill_value_validity=True,
                        fill_value=[56],
                    )
                ],
                allows_duplicates=True,
                timestamp_range=[56],
            )
        else:
            return ArraySchema(
                version=[1, 3, 0],
                array_type="dense",
                tile_order="row-major",
                cell_order="row-major",
                capacity=100000,
                coords_filter_pipeline=tiledb.cloud._common.api_v2.models.filter_pipeline.FilterPipeline(
                    filters=[
                        tiledb.cloud._common.api_v2.models.filter.Filter(
                            type="FILTER_NONE",
                            float_scale_config=tiledb.cloud._common.api_v2.models.float_scale_config.FloatScaleConfig(
                                scale=56,
                                offset=56,
                                byte_width=56,
                            ),
                            data=tiledb.cloud._common.api_v2.models.filter_data.Filter_data(
                                text="0",
                                bytes=[56],
                                int8=56,
                                uint8=56,
                                int16=56,
                                uint16=56,
                                int32=56,
                                uint32=56,
                                int64=56,
                                uint64=56,
                                float32=56,
                                float64=56,
                            ),
                        )
                    ],
                ),
                offset_filter_pipeline=tiledb.cloud._common.api_v2.models.filter_pipeline.FilterPipeline(
                    filters=[
                        tiledb.cloud._common.api_v2.models.filter.Filter(
                            type="FILTER_NONE",
                            float_scale_config=tiledb.cloud._common.api_v2.models.float_scale_config.FloatScaleConfig(
                                scale=56,
                                offset=56,
                                byte_width=56,
                            ),
                            data=tiledb.cloud._common.api_v2.models.filter_data.Filter_data(
                                text="0",
                                bytes=[56],
                                int8=56,
                                uint8=56,
                                int16=56,
                                uint16=56,
                                int32=56,
                                uint32=56,
                                int64=56,
                                uint64=56,
                                float32=56,
                                float64=56,
                            ),
                        )
                    ],
                ),
                domain=tiledb.cloud._common.api_v2.models.domain.Domain(
                    type="INT32",
                    tile_order="row-major",
                    cell_order="row-major",
                    dimensions=[
                        tiledb.cloud._common.api_v2.models.dimension.Dimension(
                            name="row",
                            type="INT32",
                            domain=tiledb.cloud._common.api_v2.models.domain_array.DomainArray(
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
                            null_tile_extent=True,
                            tile_extent=tiledb.cloud._common.api_v2.models.dimension_tile_extent.Dimension_tileExtent(),
                            filter_pipeline=tiledb.cloud._common.api_v2.models.filter_pipeline.FilterPipeline(
                                filters=[
                                    tiledb.cloud._common.api_v2.models.filter.Filter(
                                        type="FILTER_NONE",
                                        float_scale_config=tiledb.cloud._common.api_v2.models.float_scale_config.FloatScaleConfig(
                                            scale=56,
                                            offset=56,
                                            byte_width=56,
                                        ),
                                        data=tiledb.cloud._common.api_v2.models.filter_data.Filter_data(
                                            text="0",
                                            bytes=[56],
                                        ),
                                    )
                                ],
                            ),
                        )
                    ],
                ),
                attributes=[
                    tiledb.cloud._common.api_v2.models.attribute.Attribute(
                        name="attribute1",
                        type="INT32",
                        filter_pipeline=tiledb.cloud._common.api_v2.models.filter_pipeline.FilterPipeline(
                            filters=[
                                tiledb.cloud._common.api_v2.models.filter.Filter(
                                    type="FILTER_NONE",
                                    float_scale_config=tiledb.cloud._common.api_v2.models.float_scale_config.FloatScaleConfig(
                                        scale=56,
                                        offset=56,
                                        byte_width=56,
                                    ),
                                    data=tiledb.cloud._common.api_v2.models.filter_data.Filter_data(
                                        text="0",
                                        bytes=[56],
                                        int8=56,
                                        uint8=56,
                                        int16=56,
                                        uint16=56,
                                        int32=56,
                                        uint32=56,
                                        int64=56,
                                        uint64=56,
                                        float32=56,
                                        float64=56,
                                    ),
                                )
                            ],
                        ),
                        cell_val_num=1,
                        nullable=True,
                        fill_value_validity=True,
                        fill_value=[56],
                    )
                ],
            )

    def testArraySchema(self):
        """Test ArraySchema"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
