import os
import tempfile
import unittest

import tiledb
import tiledb.cloud

tiledb.cloud.login(
    token=os.environ["TILEDB_CLOUD_HELPER_VAR"],
    host=os.environ.get("TILEDB_CLOUD_REST_HOST", None),
)


class FileTests(unittest.TestCase):
    def test_simple_file_export(self):
        test_file = "tiledb://TileDB-Inc/VLDB17_TileDB"

        with tempfile.TemporaryDirectory() as dirpath:
            output_path = os.path.join(dirpath, "VLDB17_TileDB.pdf")
            tiledb.cloud.file.export_file_local(test_file, output_path)

            self.assertTrue(os.path.exists(output_path))
            self.assertGreater(os.path.getsize(output_path), 0)
