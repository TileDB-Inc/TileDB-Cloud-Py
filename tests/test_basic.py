import tiledb, tiledb.cloud
import sys, os, platform, unittest
import numpy as np
from tiledb.cloud import cloudarray

tiledb.cloud.login(
    token=os.environ["TILEDB_CLOUD_HELPER_VAR"],
    host=os.environ.get("TILEDB_CLOUD_REST_HOST", None),
)


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

            import numpy

            orig = A[:]
            self.assertEqual(
                A.apply(lambda x: numpy.sum(x["a"]), [(1, 4), (1, 4)]),
                numpy.sum(orig["a"]),
            )

            orig = A.multi_index[[1, slice(2, 4)], [slice(1, 2), 4]]
            self.assertEqual(
                A.apply(lambda x: numpy.sum(x["a"]), [[1, slice(2, 4)], [(1, 2), 4]]),
                numpy.sum(orig["a"]),
            )

    def test_context(self):
        with self.assertRaises(ValueError):
            tiledb.cloud.Ctx({"rest.server_address": "1.1.1.1"})

        test_cache_size = str(int(3.14159 * 100000))
        ctx = tiledb.cloud.Ctx({"sm.tile_cache_size": test_cache_size})
        self.assertEqual(ctx.config()["sm.tile_cache_size"], test_cache_size)


class RangesTest(unittest.TestCase):
    def test_parse_ranges(self):
        ibid = lambda x, y, z: (x, y, z)
        parse_ranges = lambda x: cloudarray.parse_ranges(x, ibid)

        a = [1]
        b = [(0, 1, 1)]
        self.assertEqual(parse_ranges(a), b)

        a = [1, 2]
        b = [(0, 1, 1), (1, 2, 2)]
        self.assertEqual(parse_ranges(a), b)

        a = [[1, 2], 3]
        b = [(0, 1, 1), (0, 2, 2), (1, 3, 3)]
        self.assertEqual(parse_ranges(a), b)

        # tuples
        a = [1, (1, 2)]
        b = [(0, 1, 1), (1, 1, 2)]
        self.assertEqual(parse_ranges(a), b)

        a = [1, [(1, 2)]]
        b = [(0, 1, 1), (1, 1, 2)]
        self.assertEqual(parse_ranges(a), b)

        a = [1, [slice(1, 2)]]
        b = [(0, 1, 1), (1, 1, 2)]
        self.assertEqual(parse_ranges(a), b)

        a = [1, slice(2, 3)], [(1, 2), 4]
        b = [(0, 1, 1), (0, 2, 3), (1, 1, 2), (1, 4, 4)]
        self.assertEqual(parse_ranges(a), b)
