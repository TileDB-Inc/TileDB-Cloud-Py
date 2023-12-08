import unittest
from unittest import mock

import tiledb
from tiledb.cloud.bioimg.exportation import build_io_uris_exportation
from tiledb.cloud.bioimg.ingestion import build_io_uris_ingestion
from tiledb.vfs import VFS


class BioimgTest(unittest.TestCase):
    def setUp(self) -> None:
        self.out_path = "out"
        return super().setUp()

    def test_build_io_uris_ingestion(self):
        ingest_uri_sample = {
            "test1": ["test1.tiff", "test2.tiff", "test3.tiff"],
            "test2": [],
            "test3": ["test1.tiff", "test2.tiff", "test3.zarr"],
        }

        # Case 1-1 Ingestion - Ingest mode has tdb as target suffix
        out_suffix = "tdb"
        test1 = ingest_uri_sample["test1"]
        with mock.patch.object(VFS, "is_dir", return_value=False):
            with mock.patch.object(VFS, "ls", return_value=test1):
                result_1 = build_io_uris_ingestion(test1, self.out_path, out_suffix)
                expected_1 = (
                    ("test1.tiff", "out/test1.tdb"),
                    ("test2.tiff", "out/test2.tdb"),
                    ("test3.tiff", "out/test3.tdb"),
                )
                self.assertTupleEqual(result_1, expected_1)

            # Case 1-2 Ingestion - Empty input list
            with mock.patch.object(VFS, "ls", return_value=ingest_uri_sample["test2"]):
                # Empty input list raises error
                with self.assertRaises(ValueError):
                    build_io_uris_ingestion(
                        ingest_uri_sample["test2"], self.out_path, out_suffix
                    )

            # Case 1-3 Ingestion - Files with different suffices
            test3 = ingest_uri_sample["test3"]
            with mock.patch.object(VFS, "ls", return_value=test3):
                result_3 = build_io_uris_ingestion(test3, self.out_path, out_suffix)
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
        with mock.patch.object(tiledb, "object_type", return_value="group"):
            with mock.patch.object(VFS, "ls", return_value=test1):
                result = build_io_uris_exportation(test1, self.out_path, out_suffix)
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
                with self.assertRaises(ValueError):
                    build_io_uris_exportation(test2, self.out_path, out_suffix)
