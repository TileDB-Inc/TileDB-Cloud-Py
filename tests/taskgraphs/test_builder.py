import operator
import sys
import unittest
import uuid
from unittest import mock

import numpy

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
            node_a = grf.array_read("tiledb://uri/i", raw_ranges=[], buffers=["here"])
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

    def test_complex(self):
        uuid_factory = testonly.sequential_uuids("0badc0de-dead-beef-cafe-000000000000")
        with mock.patch.object(uuid, "uuid4", side_effect=uuid_factory):
            grf = builder.TaskGraphBuilder("it's complicated")

            # All the functions we use in this test are from other modules.
            # This means that they can be serialized by name rather than value.
            # Using lambdas or other functions introduces environment-dependent
            # file/line numbers into the pickles.  Verifying that user-written
            # functions are properly serialized and executed takes place with a
            # builder-to-executor round trip test.

            # Use a user-provided input in the array read.
            array_uri = grf.input("array_uri", "tiledb://TileDB-Inc/quickstart_dense")
            array_query = grf.array_read(
                array_uri,
                raw_ranges=[[1, 1, 2, 4], []],
                name="read an array",
            )

            # a chain equivalent to `lambda x: int(numpy.sum(x["a"]))`
            get_a = grf.udf(operator.itemgetter("a"), types.args(array_query))
            sum_it = grf.udf(numpy.sum, types.args(get_a))
            intify = grf.udf(int, types.args(sum_it))

            format_it = grf.udf(
                "sum of {name!r} is {sum!r}".format,
                types.args(name=array_uri, sum=intify),
            )

            # Execute an SQL query with parameterized input.
            sql_input = grf.input("sql_value")
            sql_node = grf.sql(
                "select 2 * ? as doubleit",
                parameters=[sql_input],
                result_format="json",
            )
            # Artificially constrain `format_it` to run after `sql_node`.
            grf.add_dep(parent=sql_node, child=format_it)

            summary = grf.udf(
                "array {!r} gave result {}; sql gave {}".format,
                types.args(
                    array_uri,
                    format_it,
                    sql_node,
                ),
                name="output",
            )

            grf.udf(
                "TileDB-Inc/example_registration",
                types.args(summary),
                name="hello world",
            )

        # The pickle of the `itemgetter("a")` object above changes at py3.9.
        # Both of these represent the same thing.
        itemgetter_pickle = (
            "gASVIgAAAAAAAACMCG9wZXJhdG9ylIwKaXRlbWdldHRlcpSTlIwBYZSFlFIu"
            if sys.version_info < (3, 9)
            else "gASVIwAAAAAAAACMCG9wZXJhdG9ylIwKaXRlbWdldHRlcpSTlIwBYZSFlFKULg=="
        )

        expected = {
            "name": "it's complicated",
            "nodes": [
                {
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000000",
                    "depends_on": [],
                    "input_node": {
                        "default_value": "tiledb://TileDB-Inc/quickstart_dense"
                    },
                    "name": "array_uri",
                },
                {
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000006",
                    "depends_on": [],
                    "input_node": {},
                    "name": "sql_value",
                },
                {
                    "array_node": {
                        "buffers": None,
                        "parameter_id": "0badc0de-dead-beef-cafe-000000000001",
                        "ranges": [[1, 1, 2, 4], []],
                        "uri": {
                            "__tdbudf__": "node_output",
                            "client_node_id": "0badc0de-dead-beef-cafe-000000000000",
                        },
                    },
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000001",
                    "depends_on": ["0badc0de-dead-beef-cafe-000000000000"],
                    "name": "read an array",
                },
                {
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000007",
                    "depends_on": ["0badc0de-dead-beef-cafe-000000000006"],
                    "name": None,
                    "sql_node": {
                        "init_commands": (),
                        "parameters": [
                            {
                                "__tdbudf__": "node_output",
                                "client_node_id": "0badc0de-dead-beef-cafe-000000000006",
                            }
                        ],
                        "query": "select 2 * ? as doubleit",
                        "result_format": "json",
                    },
                },
                {
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000002",
                    "depends_on": ["0badc0de-dead-beef-cafe-000000000001"],
                    "name": None,
                    "udf_node": {
                        "args": [
                            {
                                "value": {
                                    "__tdbudf__": "node_output",
                                    "client_node_id": "0badc0de-dead-beef-cafe-000000000001",
                                }
                            }
                        ],
                        "environment": {
                            "language": "python",
                            "language_version": utils.PYTHON_VERSION,
                        },
                        "executable_code": itemgetter_pickle,
                        "result_format": "python_pickle",
                    },
                },
                {
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000003",
                    "depends_on": ["0badc0de-dead-beef-cafe-000000000002"],
                    "name": None,
                    "udf_node": {
                        "args": [
                            {
                                "value": {
                                    "__tdbudf__": "node_output",
                                    "client_node_id": "0badc0de-dead-beef-cafe-000000000002",
                                }
                            }
                        ],
                        "environment": {
                            "language": "python",
                            "language_version": utils.PYTHON_VERSION,
                        },
                        "executable_code": "gASVEQAAAAAAAACMBW51bXB5lIwDc3VtlJOULg==",
                        "result_format": "python_pickle",
                    },
                },
                {
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000004",
                    "depends_on": ["0badc0de-dead-beef-cafe-000000000003"],
                    "name": None,
                    "udf_node": {
                        "args": [
                            {
                                "value": {
                                    "__tdbudf__": "node_output",
                                    "client_node_id": "0badc0de-dead-beef-cafe-000000000003",
                                }
                            }
                        ],
                        "environment": {
                            "language": "python",
                            "language_version": utils.PYTHON_VERSION,
                        },
                        "executable_code": "gASVFAAAAAAAAACMCGJ1aWx0aW5zlIwDaW50lJOULg==",
                        "result_format": "python_pickle",
                    },
                },
                {
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000005",
                    "depends_on": [
                        "0badc0de-dead-beef-cafe-000000000000",
                        "0badc0de-dead-beef-cafe-000000000004",
                        "0badc0de-dead-beef-cafe-000000000007",
                    ],
                    "name": None,
                    "udf_node": {
                        "args": [
                            {
                                "name": "name",
                                "value": {
                                    "__tdbudf__": "node_output",
                                    "client_node_id": "0badc0de-dead-beef-cafe-000000000000",
                                },
                            },
                            {
                                "name": "sum",
                                "value": {
                                    "__tdbudf__": "node_output",
                                    "client_node_id": "0badc0de-dead-beef-cafe-000000000004",
                                },
                            },
                        ],
                        "environment": {
                            "language": "python",
                            "language_version": utils.PYTHON_VERSION,
                        },
                        "executable_code": "gASVQgAAAAAAAACMCGJ1aWx0aW5zlIwHZ2V0YXR0cpSTlIwac3VtIG9mIHtuYW1lIXJ9IGlzIHtzdW0hcn2UjAZmb3JtYXSUhpRSlC4=",
                        "result_format": "python_pickle",
                    },
                },
                {
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000008",
                    "depends_on": [
                        "0badc0de-dead-beef-cafe-000000000000",
                        "0badc0de-dead-beef-cafe-000000000005",
                        "0badc0de-dead-beef-cafe-000000000007",
                    ],
                    "name": "output",
                    "udf_node": {
                        "args": [
                            {
                                "value": {
                                    "__tdbudf__": "node_output",
                                    "client_node_id": "0badc0de-dead-beef-cafe-000000000000",
                                }
                            },
                            {
                                "value": {
                                    "__tdbudf__": "node_output",
                                    "client_node_id": "0badc0de-dead-beef-cafe-000000000005",
                                }
                            },
                            {
                                "value": {
                                    "__tdbudf__": "node_output",
                                    "client_node_id": "0badc0de-dead-beef-cafe-000000000007",
                                }
                            },
                        ],
                        "environment": {
                            "language": "python",
                            "language_version": utils.PYTHON_VERSION,
                        },
                        "executable_code": "gASVTgAAAAAAAACMCGJ1aWx0aW5zlIwHZ2V0YXR0cpSTlIwmYXJyYXkgeyFyfSBnYXZlIHJlc3VsdCB7fTsgc3FsIGdhdmUge32UjAZmb3JtYXSUhpRSlC4=",
                        "result_format": "python_pickle",
                    },
                },
                {
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000009",
                    "depends_on": ["0badc0de-dead-beef-cafe-000000000008"],
                    "name": "hello world",
                    "udf_node": {
                        "args": [
                            {
                                "value": {
                                    "__tdbudf__": "node_output",
                                    "client_node_id": "0badc0de-dead-beef-cafe-000000000008",
                                }
                            }
                        ],
                        "environment": {},
                        "registered_udf_name": "TileDB-Inc/example_registration",
                        "result_format": "python_pickle",
                    },
                },
            ],
        }
        self.assertEqual(expected, grf._tdb_to_json())
