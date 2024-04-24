import unittest

import tiledb
from tiledb.cloud import client
from tiledb.cloud import groups
from tiledb.cloud._common import testonly
from tiledb.cloud.array import delete_array
from tiledb.cloud.array import info
from tiledb.cloud.file_ingestion import add_arrays_to_group_udf
from tiledb.cloud.file_ingestion import chunk_results_udf
from tiledb.cloud.file_ingestion import ingest_files_udf
from tiledb.cloud.file_ingestion import sanitize_filename


class TestFiles(unittest.TestCase):
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
        cls.destination = cls.storage_path.rstrip("/")

        cls.group_name = testonly.random_name("file_ingestion_test_group")
        cls.group_uri = f"tiledb://{cls.namespace}/{cls.group_name}"
        cls.group_destination = f"{cls.destination}/{cls.group_name}"
        groups.create(cls.group_name, storage_uri=cls.group_destination)

        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        """Cleanup test and ingested files and folders after tests have finished."""
        groups.deregister(cls.group_uri)
        return super().tearDownClass()

    def tearDown(self) -> None:
        """Cleanup registered arrays between tests"""
        for fname in self.input_file_names:
            try:
                delete_array(f"tiledb://{self.namespace}/{fname}")
            except Exception:
                continue

        return super().tearDown()

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
                self.assertEqual(sanitize_filename(fname), sanitized)

    def test_chunk_results(self):
        subjects = {
            "test_1": (["1", "2", "3", "4", "5"], 3, [["1", "2", "3"], ["4", "5"]]),
            "test_2": (
                ("1", "2", "3", "4", "5"),
                1,
                [["1"], ["2"], ["3"], ["4"], ["5"]],
            ),
            "test_3": (["1", "2", "3", "4", "5"], None, [["1", "2", "3", "4", "5"]]),
            "test_4": (
                [["1"], ["2"], ["3"], ["4"], ["5"]],
                None,
                [["1", "2", "3", "4", "5"]],
            ),
            "test_5": (
                [["1"], ["2"], ["3"], ["4"], ["5"]],
                4,
                [["1", "2", "3", "4"], ["5"]],
            ),
            "test_6": (
                [["1"], ("2", "3"), ("4", "5")],
                None,
                [["1", "2", "3", "4", "5"]],
            ),
        }

        for test_name, (chunks_in, batch_size, chunks_out) in subjects.items():
            with self.subTest(f"case: {test_name}"):
                if batch_size is not None:
                    result = chunk_results_udf(
                        udf_results=chunks_in, batch_size=batch_size
                    )
                else:
                    result = chunk_results_udf(udf_results=chunks_in)

                self.assertEqual(result, chunks_out)

    def test_files_ingestion_udf(self):
        ingested_uris = ingest_files_udf(
            dataset_uri=self.destination,
            file_uris=self.test_file_uris,
            acn=self.acn,
            namespace=self.namespace,
        )
        self.assertEqual(len(ingested_uris), len(self.input_file_names))

        for fname in self.input_file_names:
            array_info = info(f"tiledb://{self.namespace}/{fname}")
            self.assertEqual(array_info.name, fname)
            self.assertEqual(array_info.namespace, self.namespace)

    def test_files_ingestion_udf_into_group(self):
        ingested_uris = ingest_files_udf(
            dataset_uri=self.group_destination,
            file_uris=self.test_file_uris,
            acn=self.acn,
            namespace=self.namespace,
        )
        self.assertEqual(len(ingested_uris), len(self.input_file_names))

        add_arrays_to_group_udf(
            array_uris=ingested_uris,
            namespace=self.namespace,
            register_name=self.group_name,
            config=client.Ctx().config().dict(),
        )

        group_info = groups.info(self.group_uri)
        self.assertEqual(group_info.asset_count, len(self.test_file_uris))

        for fname in self.input_file_names:
            array_info = info(f"tiledb://{self.namespace}/{fname}")
            self.assertEqual(array_info.name, fname)
            self.assertEqual(array_info.namespace, self.namespace)

    def test_files_ingestion_udf_into_bad_group_uri_raises(self):
        with self.assertRaises(tiledb.TileDBError):
            add_arrays_to_group_udf(
                array_uris=[f"tiledb://{self.namespace}/{self.input_file_names[0]}"],
                namespace="very-bad-namespace",
                register_name="bad-group",
                config=client.Ctx().config().dict(),
            )
