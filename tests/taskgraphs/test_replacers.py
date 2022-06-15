import unittest
import uuid
from typing import Optional

import attrs

from tiledb.cloud._common import ordered
from tiledb.cloud.taskgraphs.client_executor import _base
from tiledb.cloud.taskgraphs.client_executor import _replacers


class NodeOutputValueReplacerTest(unittest.TestCase):
    def test_no_nodes(self):
        input = {
            "here": "there",
            "up": "down",
            "list": [
                1,
                {
                    "__tdbudf__": "immediate",
                    "format": "json",
                    "base64_data": "Mg==",
                },
                3,
                {
                    "__tdbudf__": "__escape__",
                    "__escape__": {
                        "number": "four",
                        "__tdbudf__": 4,
                    },
                },
            ],
        }
        replacer = _replacers.NodeOutputValueReplacer({})
        output = replacer.visit(input)
        expected = {
            "here": "there",
            "up": "down",
            "list": [1, 2, 3, {"number": "four", "__tdbudf__": 4}],
        }
        self.assertEqual(expected, output)

    def test_nodes(self):
        input = [
            None,
            1,
            {
                "__tdbudf__": "immediate",
                "format": "bytes",
                "base64_data": "dGVzdF9ub2Rlcw==",
            },
            {
                "__tdbudf__": "__escape__",
                "__escape__": {
                    "eights": 888,
                    "__tdbudf__": {
                        "__tdbudf__": "node_output",
                        "client_node_id": "88888888-8888-8888-8888-888888888888",
                    },
                },
            },
        ]
        replacer = _replacers.NodeOutputValueReplacer(
            {
                uuid.UUID("88888888-8888-8888-8888-888888888888"): _TestNode(
                    uuid.UUID("99999999-9999-9999-9999-999999999999")
                ),
            }
        )
        output = replacer.visit(input)
        expected = [
            None,
            1,
            b"test_nodes",
            {
                "eights": 888,
                "__tdbudf__": "result of 99999999-9999-9999-9999-999999999999",
            },
        ]
        self.assertEqual(expected, output)


class UDFParamReplacerTest(unittest.TestCase):
    def test_no_nodes(self):
        input = {
            "here": "there",
            "up": "down",
            "list": [
                {"__tdbudf__": "bogus"},
                {
                    "__tdbudf__": "__escape__",
                    "__escape__": {"__tdbudf__": [True, False]},
                },
            ],
        }
        replacer = _replacers.UDFParamReplacer({}, _base.ParamFormat.STORED_PARAMS)
        output = replacer.visit(input)
        self.assertEqual(input, output)
        self.assertEqual(replacer.seen_nodes, ordered.Set())

    def test_with_nodes(self):
        input = {
            "here": "there",
            "first": {
                "__tdbudf__": "node_output",
                "client_node_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            },
            "second": [
                {
                    "__tdbudf__": "__escape__",
                    "__escape__": {
                        "__tdbudf__": "value",
                        "dont_visit": {
                            "__tdbudf__": "bogus",
                            "value": {"__tdbudf__": "node_output"},
                        },
                        "do_visit": {
                            "__tdbudf__": "node_output",
                            "client_node_id": "00000000-1111-2222-3333-444444444444",
                        },
                    },
                },
            ],
        }

        expected = {
            "here": "there",
            "first": (
                "encoded 55555555-5555-5555-5555-555555555555 "
                "in ParamFormat.STORED_PARAMS"
            ),
            "second": [
                {
                    "__tdbudf__": "__escape__",
                    "__escape__": {
                        "__tdbudf__": "value",
                        "dont_visit": {
                            "__tdbudf__": "bogus",
                            "value": {"__tdbudf__": "node_output"},
                        },
                        "do_visit": (
                            "encoded ffffffff-ffff-ffff-ffff-ffffffffffff "
                            "in ParamFormat.STORED_PARAMS"
                        ),
                    },
                },
            ],
        }
        visitor = _replacers.UDFParamReplacer(
            {
                uuid.UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"): _TestNode(
                    uuid.UUID("55555555-5555-5555-5555-555555555555")
                ),
                uuid.UUID("00000000-1111-2222-3333-444444444444"): _TestNode(
                    uuid.UUID("ffffffff-ffff-ffff-ffff-ffffffffffff")
                ),
            },
            _base.ParamFormat.STORED_PARAMS,
        )
        self.assertEqual(expected, visitor.visit(input))
        self.assertEqual(
            ordered.Set(
                (
                    _TestNode(uuid.UUID("55555555-5555-5555-5555-555555555555")),
                    _TestNode(uuid.UUID("ffffffff-ffff-ffff-ffff-ffffffffffff")),
                )
            ),
            visitor.seen_nodes,
        )

    def test_small(self):
        input = {
            "__tdbudf__": "node_output",
            "client_node_id": "99999999-9999-9999-9999-999999999999",
        }

        visitor = _replacers.UDFParamReplacer(
            {
                uuid.UUID("99999999-9999-9999-9999-999999999999"): _TestNode(
                    uuid.UUID("33333333-3333-3333-3333-333333333333")
                )
            },
            _base.ParamFormat.VALUES,
        )
        expected = "encoded 33333333-3333-3333-3333-333333333333 in ParamFormat.VALUES"
        self.assertEqual(expected, visitor.visit(input))
        self.assertEqual(
            ordered.Set([_TestNode(uuid.UUID("33333333-3333-33333333--333333333333"))]),
            visitor.seen_nodes,
        )


@attrs.define(frozen=True, slots=True)
class _TestNode:
    """A dummy class which implements just what the visitors use."""

    _task_id: Optional[uuid.UUID] = None

    def result(self, timeout=None):
        return f"result of {self._task_id}"

    def _encode_for_param(self, mode):
        return f"encoded {self._task_id} in {mode}"

    def task_id(self):
        return self._task_id
