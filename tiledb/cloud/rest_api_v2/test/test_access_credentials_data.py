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

import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.models.access_credentials_data import (
    AccessCredentialsData,
)  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestAccessCredentialsData(unittest.TestCase):
    """AccessCredentialsData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AccessCredentialsData
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.access_credentials_data.AccessCredentialsData()  # noqa: E501
        if include_optional:
            return AccessCredentialsData(
                credentials=[
                    tiledb.cloud.rest_api.models.access_credential.AccessCredential(
                        name="0",
                        provider="AWS",
                        provider_default=True,
                        created_at=datetime.datetime.strptime(
                            "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                        ),
                        updated_at=datetime.datetime.strptime(
                            "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                        ),
                        credential=tiledb.cloud.rest_api.models.access_credential_credential.AccessCredential_credential(
                            aws=tiledb.cloud.rest_api.models.aws_credential.AWSCredential(
                                access_key_id="0",
                                secret_access_key="0",
                                endpoint="https://example.us-west-2.amazonaws.com",
                            ),
                            azure=tiledb.cloud.rest_api.models.azure_credential.AzureCredential(
                                account_name="0",
                                account_key="0",
                            ),
                        ),
                        role=tiledb.cloud.rest_api.models.access_credential_role.AccessCredential_role(),
                    )
                ],
                pagination_metadata=tiledb.cloud.rest_api.models.pagination_metadata.PaginationMetadata(
                    page=1.0,
                    per_page=10.0,
                    total_pages=14.0,
                    total_items=138.0,
                ),
            )
        else:
            return AccessCredentialsData()

    def testAccessCredentialsData(self):
        """Test AccessCredentialsData"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
