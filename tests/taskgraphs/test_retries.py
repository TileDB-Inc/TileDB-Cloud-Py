import operator
import unittest
from concurrent import futures

import tiledb.cloud.taskgraphs as tg
from tiledb.cloud import client
from tiledb.cloud import testonly
from tiledb.cloud.taskgraphs import client_executor


class RetryTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._me = client.default_user().username

    def test_retry_one(self):
        fail_name = testonly.random_name("retry_one")
        grf = tg.Builder("retry_one")
        fail = grf.udf(f"{self._me}/{fail_name}")
        last = grf.udf(lambda prev: f"got {prev!r}", tg.args(fail))

        exec = tg.execute(grf)
        fail_node = exec.node(fail)
        last_node = exec.node(last)
        with self.assertRaises(Exception):
            fail_node.result(10)
        with self.assertRaises(tg.ParentFailedError) as cm:
            last_node.result(1)
        self.assertIs(last_node.status, tg.Status.PARENT_FAILED)
        self.assertIs(cm.exception.node, fail_node)

        with testonly.register_udf(lambda: 100, fail_name):
            fail_node.retry()
            self.assertEqual(100, fail_node.result(10))
            self.assertEqual("got 100", last_node.result(10))
        exec.wait(1)

    def test_retry_cascade(self):
        grf = tg.Builder("retry_cancelled")
        one = grf.udf(lambda: 1)
        two = grf.udf(operator.add, tg.args(one, one))
        three = grf.udf(operator.add, tg.args(one, two))
        four = grf.udf(operator.add, tg.args(one, three))
        seven = grf.udf(operator.add, tg.args(four, three))

        exec = client_executor.LocalExecutor(grf)
        one_node = exec.node(one)
        two_node = exec.node(two)
        seven_node = exec.node(seven)
        two_node.cancel()
        exec.execute()
        self.assertEqual(1, one_node.result(10))
        with self.assertRaises(futures.CancelledError):
            two_node.result(1)
        with self.assertRaises(tg.ParentFailedError):
            seven_node.result(1)
        exec.retry(two_node)
        self.assertEqual(7, seven_node.result(20))
        exec.wait(1)

    def test_retry_all(self):
        retry_all_b = testonly.random_name("retry_all_b")
        grf = tg.Builder("retry_all")

        def a_func():
            return "a"

        a = grf.udf(a_func, name="node a")
        b = grf.udf(f"{self._me}/{retry_all_b}", name="node b")
        c = grf.udf(lambda x: x, tg.args("c"), name="node c")

        merge = grf.udf(" ".join, tg.args((a, b, c)), name="joiner")
        final = grf.udf(repr, tg.args(merge), name="repr")

        exec = client_executor.LocalExecutor(grf)
        c_node = exec.node(c)
        c_node.cancel()
        final_node = exec.node(final)
        final_node.cancel()

        exec.execute()

        with testonly.register_udf(lambda: "b", func_name=retry_all_b):
            exec.retry_all()

            exec.wait(30)

        self.assertEqual("'a b c'", final_node.result(1))
