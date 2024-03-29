import operator
import unittest
import uuid
from unittest import mock

import numpy

from tiledb.cloud._common import functions
from tiledb.cloud._common import testonly
from tiledb.cloud._common import utils
from tiledb.cloud.taskgraphs import _codec
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
            the_node = builder._InputNode(builder, "hello", "world")

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
                local=True,
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
                            "arguments": [
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
                            "result_format": "tiledb_json",
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
                            "arguments": [
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
                                "run_client_side": True,
                            },
                            "executable_code": "gASVQwAAAAAAAACMCGJ1aWx0aW5zlIwHZ2V0YXR0cpSTlIwbe2l0IXJ9IGhhcyBhIGxlbmd0aCBvZiB7bG59lIwGZm9ybWF0lIaUUpQu",
                            "result_format": "tiledb_json",
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
            sum_it = grf.udf(
                numpy.sum, types.args(get_a), timeout=100, namespace="fido"
            )
            intify = grf.udf(int, types.args(sum_it), resource_class="llama")

            format_it = grf.udf(
                "sum of {name!r} is {sum!r}".format,
                types.args(name=array_uri, sum=intify),
                download_results=False,
            )

            # Execute an SQL query with parameterized input.
            sql_input = grf.input("sql_value")
            sql_node = grf.sql(
                "select 2 * ? as doubleit",
                parameters=[sql_input],
                result_format="json",
                namespace="beans",
                download_results=True,
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
                local=True,
            )

            grf.udf(
                "TileDB-Inc/example_registration",
                types.args(summary),
                name="hello world",
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
                        "ranges": {"layout": None, "ranges": [[1, 1, 2, 4], []]},
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
                    "name": "SQL query",
                    "sql_node": {
                        "download_results": True,
                        "init_commands": (),
                        "namespace": "beans",
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
                    "name": "operator.itemgetter('a')",
                    "udf_node": {
                        "arguments": [
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
                        "executable_code": "gASVIwAAAAAAAACMCG9wZXJhdG9ylIwKaXRlbWdldHRlcpSTlIwBYZSFlFKULg==",
                        "result_format": "tiledb_json",
                    },
                },
                {
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000003",
                    "depends_on": ["0badc0de-dead-beef-cafe-000000000002"],
                    "name": "numpy.sum",
                    "udf_node": {
                        "arguments": [
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
                            "namespace": "fido",
                            "timeout": 100,
                        },
                        "executable_code": "gASVEQAAAAAAAACMBW51bXB5lIwDc3VtlJOULg==",
                        "source_text": functions.getsourcelines(numpy.sum),
                        "result_format": "tiledb_json",
                    },
                },
                {
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000004",
                    "depends_on": ["0badc0de-dead-beef-cafe-000000000003"],
                    "name": "builtins.int",
                    "udf_node": {
                        "arguments": [
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
                            "resource_class": "llama",
                        },
                        "executable_code": "gASVFAAAAAAAAACMCGJ1aWx0aW5zlIwDaW50lJOULg==",
                        "result_format": "tiledb_json",
                    },
                },
                {
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000005",
                    "depends_on": [
                        "0badc0de-dead-beef-cafe-000000000000",
                        "0badc0de-dead-beef-cafe-000000000004",
                        "0badc0de-dead-beef-cafe-000000000007",
                    ],
                    "name": "str.format",
                    "udf_node": {
                        "arguments": [
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
                        "download_results": False,
                        "environment": {
                            "language": "python",
                            "language_version": utils.PYTHON_VERSION,
                        },
                        "executable_code": "gASVQgAAAAAAAACMCGJ1aWx0aW5zlIwHZ2V0YXR0cpSTlIwac3VtIG9mIHtuYW1lIXJ9IGlzIHtzdW0hcn2UjAZmb3JtYXSUhpRSlC4=",
                        "result_format": "tiledb_json",
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
                        "arguments": [
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
                            "run_client_side": True,
                        },
                        "executable_code": "gASVTgAAAAAAAACMCGJ1aWx0aW5zlIwHZ2V0YXR0cpSTlIwmYXJyYXkgeyFyfSBnYXZlIHJlc3VsdCB7fTsgc3FsIGdhdmUge32UjAZmb3JtYXSUhpRSlC4=",
                        "result_format": "tiledb_json",
                    },
                },
                {
                    "client_node_id": "0badc0de-dead-beef-cafe-000000000009",
                    "depends_on": ["0badc0de-dead-beef-cafe-000000000008"],
                    "name": "hello world",
                    "udf_node": {
                        "arguments": [
                            {
                                "value": {
                                    "__tdbudf__": "node_output",
                                    "client_node_id": "0badc0de-dead-beef-cafe-000000000008",
                                }
                            }
                        ],
                        "environment": {},
                        "registered_udf_name": "TileDB-Inc/example_registration",
                        "result_format": "tiledb_json",
                    },
                },
            ],
        }
        self.assertEqual(expected, grf._tdb_to_json())

    def test_name_collisions(self):
        grf = builder.TaskGraphBuilder()
        uuid_factory = testonly.sequential_uuids("aaaaaaaa-bbbb-cccc-dddd-000000000000")
        with mock.patch.object(uuid, "uuid4", side_effect=uuid_factory):
            # Ensure that, despite the fact that the `b64_str` node with
            # a fallback name of `....b64_str` is added first, the input node
            # with that name overrides it for naming purposes.
            collider_node = grf.udf(_codec.b64_str, types.args("it"))
            in_node = grf.input("tiledb.cloud.taskgraphs._codec.b64_str")
            grf.udf(
                _codec.b64_str,
                types.args([collider_node, in_node]),
                include_source=False,
            )

        expected = {
            "name": None,
            "nodes": [
                {
                    "client_node_id": "aaaaaaaa-bbbb-cccc-dddd-000000000000",
                    "depends_on": [],
                    "name": "tiledb.cloud.taskgraphs._codec.b64_str (00)",
                    "udf_node": {
                        "arguments": [{"value": "it"}],
                        "environment": {
                            "language": "python",
                            "language_version": utils.PYTHON_VERSION,
                        },
                        "executable_code": utils.b64_pickle(_codec.b64_str),
                        "result_format": "tiledb_json",
                        "source_text": (
                            "def b64_str(val: bytes) -> str:\n"
                            '    return base64.b64encode(val).decode("ascii")\n'
                        ),
                    },
                },
                {
                    "client_node_id": "aaaaaaaa-bbbb-cccc-dddd-000000000001",
                    "depends_on": [],
                    "name": "tiledb.cloud.taskgraphs._codec.b64_str",
                    "input_node": {},
                },
                {
                    "client_node_id": "aaaaaaaa-bbbb-cccc-dddd-000000000002",
                    "depends_on": [
                        "aaaaaaaa-bbbb-cccc-dddd-000000000000",
                        "aaaaaaaa-bbbb-cccc-dddd-000000000001",
                    ],
                    "name": "tiledb.cloud.taskgraphs._codec.b64_str (02)",
                    "udf_node": {
                        "arguments": [
                            {
                                "value": [
                                    {
                                        "__tdbudf__": "node_output",
                                        "client_node_id": "aaaaaaaa-bbbb-cccc-dddd-000000000000",
                                    },
                                    {
                                        "__tdbudf__": "node_output",
                                        "client_node_id": "aaaaaaaa-bbbb-cccc-dddd-000000000001",
                                    },
                                ]
                            }
                        ],
                        "environment": {
                            "language": "python",
                            "language_version": utils.PYTHON_VERSION,
                        },
                        "executable_code": utils.b64_pickle(_codec.b64_str),
                        "result_format": "tiledb_json",
                        # No source text here!
                    },
                },
            ],
        }
        self.assertEqual(expected, grf._tdb_to_json())

    def test_no_mixing(self):
        bld_a = builder.TaskGraphBuilder()
        node_a = bld_a.udf(lambda: None)
        bld_b = builder.TaskGraphBuilder()
        with self.assertRaises(ValueError):
            bld_b.udf(lambda x: x, types.args(node_a))


class GenerateNameTest(unittest.TestCase):
    def test_regular(self):
        grf = builder.TaskGraphBuilder()
        fake_id = uuid.UUID("38b00ae6-eca7-e9a9-f022-eaa33ccb1c3c")
        with mock.patch.object(uuid, "uuid4", return_value=fake_id):
            len_node = grf.udf(len)
        existing = {"builtins.len", "builtins.len (ab)", "builtins.len (3c)"}
        self.assertEqual(len_node._registration_name(existing), "builtins.len (1c3c)")
        self.assertEqual(
            existing,
            {
                "builtins.len",
                "builtins.len (ab)",
                "builtins.len (3c)",
                "builtins.len (1c3c)",
            },
        )
        int_node = grf.udf(int)
        self.assertEqual(int_node._registration_name(existing), "builtins.int")
        self.assertEqual(
            existing,
            {
                "builtins.len",
                "builtins.len (ab)",
                "builtins.len (3c)",
                "builtins.len (1c3c)",
                "builtins.int",
            },
        )

    def test_adversarial(self):
        grf = builder.TaskGraphBuilder()

        node_id = uuid.UUID("3cd50ab3-a6b9-aed8-d2a0-46964788fae0")
        with mock.patch.object(uuid, "uuid4", return_value=node_id):
            node = grf.udf(id)

        existing = {
            "builtins.id",
            "builtins.id (e0)",
            "builtins.id (fae0)",
            "builtins.id (88fae0)",
            "builtins.id (4788fae0)",
            "builtins.id (964788fae0)",
            "builtins.id (46964788fae0)",
        }
        second_id = uuid.UUID("11805aa8-1c78-2699-daeb-f7339eb9b5e0")
        with mock.patch.object(uuid, "uuid4", return_value=second_id):
            self.assertEqual(
                node._registration_name(existing),
                "builtins.id (b5e0)",
            )
            self.assertEqual(
                existing,
                {
                    "builtins.id",
                    "builtins.id (e0)",
                    "builtins.id (fae0)",
                    "builtins.id (88fae0)",
                    "builtins.id (4788fae0)",
                    "builtins.id (964788fae0)",
                    "builtins.id (46964788fae0)",
                    "builtins.id (b5e0)",
                },
            )
