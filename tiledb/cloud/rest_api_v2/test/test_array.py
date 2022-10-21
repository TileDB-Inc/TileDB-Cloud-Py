# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import tiledb.cloud.rest_api_v2
from tiledb.cloud.rest_api_v2.models.array import Array  # noqa: E501
from tiledb.cloud.rest_api_v2.rest import ApiException

class TestArray(unittest.TestCase):
    """Array unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Array
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = tiledb.cloud.rest_api_v2.models.array.Array()  # noqa: E501
        if include_optional :
            return Array(
                timestamp = 1540471791873, 
                query_type = 'READ', 
                uri = '0'
            )
        else :
            return Array(
                timestamp = 1540471791873,
                query_type = 'READ',
                uri = '0',
        )

    def testArray(self):
        """Test Array"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
