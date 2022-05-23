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
from tiledb.cloud.rest_api.models.group_entry import GroupEntry  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestGroupEntry(unittest.TestCase):
    """GroupEntry unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test GroupEntry
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.group_entry.GroupEntry()  # noqa: E501
        if include_optional:
            return GroupEntry(
                group=tiledb.cloud.rest_api.models.group_info.GroupInfo(
                    id="00000000-0000-0000-0000-000000000000",
                    namespace="user1",
                    name="myarray1",
                    description="",
                    uri="s3://bucket/asset",
                    tiledb_uri="",
                    asset_count=12.0,
                    group_count=4.0,
                    size=16.0,
                    last_accessed=datetime.datetime.strptime(
                        "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                    ),
                    allowed_actions=["read"],
                    logo="",
                    access_credentials_name="",
                    share_count=1.337,
                    public_share=True,
                    tags=[""],
                    license_id="",
                    license_text="",
                ),
                array=tiledb.cloud.rest_api.models.array_info.ArrayInfo(
                    id="00000000-0000-0000-0000-000000000000",
                    file_type="notebook",
                    file_properties={"key": ""},
                    uri="s3://bucket/array",
                    namespace="user1",
                    size=1024.0,
                    last_accessed=datetime.datetime.strptime(
                        "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                    ),
                    description="",
                    name="myarray1",
                    allowed_actions=["read"],
                    pricing=[
                        tiledb.cloud.rest_api.models.pricing.Pricing(
                            id="planID",
                            array_uuid="00000000-0000-0000-0000-000000000000",
                            pricing_name="",
                            pricing_type="egress",
                            product_name="",
                            product_statement_descriptor="",
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
                    logo="",
                    access_credentials_name="",
                    type="sparse",
                    share_count=1.337,
                    public_share=True,
                    namespace_subscribed=False,
                    tiledb_uri="",
                    tags=[""],
                    license_id="",
                    license_text="",
                    read_only=False,
                    is_favorite=True,
                ),
            )
        else:
            return GroupEntry()

    def testGroupEntry(self):
        """Test GroupEntry"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
