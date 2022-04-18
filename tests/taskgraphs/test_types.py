import unittest

from tiledb.cloud.taskgraphs import types


class TestTypes(unittest.TestCase):
    def test_args(self):
        args = types.args(1, "A", b=frozenset(), c=b"d")
        self.assertEqual(
            args,
            types.Arguments((1, "A"), {"b": frozenset(), "c": b"d"}),
        )
        self.assertEqual("args(1, 'A', b=frozenset(), c=b'd')", repr(args))
