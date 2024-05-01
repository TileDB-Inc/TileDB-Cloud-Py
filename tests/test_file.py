import hashlib
import os
import tempfile
import unittest
from typing import List

import tiledb
from tiledb.cloud import client
from tiledb.cloud import groups
from tiledb.cloud._common import testonly
from tiledb.cloud.array import delete_array
from tiledb.cloud.array import info
from tiledb.cloud.file import ingestion as file_ingestion
from tiledb.cloud.file import udfs as file_udfs
from tiledb.cloud.file import utils as file_utils

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class TestFileUtils(unittest.TestCase):
    def test_simple_file_export(self):
        test_file = "tiledb://TileDB-Inc/VLDB17_TileDB"

        with tempfile.TemporaryDirectory() as dirpath:
            output_path = os.path.join(dirpath, "VLDB17_TileDB.pdf")
            file_utils.export_file_local(test_file, output_path)

            with open(output_path, "rb") as exported:
                digest = hashlib.sha256(exported.read()).hexdigest()
                self.assertEqual(619181, exported.tell(), "exported file size")

            self.assertEqual(
                "14065c5debdf5eeff1478533a6484b9d26dc0b9d7a4cb228aa03f9e22f390300",
                digest,
            )

    def test_sanitize_filename(self):
        subjects = {
            "test_1": ("test_filename.txt", "test_filename.txt"),
            "test_2": (
                "test filename with spaces.txt",
                "test_filename_with_spaces.txt",
            ),
            "test_3": ("test,filename,with,commas.txt", "testfilenamewithcommas.txt"),
            "test_4": ("test._m'ixed, file  .name.pdf", "test_mixed_file_name.pdf"),
            "test_5": ("O'Reilly_-_Python_Cookbook.pdf", "OReilly_Python_Cookbook.pdf"),
        }

        for test_name, (fname, sanitized) in subjects.items():
            with self.subTest(f"case: {test_name}"):
                self.assertEqual(file_ingestion.sanitize_filename(fname), sanitized)

    def test_basename_match(self):
        test_fname = os.path.join(
            CURRENT_DIR, "data", "simple_files", "contains_word_1.txt"
        )
        subjects = {
            "test_1": (None, False),
            "test_2": ("*.txt", True),
            "test_3": ("start_*", False),
            "test_4": ("contains_*", True),
            "test_5": ("*_1.txt", True),
            "test_6": ("*_word_*", True),
            "test_7": ("_word_", False),
            "test_8": ("_word_*", False),
            "test_9": ("*_word_", False),
        }

        for test_name, (pattern, result) in subjects.items():
            with self.subTest(f"case: {test_name}"):
                self.assertEqual(file_utils.basename_match(test_fname, pattern), result)


class TestFileUDFs(unittest.TestCase):
    def test_find_uris_udf(self):
        local_test_files = os.path.join(CURRENT_DIR, "data", "simple_files")
        subjects = {
            "test_1": ("*.txt", None, 5),
            "test_2": (None, "*.txt", 1),
            "test_3": ("start_*", None, 3),
            "test_4": (None, "start_*", 3),
            "test_5": ("*_word_*", None, 2),
            "test_6": (None, "*_word_*", 4),
            "test_7": ("*.txt", "*.csv", 5),
        }

        for test_name, (pattern, ignore, found) in subjects.items():
            with self.subTest(f"case: {test_name}"):
                uris = file_udfs.find_uris_udf(
                    local_test_files, include=pattern, exclude=ignore
                )
                self.assertEqual(len(uris), found)

    def test_chunk_results(self):
        subjects = {
            "test_1": (
                ["1", "2", "3", "4", "5"],
                3,
                True,
                [["1", "2", "3"], ["4", "5"]],
            ),
            "test_2": (
                ("1", "2", "3", "4", "5"),
                1,
                True,
                [["1"], ["2"], ["3"], ["4"], ["5"]],
            ),
            "test_3": (
                ["1", "2", "3", "4", "5"],
                None,
                True,
                [["1", "2", "3", "4", "5"]],
            ),
            "test_4": (
                [["1"], ["2"], ["3"], ["4"], ["5"]],
                None,
                True,
                [["1", "2", "3", "4", "5"]],
            ),
            "test_5": (
                [["1"], ["2"], ["3"], ["4"], ["5"]],
                4,
                True,
                [["1", "2", "3", "4"], ["5"]],
            ),
            "test_6": (
                [["1"], ("2", "3"), ("4", "5")],
                None,
                True,
                [["1", "2", "3", "4", "5"]],
            ),
            "test_7": (
                ["1", "2", "3", "4", "5"],
                2,
                False,
                [["1", "2"], ["3", "4"], ["5"]],
            ),
        }

        for test_name, (chunks_in, batch_size, flatten, chunks_out) in subjects.items():
            with self.subTest(f"case: {test_name}"):
                result = file_udfs.chunk_udf(
                    items=chunks_in, batch_size=batch_size, flatten_items=flatten
                )
                self.assertEqual(result, chunks_out)


