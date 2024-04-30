import unittest
from time import sleep
from typing import List

import tiledb
from tiledb.cloud import client
from tiledb.cloud import groups
from tiledb.cloud._common import testonly
from tiledb.cloud._common import utils
from tiledb.cloud.array import delete_array
from tiledb.cloud.array import info
from tiledb.cloud.dag import server_logs
from tiledb.cloud.file_ingestion import add_arrays_to_group_udf
from tiledb.cloud.file_ingestion import chunk_results_udf
from tiledb.cloud.file_ingestion import ingest_files
from tiledb.cloud.file_ingestion import ingest_files_udf
from tiledb.cloud.file_ingestion import sanitize_filename
from tiledb.cloud.rest_api import ApiException
from tiledb.cloud.rest_api import TaskGraphLogStatus


class BaseFileIngestionTestClass(unittest.TestCase):
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
            ],
            handle_not_unique=True,
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
    def __cleanup_residual_test_arrays(
        array_uris: List[str],
        handle_not_unique: bool = False,
    ) -> None:
        """Deletes every array in a list"""
        not_unique = []
        for array_uri in array_uris:
            try:
                delete_array(array_uri)
            except Exception as exc:
                error_msg = str(exc)
                if "is not unique" in error_msg:
                    not_unique += error_msg[
                        error_msg.find("[") + 1 : error_msg.find("]")
                    ].split(" ")
                continue

        if handle_not_unique and len(not_unique) > 0:
            namespace, _ = utils.split_uri(array_uris[0])
            for uid in not_unique:
                try:
                    delete_array(f"tiledb://{namespace}/{uid}")
                except Exception:
                    continue


class TestFiles(BaseFileIngestionTestClass):
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
        self.ingested_array_uris = ingest_files_udf(
            dataset_uri=self.destination,
            file_uris=self.test_file_uris,
            acn=self.acn,
            namespace=self.namespace,
            verbose=True,
        )
        self.assertEqual(len(self.ingested_array_uris), len(self.input_file_names))

        for uri in self.ingested_array_uris:
            array_info = info(uri)
            self.assertTrue(array_info.name in self.input_file_names)
            self.assertEqual(array_info.namespace, self.namespace)

    def test_files_ingestion_udf_into_group(self):
        self.ingested_array_uris = ingest_files_udf(
            dataset_uri=self.group_destination,
            file_uris=self.test_file_uris,
            acn=self.acn,
            namespace=self.namespace,
            verbose=True,
        )
        self.assertEqual(len(self.ingested_array_uris), len(self.input_file_names))

        add_arrays_to_group_udf(
            array_uris=self.ingested_array_uris,
            group_uri=self.group_uri,
            config=client.Ctx().config().dict(),
            verbose=True,
        )

        group_info = groups.info(self.group_uri)
        self.assertEqual(group_info.asset_count, len(self.test_file_uris))

        for uri in self.ingested_array_uris:
            array_info = info(uri)
            self.assertTrue(array_info.name in self.input_file_names)
            self.assertEqual(array_info.namespace, self.namespace)

    def test_add_array_to_group_udf_raises_bad_namespace_error(self):
        with self.assertRaises(tiledb.TileDBError):
            add_arrays_to_group_udf(
                array_uris=[f"tiledb://{self.namespace}/{self.input_file_names[0]}"],
                group_uri=f"tiledb://very-bad-namespace/{self.group_name}",
                config=client.Ctx().config().dict(),
                verbose=True,
            )

    def test_add_array_to_group_udf_non_existing_group_raises_value_error(self):
        with self.assertRaises(ValueError):
            add_arrays_to_group_udf(
                array_uris=[f"tiledb://{self.namespace}/{self.input_file_names[0]}"],
                group_uri=f"tiledb://{self.namespace}/non-existing-group",
                config=client.Ctx().config().dict(),
                verbose=True,
            )


class TestFilesIngestionDAG(BaseFileIngestionTestClass):
    def test_ingest_files(self):
        dag_id = ingest_files(
            dataset_uri=self.destination,
            search_uri=self.input_file_location,
            namespace=self.namespace,
            acn=self.acn,
            batch_size=(len(self.input_file_names) // 2) + 1,
            taskgraph_name="test_ingest_files",
        )
        logs = server_logs(dag_or_id=dag_id, namespace=self.namespace)
        self.assertEqual(len(logs.nodes), 3)
        self.assertTrue("Find file URIs" in logs.nodes[0].name)
        self.assertTrue("Break Found Files in Chunks" in logs.nodes[1].name)
        self.assertTrue("Ingest file URIs" in logs.nodes[2].name)

        while logs.status in [TaskGraphLogStatus.RUNNING, TaskGraphLogStatus.SUBMITTED]:
            sleep(2)
            logs = server_logs(dag_or_id=dag_id, namespace=self.namespace)
        self.assertEqual(logs.status, TaskGraphLogStatus.SUCCEEDED)

    def test_ingest_files_into_group(self):
        dag_id = ingest_files(
            dataset_uri=self.group_destination,
            search_uri=self.input_file_location,
            group_uri=self.group_uri,
            namespace=self.namespace,
            acn=self.acn,
            batch_size=(len(self.input_file_names) // 2) + 1,
            taskgraph_name="test_ingest_files_into_group",
        )
        logs = server_logs(dag_or_id=dag_id, namespace=self.namespace)
        self.assertEqual(len(logs.nodes), 4)
        self.assertTrue("Find file URIs" in logs.nodes[0].name)
        self.assertTrue("Break Found Files in Chunks" in logs.nodes[1].name)
        self.assertTrue("Ingest file URIs" in logs.nodes[2].name)
        self.assertTrue("add_arrays_to_group_udf" in logs.nodes[3].name)

        while logs.status in [TaskGraphLogStatus.RUNNING, TaskGraphLogStatus.SUBMITTED]:
            sleep(2)
            logs = server_logs(dag_or_id=dag_id, namespace=self.namespace)
        self.assertEqual(logs.status, TaskGraphLogStatus.SUCCEEDED)

    def test_bad_namespace_raises_api_exception(self):
        with self.assertRaises(ApiException) as exc:
            malformed_uri = f"tiledb://very-bad-namespace/{self.group_name}"
            ingest_files(
                dataset_uri=self.destination,
                search_uri=self.input_file_location,
                group_uri=malformed_uri,
            )
            self.assertEqual(404, exc.status)
