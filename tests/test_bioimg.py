import unittest

from tiledb.cloud.bioimg.helpers import validate_io_paths


class BioimgTest(unittest.TestCase):
    def setUp(self) -> None:
        self.out_path = "out"
        self.accepted_pairs = {
            # 1 File -> Output: 1 Folder
            "test1": (["s3://test_in/a.tiff"], ["s3://test_out/b/"]),
            # 1 File -> Output: 1 File
            "test3": (["s3://test_in/a.tiff"], ["s3://test_out/b"]),
            # 1 Folder -> Output: 1 Folder
            "test5": (["s3://test_in/a/"], ["s3://test_out/b/"]),
            # Multiple Files -> Output: 1 Folder
            "test10": (
                ["s3://test_in/a.tiff", "s3://test_in/c.tiff"],
                ["s3://test_out/b/"],
            ),
            # Multiple Files -> Output: Multiple Files (Matching number)
            "test11": (
                ["s3://test_in/a.tiff", "s3://test_in/c.tiff"],
                ["s3://test_out/b", "s3://test_out/d"],
            ),
            # Multiple Folders -> Output: 1 Folder
            "test14": (["s3://test_in/a/", "s3://test_in/c/"], ["s3://test_out/b/"]),
            # Mix of Files and Folders -> Output: 1 Folder
            "test16": (["s3://test_in/a", "s3://test_in/c/"], ["s3://test_out/b/"]),
        }
        self.non_accepted_pairs = {
            # 1 File -> Output: Multiple Folders
            "test2": (
                ["s3://test_in/a.tiff"],
                ["s3://test_out/b/", "s3://test_out/c/"],
            ),
            # 1 File -> Output: Multiple Files
            "test4": (["s3://test_in/a"], ["s3://test_out/b", "s3://test_out/c"]),
            # 1 Folder -> Output: 1 File
            "test6": (["s3://test_in/a/"], ["s3://test_out/b"]),
            #  1 Folder -> Output: Multiple Files
            "test7": (["s3://test_in/a/"], ["s3://test_out/b", "s3://test_out/c"]),
            # 1 Folder -> Output: Multiple Folders
            "test8": (["s3://test_in/a/"], ["s3://test_out/b/", "s3://test_out/c/"]),
            # Multiple Files -> Output: 1 File
            "test9": (["s3://test_in/a", "s3://test_in/c"], ["s3://test_out/b"]),
            # Multiple Files -> Output: Multiple Files  (Non-Matching number)
            "test12": (
                ["s3://test_in/a", "s3://test_in/c"],
                ["s3://test_out/b", "s3://test_out/d", "s3://test_out/e"],
            ),
            # Multiple Files -> Output: Multiple Folders
            # (Matching or non-matching length)
            # Non-matching
            "test13a": (
                ["s3://test_in/a", "s3://test_in/c"],
                ["s3://test_out/b/", "s3://test_out/d/", "s3://test_out/e/"],
            ),
            # matching
            "test13b": (
                ["s3://test_in/a", "s3://test_in/c"],
                ["s3://test_out/b/", "s3://test_out/d/"],
            ),
            # Multiple Folders -> Output: 1 File
            "test15": (["s3://test_in/a/", "s3://test_in/c/"], ["s3://test_out/b"]),
            # Multiple Folders -> Output: Multiple Files
            # (Matching or non-matching length)
            # Matching
            "test17a": (
                ["s3://test_in/a/", "s3://test_in/c/"],
                ["s3://test_out/b", "s3://test_out/d", "s3://test_out/e"],
            ),
            # Non Matching
            "test17b": (
                ["s3://test_in/a/", "s3://test_in/c/"],
                ["s3://test_out/b", "s3://test_out/d"],
            ),
            # Multiple Folders -> Output: Multiple Folders (Non-Matching number)
            "test18": (
                ["s3://test_in/a/", "s3://test_in/c/"],
                ["s3://test_out/b", "s3://test_out/d", "s3://test_out/e"],
            ),
            # Mix of Files and Folders -> Output: 1 File
            "test20": (["s3://test_in/a", "s3://test_in/c/"], ["s3://test_out/b"]),
            # Mix of Files and Folders -> Output: Multiple Files and Folders
            "test21": (
                ["s3://test_in/a/", "s3://test_in/c"],
                ["s3://test_out/b", "s3://test_out/d/"],
            ),
        }
        return super().setUp()

    def test_validate_io_paths(self):
        # Accepted cases
        for test_name, io_tuple in self.accepted_pairs.items():
            source, dest = io_tuple
            source = [source] if isinstance(source, str) else source
            dest = [dest] if isinstance(dest, str) else dest
            print(f"{test_name}:", source, dest)
            validate_io_paths(source, dest)

        # Non Accepted cases
        for test_name, io_tuple in self.non_accepted_pairs.items():
            source, dest = io_tuple
            source = [source] if isinstance(source, str) else source
            dest = [dest] if isinstance(dest, str) else dest
            print(f"{test_name}:", source, dest)
            with self.assertRaises(ValueError):
                validate_io_paths(source, dest)
