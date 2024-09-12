import hashlib
import os
import pathlib
import tempfile
import unittest

from tiledb.cloud import array
from tiledb.cloud import client
from tiledb.cloud._common import testonly
from tiledb.cloud.files import udfs as file_udfs
from tiledb.cloud.files import utils as file_utils

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
