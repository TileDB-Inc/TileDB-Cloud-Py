"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.model.array_actions import ArrayActions
from tiledb.cloud.rest_api.model.group_actions import GroupActions

globals()["ArrayActions"] = ArrayActions
globals()["GroupActions"] = GroupActions
from tiledb.cloud.rest_api.model.group_sharing_request import GroupSharingRequest


class TestGroupSharingRequest(unittest.TestCase):
    """GroupSharingRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGroupSharingRequest(self):
        """Test GroupSharingRequest"""
        # FIXME: construct object with mandatory attributes with example values
        # model = GroupSharingRequest()  # noqa: E501
        pass


if __name__ == "__main__":
    unittest.main()
