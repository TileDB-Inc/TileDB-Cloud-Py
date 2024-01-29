import unittest

from tiledb.cloud.bioimg.helpers import validate_io_paths


class BioimgTest(unittest.TestCase):
    def setUp(self) -> None:
        self.out_path = "out"
        self.accepted_pairs = {
            # One file in one file out
            "test1": ("s3://test_in/a.tiff", "s3://test_out/b"),
            # One file in one file out - out 1-elem list
            "test2": ("s3://test_in/a.tiff", ["s3://test_out/b"]),
            # One file in one file out - in 1-elem list
            "test3": (["s3://test_in/a.tiff"], "s3://test_out/b"),
            # One file in one file out - in & out 1-elem list
            "test4": (["s3://test_in/a.tiff"], ["s3://test_out/b"]),
            # One folder in one folder out
            "test5": ("s3://test_in/a/", "s3://test_out/b/"),
            # One folder in one file out - in & out 1-elem list
            "test6": (["s3://test_in/a/"], ["s3://test_out/b/"]),
            # One folder in one file out - out 1-elem list
            "test7": ("s3://test_in/a/", ["s3://test_out/b/"]),
            # One folder in one file out - in 1-elem list
            "test8": (["s3://test_in/a/"], "s3://test_out/b/"),
            # One file in one folder out
            "test9": ("s3://test_in/a.tiff", "s3://test_out/b/"),
            # One file in one folder out - in 1- elem list
            "test10": (["s3://test_in/a.tiff"], "s3://test_out/b/"),
            # One file in one folder out - out 1- elem list
            "test11": ("s3://test_in/a.tiff", ["s3://test_out/b/"]),
            # One file in one folder out - in & out 1- elem list
            "test12": (["s3://test_in/a.tiff"], ["s3://test_out/b/"]),
            # Multiple files in one folder out
            "test13": (
                ["s3://test_in/a.tiff", "s3://test_in/c.tiff"],
                "s3://test_out/b/",
            ),
            # Multiple files in one folder out
            "test14": (
                ["s3://test_in/a.tiff", "s3://test_in/c.tiff"],
                ["s3://test_out/b/"],
            ),
            # Multiple files in multiple files out - equal length
            # a -> b & c -> d
            "test15": (
                ["s3://test_in/a.tiff", "s3://test_in/c.tiff"],
                ["s3://test_out/b", "s3://test_out/d"],
            ),
        }

        return super().setUp()

    def test_validate_io_paths(self):
        # Accepted cases
        for test_name, io_tuple in self.accepted_pairs.items():
            source, dest = io_tuple
            print(f"{test_name}:", source, dest)
            validate_io_paths(source, dest)

        io_validation_ni_errors = {
            "test3": ("s3://test_in/a", ["s3://test_out/b/", "s3://test_out/d/"]),
        }

        for test_name, io_tuple in io_validation_ni_errors.items():
            source, dest = io_tuple
            print(f"{test_name}:", source, dest)
            with self.assertRaises(NotImplementedError):
                validate_io_paths(source, dest)

        io_validation_value_errors = {
            # Folder in - single file out
            "test1": ("s3://test_in/a/", "s3://test_out/b"),
            "test2": (["s3://test_in/a/"], "s3://test_out/b"),
            "test3": ("s3://test_in/a/", ["s3://test_out/b"]),
            "test4": (["s3://test_in/a/"], ["s3://test_out/b"]),
            # Input list cannot contain dir
            # One of the input is folder - out is folder
            "test16": (["s3://test_in/a", "s3://test_in/c/"], "s3://test_out/b/"),
            # One of the input is folder - out is folder and list
            "test17": (["s3://test_in/a", "s3://test_in/c/"], ["s3://test_out/b/"]),
        }

        for test_name, io_tuple in io_validation_value_errors.items():
            source, dest = io_tuple
            print(f"{test_name}:", source, dest)
            with self.assertRaises(ValueError):
                validate_io_paths(source, dest)

    # def test_build_io_uris_ingestion(self):
    #     out_suffix = "tdb"
    #     mock_contents = ['s3://test_in/a/x.svs', 's3://test_in/a/y.svs']
    #     with mock.patch.object(VFS, "ls", return_value=mock_contents):
    #         out_suffix = "tdb"
    #         for test_name, pair in self.accepted_pairs.items():
    #             source, output = pair
    #             source = [source] if isinstance(source, str) else source
    #             output = [output] if isinstance(output, str) else output

    #             paths = build_io_uris_ingestion(source,
    #                                     output,
    #                                     out_suffix,
    #                                     _SUPPORTED_EXTENSIONS)
    #             print(f"{test_name}: {pair} -> {paths}")
