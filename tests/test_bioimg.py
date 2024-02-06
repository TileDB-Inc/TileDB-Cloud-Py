import unittest

from tiledb.cloud.bioimg.helpers import validate_io_paths


class BioimgTest(unittest.TestCase):
    def test_validate_io_paths_accepted(self):
        # Accepted cases
        accepted_pairs = {
            # 1 File -> Output: 1 Folder
            "test1": (["s3://test_in/a.tiff"], ["s3://test_out/b/"]),
            # 1 File -> Output: 1 File
            "test3": (["s3://test_in/a.tiff"], ["s3://test_out/b"]),
            # 1 Folder -> Output: 1 Folder
            "test5": (["s3://test_in/a/"], ["s3://test_out/b/"]),
            # Multiple Files -> Output: Multiple Files (Matching number)
            "test11": (
                ["s3://test_in/a.tiff", "s3://test_in/c.tiff"],
                ["s3://test_out/b", "s3://test_out/d"],
            ),
        }
        for test_name, (source, dest) in accepted_pairs.items():
            with self.subTest(f"case: {test_name}"):
                validate_io_paths(source, dest)

        # Non Accepted cases
        non_accepted_pairs = {
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
            # Multiple Folders -> Output: 1 Folder
            "test22": (["s3://test_in/a/", "s3://test_in/c/"], ["s3://test_out/b/"]),
            # Mix of Files and Folders -> Output: 1 Folder
            "test23": (["s3://test_in/a", "s3://test_in/c/"], ["s3://test_out/b/"]),
            # Multiple Files -> Output: 1 Folder
            "test10": (
                ["s3://test_in/a.tiff", "s3://test_in/c.tiff"],
                ["s3://test_out/b/"],
            ),
        }
        for test_name, (source, dest) in non_accepted_pairs.items():
            with self.subTest(f"case: {test_name}"):
                with self.assertRaises(ValueError):
                    validate_io_paths(source, dest)
