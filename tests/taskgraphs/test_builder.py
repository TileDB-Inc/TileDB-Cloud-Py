import unittest
import uuid
from unittest import mock

from tiledb.cloud import testonly
from tiledb.cloud.taskgraphs import builder


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
