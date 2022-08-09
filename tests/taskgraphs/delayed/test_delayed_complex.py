import unittest

import numpy as np

import tiledb
import tiledb.cloud
from tiledb.cloud import testonly
from tiledb.cloud.taskgraphs.delayed import Delayed
from tiledb.cloud.taskgraphs.delayed import DelayedArray
from tiledb.cloud.taskgraphs.delayed import DelayedArrayUDF

SPARSE = "tiledb://TileDB-Inc/quickstart_sparse"
DENSE = "tiledb://TileDB-Inc/quickstart_dense"


class ArraysTest(unittest.TestCase):
    def test_sum(self):
        with tiledb.open(SPARSE, ctx=tiledb.cloud.Ctx()) as arr:
            orig = arr[:]

        node = DelayedArrayUDF(
            SPARSE,
            lambda x, y: np.sum(x["a"]) + y,
            raw_ranges=((), ()),
            name="node",
        )(5)

        self.assertEqual(node.compute(30), np.sum(orig["a"]) + 5)

    def test_multi_sum(self):
        # TileDB array indices are [start:end) based, but ranges passed to
        # DelayedArray are [start, end].
        with tiledb.open(SPARSE, ctx=tiledb.cloud.Ctx()) as arr_sp:
            orig_sp = arr_sp[1:4, 1:4]
        with tiledb.open(DENSE, ctx=tiledb.cloud.Ctx()) as arr_de:
            orig_de = arr_de[1:4, 1:4]

        d_uri = Delayed("tiledb://TileDB-Inc/quickstart_{}".format)

        def sum_it(left, right):
            import numpy as np

            return np.sum(left["a"]) + np.sum(right["a"])

        one_to_three = Delayed(lambda *args: args)(1, 3)
        two_of_them = Delayed(lambda x: (x, x))

        # Also test passing upstream nodes as range parameters, along with
        # providing a mix of nodes and raw data.
        d_sum = Delayed(sum_it)(
            DelayedArray(d_uri("sparse"), raw_ranges=((1, 3), one_to_three)),
            DelayedArray(d_uri("dense"), raw_ranges=two_of_them(one_to_three)),
        )

        expected = np.sum(orig_sp["a"]) + np.sum(orig_de["a"])

        self.assertEqual(expected, d_sum.compute(30))

    def test_sum_by_name(self):
        with tiledb.open(SPARSE, ctx=tiledb.cloud.Ctx()) as arr:
            orig = arr[:]

        def sum_a(x):
            import numpy as np

            return np.sum(x["a"])

        with testonly.register_udf(sum_a) as sum_a_name:
            node = Delayed(sum_a_name)(DelayedArray(SPARSE, raw_ranges=((), ())))

            self.assertEqual(np.sum(orig["a"]), node.compute(30))
