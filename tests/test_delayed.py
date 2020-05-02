import time
import unittest
import os

import numpy as np
from tiledb.cloud.compute import Delayed, DelayedSQL, DelayedArrayUDF, Status
import tiledb.cloud

tiledb.cloud.login(
    token=os.environ["TILEDB_CLOUD_HELPER_VAR"],
    host=os.environ.get("TILEDB_CLOUD_REST_HOST", None),
)


class DelayedClassTest(unittest.TestCase):
    def test_simple_local_delayed(self):

        node_1 = Delayed(np.median, name="node_1", local=True)
        node_1([1, 2, 3])
        node_2 = Delayed(lambda x: x * 2, name="node_2", local=True)(node_1)
        node_3 = Delayed(lambda x: x * 2, name="node_3", local=True)(node_2)

        node_3.compute()

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), 8)

    def test_kwargs(self):
        def string_multi(multiplier, str=None):
            return int(multiplier) * str

        node_1 = Delayed(np.median, local=True, name="node_1")([1, 2, 3])
        node_2 = Delayed(lambda x: x * 2, name="node_2")(node_1)
        node_3 = Delayed(string_multi, local=True, name="node_3")(node_2, str="a")

        node_3.compute()

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), "aaaa")

    def test_multi_dependencies(self):
        node_1 = Delayed(np.median, name="multi_node_1", local=True)([1, 2, 3])
        l = lambda x: x * 2
        node_2 = Delayed(l, local=True, name="multi_node_2")(node_1)
        node_3 = Delayed(l, local=True, name="multi_node_3")(node_2)
        node_4 = Delayed(l, local=True, name="multi_node_4")(node_2)
        node_5 = Delayed(l, local=True, name="multi_node_5")(node_2)

        node_6 = Delayed(lambda *x: np.sum(x), local=True, name="multi_node_6")(
            node_3, node_4, node_5
        )

        node_6.compute()

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), 8)
        self.assertEqual(node_4.result(), 8)
        self.assertEqual(node_5.result(), 8)
        self.assertEqual(node_6.result(), 24)


class DelayedFailureTest(unittest.TestCase):
    def test_failure(self):
        with self.assertRaises(TypeError):
            node = Delayed(lambda x: x * 2, local=True, name="node")(np.median)

            node.compute()

            self.assertEqual(node.result(), None)
            self.assertIsNotNone(node.dag)
            self.assertEqual(node.status, Status.FAILED)
            self.assertEqual(
                str(node.error),
                "unsupported operand type(s) for *: 'function' and 'int'",
            )

    def test_dependency_fail_early(self):

        with self.assertRaises(TypeError):
            node = Delayed(lambda x: x * 2, local=True, name="node")(np.median)
            node2 = Delayed(lambda x: x * 2, local=True, name="node2")(10)
            node2.depends_on(node)

            node2.compute()

            self.assertEqual(node.result(), None)
            self.assertEqual(node.status, Status.FAILED)
            self.assertEqual(
                str(node.error),
                "unsupported operand type(s) for *: 'function' and 'int'",
            )
            self.assertEqual(node2.result(), None)
            self.assertEqual(node2.status, Status.NOT_STARTED)
            self.assertEqual(node2.dag.status, Status.FAILED)


class DelayedCancelTest(unittest.TestCase):
    def test_cancel(self):
        with self.assertRaises(TimeoutError):
            node = Delayed(time.sleep, local=True, name="multi_node_2")(100)
            node_2 = Delayed(np.mean, local=True, name="multi_node_2")([1, 1])
            node_2.depends_on(node)

            # Set timeout to 1 second, the dependency on node will wait for 100 second, so we'll timeout and cancel
            node_2.set_timeout(1)

            node_2.compute()

            # Cancel DAG
            node_2.dag.cancel()

            self.assertEqual(node.result(), None)
            self.assertEqual(node.status, Status.CANCELLED)
            self.assertEqual(node_2.dag.status, Status.CANCELLED)


