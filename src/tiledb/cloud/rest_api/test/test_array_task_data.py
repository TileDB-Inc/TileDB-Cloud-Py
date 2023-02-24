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
from tiledb.cloud.rest_api.models.array_task_data import ArrayTaskData  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestArrayTaskData(unittest.TestCase):
    """ArrayTaskData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ArrayTaskData
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.array_task_data.ArrayTaskData()  # noqa: E501
        if include_optional:
            return ArrayTaskData(
                array_tasks=[
                    tiledb.cloud.rest_api.models.array_task.ArrayTask(
                        id="0",
                        name="subarray-multiplier",
                        description="Return attr a1 in the subarray bounded by coordinates and multiply attr1 by 2",
                        array_metadata=tiledb.cloud.rest_api.models.array_info.ArrayInfo(
                            id="00000000-0000-0000-0000-000000000000",
                            file_type="notebook",
                            file_properties={"key": "0"},
                            uri="s3://bucket/array",
                            namespace="user1",
                            size=1024.0,
                            last_accessed=datetime.datetime.strptime(
                                "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                            ),
                            description="0",
                            name="myarray1",
                            allowed_actions=["read"],
                            pricing=[
                                tiledb.cloud.rest_api.models.pricing.Pricing(
                                    id="planID",
                                    array_uuid="00000000-0000-0000-0000-000000000000",
                                    pricing_name="0",
                                    pricing_type="egress",
                                    product_name="0",
                                    product_statement_descriptor="0",
                                    product_unit_label="byte",
                                    currency="USD",
                                    aggregate_usage="sum",
                                    interval="month",
                                    divided_by=1048576,
                                    charge=1.337,
                                    activated=False,
                                )
                            ],
                            subscriptions=[
                                tiledb.cloud.rest_api.models.subscription.Subscription(
                                    id="subscriptionID",
                                    owner_namespace_uuid="00000000-0000-0000-0000-000000000000",
                                    customer_namespace_uuid="00000000-0000-0000-0000-000000000000",
                                )
                            ],
                            logo="0",
                            access_credentials_name="0",
                            type="sparse",
                            share_count=1.337,
                            public_share=True,
                            namespace_subscribed=False,
                            tiledb_uri="0",
                            tags=["0"],
                            license_id="0",
                            license_text="0",
                            read_only=False,
                            is_favorite=True,
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
                        memory=1073741824,
                        cpu=4000,
                        namespace="organization1",
                        status="QUEUED",
                        start_time=datetime.datetime.strptime(
                            "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                        ),
                        finish_time=datetime.datetime.strptime(
                            "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                        ),
                        cost=0.12,
                        egress_cost=0.12,
                        access_cost=0.12,
                        query_type="READ",
                        udf_code="0",
                        udf_language="0",
                        sql_query="0",
                        type="SQL",
                        activity=[
                            tiledb.cloud.rest_api.models.array_activity_log.ArrayActivityLog(
                                event_at=datetime.datetime.strptime(
                                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                                ),
                                action="read_schema",
                                username="user1",
                                bytes_sent=1073741824,
                                bytes_received=1073741824,
                                array_task_id="00000000-0000-0000-0000-000000000000",
                                id="00000000-0000-0000-0000-000000000000",
                                query_ranges='{"rows":[{"start": 1, "end": 1},{"start": 3, "end": 4}],"cols":[{"start": 1, "end": 4}]}',
                                query_stats='{"timers": {"Context.StorageManager.read_load_array_schema_from_uri.sum": 0.0255293, "...": "..."}, "counters": {"Context.StorageManager.read_unfiltered_byte_num": 191, "...": "..."}}',
                            )
                        ],
                        logs="0",
                        duration=3.41e11,
                        sql_init_commands=["0"],
                        sql_parameters=[None],
                        result_format="python_pickle",
                        task_graph_uuid="0",
                        client_node_uuid="0",
                    )
                ],
                pagination_metadata=tiledb.cloud.rest_api.models.pagination_metadata.PaginationMetadata(
                    page=1.0,
                    per_page=10.0,
                    total_pages=14.0,
                    total_items=138.0,
                ),
            )
        else:
            return ArrayTaskData()

    def testArrayTaskData(self):
        """Test ArrayTaskData"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()