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
from tiledb.cloud.rest_api.models.tgudf_environment import (  # noqa: E501
    TGUDFEnvironment,
)
from tiledb.cloud.rest_api.rest import ApiException


class TestTGUDFEnvironment(unittest.TestCase):
    """TGUDFEnvironment unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TGUDFEnvironment
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.tgudf_environment.TGUDFEnvironment()  # noqa: E501
        if include_optional:
            return TGUDFEnvironment(
                language="python",
                language_version="0",
                image_name="0",
                resource_class="0",
            )
        else:
            return TGUDFEnvironment()

    def testTGUDFEnvironment(self):
        """Test TGUDFEnvironment"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
