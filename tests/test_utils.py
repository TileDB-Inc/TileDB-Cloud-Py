import base64
import importlib
import os
import os.path
import pickle
import sys
import tempfile
import textwrap
import unittest

from tiledb.cloud import utils


class SourceLinesTest(unittest.TestCase):
    def test_this_function(self):
        me = utils.getsourcelines(self.test_this_function)
        self.assertIsInstance(me, str)

    def test_missing_function(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            testfile = os.path.join(tmpdir, "bogus_module.py")
            with open(testfile, "w") as out:
                out.write(
                    textwrap.dedent(
                        """\
                        def unimportant_function(a):
                            pass
                        """
                    )
                )
            sys.path.insert(0, tmpdir)
            try:
                bogus = importlib.import_module("bogus_module")
            finally:
                sys.path.pop(0)
                sys.modules.pop("bogus_module", None)

            os.remove(testfile)
            self.assertIsNone(utils.getsourcelines(bogus.unimportant_function))


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
