import tiledb, tiledb.cloud
import sys, os, platform, unittest
import numpy as np
from tiledb.tests.common import DiskTestCase, assert_subarrays_equal

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


def threadtest_create_array(uri,):
    data = np.random.rand(20)
    schema = tiledb.libtiledb.schema_like(data)
    tiledb.Array.create(uri, schema)
    with tiledb.DenseArray(uri, "w") as A:
        A[:] = data


def threadtest_run_workers(uri):
    def worker(n, uri):
        with tiledb.DenseArray(uri) as A:
            res = A.shape

        return res

    import concurrent.futures

    executor_cls = concurrent.futures.ThreadPoolExecutor
    with executor_cls(max_workers=2) as executor:
        futures = [executor.submit(worker, n, uri) for n in range(0, 5)]
        res = [f.result() for f in concurrent.futures.as_completed(futures)]


class ThreadedImportTest(DiskTestCase):
    def test_threaded_import(self):
        import multiprocessing as mp

        uri = self.path("test_threaded_import")
        mpctx = mp.get_context("spawn")

        p = mpctx.Process(target=threadtest_create_array, args=(uri,))
        p.start()
        p.join(5)
        self.assertEqual(p.exitcode, 0)

        p2 = mpctx.Process(target=threadtest_run_workers, args=(uri,))
        p2.start()
        p2.join()
        self.assertEqual(p2.exitcode, 0)

        with tiledb.DenseArray(uri) as A:
            from tiledb.cloud.cloudarray import CloudArray

            self.assertTrue(CloudArray in A.__class__.__bases__)
