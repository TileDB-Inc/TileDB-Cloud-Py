import hashlib
import os.path
import tempfile
import unittest

from tiledb.cloud import file


class FileTests(unittest.TestCase):
    def test_simple_file_export(self):
        test_file = "tiledb://TileDB-Inc/VLDB17_TileDB"

        with tempfile.TemporaryDirectory() as dirpath:
            output_path = os.path.join(dirpath, "VLDB17_TileDB.pdf")
            file.export_file_local(test_file, output_path)

            with open(output_path, "rb") as exported:
                digest = hashlib.sha256(exported.read()).hexdigest()
                self.assertEqual(619181, exported.tell(), "exported file size")

            self.assertEqual(
                "14065c5debdf5eeff1478533a6484b9d26dc0b9d7a4cb228aa03f9e22f390300",
                digest,
            )
