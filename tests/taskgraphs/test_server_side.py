"""Tests of tiledb.cloud.taskgraphs.

Almost all of these tests require remote code execution that is time
consuming and restricted to certain versions of Python. To skip, pass
-m 'not udf' to pytest.
"""

import unittest

import pytest

import tiledb.cloud.taskgraphs as tg
from tiledb.cloud import dag
from tiledb.cloud.taskgraphs.server_executor import impl

pytestmark = pytest.mark.udf

_WAIT_TIME_S = 120


class ConnectToExistingTest(unittest.TestCase):
    @pytest.mark.xfail(reason="Time to complete is not predictable.")
    def test_completed_graph(self) -> None:
        to_run = dag.DAG(mode=dag.Mode.BATCH)
        one = to_run.submit(lambda: 1, name="one")
        to_run.submit(lambda x: x + x, one, name="two")
        to_run.compute()
        to_run.wait(_WAIT_TIME_S)
        connected = connect_to(to_run)
        self.assertIs(connected.status, tg.Status.SUCCEEDED)
        self.assertEqual(connected.node("one").result(1), 1)
        self.assertEqual(connected.node("two").result(1), 2)

    @pytest.mark.xfail(reason="Server side error, graph not computed in expected time.")
    def test_running_graph(self) -> None:
        to_run = dag.DAG(mode=dag.Mode.BATCH)
        one = to_run.submit(lambda: 1, name="one")

        def second_func(inval):
            import time

            time.sleep(20)
            return inval + inval

        to_run.submit(second_func, one, name="two")
        to_run.compute()
        connected = connect_to(to_run)
        # Here we're assuming that we will connect to the running task graph
        # before it has a chance to complete. Technically this is a race,
        # but we're probably going to beat time.sleep(20).
        self.assertFalse(connected.status.is_terminal())
        self.assertEqual(connected.node("one").result(_WAIT_TIME_S), 1)
        self.assertEqual(connected.node("two").result(_WAIT_TIME_S), 2)
        self.assertIs(connected.node("two").status, tg.Status.SUCCEEDED)
        self.assertIs(connected.status, tg.Status.SUCCEEDED)

    @pytest.mark.xfail(reason="Server side error, graph not computed in expected time.")
    def test_failing_graph(self) -> None:
        to_run = dag.DAG(mode=dag.Mode.BATCH)
        to_run.submit(lambda: 1 / 0, name="oops")
        to_run.compute()
        connected = connect_to(to_run)
        with self.assertRaises(ZeroDivisionError):
            connected.node("oops").result(_WAIT_TIME_S)
        self.assertIs(connected.status, tg.Status.FAILED)


def connect_to(grf: dag.DAG) -> impl.ServerExecutor:
    graph_id = grf.server_graph_uuid
    assert graph_id
    return impl.connect(graph_id)
