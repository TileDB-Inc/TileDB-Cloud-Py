import unittest

from tiledb.cloud.taskgraphs import types


class TestTypes(unittest.TestCase):
    def test_args(self):
        args = types.args(1, "A", b=frozenset())
        self.assertEqual(args, types.Arguments((1, "A"), {"b": frozenset()}))
