import tiledb, tiledb.cloud
import os
import sys, os, platform, unittest

tiledb.cloud.login(token=os.environ["TILEDB_CLOUD_HELPER_VAR"])


class BasicTests(unittest.TestCase):
    def test_quickstart(self):
        with tiledb.open(
            "tiledb://TileDB-Inc/quickstart_dense", ctx=tiledb.cloud.Ctx()
        ) as A:
            print("quickstart_dense:")
            print(A[:])

        with tiledb.open(
            "tiledb://TileDB-Inc/quickstart_sparse", ctx=tiledb.cloud.Ctx()
        ) as A:
            print("quickstart_sparse:")
            print(A[:])
