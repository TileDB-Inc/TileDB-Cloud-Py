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
from tiledb.cloud.rest_api.models.notebook_favorite import (  # noqa: E501
    NotebookFavorite,
)
from tiledb.cloud.rest_api.rest import ApiException


class TestNotebookFavorite(unittest.TestCase):
    """NotebookFavorite unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test NotebookFavorite
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.notebook_favorite.NotebookFavorite()  # noqa: E501
        if include_optional:
            return NotebookFavorite(notebook_uuid="0", namespace="0", name="0")
        else:
            return NotebookFavorite()

    def testNotebookFavorite(self):
        """Test NotebookFavorite"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
