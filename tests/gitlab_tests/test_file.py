import os
import unittest
from typing import List

from tqdm import tqdm

import tiledb
import tiledb.vfs
from tiledb.cloud import groups
from tiledb.cloud._common import testonly
from tiledb.cloud._common import utils
from tiledb.cloud.array import delete_array
from tiledb.cloud.files import ingestion as file_ingestion

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
print(os.getcwd())


def _cleanup_residual_test_arrays(array_uris: List[str]) -> None:
    """Deletes every array in a list and potential non unique tables"""
    for array_uri in array_uris:
        try:
            print(f"Deleting array: {array_uri}")
            delete_array(array_uri)
        except Exception as exc:
            error_msg = str(exc)
            print(f"-- {error_msg}")
            if "is not unique" in error_msg:
                namespace, _ = utils.split_uri(array_uri)
                uuids = error_msg[error_msg.find("[") + 1 : error_msg.find("]")]
                uuids = uuids.split(" ")
                for uid in tqdm(
                    uuids, desc=f"Deleting multiple arrays with URI: {array_uri}"
                ):
                    try:
                        delete_array(f"tiledb://{namespace}/{uid}")
                    except Exception:
                        continue
            continue


class TestFileIngestion(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Setup group and destinations once before the file tests start."""
        cls.vfs = tiledb.VFS()
        cls.s3_bucket = "s3://tiledb-cloud-py-ci"
        cls.test_files_folder = os.path.join(CURRENT_DIR, "data", "file_ingestion")

        cls.namespace, cls.storage_path, cls.acn = groups._default_ns_path_cred()
        cls.namespace = cls.namespace.rstrip("/")
        cls.storage_path = cls.storage_path.rstrip("/")
        cls.destination = f"{cls.storage_path}/{testonly.random_name('file_test')}"

        cls.group_name = testonly.random_name("file_ingestion_test_group")
        cls.group_uri = f"tiledb://{cls.namespace}/{cls.group_name}"
        cls.group_destination = f"{cls.storage_path}/{cls.group_name}"
        groups.create(cls.group_name, storage_uri=cls.group_destination)

        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        """Cleanup after the tests have run"""
        groups.delete(cls.group_uri, recursive=True)
        return super().tearDownClass()

    def setUp(self) -> None:
        s3_test_folder = testonly.random_name("file_ingestion_test_files")
        self.cleanup_arrays = []
        self.s3_test_folder_uri = f"{self.s3_bucket}/{s3_test_folder}"
        self.vfs.create_dir(self.s3_test_folder_uri)

        # VFS does not yet support copying across file systems.
        # Therefore we write the files in the folder instead
        # self.vfs.copy_file(
        #     old_uri=os.path.join(self.test_files_folder, fname),
        #     new_uri=f"{self.s3_test_folder_uri}/{testonly.random_name(fn)}.{suffix}",
        # )
        self.test_file_uris = []
        for fname in os.listdir(self.test_files_folder):
            fn, suffix = os.path.splitext(fname)
            s3_uri = f"{self.s3_test_folder_uri}/{testonly.random_name(fn)}{suffix}"
            with open(os.path.join(self.test_files_folder, fname)) as fp:
                with self.vfs.open(s3_uri, mode="wb") as vfp:
                    vfp.write(fp.read())
                    self.test_file_uris.append(s3_uri)

        return super().setUp()

    def tearDown(self) -> None:
        """Clean up ingested arrays and tmp file folder from s3"""
        _cleanup_residual_test_arrays(array_uris=self.cleanup_arrays)
        self.vfs.remove_dir(self.s3_test_folder_uri)
        return super().tearDown()

    def test_files_ingestion_udf(self):
        ingested_array_uris = file_ingestion.ingest_files_udf(
            dataset_uri=self.destination,
            file_uris=self.test_file_uris,
            acn=self.acn,
            namespace=self.namespace,
        )

        self.assertEqual(len(ingested_array_uris), len(self.test_file_uris))
        # Add arrays for cleanup on tearDown
        self.cleanup_arrays += ingested_array_uris


#     def test_files_ingestion_udf_into_group(self):
#         ingested_array_uris = file_ingestion.ingest_files_udf(
#             dataset_uri=self.group_destination,
#             file_uris=self.test_file_uris,
#             acn=self.acn,
#             namespace=self.namespace,
#         )

#         file_ingestion.add_arrays_to_group_udf(
#             array_uris=ingested_array_uris,
#             group_uri=self.group_uri,
#             config=client.Ctx().config().dict(),
#             verbose=True,
#         )

#         group_info = groups.info(self.group_uri)
#         self.assertEqual(group_info.asset_count, len(self.test_file_uris))
#         # Clean up
#         _cleanup_residual_test_arrays(array_uris=ingested_array_uris)

#     def test_add_array_to_group_udf_raises_bad_namespace_error(self):
#         with self.assertRaises(tiledb.TileDBError):
#             file_ingestion.add_arrays_to_group_udf(
#                 array_uris=[f"tiledb://{self.namespace}/{self.test_file_uris[0]}"],
#                 group_uri=f"tiledb://very-bad-namespace/{self.group_name}",
#                 config=client.Ctx().config().dict(),
#                 verbose=True,
#             )

#     def test_add_array_to_group_udf_non_existing_group_raises_value_error(self):
#         with self.assertRaises(ValueError):
#             file_ingestion.add_arrays_to_group_udf(
#                 array_uris=[f"tiledb://{self.namespace}/{self.test_file_uris[0]}"],
#                 group_uri=f"tiledb://{self.namespace}/non-existing-group",
#                 config=client.Ctx().config().dict(),
#                 verbose=True,
#             )


# class TestFileIndexing(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         """
#         Setup test files, group and destinations once before the file tests start.
#         """
#         cls.input_file_location = "s3://tiledb-unittest/groups/file_indexing_test_files"
#         # Files with name "input_file_<n[0, 4]>.pdf" have already been placed
#         # in the "cls.input_file_location"
#         cls.input_file_names = [f"file_to_index_{i}.pdf" for i in range(5)]
#         cls.test_file_uris = [
#             f"{cls.input_file_location}/{fname}" for fname in cls.input_file_names
#         ]

#         cls.namespace, cls.storage_path, cls.acn = groups._default_ns_path_cred()
#         cls.namespace = cls.namespace.rstrip("/")
#         cls.storage_path = cls.storage_path.rstrip("/")
#         cls.destination = (
#             f"{cls.storage_path}/{testonly.random_name('file-indexing-test')}"
#         )

#         # Ingest test files for testing
#         cls.ingested_array_uris = file_ingestion.ingest_files_udf(
#             dataset_uri=cls.destination,
#             file_uris=cls.test_file_uris,
#             acn=cls.acn,
#             namespace=cls.namespace,
#         )

#         return super().setUpClass()

#     @classmethod
#     def tearDownClass(cls) -> None:
#         """Remove index testing residuals"""
#         _cleanup_residual_test_arrays(array_uris=cls.ingested_array_uris)
#         return super().tearDownClass()

#     def tearDown(self) -> None:
#         """Cleanup indexing arrays between tests"""
#         groups.delete(self.created_index_uri, recursive=True)
#         # FIXME: Not a nice way to cleanup vector search residuals:
#         _cleanup_residual_test_arrays(
#             array_uris=[
#                 f"tiledb://{self.namespace}/object_metadata",
#                 f"tiledb://{self.namespace}/updates",
#                 f"tiledb://{self.namespace}/shuffled_vectors",
#                 f"tiledb://{self.namespace}/shuffled_vector_ids",
#                 f"tiledb://{self.namespace}/partition_indexes",
#                 f"tiledb://{self.namespace}/partition_centroids",
#             ]
#         )
#         return super().tearDown()

#     @unittest.skip("Extremely slow execution times in the CI/CD client")
#     def test_create_and_update_dataset_udf(self):
#         with self.assertLogs(get_logger_wrapper()) as lg:
#             # Create a vector search group with 1 file
#             self.created_index_uri = file_indexing.create_dataset_udf(
#                 search_uri=self.input_file_location,
#                 index_uri=f"tiledb://{self.namespace}/{self.destination}",
#                 config=client.Ctx().config().dict(),
#                 max_files=3,
#             )
#             self.assertTrue("Creating dataset" in lg.output[0])

#             # Update the group with all the available files
#             file_indexing.create_dataset_udf(
#                 search_uri=self.input_file_location,
#                 index_uri=self.created_index_uri,
#                 config=client.Ctx().config().dict(),
#             )
#             self.assertTrue("Updating reader" in lg.output[1])
#             index_group_info = groups.info(self.created_index_uri)
#             self.assertIsNotNone(index_group_info)
#             self.assertEqual(index_group_info.asset_count, 6)