class DelayedCloudApplyTest(unittest.TestCase):
    def test_array_apply(self):

        uri = "tiledb://TileDB-inc/quickstart_sparse"
        with tiledb.open(uri, ctx=tiledb.cloud.Ctx()) as A:
            orig = A[:]

        import numpy

        node = DelayedArrayUDF(uri, lambda x: numpy.sum(x["a"]), name="node")(
            [(1, 4), (1, 4)]
        )

        node.compute()

        self.assertEqual(node.result(), numpy.sum(orig["a"]))

    def test_udf_exec(self):
        import numpy

        node = Delayed(lambda x: numpy.sum(x), name="node")([1, 4, 10, 40])

        node.compute()

        self.assertEqual(node.result(), 55)

    def test_sql_exec(self):

        uri = "tiledb://TileDB-inc/quickstart_sparse"
        with tiledb.open(uri, ctx=tiledb.cloud.Ctx()) as A:
            orig = A[:]

        import numpy

        node = DelayedSQL("select SUM(`a`) as a from `{}`".format(uri), name="node")

        node.compute()

        self.assertEqual(node.result()["a"][0], numpy.sum(orig["a"]))

    def test_apply_exec_multiple(self):

        uri_sparse = "tiledb://TileDB-inc/quickstart_sparse"
        uri_dense = "tiledb://TileDB-inc/quickstart_dense"
        with tiledb.open(uri_sparse, ctx=tiledb.cloud.Ctx()) as A:
            orig = A[:]

        with tiledb.open(uri_dense, ctx=tiledb.cloud.Ctx()) as A:
            orig_dense = A[:]

        import numpy

        node_array_apply = DelayedArrayUDF(
            uri_sparse, lambda x: numpy.sum(x["a"]), name="node_array_apply"
        )([(1, 4), (1, 4)])
        node_sql = DelayedSQL(
            "select SUM(`a`) as a from `{}`".format(uri_dense), name="node_sql",
        )

        def mean(args):
            import numpy
            import pandas

            for i in range(len(args)):
                item = args[i]
                if isinstance(item, pandas.DataFrame):
                    args[i] = item["a"][0]

            return numpy.mean(args)

        node_exec = Delayed(mean, name="node_exec")([node_array_apply, node_sql])

        node_exec.compute()

        self.assertEqual(node_array_apply.result(), numpy.sum(orig["a"]))
        self.assertEqual(node_sql.result()["a"][0], numpy.sum(orig_dense["a"]))
        self.assertEqual(
            node_exec.result(),
            numpy.mean([numpy.sum(orig["a"]), numpy.sum(orig_dense["a"])]),
        )
        self.assertEqual(node_exec.dag.status, Status.COMPLETED)

    def test_apply_exec_multiple_2(self):

        uri_sparse = "tiledb://TileDB-inc/quickstart_sparse"
        uri_dense = "tiledb://TileDB-inc/quickstart_dense"
        with tiledb.open(uri_sparse, ctx=tiledb.cloud.Ctx()) as A:
            orig = A[:]

        with tiledb.open(uri_dense, ctx=tiledb.cloud.Ctx()) as A:
            orig_dense = A[:]

        import numpy

        node_local = Delayed(lambda x: x * 2, local=True)(100)

        node_array_apply = DelayedArrayUDF(
            uri_sparse, lambda x: numpy.sum(x["a"]), name="node_array_apply"
        )([(1, 4), (1, 4)])
        node_sql = DelayedSQL(
            "select SUM(`a`) as a from `{}`".format(uri_dense), name="node_sql"
        )

        def mean(args):
            import numpy
            import pandas

            for i in range(len(args)):
                item = args[i]
                if isinstance(item, pandas.DataFrame):
                    args[i] = item["a"][0]

            return numpy.mean(args)

        node_exec = Delayed(func_exec=mean, name="node_exec")(
            [node_local, node_array_apply, node_sql],
        )

        node_exec.compute()

        self.assertEqual(node_local.result(), 200)
        self.assertEqual(node_array_apply.result(), numpy.sum(orig["a"]))
        self.assertEqual(node_sql.result()["a"][0], numpy.sum(orig_dense["a"]))
        self.assertEqual(
            node_exec.result(),
            numpy.mean([200, numpy.sum(orig["a"]), numpy.sum(orig_dense["a"])]),
        )
        self.assertEqual(node_exec.status, Status.COMPLETED)

    def test_name_to_task_name(self):

        uri_sparse = "tiledb://TileDB-inc/quickstart_sparse"
        uri_dense = "tiledb://TileDB-inc/quickstart_dense"
        with tiledb.open(uri_sparse, ctx=tiledb.cloud.Ctx()) as A:
            orig = A[:]

        with tiledb.open(uri_dense, ctx=tiledb.cloud.Ctx()) as A:
            orig_dense = A[:]

        import numpy

        node_local = Delayed(lambda x: x * 2, local=True)(100)

        node_array_apply = DelayedArrayUDF(
            uri_sparse, lambda x: numpy.sum(x["a"]), name="node_array_apply"
        )([(1, 4), (1, 4)])
        node_sql = DelayedSQL(
            "select SUM(`a`) as a from `{}`".format(uri_dense), name="node_sql"
        )

        def mean(args):
            import numpy
            import pandas

            for i in range(len(args)):
                item = args[i]
                if isinstance(item, pandas.DataFrame):
                    args[i] = item["a"][0]

            return numpy.mean(args)

        node_exec = Delayed(func_exec=mean, name="node_exec")(
            [node_local, node_array_apply, node_sql],
        )

        node_exec.compute()

        self.assertEqual(node_local.result(), 200)
        self.assertEqual(node_array_apply.result(), numpy.sum(orig["a"]))
        self.assertEqual(node_sql.result()["a"][0], numpy.sum(orig_dense["a"]))
        self.assertEqual(
            node_exec.result(),
            numpy.mean([200, numpy.sum(orig["a"]), numpy.sum(orig_dense["a"])]),
        )
        self.assertEqual(node_exec.status, Status.COMPLETED)
