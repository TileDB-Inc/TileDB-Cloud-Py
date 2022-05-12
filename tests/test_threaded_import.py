import numpy as np

import tiledb
from tiledb.tests.common import DiskTestCase
from tiledb.tests.common import assert_subarrays_equal


def threadtest_create_array(uri):
    data = np.random.rand(20)
    schema = tiledb.libtiledb.schema_like(data)
    tiledb.Array.create(uri, schema)
    with tiledb.open(uri, "w") as A:
        A[:] = data


def threadtest_run_workers(uri):
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(worker, uri) for _ in range(0, 5)]
        res = [f.result() for f in concurrent.futures.as_completed(futures)]
        assert all(res), res


def worker(uri):
    with tiledb.open(uri) as A:
        pass
    from tiledb.cloud.cloudarray import CloudArray

    return isinstance(A, CloudArray)


class TestThreadedImport(DiskTestCase):
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
        # fixed by https://github.com/TileDB-Inc/TileDB-Py/pull/1096
        self.assertEqual(p2.exitcode, 1 if tiledb.__version__ < "0.15.2" else 0)
