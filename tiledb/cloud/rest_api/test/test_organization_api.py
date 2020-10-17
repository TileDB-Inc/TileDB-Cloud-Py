# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.0.13
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import rest_api
from tiledb.cloud.rest_api.api.organization_api import OrganizationApi  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestOrganizationApi(unittest.TestCase):
    """OrganizationApi unit test stubs"""

    def setUp(self):
        self.api = (
            tiledb.cloud.rest_api.api.organization_api.OrganizationApi()
        )  # noqa: E501

    def tearDown(self):
        pass

    def test_add_aws_access_credentials(self):
        """Test case for add_aws_access_credentials"""
        pass

    def test_add_user_to_organization(self):
        """Test case for add_user_to_organization"""
        pass

    def test_check_aws_access_credentials(self):
        """Test case for check_aws_access_credentials"""
        pass

    def test_check_aws_access_credentials_by_name(self):
        """Test case for check_aws_access_credentials_by_name"""
        pass

    def test_create_organization(self):
        """Test case for create_organization"""
        pass

    def test_delete_aws_access_credentials(self):
        """Test case for delete_aws_access_credentials"""
        pass

    def test_delete_organization(self):
        """Test case for delete_organization"""
        pass

    def test_delete_user_from_organization(self):
        """Test case for delete_user_from_organization"""
        pass

    def test_get_all_organizations(self):
        """Test case for get_all_organizations"""
        pass

    def test_get_organization(self):
        """Test case for get_organization"""
        pass

    def test_get_organization_user(self):
        """Test case for get_organization_user"""
        pass

    def test_update_aws_access_credentials(self):
        """Test case for update_aws_access_credentials"""
        pass

    def test_update_organization(self):
        """Test case for update_organization"""
        pass

    def test_update_user_in_organization(self):
        """Test case for update_user_in_organization"""
        pass


if __name__ == "__main__":
    unittest.main()
