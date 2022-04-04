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
from tiledb.cloud.rest_api.models.group_info import GroupInfo  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestGroupInfo(unittest.TestCase):
    """GroupInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test GroupInfo
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.group_info.GroupInfo()  # noqa: E501
        if include_optional:
            return GroupInfo(
                id="00000000-0000-0000-0000-000000000000",
                namespace="user1",
                name="myarray1",
                description="0",
                uri="s3://bucket/asset",
                tiledb_uri="0",
                asset_count=12.0,
                group_count=4.0,
                size=16.0,
                last_accessed=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                allowed_actions=["read"],
                logo="0",
                access_credentials_name="0",
                share_count=1.337,
                public_share=True,
                tags=["0"],
                license_id="0",
                license_text="0",
            )
        else:
            return GroupInfo()

    def testGroupInfo(self):
        """Test GroupInfo"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
