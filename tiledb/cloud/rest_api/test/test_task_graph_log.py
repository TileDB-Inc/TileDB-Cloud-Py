"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import tiledb.cloud.rest_api
from tiledb.cloud.rest_api.model.task_graph_log_status import TaskGraphLogStatus
from tiledb.cloud.rest_api.model.task_graph_node_metadata import TaskGraphNodeMetadata

globals()["TaskGraphLogStatus"] = TaskGraphLogStatus
globals()["TaskGraphNodeMetadata"] = TaskGraphNodeMetadata
from tiledb.cloud.rest_api.model.task_graph_log import TaskGraphLog


class TestTaskGraphLog(unittest.TestCase):
    """TaskGraphLog unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTaskGraphLog(self):
        """Test TaskGraphLog"""
        # FIXME: construct object with mandatory attributes with example values
        # model = TaskGraphLog()  # noqa: E501
        pass


if __name__ == "__main__":
    unittest.main()
