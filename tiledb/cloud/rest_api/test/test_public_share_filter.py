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
from tiledb.cloud.rest_api.models.public_share_filter import PublicShareFilter  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestPublicShareFilter(unittest.TestCase):
    """PublicShareFilter unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PublicShareFilter
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.public_share_filter.PublicShareFilter()  # noqa: E501
        if include_optional:
            return PublicShareFilter()
        else:
            return PublicShareFilter()

    def testPublicShareFilter(self):
        """Test PublicShareFilter"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
