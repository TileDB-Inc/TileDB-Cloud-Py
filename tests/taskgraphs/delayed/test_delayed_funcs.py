"""Tests of tiledb.cloud.taskgraphs.delayed.

Almost all of these tests require remote code execution that is time
consuming and restricted to certain versions of Python. To skip, pass
-m 'not udf' to pytest.
"""

import operator
import os.path
import tempfile
import time
import unittest

import numpy as np
import pytest

from tiledb.cloud import client
from tiledb.cloud import taskgraphs
from tiledb.cloud._common import futures
from tiledb.cloud._common import testonly
from tiledb.cloud.taskgraphs import delayed
from tiledb.cloud.taskgraphs import executor
from tiledb.cloud.taskgraphs import registration

pytestmark = pytest.mark.udf


class FunctionsTest(unittest.TestCase):
    def test_basic_functions(self):
        passthrough = delayed.udf(lambda *x: x)

        nothing = passthrough.set(name="nothing")()
        a = passthrough.set(name="a")("a", nothing)
        b = passthrough.set(name="b")(nothing, "b")
        c = passthrough.set(name="c")(a, b)
        d = delayed.udf(repr, name="d")(c)

        self.assertEqual("[['a', []], [[], 'b']]", d.compute(30))

    def test_two_delayeds(self):
        d_repr = delayed.udf(repr)

        repr_call = d_repr(1)
        self.assertEqual("1", repr_call.compute(10))

        repr_repr_call = d_repr(repr_call)
        self.assertEqual("'1'", repr_repr_call.compute(10))

    def test_simple(self):
        node_1 = delayed.udf(np.median, name="node_1")([1, 2, 3])
        node_2 = delayed.udf(lambda x: x * 2, name="node_2")(node_1)
        node_3 = delayed.udf(lambda x: x * 2, name="node_3")(node_2)

        node_3.compute(timeout=30)

        self.assertEqual(2, node_1.result())
        self.assertEqual(4, node_2.result())
        self.assertEqual(8, node_3.result())

    def test_kwargs(self):
        def string_multi(multiplier, st=None):
            return int(multiplier) * st

        node_1 = delayed.udf(np.median, name="node_1")([1, 2, 3])
        node_2 = delayed.udf(lambda x: x * 2, name="node_2")(node_1)
        node_3 = delayed.udf(string_multi, name="node_3")(node_2, st="a")

        node_3.compute(timeout=30)

        self.assertEqual(2, node_1.result())
        self.assertEqual(4, node_2.result())
        self.assertEqual("aaaa", node_3.result())

    def test_multi_dependencies(self):
        node_1 = delayed.udf(np.median, name="multi_node_1")([1, 2, 3])
        d_double = delayed.udf(lambda x: x * 2)
        node_2 = d_double.set(name="multi_node_2")(node_1)
        node_3 = d_double.set(name="multi_node_3")(node_2)
        node_4 = d_double.set(name="multi_node_4")(node_2)
        node_5 = d_double.set(name="multi_node_5")(node_2)

        node_6 = delayed.udf(lambda *x: np.sum(x), name="multi_node_6")(
            node_3, node_4, node_5
        )
        node_6.compute(30)

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), 8)
        self.assertEqual(node_4.result(), 8)
        self.assertEqual(node_5.result(), 8)
        self.assertEqual(node_6.result(), 24)

    def test_local(self):
        def touch(file):
            open(file, "w").close()
            return file

        d_touch = delayed.udf(touch, local=True)

        with tempfile.TemporaryDirectory() as tmpdir:
            fn = os.path.join(tmpdir, "testfile")

            node = d_touch(fn)
            self.assertEqual(fn, node.compute(5))
            self.assertTrue(os.path.exists(fn))

    def test_register(self):
        d_repr = delayed.udf(repr)
        parent = d_repr(1)
        middle = d_repr(parent)
        child = d_repr.set(name="output")(middle)

        grf_name = testonly.random_name("register_delayed")
        child.register(name=grf_name)
        try:
            time.sleep(1)
            exec = taskgraphs.execute(grf_name)
            self.assertEqual('''"'1'"''', exec.node("output").result(30))
        finally:
            registration.delete(grf_name)

        with self.assertWarnsRegex(UserWarning, "update"):
            # Ensure that we issue a warning when the user updates.
            last = d_repr(child)
        owner = last._owner
        self.assertIsNone(owner._builder)
        for n in owner._deps:
            self.assertIsNone(n._builder_node)


class FailureTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self._me = client.default_user().username

    def test_failure(self):
        node = delayed.udf(lambda x: x * 2)(np.median)
        with self.assertRaisesRegex(Exception, "unsupported operand"):
            node.compute(timeout=30)

        self.assertIsNotNone(node._owner._execution)

    def test_dependency_fail_early(self):
        node = delayed.udf(lambda x: x * 2)(np.median)
        node_2 = delayed.udf(lambda x: x * 2)(10)
        node_2.depends_on(node)

        with self.assertRaises(futures.CancelledError):
            node_2.compute(30)
        self.assertEqual(executor.Status.FAILED, node.status)
        self.assertEqual(executor.Status.PARENT_FAILED, node_2.status)

    def test_failure_retry(self):
        fail_name = testonly.random_name("delayed_retry")

        fail = delayed.udf(f"{self._me}/{fail_name}")()
        last = delayed.udf("got {!r}".format)(fail)

        with self.assertRaises(executor.ParentFailedError):
            last.compute(30)

        self.assertIs(executor.Status.FAILED, fail.status)
        self.assertIs(executor.Status.PARENT_FAILED, last.status)

        with testonly.register_udf(lambda: 100, fail_name):
            fail.retry()
            self.assertEqual(100, fail.result(10))
            self.assertEqual("got 100", last.result(10))

    def test_retry_all(self):
        fail_name = testonly.random_name("delayed_retry_all")

        left = delayed.udf(f"{self._me}/{fail_name}")()
        right = delayed.udf(f"{self._me}/{fail_name}")()

        merge = delayed.udf(operator.add)(left, right)

        with self.assertRaises(executor.ParentFailedError):
            merge.compute(30)

        with testonly.register_udf(lambda: "str", fail_name):
            merge.retry_all()
            self.assertEqual("strstr", merge.result(30))
