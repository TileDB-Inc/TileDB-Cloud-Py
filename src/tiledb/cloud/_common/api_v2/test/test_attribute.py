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
from tiledb.cloud._common.api_v2.models.attribute import Attribute  # noqa: E501
from tiledb.cloud._common.api_v2.rest import ApiException


class TestAttribute(unittest.TestCase):
    """Attribute unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Attribute
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud._common.api_v2.models.attribute.Attribute()  # noqa: E501
        if include_optional:
            return Attribute(
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
        else:
            return Attribute(
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
            )

    def testAttribute(self):
        """Test Attribute"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()