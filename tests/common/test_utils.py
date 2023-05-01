import base64
import datetime
import pickle
import unittest

import pytz  # Test-only dependency.

from tiledb.cloud._common import utils


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


def _b64_unpickle(x):
    raw = base64.b64decode(x)
    return pickle.loads(raw)
