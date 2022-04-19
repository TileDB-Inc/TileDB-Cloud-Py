import unittest
import uuid
from unittest import mock

from tiledb.cloud import testonly
from tiledb.cloud import utils
from tiledb.cloud.taskgraphs import builder
from tiledb.cloud.taskgraphs import depgraph
from tiledb.cloud.taskgraphs import types


class TestEscaper(unittest.TestCase):
    maxDiff = None

    def test_no_nodes(self):
        cases = [
            ("simple str", "simple str"),
            (
                b"blinding lights",
                {
                    "__tdbudf__": "immediate",
                    "format": "bytes",
                    "base64_data": "YmxpbmRpbmcgbGlnaHRz",
                },
            ),
            (
                {complex(1, 1): "complex"},
                {
                    "__tdbudf__": "immediate",
                    "format": "python_pickle",
                    "base64_data": (
                        "gASVOwAAAAAAAAB9lIwIYnVpbHRpbnOUjAdjb21wbGV4lJOURz/"
                        "wAAAAAAAARz/wAAAAAAAAhpRSlIwHY29tcGxleJRzLg=="
                    ),
                },
            ),
            (
                {"__tdbudf__": "has tdbudf"},
                {
                    "__tdbudf__": "__escape__",
                    "__escape__": {"__tdbudf__": "has tdbudf"},
                },
            ),
        ]
        for inval, expected in cases:
            with self.subTest(inval):
                self._do_test(inval, expected, ())

    def test_sub_nodes(self):
        fake_id = uuid.UUID("6E767267-6F6E-6E61-6776-65796F757570")
        with mock.patch.object(uuid, "uuid4", return_value=fake_id):
            the_node = builder._InputNode("hello", "world")

        self._do_test(
            inval=["one", "two", the_node],
            expected=[
                "one",
                "two",
                {
                    "__tdbudf__": "node_output",
                    "client_node_id": "6e767267-6f6e-6e61-6776-65796f757570",
                },
            ],
            nodes=(the_node,),
        )

    def test_many_nodes(self):
        fake_ids = [
            uuid.UUID("abcdef12-1234-1234-1234-34567890abcd"),
            uuid.UUID("98765432-abcd-abcd-abcd-111111111111"),
        ]
        grf = builder.TaskGraphBuilder()
        with mock.patch.object(uuid, "uuid4", side_effect=fake_ids):
            node_a = grf.input("in_a", "one")
            node_b = grf.udf(len)

        self._do_test(
            inval={
                "__tdbudf__": "this must be escaped",
                "sublist": [node_a, node_a, node_b],
            },
            expected={
                "__tdbudf__": "__escape__",
                "__escape__": {
                    "__tdbudf__": "this must be escaped",
                    "sublist": [
                        {
                            "__tdbudf__": "node_output",
                            "client_node_id": "abcdef12-1234-1234-1234-34567890abcd",
                        },
                        {
                            "__tdbudf__": "node_output",
                            "client_node_id": "abcdef12-1234-1234-1234-34567890abcd",
                        },
                        {
                            "__tdbudf__": "node_output",
                            "client_node_id": "98765432-abcd-abcd-abcd-111111111111",
                        },
                    ],
                },
            },
            nodes=(node_a, node_b),
        )

    def _do_test(self, inval, expected, nodes):
        esc = builder._ParameterEscaper()
        actual = esc.visit(inval)
        self.assertEqual(expected, actual)
        self.assertEqual(frozenset(nodes), frozenset(esc.seen_nodes))


class TestBuilder(unittest.TestCase):
    maxDiff = None

    def test_basic(self):
        uuid_factory = testonly.sequential_uuids("09f91102-9d74-e35b-d841-000000000000")
        with mock.patch.object(uuid, "uuid4", side_effect=uuid_factory):
            grf = builder.TaskGraphBuilder(name="my cool task graph")
            self.assertEqual(
                {"name": "my cool task graph", "nodes": []}, grf._tdb_to_json()
            )
            start = grf.input("start", "value")
            length = grf.udf(len, types.args(start), name="length")
            result = grf.udf(
                "{it!r} has a length of {ln}".format,
                types.args(it=start, ln=length),
                name="result",
            )
            expected = {
                "name": "my cool task graph",
                "nodes": [
                    {
                        "client_node_id": "09f91102-9d74-e35b-d841-000000000000",
                        "depends_on": [],
                        "input_node": {"default_value": "value"},
                        "name": "start",
                    },
                    {
                        "client_node_id": "09f91102-9d74-e35b-d841-000000000001",
                        "depends_on": ["09f91102-9d74-e35b-d841-000000000000"],
                        "name": "length",
                        "udf_node": {
                            "args": [
                                {
                                    "value": {
                                        "__tdbudf__": "node_output",
                                        "client_node_id": "09f91102-9d74-e35b-d841-000000000000",
                                    }
                                }
                            ],
                            "environment": {
                                "language": "python",
                                "language_version": utils.PYTHON_VERSION,
                            },
                            "executable_code": "gASVFAAAAAAAAACMCGJ1aWx0aW5zlIwDbGVulJOULg==",
                            "result_format": "python_pickle",
                        },
                    },
                    {
                        "client_node_id": "09f91102-9d74-e35b-d841-000000000002",
                        "depends_on": [
                            "09f91102-9d74-e35b-d841-000000000000",
                            "09f91102-9d74-e35b-d841-000000000001",
                        ],
                        "name": "result",
                        "udf_node": {
                            "args": [
                                {
                                    "name": "it",
                                    "value": {
                                        "__tdbudf__": "node_output",
                                        "client_node_id": "09f91102-9d74-e35b-d841-000000000000",
                                    },
                                },
                                {
                                    "name": "ln",
                                    "value": {
                                        "__tdbudf__": "node_output",
                                        "client_node_id": "09f91102-9d74-e35b-d841-000000000001",
                                    },
                                },
                            ],
                            "environment": {
                                "language": "python",
                                "language_version": utils.PYTHON_VERSION,
                            },
                            "executable_code": "gASVQwAAAAAAAACMCGJ1aWx0aW5zlIwHZ2V0YXR0cpSTlIwbe2l0IXJ9IGhhcyBhIGxlbmd0aCBvZiB7bG59lIwGZm9ybWF0lIaUUpQu",
                            "result_format": "python_pickle",
                        },
                    },
                ],
            }
            self.assertEqual(expected, grf._tdb_to_json())
            with self.assertRaises(depgraph.CyclicGraphError):
                grf.add_dep(parent=result, child=length)
