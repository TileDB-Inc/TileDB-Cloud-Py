# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.api.notebooks_api import NotebooksApi  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestNotebooksApi(unittest.TestCase):
    """NotebooksApi unit test stubs"""

    def setUp(self):
        self.api = tiledb.cloud.rest_api.api.notebooks_api.NotebooksApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_notebooks_namespace_array_end_timestamps_get(self):
        """Test case for notebooks_namespace_array_end_timestamps_get"""
        pass


if __name__ == "__main__":
    unittest.main()
