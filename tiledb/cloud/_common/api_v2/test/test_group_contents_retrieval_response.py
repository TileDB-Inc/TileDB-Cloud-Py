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
from tiledb.cloud._common.api_v2.models.group_contents_retrieval_response import (  # noqa: E501
    GroupContentsRetrievalResponse,
)
from tiledb.cloud._common.api_v2.rest import ApiException


class TestGroupContentsRetrievalResponse(unittest.TestCase):
    """GroupContentsRetrievalResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test GroupContentsRetrievalResponse
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud._common.api_v2.models.group_contents_retrieval_response.GroupContentsRetrievalResponse()  # noqa: E501
        if include_optional:
            return GroupContentsRetrievalResponse(
                members=[
                    tiledb.cloud._common.api_v2.models.group_member.GroupMember(
                        name="0",
                        uri="0",
                        type="GROUP",
                    )
                ],
                metadata=tiledb.cloud._common.api_v2.models.metadata.Metadata(
                    entries=[
                        tiledb.cloud._common.api_v2.models.metadata_entry.MetadataEntry(
                            key="0",
                            type="0",
                            value_num=56,
                            value=tiledb.cloud._common.api_v2.models.value.value(),
                            _del=True,
                        )
                    ],
                ),
            )
        else:
            return GroupContentsRetrievalResponse()

    def testGroupContentsRetrievalResponse(self):
        """Test GroupContentsRetrievalResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()