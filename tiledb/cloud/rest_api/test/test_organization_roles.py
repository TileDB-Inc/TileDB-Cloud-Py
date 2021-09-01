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
from tiledb.cloud.rest_api.models.organization_roles import (
    OrganizationRoles,
)  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestOrganizationRoles(unittest.TestCase):
    """OrganizationRoles unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test OrganizationRoles
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.organization_roles.OrganizationRoles()  # noqa: E501
        if include_optional:
            return OrganizationRoles()
        else:
            return OrganizationRoles()

    def testOrganizationRoles(self):
        """Test OrganizationRoles"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
