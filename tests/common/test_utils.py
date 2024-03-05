import base64
import datetime
import pickle
import unittest
from unittest import mock

import pytz  # Test-only dependency.
from pyfakefs.fake_filesystem_unittest import TestCase as FileTestCase

from tiledb.cloud._common import utils
from tiledb.cloud.utilities import find
from tiledb.vfs import VFS


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


class FindTest(FileTestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_find(self):
        test_1 = [
            self.fs.create_file("/var/data.dat"),
            self.fs.create_file("/var/data/xx1.txt"),
            self.fs.create_file("/var/data/xx2.txt"),
        ]

        with mock.patch.object(VFS, "ls", return_value=test_1):
            with mock.patch.object(VFS, "is_dir", return_value=True) as mock_is_dir:
                mock_is_dir.side_effect = lambda f: self.fs.isdir(f.name)
                self.assertEqual(len(list(find("."))), len(test_1))

                for v in range(2):
                    max_count = v + 1
                    self.assertEqual(
                        len(list(find(".", max_count=max_count))), max_count
                    )

                self.assertEqual(
                    len(list(find(".", include=lambda f: f.name.endswith(".txt")))), 2
                )
                self.assertEqual(
                    len(list(find(".", exclude=lambda f: f.name.endswith(".dat")))), 2
                )
                self.assertEqual(
                    len(list(find(".", include=lambda f: f.name.endswith(".dat")))), 1
                )


def _b64_unpickle(x):
    raw = base64.b64decode(x)
    return pickle.loads(raw)
