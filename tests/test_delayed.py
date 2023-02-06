import operator
import os
import shutil
import tempfile
import unittest
from concurrent import futures

import numpy as np

import tiledb.cloud
from tiledb.cloud import testonly
from tiledb.cloud.compute import Delayed
from tiledb.cloud.compute import DelayedArrayUDF
from tiledb.cloud.compute import DelayedSQL
from tiledb.cloud.compute.delayed import DelayedMultiArrayUDF
from tiledb.cloud.compute.delayed import ParentFailedError
from tiledb.cloud.taskgraphs.executor import Status


class DelayedClassTest(unittest.TestCase):
    def test_simple_local_delayed(self):

        node_1 = Delayed(np.median, name="node_1", local=True)
        node_1([1, 2, 3])
        node_2 = Delayed(lambda x: x * 2, name="node_2", local=True)(node_1)
        node_3 = Delayed(lambda x: x * 2, name="node_3", local=True)(node_2)

        # Add timeout so we don't wait forever in CI
        node_3.set_timeout(30)
        node_3.compute()

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), 8)

    def test_simple_delayed_batch_execution(self):

        node_1 = Delayed(np.median, name="node_1")
        node_1([1, 2, 3])
        node_2 = Delayed(lambda x: x * 2, name="node_2")(node_1)
        node_3 = Delayed(lambda x: x * 2, name="node_3")(node_2)

        # Add timeout so we don't wait forever in CI
        node_3.set_timeout(300)
        node_3.compute(batch=True)

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), 8)

    def test_simple_delayed_failure_batch_execution(self):
        def fail(x):
            raise NotImplementedError("UDF failure")

        node_1 = Delayed(np.median, name="node_1")
        node_1([1, 2, 3])
        node_2 = Delayed(fail, name="node_2")(node_1)
        node_3 = Delayed(lambda x: x * 2, name="node_3")(node_2)

        # Add timeout so we don't wait forever in CI
        node_3.set_timeout(300)
        with self.assertRaises(RuntimeError):
            node_3.compute(batch=True)

        self.assertEqual(node_1.result(), 2)
        with self.assertRaises(RuntimeError):
            node_2.result()
        self.assertTrue(isinstance(node_2.exception(), NotImplementedError))
        self.assertEqual(str(node_2.exception()), "UDF failure")
        with self.assertRaises(RuntimeError):
            node_3.result()
        self.assertEqual(node_3.exception(), None)

    def test_kwargs(self):
        def string_multi(multiplier, str=None):
            return int(multiplier) * str

        node_1 = Delayed(np.median, local=True, name="node_1")([1, 2, 3])
        node_2 = Delayed(lambda x: x * 2, name="node_2")(node_1)
        node_3 = Delayed(string_multi, local=True, name="node_3")(node_2, str="a")

        # Add timeout so we don't wait forever in CI
        node_3.set_timeout(30)
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

        # Add timeout so we don't wait forever in CI
        node_6.set_timeout(30)
        node_6.compute()

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), 8)
        self.assertEqual(node_4.result(), 8)
        self.assertEqual(node_5.result(), 8)
        self.assertEqual(node_6.result(), 24)

    def test_two_delayeds(self):
        node_1 = Delayed(len)([1, 2, 3])
        node_1.set_timeout(30)
        node_1.compute()
        self.assertEqual(node_1.result(), 3)

        node_2 = Delayed("result was {}".format)(node_1)
        node_2.set_timeout(30)
        node_2.compute()
        self.assertEqual(node_2.result(), "result was 3")


