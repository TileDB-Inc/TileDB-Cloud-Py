# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import tiledb.cloud.rest_api_v2
from tiledb.cloud.rest_api_v2.api.organization_api import OrganizationApi  # noqa: E501
from tiledb.cloud.rest_api_v2.rest import ApiException


class TestOrganizationApi(unittest.TestCase):
    """OrganizationApi unit test stubs"""

    def setUp(self):
        self.api = tiledb.cloud.rest_api_v2.api.organization_api.OrganizationApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_credential(self):
        """Test case for add_credential

        """
        pass

    def test_delete_credential(self):
        """Test case for delete_credential

        """
        pass

    def test_get_credential(self):
        """Test case for get_credential

        """
        pass

    def test_list_credentials(self):
        """Test case for list_credentials

        """
        pass

    def test_update_credential(self):
        """Test case for update_credential

        """
        pass


if __name__ == '__main__':
    unittest.main()
