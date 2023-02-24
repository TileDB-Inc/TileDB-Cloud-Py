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
from tiledb.cloud.rest_api.models.array_activity_log import (  # noqa: E501
    ArrayActivityLog,
)
from tiledb.cloud.rest_api.rest import ApiException


class TestArrayActivityLog(unittest.TestCase):
    """ArrayActivityLog unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ArrayActivityLog
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # model = tiledb.cloud.rest_api.models.array_activity_log.ArrayActivityLog()  # noqa: E501
        if include_optional:
            return ArrayActivityLog(
                event_at=datetime.datetime.strptime(
                    "2013-10-20 19:20:30.00", "%Y-%m-%d %H:%M:%S.%f"
                ),
                action="read_schema",
                username="user1",
                bytes_sent=1073741824,
                bytes_received=1073741824,
                array_task_id="00000000-0000-0000-0000-000000000000",
                id="00000000-0000-0000-0000-000000000000",
                query_ranges='{"rows":[{"start": 1, "end": 1},{"start": 3, "end": 4}],"cols":[{"start": 1, "end": 4}]}',
                query_stats='{"timers": {"Context.StorageManager.read_load_array_schema_from_uri.sum": 0.0255293, "...": "..."}, "counters": {"Context.StorageManager.read_unfiltered_byte_num": 191, "...": "..."}}',
            )
        else:
            return ArrayActivityLog()

    def testArrayActivityLog(self):
        """Test ArrayActivityLog"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()