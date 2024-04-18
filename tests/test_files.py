import os
import tempfile
import unittest

import tiledb
from tiledb.cloud import client
from tiledb.cloud import groups
from tiledb.cloud._common import testonly
from tiledb.cloud.array import deregister_array
from tiledb.cloud.file_ingestion import chunk_results_udf
from tiledb.cloud.file_ingestion import ingest_files_udf
from tiledb.cloud.file_ingestion import sanitize_filename
from tiledb.vfs import VFS


class TestFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Setup test files, group and destinations once before the file tests start."""
        with tiledb.scope_ctx() as ctx:
            cls.vfs = VFS(ctx=ctx)

        cls.namespace, cls.storage_path, cls.acn = groups._default_ns_path_cred()
        cls.input_file_location = (
            f"{cls.storage_path}/{testonly.random_name('file_ingestion_test_input')}"
        )
        cls.destination = (
            f"{cls.storage_path}/{testonly.random_name('file_ingestion_test')}"
        )

        cls.input_file_names = []
        for i in range(5):
            with tempfile.TemporaryFile() as fp:
                fp.write(f"Test file {1}".encode())
                cls.input_file_names.append(f"in_file_{i}.txt")
                with cls.vfs.open(
                    f"{cls.input_file_location}/{cls.input_file_names[i]}", mode="wb"
                ) as fp_out:
                    fp_out.write(fp.read())

        group_name = testonly.random_name("file_ingestion_test_group")
        cls.group_uri = f"tiledb://{cls.namespace}/{group_name}"
        cls.group_destination = f"{cls.destination}/{testonly.random_name(group_name)}"
        groups.create(group_name, storage_uri=cls.group_destination)

        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        """Cleanup test and ingested files and folders after tests have finished."""
        cls.vfs.remove_dir(cls.input_file_location)
        cls.vfs.remove_dir(cls.group_destination)
        cls.vfs.remove_dir(cls.destination)

        groups.deregister(cls.group_uri)

        return super().tearDownClass()

    def tearDown(self) -> None:
        """Cleanup registered arrays between tests"""
        for fname in self.input_file_names:
            try:
                deregister_array(f"tiledb://{self.namespace}/{fname}")
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
            "test_4": ("test_mixed, file  name.pdf", "test_mixed_file__name.pdf"),
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
        ingest_files_udf(
            dataset_uri=self.namespace,
            file_uris=self.vfs.ls(self.input_file_location),
            destination=self.destination,
            acn=self.acn,
            namespace=self.namespace,
        )

        destination_files = [
            os.path.basename(fpath)
            for fpath in self.vfs.ls(self.destination)
            if fpath.endswith(
                ".txt"
            )  # Remove some ls output to check if all the files are present.
        ]
        self.assertListEqual(destination_files, self.input_file_names)

    def test_files_ingestion_udf_into_group(self):
        ingest_files_udf(
            dataset_uri=self.group_uri,
            file_uris=self.vfs.ls(self.input_file_location),
            destination=self.group_destination,
            acn=self.acn,
            namespace=self.namespace,
            config=client.Ctx().config().dict(),
        )

        destination_files = [
            os.path.basename(fpath)
            for fpath in self.vfs.ls(self.group_destination)
            if fpath.endswith(
                ".txt"
            )  # Remove some ls output to check if all the files are present.
        ]
        self.assertListEqual(destination_files, self.input_file_names)

        group = groups.info(self.group_uri)
        self.assertEqual(group.asset_count, len(self.input_file_names))
