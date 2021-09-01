# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import rest_api
from tiledb.cloud.rest_api.models.subscription import Subscription  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestSubscription(unittest.TestCase):
    """Subscription unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Subscription
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.subscription.Subscription()  # noqa: E501
        if include_optional:
            return Subscription(
                id="subscriptionID",
                owner_namespace_uuid="00000000-0000-0000-0000-000000000000",
                customer_namespace_uuid="00000000-0000-0000-0000-000000000000",
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
            )
        else:
            return Subscription()

    def testSubscription(self):
        """Test Subscription"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