class DelayedFailureTest(unittest.TestCase):
    def test_failure(self):
        node = Delayed(lambda x: x * 2, local=True, name="node")(np.median)
        # Add timeout so we don't wait forever in CI
        node.set_timeout(30)

        with self.assertRaises(TypeError):
            node.compute()

        self.assertEqual(node.status, Status.FAILED)
        self.assertEqual(
            str(node.error),
            "unsupported operand type(s) for *: 'function' and 'int'",
        )
        with self.assertRaises(TypeError):
            node.result()

    def test_dependency_fail_early(self):
        node = Delayed(lambda x: x * 2, local=True, name="node")(np.median)
        node2 = Delayed(lambda x: x * 2, local=True, name="node2")(10)
        node2.depends_on(node)
        # Add timeout so we don't wait forever in CI
        node2.set_timeout(30)

        with self.assertRaisesRegex(ParentFailedError, r"operand type\(s\)") as cm:
            node2.compute()
        self.assertEqual(node, cm.exception.node)

        self.assertEqual(node.status, Status.FAILED)
        self.assertIn(
            "unsupported operand type(s) for *: 'function' and 'int'",
            str(node.error),
        )
        with self.assertRaises(TypeError):
            node.result()

        node2.wait(1)
        self.assertEqual(node2.status, Status.PARENT_FAILED)
        with self.assertRaises(futures.CancelledError):
            node2.result()

    def test_failure_retry(self):
        n1 = Delayed(self._fail_once_func(), 5, local=True)
        n1.set_timeout(5)
        n2 = Delayed(operator.pow, n1, n1)
        n2.set_timeout(15)
        with self.assertRaises(futures.CancelledError):
            n2.compute()
        with self.assertRaises(FloatingPointError):
            n1.result()
        self.assertEqual(n2.status, Status.PARENT_FAILED)
        self.assertEqual(n1.status, Status.FAILED)
        n1.retry()
        self.assertEqual(n2.result(15), 3125)

    def _fail_once_func(self):
        dir = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(dir))

        def fail_once(val=None):
            try:
                open(os.path.join(dir, "file"), "x").close()
            except FileExistsError:
                return val
            raise FloatingPointError("fails first time")

        return fail_once


class DelayedCancelTest(unittest.TestCase):
    def test_cancel(self):
        def wait_and_return(dur, value):
            import time

            time.sleep(dur)
            return value

        node = Delayed(wait_and_return, local=True, name="multi_node")(10, 3)
        node_2 = Delayed(np.mean, local=True, name="multi_node_2")([node, node])

        with self.assertRaises(futures.TimeoutError):
            node_2.set_timeout(1)
            node_2.compute()

        node_2.cancel()

        self.assertEqual(node_2.status, Status.CANCELLED)

        # Because an already-running node can't be cancelled, the sleep will
        # still run to completion.
        self.assertEqual(node.result(15), 3)

        self.assertEqual(node_2.status, Status.CANCELLED)
        with self.assertRaises(futures.CancelledError):
            node_2.result()

        node_2.retry()
        self.assertEqual(node_2.result(10), 3)