class TestFileIngestion(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Setup test files, group and destinations once before the file tests start."""
        cls.input_file_location = (
            "s3://tiledb-unittest/groups/file_ingestion_test_files"
        )
        # Files with name "input_file_<n[0, 4]>.pdf" have already been placed
        # in the "cls.input_file_location"
        cls.input_file_names = [f"input_file_{i}.pdf" for i in range(5)]
        cls.test_file_uris = [
            f"{cls.input_file_location}/{fname}" for fname in cls.input_file_names
        ]

        cls.namespace, cls.storage_path, cls.acn = groups._default_ns_path_cred()
        cls.namespace = cls.namespace.rstrip("/")
        cls.storage_path = cls.storage_path.rstrip("/")
        cls.destination = (
            f"{cls.storage_path}/{testonly.random_name('file_ingestion_test')}"
        )

        cls.group_name = testonly.random_name("file_ingestion_test_group")
        cls.group_uri = f"tiledb://{cls.namespace}/{cls.group_name}"
        cls.group_destination = f"{cls.storage_path}/{cls.group_name}"
        groups.create(cls.group_name, storage_uri=cls.group_destination)

        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        """Cleanup test and ingested files and folders after tests have finished."""
        cls.__cleanup_residual_test_arrays(
            array_uris=[
                f"tiledb://{cls.namespace}/{fname}" for fname in cls.input_file_names
            ]
        )
        groups.deregister(cls.group_uri)
        return super().tearDownClass()

    def setUp(self) -> None:
        """Initialize between tests"""
        self.ingested_array_uris = []
        return super().setUp()

    def tearDown(self) -> None:
        """Cleanup registered arrays between tests"""
        self.__cleanup_residual_test_arrays(array_uris=self.ingested_array_uris)
        return super().tearDown()

    @staticmethod
    def __cleanup_residual_test_arrays(array_uris: List[str]) -> None:
        """Deletes every array in a list"""
        for array_uri in array_uris:
            try:
                delete_array(array_uri)
            except Exception:
                continue

    def test_files_ingestion_udf(self):
        self.ingested_array_uris = file_ingestion.ingest_files_udf(
            dataset_uri=self.destination,
            file_uris=self.test_file_uris,
            acn=self.acn,
            namespace=self.namespace,
            verbose=True,
        )
        self.assertEqual(len(self.ingested_array_uris), len(self.input_file_names))

        for fname in self.input_file_names:
            array_info = info(f"tiledb://{self.namespace}/{fname}")
            self.assertEqual(array_info.name, fname)
            self.assertEqual(array_info.namespace, self.namespace)

    def test_files_ingestion_udf_into_group(self):
        self.ingested_array_uris = file_ingestion.ingest_files_udf(
            dataset_uri=self.group_destination,
            file_uris=self.test_file_uris,
            acn=self.acn,
            namespace=self.namespace,
            verbose=True,
        )
        self.assertEqual(len(self.ingested_array_uris), len(self.input_file_names))

        file_ingestion.add_arrays_to_group_udf(
            array_uris=self.ingested_array_uris,
            group_uri=self.group_uri,
            config=client.Ctx().config().dict(),
            verbose=True,
        )

        group_info = groups.info(self.group_uri)
        self.assertEqual(group_info.asset_count, len(self.test_file_uris))

        for fname in self.input_file_names:
            array_info = info(f"tiledb://{self.namespace}/{fname}")
            self.assertEqual(array_info.name, fname)
            self.assertEqual(array_info.namespace, self.namespace)

    def test_add_array_to_group_udf_raises_bad_namespace_error(self):
        with self.assertRaises(tiledb.TileDBError):
            file_ingestion.add_arrays_to_group_udf(
                array_uris=[f"tiledb://{self.namespace}/{self.input_file_names[0]}"],
                group_uri=f"tiledb://very-bad-namespace/{self.group_name}",
                config=client.Ctx().config().dict(),
                verbose=True,
            )

    def test_add_array_to_group_udf_non_existing_group_raises_value_error(self):
        with self.assertRaises(ValueError):
            file_ingestion.add_arrays_to_group_udf(
                array_uris=[f"tiledb://{self.namespace}/{self.input_file_names[0]}"],
                group_uri=f"tiledb://{self.namespace}/non-existing-group",
                config=client.Ctx().config().dict(),
                verbose=True,
            )
