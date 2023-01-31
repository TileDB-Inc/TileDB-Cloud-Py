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
from tiledb.cloud.rest_api.models.tgudf_node_data import TGUDFNodeData  # noqa: E501
from tiledb.cloud.rest_api.rest import ApiException


class TestTGUDFNodeData(unittest.TestCase):
    """TGUDFNodeData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TGUDFNodeData
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.tgudf_node_data.TGUDFNodeData()  # noqa: E501
        if include_optional:
            return TGUDFNodeData(
                registered_udf_name="0",
                executable_code="0",
                source_text="0",
                environment=tiledb.cloud.rest_api.models.tgudf_environment.TGUDFEnvironment(
                    language="python",
                    language_version="0",
                    image_name="0",
                    namespace="0",
                    resource_class="0",
                    resources=tiledb.cloud.rest_api.models.tgudf_environment_resources.TGUDFEnvironment_resources(
                        cpu="500m",
                        memory="8Gi",
                    ),
                    run_client_side=True,
                ),
                arguments=[
                    tiledb.cloud.rest_api.models.tgudf_argument.TGUDFArgument(
                        name="0",
                        value=tiledb.cloud.rest_api.models.tg_arg_value.TGArgValue(),
                    )
                ],
                result_format="python_pickle",
            )
        else:
            return TGUDFNodeData()

    def testTGUDFNodeData(self):
        """Test TGUDFNodeData"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
