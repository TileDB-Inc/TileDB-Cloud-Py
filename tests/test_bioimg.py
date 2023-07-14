import math
import unittest
from unittest import mock

from tiledb.cloud.bioimg.helpers import batch
from tiledb.cloud.bioimg.helpers import get_uris
from tiledb.cloud.bioimg.helpers import scale_calc
from tiledb.vfs import VFS


class BioimgTest(unittest.TestCase):
    def setUp(self) -> None:
        self.out_path = "out"
        return super().setUp()

    def test_get_uris_ingestion(self):
        ingest_uri_sample = {
            "test1": ["test1.tiff", "test2.tiff", "test3.tiff"],
            "test2": [],
            "test3": ["test1.tiff", "test2.tiff", "test3.zarr"],
        }

        # Case 1-1 Ingestion - Ingest mode has tdb as target suffix
        out_suffix = "tdb"
        test1 = ingest_uri_sample["test1"]
        with mock.patch.object(VFS, "ls", return_value=test1):
            out_suffix = "tdb"
            result_1 = get_uris(test1, self.out_path, None, out_suffix)
            expected_1 = (
                ("test1.tiff", "out/test1.tdb"),
                ("test2.tiff", "out/test2.tdb"),
                ("test3.tiff", "out/test3.tdb"),
            )
            self.assertTupleEqual(result_1, expected_1)

        # Case 1-2 Ingestion - Empty input list
        with mock.patch.object(VFS, "ls", return_value=ingest_uri_sample["test2"]):
            # Empty input list raises error
            self.assertRaises(
                get_uris(ingest_uri_sample["test2"], self.out_path, None, out_suffix)
            )

        # Case 1-3 Ingestion - Files with different suffices
        test3 = ingest_uri_sample["test3"]
        with mock.patch.object(VFS, "ls", return_value=test3):
            result_3 = get_uris(test3, self.out_path, None, out_suffix)
            expected_3 = (
                ("test1.tiff", "out/test1.tdb"),
                ("test2.tiff", "out/test2.tdb"),
            )
            self.assertTupleEqual(result_3, expected_3)

    def test_get_uris_exportation(self):
        export_uri_sample = {
            "test1": ["test1.tdb", "test2.tdb", "test3.tdb"],
            "test2": [],
            "test3": ["test1.tdb", "test2.tdb", "test3.zarr"],
        }

        # Case 2-1 Exportation normal mode has tiff as target suffix
        out_suffix = "tiff"
        test1 = export_uri_sample["test1"]
        with mock.patch.object(VFS, "ls", return_value=test1):
            result = get_uris(test1, self.out_path, None, out_suffix)
            expected = (
                ("test1.tdb", "out/test1.tiff"),
                ("test2.tdb", "out/test2.tiff"),
                ("test3.tdb", "out/test3.tiff"),
            )
            self.assertTupleEqual(result, expected)

        # Case 2-2 Exportation empty list
        test2 = export_uri_sample["test2"]
        with mock.patch.object(VFS, "ls", return_value=test2):
            # Empty input list raises error
            self.assertRaises(get_uris(test2, self.out_path, None, out_suffix))

        # Case 2-3 Exportation  Files with different suffices
        test3 = export_uri_sample["test3"]
        with mock.patch.object(VFS, "ls", return_value=test3):
            result_3 = get_uris(test3, self.out_path, None, out_suffix)
            expected_3 = (
                ("test1.tdb", "out/test1.tiff"),
                ("test2.tdb", "out/test2.tiff"),
            )
            self.assertTupleEqual(result_3, expected_3)

    def test_batch(self):
        samples = (
            ("test1.tiff", "out/test1.tdb"),
            ("test2.tiff", "out/test2.tdb"),
            ("test3.tiff", "out/test3.tdb"),
        )

        # Three nodes with 1 job are expected
        batch_size = 1
        result = batch(samples, batch_size)
        expected = 3
        self.assertEqual(len(tuple(result)), expected)

        # Two nodes with 2,1 jobs are expected
        batch_size = 2
        result = batch(samples, batch_size)
        expected = 2
        self.assertEqual(len(tuple(result)), expected)

        # One node with all jobs is expected
        batch_size = 3
        result = batch(samples, batch_size)
        expected = 1
        self.assertEqual(len(tuple(result)), expected)

    def test_scale_calc(self):
        samples = (
            ("test1.tiff", "out/test1.tdb"),
            ("test2.tiff", "out/test2.tdb"),
            ("test3.tiff", "out/test3.tdb"),
        )

        result = scale_calc(samples, None)
        self.assertEqual(result, (1, 20))

        expected = math.ceil(len(samples) / 2)
        result = scale_calc(samples, 2)
        self.assertEqual(result, (expected, None))

        expected = math.ceil(len(samples) / 3)
        result = scale_calc(samples, 3)
        self.assertEqual(result, (expected, None))
