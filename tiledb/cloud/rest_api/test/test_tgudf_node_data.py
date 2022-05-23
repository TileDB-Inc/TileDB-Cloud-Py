"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.model.result_format import ResultFormat
from tiledb.cloud.rest_api.model.tgudf_argument import TGUDFArgument
from tiledb.cloud.rest_api.model.tgudf_environment import TGUDFEnvironment

globals()["ResultFormat"] = ResultFormat
globals()["TGUDFArgument"] = TGUDFArgument
globals()["TGUDFEnvironment"] = TGUDFEnvironment
from tiledb.cloud.rest_api.model.tgudf_node_data import TGUDFNodeData


class TestTGUDFNodeData(unittest.TestCase):
    """TGUDFNodeData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTGUDFNodeData(self):
        """Test TGUDFNodeData"""
        # FIXME: construct object with mandatory attributes with example values
        # model = TGUDFNodeData()  # noqa: E501
        pass


if __name__ == "__main__":
    unittest.main()