class DelayedCloudApplyTest(unittest.TestCase):
    def test_array_apply(self):

        uri = "tiledb://TileDB-inc/quickstart_sparse"
        with tiledb.open(uri, ctx=tiledb.cloud.Ctx()) as A:
            orig = A[:]

        import numpy

        node = DelayedArrayUDF(uri, lambda x: numpy.sum(x["a"]), name="node")(
            [(1, 4), (1, 4)]
        )

        # Add timeout so we don't wait forever in CI
        node.set_timeout(30)
        node.compute()

        self.assertEqual(node.result(), numpy.sum(orig["a"]))

    def test_multi_array_apply(self):

        uri_sparse = "tiledb://TileDB-inc/quickstart_sparse"
        with tiledb.open(uri_sparse, ctx=tiledb.cloud.Ctx()) as A:
            orig_sparse = A[:]

        uri_dense = "tiledb://TileDB-inc/quickstart_dense"
        with tiledb.open(uri_dense, ctx=tiledb.cloud.Ctx()) as A:
            orig_dense = A[:]

        import numpy

        array_list = tiledb.cloud.array.ArrayList()
        array_list.add(uri_sparse, [(1, 4), (1, 4)], ["a"])
        array_list.add(uri_dense, [(1, 4), (1, 4)], ["a"])

        def sum_func(data):
            import numpy

            return numpy.sum(data[0]["a"]) + numpy.sum(data[1]["a"])

        node = DelayedMultiArrayUDF(sum_func, array_list, name="node")()

        # Add timeout so we don't wait forever in CI
        node.set_timeout(30)
        node.compute()

        self.assertEqual(
            node.result(), numpy.sum(orig_sparse["a"]) + numpy.sum(orig_dense["a"])
        )

    def test_array_apply_by_name(self):

        uri = "tiledb://TileDB-inc/quickstart_sparse"
        with tiledb.open(uri, ctx=tiledb.cloud.Ctx()) as A:
            orig = A[:]

        def sum_a(x):
            import numpy

            return numpy.sum(x["a"])

        with testonly.register_udf(sum_a) as sum_a_name:
            node = DelayedArrayUDF(uri, sum_a_name, name="node")([(1, 4), (1, 4)])

            # Add timeout so we don't wait forever in CI
            node.set_timeout(30)
            node.compute()

        import numpy

        self.assertEqual(node.result(), numpy.sum(orig["a"]))

    def test_udf_exec(self):
        import numpy

        node = Delayed(lambda x: numpy.sum(x), name="node")([1, 4, 10, 40])

        # Add timeout so we don't wait forever in CI
        node.set_timeout(30)
        node.compute()

        self.assertEqual(node.result(), 55)

    def test_sql_exec(self):

        uri = "tiledb://TileDB-inc/quickstart_sparse"
        with tiledb.open(uri, ctx=tiledb.cloud.Ctx()) as A:
            orig = A[:]

        import numpy

        node = DelayedSQL("select SUM(`a`) as a from `{}`".format(uri), name="node")

        # Add timeout so we don't wait forever in CI
        node.set_timeout(30)
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
            "select SUM(`a`) as a from `{}`".format(uri_dense),
            name="node_sql",
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

        # Add timeout so we don't wait forever in CI
        node_exec.set_timeout(30)
        node_exec.compute()

        self.assertEqual(node_array_apply.result(), numpy.sum(orig["a"]))
        self.assertEqual(node_sql.result()["a"][0], numpy.sum(orig_dense["a"]))
        self.assertEqual(
            node_exec.result(),
            numpy.mean([numpy.sum(orig["a"]), numpy.sum(orig_dense["a"])]),
        )

    def test_apply_exec_multiple_2(self):

        uri_sparse = "tiledb://TileDB-inc/quickstart_sparse"
        uri_dense = "tiledb://TileDB-inc/quickstart_dense"
        with tiledb.open(uri_sparse, ctx=tiledb.cloud.Ctx()) as A:
            orig = A[:]

        with tiledb.open(uri_dense, ctx=tiledb.cloud.Ctx()) as A:
            orig_dense = A[:]

        import numpy

        node_local = Delayed(lambda x: x * 2, local=True)(100)

        def sum_a(x):
            import numpy

            return numpy.sum(x["a"])

        with testonly.register_udf(sum_a) as sum_a_name:
            node_array_apply = DelayedArrayUDF(
                uri_sparse, sum_a_name, name="node_array_apply"
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

            # Add timeout so we don't wait forever in CI
            node_exec.set_timeout(30)
            node_exec.compute()

        self.assertEqual(node_local.result(), 200)
        self.assertEqual(node_array_apply.result(), numpy.sum(orig["a"]))
        self.assertEqual(node_sql.result()["a"][0], numpy.sum(orig_dense["a"]))
        self.assertEqual(
            node_exec.result(),
            numpy.mean([200, numpy.sum(orig["a"]), numpy.sum(orig_dense["a"])]),
        )
        self.assertEqual(node_exec.status, Status.SUCCEEDED)

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

        # Add timeout so we don't wait forever in CI
        node_exec.set_timeout(30)
        node_exec.compute()

        self.assertEqual(node_local.result(), 200)
        self.assertEqual(node_array_apply.result(), numpy.sum(orig["a"]))
        self.assertEqual(node_sql.result()["a"][0], numpy.sum(orig_dense["a"]))
        self.assertEqual(
            node_exec.result(),
            numpy.mean([200, numpy.sum(orig["a"]), numpy.sum(orig_dense["a"])]),
        )
        self.assertEqual(node_exec.status, Status.SUCCEEDED)

    def test_array_chain(self):
        def sum_a(arr):
            import numpy

            return int(numpy.sum(arr["a"]))

        def sum_b(arr, prev):
            import numpy

            return int(numpy.sum(arr["a"])), prev

        node_array_a = DelayedArrayUDF("tiledb://TileDB-inc/quickstart_dense")(
            sum_a, [(1, 2), (1, 2)]
        )
        node_array_b = DelayedArrayUDF("tiledb://TileDB-inc/quickstart_dense")(
            sum_b, [(3, 4), (3, 4)], prev=node_array_a
        )

        node_array_b.set_timeout(20)
        result = node_array_b.compute()
        self.assertEqual((54, 14), result)
