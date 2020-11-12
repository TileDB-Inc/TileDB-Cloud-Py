import tiledb
from tiledb.tests.common import DiskTestCase, assert_subarrays_equal
import numpy as np


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
