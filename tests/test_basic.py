import tiledb, tiledb.cloud
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

            with self.assertRaises(TypeError):
                A.apply(None, [(0, 1)])

    def test_context(self):
        with self.assertRaises(ValueError):
            tiledb.cloud.Ctx({"rest.server_address": "1.1.1.1"})

        test_cache_size = str(int(3.14159 * 100000))
        ctx = tiledb.cloud.Ctx({"sm.tile_cache_size": test_cache_size})
        self.assertEqual(ctx.config()["sm.tile_cache_size"], test_cache_size)
