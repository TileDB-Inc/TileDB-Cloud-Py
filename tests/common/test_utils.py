import base64
import pickle
import unittest

from tiledb.cloud._common import utils


class PickleTest(unittest.TestCase):
    def test_roundtrip(self):
        cases = (
            None,
            ("a", 1),
            {"some": "dict"},
        )
        for c in cases:
            with self.subTest(f"roundtrip {c!r}"):
                pickled = utils.b64_pickle(c)
                unpickled = _b64_unpickle(pickled)
                self.assertEqual(unpickled, c)


def _b64_unpickle(x):
    raw = base64.b64decode(x)
    return pickle.loads(raw)
