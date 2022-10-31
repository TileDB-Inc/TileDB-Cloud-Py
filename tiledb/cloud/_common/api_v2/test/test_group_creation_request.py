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
from tiledb.cloud._common.api_v2.models.group_creation_request import (  # noqa: E501
    GroupCreationRequest,
)
from tiledb.cloud._common.api_v2.rest import ApiException


class TestGroupCreationRequest(unittest.TestCase):
    """GroupCreationRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test GroupCreationRequest
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud._common.api_v2.models.group_creation_request.GroupCreationRequest()  # noqa: E501
        if include_optional:
            return GroupCreationRequest(
                config=tiledb.cloud._common.api_v2.models.tile_db_config.TileDBConfig(
                    entries=[
                        tiledb.cloud._common.api_v2.models.tile_db_config_entries.TileDBConfig_entries(
                            key="0",
                            value="0",
                        )
                    ],
                ),
                group_details=tiledb.cloud._common.api_v2.models.group_creation_request_group_details.GroupCreationRequest_group_details(
                    description="0",
                    name="0",
                    uri="0",
                    logo="0",
                    tags=["0"],
                    license_id="0",
                    license_text="0",
                ),
            )
        else:
            return GroupCreationRequest(
                group_details=tiledb.cloud._common.api_v2.models.group_creation_request_group_details.GroupCreationRequest_group_details(
                    description="0",
                    name="0",
                    uri="0",
                    logo="0",
                    tags=["0"],
                    license_id="0",
                    license_text="0",
                ),
            )

    def testGroupCreationRequest(self):
        """Test GroupCreationRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
