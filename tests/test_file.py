import hashlib
import os
import pathlib
import tempfile
import unittest
from typing import List

import tiledb
from tiledb.cloud import array
from tiledb.cloud import client
from tiledb.cloud import groups
from tiledb.cloud._common import testonly
from tiledb.cloud._common import utils
from tiledb.cloud.array import delete_array
from tiledb.cloud.array import info
from tiledb.cloud.files import indexing as file_indexing
from tiledb.cloud.files import ingestion as file_ingestion
from tiledb.cloud.files import udfs as file_udfs
from tiledb.cloud.files import utils as file_utils
from tiledb.cloud.utilities import get_logger_wrapper

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
                self.assertEqual(file_utils.sanitize_filename(fname), sanitized)

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


def _cleanup_residual_test_arrays(array_uris: List[str]) -> None:
    """Deletes every array in a list and potential non unique tables"""
    for array_uri in array_uris:
        try:
            delete_array(array_uri)
        except Exception as exc:
            error_msg = str(exc)
            if "is not unique" in error_msg:
                namespace, _ = utils.split_uri(array_uri)
                uuids = error_msg[error_msg.find("[") + 1 : error_msg.find("]")]
                uuids = uuids.split(" ")
                for uid in uuids:
                    try:
                        delete_array(f"tiledb://{namespace}/{uid}")
                    except Exception:
                        continue
            continue


class UploadTest(unittest.TestCase):
    def test_round_trip(self):
        namespace = client.default_user().username
        default_path = client.default_user().default_s3_path
        output = f"{default_path}/{testonly.random_name('upload')}"
        uri = file_utils.upload_file(
            __file__,
            f"tiledb://{namespace}/{output}",
            content_type="text/plain",
        )
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                tmppath = pathlib.Path(tmpdir) / "output"
                file_utils.export_file_local(uri, str(tmppath))
                me = pathlib.Path(__file__).read_bytes()
                downloaded = tmppath.read_bytes()
                self.assertEqual(me, downloaded)
        finally:
            array.delete_array(uri)


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
        # Files with name "group_input_file_<n[0, 4]>.pdf" have already been placed
        # in the "cls.input_file_location"
        cls.group_input_file_names = [f"group_input_file_{i}.pdf" for i in range(5)]
        cls.group_test_file_uris = [
            f"{cls.input_file_location}/{fname}" for fname in cls.group_input_file_names
        ]

        cls.namespace, cls.storage_path, cls.acn = groups._default_ns_path_cred()
        cls.namespace = cls.namespace.rstrip("/")
        cls.storage_path = cls.storage_path.rstrip("/")
        cls.destination = f"{cls.storage_path}/{testonly.random_name('file_test')}"

        cls.group_name = testonly.random_name("file_ingestion_test_group")
        cls.group_uri = f"tiledb://{cls.namespace}/{cls.group_name}"
        cls.group_destination = f"{cls.storage_path}/{cls.group_name}"
        groups.create(cls.group_name, storage_uri=cls.group_destination)

        cls.cleanup_these_uris = []
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        """Cleanup after the tests have run"""
        _cleanup_residual_test_arrays(array_uris=cls.cleanup_these_uris)
        groups.delete(cls.group_uri, recursive=True)
        return super().tearDownClass()

    def test_files_ingestion_udf(self):
        ingested_array_uris = file_ingestion.ingest_files_udf(
            dataset_uri=self.destination,
            file_uris=self.test_file_uris,
            acn=self.acn,
            namespace=self.namespace,
        )

        for uri in ingested_array_uris:
            array_info = info(uri)
            self.assertTrue(array_info.name in self.input_file_names)
            self.assertEqual(array_info.namespace, self.namespace)
        # Clean up
        _cleanup_residual_test_arrays(array_uris=ingested_array_uris)

    def test_files_ingestion_udf_into_group(self):
        ingested_array_uris = file_ingestion.ingest_files_udf(
            dataset_uri=self.group_destination,
            file_uris=self.group_test_file_uris,
            acn=self.acn,
            namespace=self.namespace,
        )

        file_ingestion.add_arrays_to_group_udf(
            array_uris=ingested_array_uris,
            group_uri=self.group_uri,
            config=client.Ctx().config().dict(),
            verbose=True,
        )

        groups.info(self.group_uri)
        # FIXME: Uncomment when CI has vfs access.
        # self.assertEqual(group_info.asset_count, len(self.group_test_file_uris))

        for uri in ingested_array_uris:
            array_info = info(uri)
            self.assertTrue(array_info.name in self.group_input_file_names)
            self.assertEqual(array_info.namespace, self.namespace)

        # Clean up
        _cleanup_residual_test_arrays(array_uris=ingested_array_uris)

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


class TestFileIndexing(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Setup test files, group and destinations once before the file tests start."""
        cls.input_file_location = "s3://tiledb-unittest/groups/file_indexing_test_files"
        # Files with name "input_file_<n[0, 4]>.pdf" have already been placed
        # in the "cls.input_file_location"
        cls.input_file_names = [f"file_to_index_{i}.pdf" for i in range(5)]
        cls.test_file_uris = [
            f"{cls.input_file_location}/{fname}" for fname in cls.input_file_names
        ]

        cls.namespace, cls.storage_path, cls.acn = groups._default_ns_path_cred()
        cls.namespace = cls.namespace.rstrip("/")
        cls.storage_path = cls.storage_path.rstrip("/")
        cls.destination = (
            f"{cls.storage_path}/{testonly.random_name('file-indexing-test')}"
        )

        # Ingest test files for testing
        cls.ingested_array_uris = file_ingestion.ingest_files_udf(
            dataset_uri=cls.destination,
            file_uris=cls.test_file_uris,
            acn=cls.acn,
            namespace=cls.namespace,
        )

        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        """Remove index testing residuals"""
        _cleanup_residual_test_arrays(array_uris=cls.ingested_array_uris)
        return super().tearDownClass()

    def tearDown(self) -> None:
        """Cleanup indexing arrays between tests"""
        groups.delete(self.created_index_uri, recursive=True)
        # FIXME: Not a nice way to cleanup vector search residuals:
        _cleanup_residual_test_arrays(
            array_uris=[
                f"tiledb://{self.namespace}/object_metadata",
                f"tiledb://{self.namespace}/updates",
                f"tiledb://{self.namespace}/shuffled_vectors",
                f"tiledb://{self.namespace}/shuffled_vector_ids",
                f"tiledb://{self.namespace}/partition_indexes",
                f"tiledb://{self.namespace}/partition_centroids",
            ]
        )
        return super().tearDown()

    @unittest.skip("Extremely slow execution times in the CI/CD client")
    def test_create_and_update_dataset_udf(self):
        with self.assertLogs(get_logger_wrapper()) as lg:
            # Create a vector search group with 1 file
            self.created_index_uri = file_indexing.create_dataset_udf(
                search_uri=self.input_file_location,
                index_uri=f"tiledb://{self.namespace}/{self.destination}",
                config=client.Ctx().config().dict(),
                max_files=3,
            )
            self.assertTrue("Creating dataset" in lg.output[0])

            # Update the group with all the available files
            file_indexing.create_dataset_udf(
                search_uri=self.input_file_location,
                index_uri=self.created_index_uri,
                config=client.Ctx().config().dict(),
            )
            self.assertTrue("Updating reader" in lg.output[1])
            index_group_info = groups.info(self.created_index_uri)
            self.assertIsNotNone(index_group_info)
            self.assertEqual(index_group_info.asset_count, 6)
