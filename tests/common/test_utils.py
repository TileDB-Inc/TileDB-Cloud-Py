import base64
import datetime
import pathlib
import pickle
import tempfile
import unittest

import pytz  # Test-only dependency.

from tiledb.cloud._common import utils
from tiledb.cloud.utilities import find


class UtilsTest(unittest.TestCase):
    def test_pickle_roundtrip(self):
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

    def test_datetime_to_msec(self):
        cases = [
            (0, 0),
            (
                datetime.datetime(
                    1970, 2, 3, microsecond=123999, tzinfo=datetime.timezone.utc
                ),
                2851200123,
            ),
            (
                pytz.timezone("America/New_York").localize(
                    datetime.datetime(2023, 4, 28, 12, 34, 56, 789012)
                ),
                1682699696789,
            ),
        ]
        for inval, expected in cases:
            with self.subTest(inval):
                self.assertEqual(utils.datetime_to_msec(inval), expected)

    def test_find(self):
        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = pathlib.Path(tmp_name)
            (tmp / "data.dat").write_text("test_data")
            data_dir = tmp / "data"
            data_dir.mkdir()
            (data_dir / "xx1.txt").write_text("test_xx1")
            (data_dir / "xx2.txt").write_text("test_xx2")

            self.assertEqual(len(list(find(tmp))), 3)

            for v in range(2):
                max_count = v + 1
                self.assertEqual(len(list(find(tmp, max_count=max_count))), max_count)

            self.assertEqual(
                len(list(find(tmp, include=lambda f: f.endswith(".txt")))), 2
            )
            self.assertEqual(
                len(list(find(tmp, exclude=lambda f: f.endswith(".dat")))), 2
            )
            self.assertEqual(
                len(list(find(tmp, include=lambda f: f.endswith(".dat")))), 1
            )


def _b64_unpickle(x):
    raw = base64.b64decode(x)
    return pickle.loads(raw)
