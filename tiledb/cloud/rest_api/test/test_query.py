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
from tiledb.cloud.rest_api.models.query import Query  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestQuery(unittest.TestCase):
    """Query unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Query
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.query.Query()  # noqa: E501
        if include_optional:
            return Query(
                type="READ",
                layout="row-major",
                status="FAILED",
                attribute_buffer_headers=[
                    tiledb.cloud.rest_api.models.attribute_buffer_header.AttributeBufferHeader(
                        name="attribute1",
                        fixed_len_buffer_size_in_bytes=56,
                        var_len_buffer_size_in_bytes=56,
                    )
                ],
                writer=tiledb.cloud.rest_api.models.writer.Writer(
                    check_coord_dups=True,
                    check_coord_oob=True,
                    dedup_coords=True,
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
                ),
                reader=tiledb.cloud.rest_api.models.query_reader.QueryReader(
                    layout="row-major",
                    subarray=tiledb.cloud.rest_api.models.subarray.Subarray(
                        ranges=[
                            tiledb.cloud.rest_api.models.subarray_ranges.SubarrayRanges(
                                type="INT32",
                                has_default_range=True,
                                buffer=[56],
                            )
                        ],
                    ),
                    read_state=tiledb.cloud.rest_api.models.read_state.ReadState(
                        initialized=True,
                        overflowed=True,
                        unsplittable=True,
                        subarray_partitioner=tiledb.cloud.rest_api.models.subarray_partitioner.SubarrayPartitioner(
                            budget=[
                                tiledb.cloud.rest_api.models.attribute_buffer_size.AttributeBufferSize(
                                    attribute="0",
                                    offset_bytes=56,
                                    data_bytes=56,
                                )
                            ],
                            current=tiledb.cloud.rest_api.models.subarray_partitioner_current.SubarrayPartitioner_current(
                                start=56,
                                end=56,
                                split_multi_range=True,
                            ),
                            state=tiledb.cloud.rest_api.models.subarray_partitioner_state.SubarrayPartitioner_state(
                                start=56,
                                end=56,
                                single_range=[
                                    tiledb.cloud.rest_api.models.subarray.Subarray()
                                ],
                                multi_range=[
                                    tiledb.cloud.rest_api.models.subarray.Subarray()
                                ],
                            ),
                            memory_budget=56,
                            memory_budget_var=56,
                        ),
                    ),
                    var_offsets_mode="0",
                    var_offsets_add_extra_element=True,
                    var_offsets_bitsize=56,
                ),
                array=tiledb.cloud.rest_api.models.array.Array(
                    timestamp=1540471791873,
                    query_type="READ",
                    uri="0",
                ),
                total_fixed_length_buffer_bytes=56,
                total_var_len_buffer_bytes=56,
            )
        else:
            return Query(
                type="READ",
                layout="row-major",
                status="FAILED",
                attribute_buffer_headers=[
                    tiledb.cloud.rest_api.models.attribute_buffer_header.AttributeBufferHeader(
                        name="attribute1",
                        fixed_len_buffer_size_in_bytes=56,
                        var_len_buffer_size_in_bytes=56,
                    )
                ],
                array=tiledb.cloud.rest_api.models.array.Array(
                    timestamp=1540471791873,
                    query_type="READ",
                    uri="0",
                ),
                total_fixed_length_buffer_bytes=56,
                total_var_len_buffer_bytes=56,
            )

    def testQuery(self):
        """Test Query"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
