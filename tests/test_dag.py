import base64
import collections
import collections.abc as cabc
import itertools
import operator
import pickle
import threading
import time
import unittest
import uuid
from concurrent import futures
from typing import Any

import cloudpickle
import numpy as np
import pandas as pd

import tiledb.cloud
from tiledb.cloud import client
from tiledb.cloud import dag
from tiledb.cloud import rest_api
from tiledb.cloud import tasks
from tiledb.cloud import tiledb_cloud_error as tce
from tiledb.cloud._common import visitor
from tiledb.cloud._results import decoders
from tiledb.cloud._results import results
from tiledb.cloud._results import stored_params as sp
from tiledb.cloud.dag import Mode
from tiledb.cloud.dag import dag as dag_dag
from tiledb.cloud.rest_api import models


class DAGClassTest(unittest.TestCase):
    maxDiff = None

    def test_simple_dag(self):
        d = dag.DAG(name="a cool dag")

        node_1 = d.add_node(np.median, [1, 2, 3])
        node_1.name = "node_1"
        node_2 = d.add_node(lambda x: x * 2, node_1)
        node_2.name = "node_2"
        node_3 = d.add_node(lambda x: x * 2, node_2)
        node_3.name = "node_3"

        d.compute()

        # Wait for dag to complete
        d.wait(30)

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), 8)

        ends = d.find_end_nodes()

        self.assertEqual(len(ends), 1)
        self.assertEqual(ends[0].name, node_3.name)
        self.assertDictEqual(
            d.stats(),
            {
                "percent_complete": 100,
                "running": 0,
                "failed": 0,
                "completed": 3,
                "cancelled": 0,
                "not_started": 0,
                "total_count": 3,
            },
        )

        self.assertEqual(
            d._build_log_structure(),
            models.TaskGraphLog(
                name="a cool dag",
                namespace=client.default_charged_namespace(
                    required_action=rest_api.NamespaceActions.RUN_JOB
                ),
                nodes=[
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_1.id),
                        name="node_1",
                        depends_on=[],
                        run_location="client",
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_2.id),
                        name="node_2",
                        depends_on=[str(node_1.id)],
                        run_location="client",
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_3.id),
                        name="node_3",
                        depends_on=[str(node_2.id)],
                        run_location="client",
                    ),
                ],
            ),
        )

        self.assertIsNone(dag_dag.server_logs(d))

    def test_simple_cloud_dag(self):
        d = dag.DAG(name="a cool server dag")

        node_1 = d.submit(np.median, [1, 2, 3], name="node_a")
        node_2 = d.submit(lambda x: x * 2, node_1, name="node_b")
        node_3 = d.submit(lambda x: x * 2, node_2, name="node_c")

        d.compute()

        # Wait for dag to complete
        d.wait(30)

        # The first two calls should not have downloaded results.
        res_1 = self._remote_result(node_1)
        self.assertIs(res_1._decoded, results._SENTINEL)
        self.assertIsNone(res_1._body)
        res_2 = self._remote_result(node_2)
        self.assertIs(res_2._decoded, results._SENTINEL)
        self.assertIsNone(res_2._body)
        # The last one should have.
        self.assertIsNotNone(self._remote_result(node_3)._body)

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), 8)

        ends = d.find_end_nodes()

        self.assertEqual(len(ends), 1)
        self.assertEqual(ends[0].name, node_3.name)
        self.assertDictEqual(
            d.stats(),
            {
                "percent_complete": 100,
                "running": 0,
                "failed": 0,
                "completed": 3,
                "cancelled": 0,
                "not_started": 0,
                "total_count": 3,
            },
        )

        self.assertEqual(
            d._build_log_structure(),
            models.TaskGraphLog(
                name="a cool server dag",
                namespace=client.default_charged_namespace(
                    required_action=rest_api.NamespaceActions.RUN_JOB
                ),
                nodes=[
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_1.id),
                        name="node_a",
                        depends_on=[],
                        run_location="server",
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_2.id),
                        name="node_b",
                        depends_on=[str(node_1.id)],
                        run_location="server",
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_3.id),
                        name="node_c",
                        depends_on=[str(node_2.id)],
                        run_location="server",
                    ),
                ],
            ),
        )

        # The status is set asynchronously so there may be a slight delay
        # between when we send a request and when it's actually recorded.
        time.sleep(2)
        actual_log = dag_dag.server_logs(d)
        self.assertEqual("a cool server dag", actual_log.name)
        self.assertEqual(3, len(actual_log.nodes))
        self.assertEqual("succeeded", actual_log.status)

    def _remote_result(self, node: dag_dag.Node) -> results.RemoteResult:
        """Extracts the RemoteResult out of the Node's future."""
        result = node._result  # type: ignore
        self.assertIsInstance(result, results.RemoteResult)
        return result  # type: ignore

    def test_kwargs(self):
        d = dag.DAG()

        def string_multi(multiplier, str=None):
            return int(multiplier) * str

        node_1 = d.add_node(np.median, [1, 2, 3])
        node_1.name = "node_1"
        node_2 = d.add_node(lambda x: x * 2, node_1)
        node_2.name = "node_2"
        node_3 = d.add_node(string_multi, node_2, str="a")
        node_3.name = "node_3"

        d.compute()

        # Wait for dag to complete
        d.wait(30)

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), "aaaa")

    def test_multi_dependencies_dag(self):
        d = dag.DAG()

        node_1 = d.add_node(np.median, [1, 2, 3])
        node_1.name = "multi_node_1"

        def double(x):
            return x * 2

        node_2 = d.add_node(double, node_1)
        node_2.name = "multi_node_2"
        node_3 = d.add_node(double, node_2)
        node_3.name = "multi_node_3"
        node_4 = d.add_node(double, node_2)
        node_4.name = "multi_node_4"
        node_5 = d.add_node(double, node_2)
        node_5.name = "multi_node_5"

        node_6 = d.add_node(lambda *x: np.sum(x), node_3, node_4, node_5)
        node_6.name = "multi_node_6"

        d.compute()

        # Wait for dag to complete
        d.wait(30)

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), 8)
        self.assertEqual(node_4.result(), 8)
        self.assertEqual(node_5.result(), 8)
        self.assertEqual(node_6.result(), 24)

        # The order of this assertion is somewhat fragile. It is deterministic
        # based on our implementation of toposort, but if the toposort
        # implementation changes, it may spuriously fail (but can be updated).
        self.assertEqual(
            d._build_log_structure(),
            models.TaskGraphLog(
                namespace=client.default_charged_namespace(
                    required_action=rest_api.NamespaceActions.RUN_JOB
                ),
                nodes=[
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_1.id),
                        name="multi_node_1",
                        depends_on=[],
                        run_location="client",
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_2.id),
                        name="multi_node_2",
                        depends_on=[str(node_1.id)],
                        run_location="client",
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_5.id),
                        name="multi_node_5",
                        depends_on=[str(node_2.id)],
                        run_location="client",
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_4.id),
                        name="multi_node_4",
                        depends_on=[str(node_2.id)],
                        run_location="client",
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_3.id),
                        name="multi_node_3",
                        depends_on=[str(node_2.id)],
                        run_location="client",
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_6.id),
                        name="multi_node_6",
                        depends_on=[
                            str(node_3.id),
                            str(node_4.id),
                            str(node_5.id),
                        ],
                        run_location="client",
                    ),
                ],
            ),
        )

    def test_end_nodes_dag(self):
        d = dag.DAG()

        node_1 = d.add_node(np.median, [1, 2, 3])
        node_1.name = "multi_node_1"

        def double(x):
            return x * 2

        node_2 = d.add_node(double, node_1)
        node_2.name = "multi_node_2"
        node_3 = d.add_node(double, node_2)
        node_3.name = "multi_node_3"
        node_4 = d.add_node(double, node_2)
        node_4.name = "multi_node_4"
        node_5 = d.add_node(double, node_2)
        node_5.name = "multi_node_5"

        node_6 = d.add_node(lambda *x: np.sum(x), node_3, node_4, node_5)
        node_6.name = "multi_node_6"

        d.compute()

        # Wait for dag to complete
        d.wait(30)

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), 8)
        self.assertEqual(node_4.result(), 8)
        self.assertEqual(node_5.result(), 8)
        self.assertEqual(node_6.result(), 24)

        end_nodes = d.end_nodes()
        self.assertEqual(1, len(end_nodes))
        self.assertEqual(node_6.id, end_nodes[0].id)

        end_results = d.end_results()
        self.assertEqual(1, len(end_results))
        self.assertEqual(node_6.result(), end_results[node_6.id])

        end_results = d.end_results_by_name()
        self.assertEqual(1, len(end_results))
        self.assertEqual(node_6.result(), end_results[node_6.name])

    def test_sql_node_input(self):
        import numpy

        d = dag.DAG()
        arr_node = d.submit_array_udf(
            "tiledb://TileDB-Inc/quickstart_dense",
            lambda x: int(numpy.sum(x["a"])),
            ranges=[[1, slice(2, 4)], None],
        )
        sql_node = d.submit_sql("select 2 * ? as doubleit", parameters=(arr_node,))

        def both(a: int, b: Any):
            return f"{a} and {int(b['doubleit'])}"

        join_node = d.submit_udf(both, arr_node, sql_node)

        d.compute()
        d.wait(30)
        self.assertEqual("136 and 272", join_node.result())

    def test_concurrency(self):
        task_count = 5
        barrier = threading.Barrier(task_count)

        def rendezvous(val):
            barrier.wait()
            return val

        d = dag.DAG()
        tasks = [
            d.add_node(rendezvous, f"#{i}", local_mode=True) for i in range(task_count)
        ]
        terminal = d.add_node(", ".join, tasks, local_mode=True)
        d.compute()
        d.wait(1)  # Avoid locking up forever if we deadlock.
        self.assertEqual("#0, #1, #2, #3, #4", terminal.result())

    def test_two_dags(self):
        local_timeouts = [
            (True, 10),
            (False, 30),
        ]
        for local, timeout in local_timeouts:
            with self.subTest(local):
                g1 = dag.DAG(name=f"two dags 1 (local: {local})")
                n1 = g1.submit(len, [1, 2, 3], name="two dags len", local_mode=local)
                g1.compute()
                g1.wait(timeout)

                g2 = dag.DAG(name=f"two dags 2 (local: {local})")
                n2 = g2.submit(repr, n1, name="two dags repr", local_mode=local)
                g2.compute()
                g2.wait(timeout)

                self.assertEqual(n2.result(), "3")

    def test_resource_class(self):
        def big_sum():
            # An experimentally determined value where reifying the sequence
            # is too much for a normal-sized UDF, but fine for a large UDF.
            # Tune (or replace with a better implementation) as needed.
            nums = tuple(range(128 * 1024**2))
            return sum(nums)

        grf = dag.DAG()
        small = grf.submit(big_sum)
        large = grf.submit(big_sum, resource_class="large")
        grf.compute()
        with self.assertRaises(Exception):
            small.result()
        self.assertEqual(9007199187632128, large.result(30))


class DAGFailureTest(unittest.TestCase):
    def test_dag_failure(self):
        d = dag.DAG()
        node = d.add_node(lambda x: x * 2, np.median)
        node.name = "node"

        d.compute()
        with self.assertRaises(TypeError):
            # Wait for dag to complete
            d.wait(30)
        self.assertEqual(d.status, dag.Status.FAILED)

        self.assertEqual(node.status, dag.Status.FAILED)
        self.assertEqual(
            str(node.error),
            "unsupported operand type(s) for *: 'function' and 'int'",
        )
        with self.assertRaises(TypeError):
            node.result()

    def test_dag_dependency_fail_early(self):
        d = dag.DAG()
        node = d.add_node(lambda x: x * 2, np.median)
        node.name = "node"
        node2 = d.add_node(lambda x: x * 2, 10)
        node2.name = "node2"
        node2.depends_on(node)

        d.compute()
        with self.assertRaises(TypeError):
            # Wait for dag to complete
            d.wait(30)
        self.assertEqual(d.status, dag.Status.FAILED)

        self.assertEqual(node.status, dag.Status.FAILED)
        self.assertEqual(
            str(node.error),
            "unsupported operand type(s) for *: 'function' and 'int'",
        )
        with self.assertRaises(TypeError):
            node.result()

        node2.wait(1)
        self.assertEqual(node2.status, dag.Status.PARENT_FAILED)
        with self.assertRaises(futures.CancelledError):
            node2.result()

    def test_failure_server_nodes(self):
        d = dag.DAG(name="divide by zero")
        node = d.submit(lambda: 1 / 0, name="i'm gonna do it")
        child = d.submit(lambda x: f"they got {x}", node, name="what happened")
        d.compute()

        with self.assertRaises(tce.TileDBCloudError):
            d.wait(30)
        self.assertEqual(node.status, dag.Status.FAILED)
        self.assertEqual(child.status, dag.Status.PARENT_FAILED)

    def test_cancel_only_children(self):
        d = dag.DAG()

        def fail():
            raise Exception("expected")

        definitely_failed = threading.Barrier(2, timeout=5)

        def wait(something):
            definitely_failed.wait()
            return something

        fail_node = d.submit_local(fail)
        fail_child = d.submit_local(repr, fail_node)
        wait_node = d.submit_local(wait, "value")
        wait_child = d.submit_local(repr, wait_node)

        d.compute()

        fail_node.wait(1)
        definitely_failed.wait()

        with self.assertRaisesRegex(Exception, r"^expected$"):
            d.wait(5)

        self.assertEqual(dag.Status.FAILED, d.status)
        self.assertEqual(dag.Status.FAILED, fail_node.status)
        self.assertEqual(dag.Status.PARENT_FAILED, fail_child.status)
        self.assertEqual("value", wait_node.result())
        self.assertEqual("'value'", wait_child.result())

    def test_two_dags_bad(self):
        d1 = dag.DAG()
        n1 = d1.submit(repr, "whatever")
        d2 = dag.DAG()
        with self.assertRaises(tce.TileDBCloudError):
            d2.submit(repr, n1)

    def test_retry(self):
        d = dag.DAG()

        n1 = d.submit_local(self._fail_once_func(), 5)
        n2 = d.submit(operator.mul, n1, 2)

        d.compute()

        with self.assertRaises(FloatingPointError):
            d.wait(10)

        self.assertEqual(d.status, dag.Status.FAILED)
        self.assertEqual(n1.status, dag.Status.FAILED)
        self.assertEqual(n2.status, dag.Status.PARENT_FAILED)

        self.assertTrue(n1.retry())
        d.wait(10)
        self.assertEqual(d.status, dag.Status.COMPLETED)
        self.assertEqual(n2.result(), 10)

    def test_retry_all(self):
        d = dag.DAG()

        n1 = d.submit_local(self._fail_once_func())
        n2 = d.submit_local(repr, n1)

        d.compute()

        with self.assertRaises(FloatingPointError):
            d.wait(2)
        self.assertEqual(d.status, dag.Status.FAILED)
        self.assertEqual(n1.status, dag.Status.FAILED)
        self.assertEqual(n2.status, dag.Status.PARENT_FAILED)

        d.retry_all()
        d.wait(2)
        self.assertEqual(d.status, dag.Status.COMPLETED)
        self.assertEqual(n1.result(), None)
        self.assertEqual(n2.result(), "None")

    def test_retry_cancelled(self):
        d = dag.DAG()

        barrier = threading.Barrier(2)

        def rendezvous(value=None):
            barrier.wait()
            barrier.wait()
            return value

        n1 = d.submit_local(rendezvous, 5)
        n2 = d.submit_local(self._fail_once_func(), n1)
        n3 = d.submit("the value is {v}".format, v=n2)

        d.compute()

        barrier.wait(2)
        d.cancel()
        barrier.wait(1)

        self.assertEqual(n2.status, dag.Status.CANCELLED)
        self.assertEqual(n3.status, dag.Status.PARENT_FAILED)
        d.wait(1)

        d.retry_all()
        with self.assertRaises(FloatingPointError):
            d.wait(2)
        self.assertEqual(n3.status, dag.Status.PARENT_FAILED)

        n2.retry()
        d.wait(10)
        self.assertEqual(n3.result(1), "the value is 5")

    def _fail_once_func(self):
        ran = False

        def fail_once(val=None):
            nonlocal ran
            if not ran:
                ran = True
                raise FloatingPointError("fails first time")
            return val

        return fail_once


class DAGBatchModeTest(unittest.TestCase):
    def test_simple_batch_dag(self):
        d = dag.DAG(mode=Mode.BATCH)

        node_1 = d.submit(
            np.median,
            [1, 2, 3],
            name="node_a",
            resources={"cpu": "1", "memory": "500Mi"},
        )
        node_2 = d.submit(
            lambda x: x * 2,
            node_1,
            name="node_b",
            resources={"cpu": "1", "memory": "500Mi"},
        )
        node_3 = d.submit(
            lambda x: x * 2,
            node_2,
            name="node_c",
            resources={"cpu": "1", "memory": "500Mi"},
        )

        d.compute()

        # Wait for dag to complete
        d.wait(300)

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), 8)

    def test_batch_dag_failure(self):
        d = dag.DAG(mode=Mode.BATCH)
        node = d.submit(
            lambda x: x * 2,
            np.median,
            name="node",
            resources={"cpu": "1", "memory": "500Mi"},
        )

        d.compute()
        with self.assertRaises(TypeError):
            # Wait for dag to complete
            d.wait(300)
        self.assertEqual(d.status, dag.Status.FAILED)

        self.assertEqual(node.status, dag.Status.FAILED)
        self.assertEqual(
            str(node.error),
            "unsupported operand type(s) for *: 'function' and 'int'",
        )
        with self.assertRaises(TypeError):
            node.result()

    def test_dynamic_batch_dag(self):
        d = dag.DAG(mode=Mode.BATCH, max_workers=2)

        def generate_split():
            return [
                [*range(0, 100)],
                [*range(100, 200)],
                [*range(200, 300)],
                [*range(300, 400)],
            ]

        def multiply(x, y):
            return x * y

        def print_result(x):
            print(f"Result: {x}")
            return x

        split = d.submit(
            generate_split,
            name="split",
            resources={"cpu": "1", "memory": "500Mi"},
            result_format=models.ResultFormat.JSON,
        )
        median = d.submit_udf_stage(
            np.median,
            split,
            expand_node_output=split,
            name="median",
            resources={"cpu": "1", "memory": "500Mi"},
            result_format=models.ResultFormat.JSON,
        )
        mult = d.submit_udf_stage(
            multiply,
            median,
            2,
            expand_node_output=median,
            name="multiply",
            resources={"cpu": "1", "memory": "500Mi"},
            result_format=models.ResultFormat.JSON,
        )
        print_node = d.submit(
            print_result,
            mult,
            name="print",
            resources={"cpu": "1", "memory": "500Mi"},
            result_format=models.ResultFormat.JSON,
        )

        d.compute()

        # Wait for dag to complete
        d.wait(300)
        self.assertEqual(print_node.result(), [99.0, 299.0, 499.0, 699.0])

    def test_batch_dag_retries(self):
        def random_failure():
            import random

            if random.random() > 0.5:
                raise RuntimeError("Random error!")

        d = dag.DAG(
            mode=Mode.BATCH,
            retry_strategy=models.RetryStrategy(
                limit=10,
                retry_policy="Always",
            ),
        )
        d.submit(
            random_failure,
            name="node",
            resources={"cpu": "1", "memory": "500Mi"},
        )

        d.compute()
        d.wait(600)
        self.assertEqual(d.status, dag.Status.COMPLETED)

    def test_batch_dag_deadline(self):
        d = dag.DAG(mode=Mode.BATCH, deadline=20)
        d.submit(
            time.sleep,
            1000,
            name="node",
            resources={"cpu": "1", "memory": "500Mi"},
            retry_strategy=models.RetryStrategy(
                limit=10,
                retry_policy="Always",
            ),
        )

        d.compute()
        with self.assertRaises(rest_api.ApiException):
            # Wait for dag to complete
            d.wait(300)
        self.assertEqual(d.status, dag.Status.FAILED)

    def test_batch_dag_manual_retries(self):
        def random_failure():
            import random

            if random.random() > 0.5:
                raise RuntimeError("Random error!")

        d = dag.DAG(
            mode=Mode.BATCH,
        )
        d.submit(
            random_failure,
            name="node",
            resources={"cpu": "1", "memory": "500Mi"},
        )

        finished = False
        d.compute()
        while not finished:
            try:
                d.wait(600)
            except RuntimeError:
                d.retry_all()
            else:
                finished = True
        self.assertEqual(d.status, dag.Status.COMPLETED)

    def test_cancel_batch_dag(self):
        d = dag.DAG(mode=Mode.BATCH)
        d.submit(
            time.sleep,
            50,
            name="node",
            resources={"cpu": "1", "memory": "500Mi"},
        )

        d.compute()
        time.sleep(20)
        d.cancel()
        d.wait(300)
        self.assertEqual(d.status, dag.Status.CANCELLED)


class DAGCancelTest(unittest.TestCase):
    def test_dag_cancel(self):
        in_node = futures.Future()
        leave_node = futures.Future()

        def rendezvous(value):
            in_node.set_result(None)
            leave_node.result(1)
            return value

        d = dag.DAG()
        node = d.add_node(rendezvous, 100)
        node_2 = d.add_node(np.mean, [node, node])

        d.compute()
        # Cancel DAG when we know the first node is running.
        in_node.result(1)
        d.cancel()
        leave_node.set_result(None)

        d.wait(1)
        self.assertEqual(d.status, dag.Status.CANCELLED)

        # Because an already-running node can't be cancelled, rendezvous will
        # still run to completion.
        self.assertEqual(node.result(), 100)

        node_2.wait(1)
        self.assertEqual(node_2.status, dag.Status.CANCELLED)
        with self.assertRaises(futures.CancelledError):
            node_2.result()


class DAGCloudApplyTest(unittest.TestCase):
    def test_dag_array_apply(self):
        uri = "tiledb://TileDB-Inc/quickstart_sparse"
        with tiledb.open(uri, ctx=tiledb.cloud.Ctx()) as A:
            orig = A[:]

        import numpy

        d = dag.DAG()

        node = d.add_node(
            tiledb.cloud.array.apply, uri, lambda x: numpy.sum(x["a"]), [(1, 4), (1, 4)]
        )
        node.name = "node"

        d.compute()

        # Wait for dag to complete
        d.wait(30)

        self.assertEqual(node.result(), numpy.sum(orig["a"]))

    def test_dag_udf_exec(self):
        import numpy

        d = dag.DAG()

        node = d.add_node(tiledb.cloud.udf.exec, lambda x: numpy.sum(x), [1, 4, 10, 40])
        node.name = "node"

        d.compute()

        # Wait for dag to complete
        d.wait(30)

        self.assertEqual(node.result(), 55)

    def test_dag_sql_exec(self):
        uri = "tiledb://TileDB-Inc/quickstart_sparse"
        with tiledb.open(uri, ctx=tiledb.cloud.Ctx()) as A:
            orig = A[:]

        import numpy

        d = dag.DAG()

        node = d.add_node(
            tiledb.cloud.sql.exec, "select SUM(`a`) as a from `{}`".format(uri)
        )
        node.name = "node"

        d.compute()

        # Wait for dag to complete
        d.wait(30)

        self.assertEqual(node.result()["a"][0], numpy.sum(orig["a"]))

    def test_dag_apply_exec_multiple(self):
        uri_sparse = "tiledb://TileDB-Inc/quickstart_sparse"
        uri_dense = "tiledb://TileDB-Inc/quickstart_dense"
        with tiledb.open(uri_sparse, ctx=tiledb.cloud.Ctx()) as A:
            orig = A[:]

        with tiledb.open(uri_dense, ctx=tiledb.cloud.Ctx()) as A:
            orig_dense = A[:]

        import numpy

        d = dag.DAG()

        node_array_apply = d.add_node(
            tiledb.cloud.array.apply,
            uri_sparse,
            lambda x: numpy.sum(x["a"]),
            [(1, 4), (1, 4)],
            name="node_array_apply",
        )
        node_sql = d.add_node(
            tiledb.cloud.sql.exec,
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

        node_exec = d.add_node(
            tiledb.cloud.udf.exec,
            mean,
            [node_array_apply, node_sql],
            name="node_exec",
        )

        d.compute()

        # Wait for dag to complete
        d.wait(30)

        self.assertEqual(node_array_apply.result(), numpy.sum(orig["a"]))
        self.assertEqual(node_sql.result()["a"][0], numpy.sum(orig_dense["a"]))
        self.assertEqual(
            node_exec.result(),
            numpy.mean([numpy.sum(orig["a"]), numpy.sum(orig_dense["a"])]),
        )
        self.assertEqual(d.status, dag.Status.COMPLETED)

    def test_dag_apply_exec_multiple_2(self):
        uri_sparse = "tiledb://TileDB-Inc/quickstart_sparse"
        uri_dense = "tiledb://TileDB-Inc/quickstart_dense"
        with tiledb.open(uri_sparse, ctx=tiledb.cloud.Ctx()) as A:
            orig = A[:]

        with tiledb.open(uri_dense, ctx=tiledb.cloud.Ctx()) as A:
            orig_dense = A[:]

        import numpy

        d = dag.DAG()

        node_local = d.submit_local(lambda x: x * 2, 100)

        node_array_apply = d.submit_array_udf(
            uri_sparse,
            lambda x: numpy.sum(x["a"]),
            [(1, 4), (1, 4)],
            name="node_array_apply",
        )
        node_sql = d.submit_sql(
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

        node_exec = d.submit_udf(mean, [node_array_apply, node_sql], name="node_exec")

        d.compute()

        # Wait for dag to complete
        d.wait(30)

        self.assertEqual(node_local.result(), 200)
        self.assertEqual(node_array_apply.result(), numpy.sum(orig["a"]))
        self.assertEqual(node_sql.result()["a"][0], numpy.sum(orig_dense["a"]))
        self.assertEqual(
            node_exec.result(),
            numpy.mean([numpy.sum(orig["a"]), numpy.sum(orig_dense["a"])]),
        )
        self.assertEqual(d.status, dag.Status.COMPLETED)

        # Also test downloads.
        self.assertEqual(
            numpy.sum(orig["a"]),
            tasks.fetch_results(node_array_apply.task_id()),
        )
        self.assertEqual(
            numpy.sum(orig_dense["a"]),
            tasks.fetch_results_pandas(
                node_sql.task_id(),
                result_format=tiledb.cloud.ResultFormat.ARROW,
            ).iat[0, 0],
        )
        self.assertEqual(
            numpy.mean([numpy.sum(orig["a"]), numpy.sum(orig_dense["a"])]),
            tasks.fetch_results(node_exec.task_id()),
        )


class DAGCallbackTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.status_updates = 0
        self.done_updates = 0

    def test_simple_dag(self):
        def status_callback_test(dag):
            self.status_updates += 1

        def done_callback_test(dag):
            self.done_updates += 1

        d = dag.DAG(
            update_callback=status_callback_test, done_callback=done_callback_test
        )

        node_1 = d.add_node(np.median, [1, 2, 3], name="node_1")
        node_2 = d.add_node(lambda x: x * 2, node_1, name="node_2")
        node_3 = d.add_node(lambda x: x * 2, node_2, name="node_3")

        d.compute()

        # Wait for dag to complete
        d.wait(30)

        self.assertEqual(node_1.result(), 2)
        self.assertEqual(node_2.result(), 4)
        self.assertEqual(node_3.result(), 8)
        self.assertEqual(self.status_updates, 6)  # two for each Node
        self.assertEqual(self.done_updates, 1)


class TopoSortTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(dag_dag._topo_sort([]), [])

    def test_graphs(self):
        cases = [
            [self._node("root")],
            [self._node("two"), self._node("roots")],
            [self._node("parent"), self._node("child", ["parent"])],
            [self._node("p1"), self._node("p2"), self._node("c", ["p1", "p2"])],
            [
                self._node("p"),
                self._node("c1", depends_on=["p"]),
                self._node("c2", depends_on=["p"]),
            ],
            [
                self._node("r"),
                self._node("mid1", ["r"]),
                self._node("mid2", ["r"]),
                self._node("leaf", ["mid1", "mid2"]),
            ],
            [
                self._node("root1"),
                self._node("root2"),
                self._node("mid", ["root1", "root2"]),
                self._node("second", ["root1", "mid"]),
                self._node("only1", ["root1"]),
                self._node("leaf", ["root2", "second"]),
            ],
        ]
        for i, lst in enumerate(cases):
            with self.subTest(f"case {i}"):
                for j, perm in enumerate(itertools.permutations(lst)):
                    ids = [n.client_node_uuid for n in perm]
                    with self.subTest(f"permutation {j}: {ids}"):
                        result = dag_dag._topo_sort(perm)
                        self.assertCountEqual(perm, result)
                        self.assert_topo_sorted(result)

    def test_preserves_order(self):
        """Verifies that, for a disconnected graph, order is preserved."""
        nodes = [self._node(str(n)) for n in range(100)]
        result = dag_dag._topo_sort(nodes)
        self.assertEqual(nodes, result)

    def test_cycle(self):
        with self.assertRaises(ValueError):
            dag_dag._topo_sort(
                [
                    self._node("a", ["b"]),
                    self._node("b", ["c"]),
                    self._node("c", ["a"]),
                ]
            )

    def test_self(self):
        with self.assertRaises(ValueError):
            dag_dag._topo_sort([self._node("me", ["me"])])

    def test_missing(self):
        with self.assertRaises(ValueError):
            dag_dag._topo_sort([self._node("anything", ["missing"])])

    def assert_topo_sorted(self, nodes):
        seen = set()
        for node in nodes:
            for parent in node.depends_on:
                self.assertIn(parent, seen)
            seen.add(node.client_node_uuid)

    def _node(self, id, depends_on=()):
        return models.TaskGraphNodeMetadata(
            client_node_uuid=id,
            depends_on=depends_on,
        )


class CustomSeq(cabc.MutableSequence):
    """Custom sequence implementation to test value replacement."""

    def __init__(self, items=()):
        self.lst = list(items)

    def __len__(self):
        return len(self.lst)

    def __getitem__(self, idx):
        return self.lst[idx]

    def __setitem__(self, idx, val):
        self.lst[idx] = val

    def __delitem__(self, idx):
        del self.lst[idx]

    def insert(self, idx, val):
        self.lst.insert(idx, val)

    def __eq__(self, other):
        return type(self) == type(other) and self.lst == other.lst


class Doubler(visitor.ReplacingVisitor):
    """Example implementation that doubles every int (but not float) it sees."""

    def maybe_replace(self, arg):
        if isinstance(arg, int):
            return visitor.Replacement(arg * 2)
        return None


class ReplaceNodesTest(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(5, dag_dag._replace_nodes_with_results(5))
        self.assertEqual("hi", dag_dag._replace_nodes_with_results(_node("hi")))

    def test_sequences(self):
        self.assertEqual(
            ["a", "b", "c"],
            dag_dag._replace_nodes_with_results([_node("a"), "b", _node("c")]),
        )
        self.assertEqual(
            (1, 2, ["i", "ii"]),
            dag_dag._replace_nodes_with_results((1, 2, [_node("i"), "ii"])),
        )

    def test_special_sequences(self):
        self.assertEqual(
            "some_string", dag_dag._replace_nodes_with_results("some_string")
        )
        self.assertEqual(b"bytes", dag_dag._replace_nodes_with_results(b"bytes"))
        self.assertEqual(range(100), dag_dag._replace_nodes_with_results(range(100)))

    def test_self_recursion(self):
        dct = {
            "nod": _node(("a", "b", "c")),
        }
        lst = [dct, _node("nod")]
        dct["lst"] = lst
        tup = (_node("a lst:"), lst, _node("a dct:"), dct)
        lst.append(tup)
        got_lst = dag_dag._replace_nodes_with_results(lst)

        want_dct = {
            "nod": ("a", "b", "c"),
        }
        want_lst = [want_dct, "nod"]
        want_dct["lst"] = want_lst
        want_tup = ("a lst:", want_lst, "a dct:", want_dct)
        want_lst.append(want_tup)

        # assertEqual will blow up if you try to compare a recursive structure.
        # However, pickle handles recursion, so we just see if the results
        # have the same pickling.
        self.assertEqual(pickle.dumps(want_lst), pickle.dumps(got_lst))

    def test_custom_types(self):
        my_seq = CustomSeq(["a", "b", 0xC, "d", 0xE, CustomSeq(("F", 0x10)), "h"])

        self.assertEqual(
            CustomSeq(("a", "b", 0x18, "d", 0x1C, CustomSeq(("F", 0x20)), "h")),
            Doubler().visit(my_seq),
        )

        self.assertEqual(
            collections.OrderedDict(zero=0, one=1.0, two=2),
            Doubler().visit(
                collections.OrderedDict(
                    zero=0,
                    one=1.0,
                    two=1,
                )
            ),
        )

    def test_dont_enter_special_types(self):
        df = pd.DataFrame([{"a": 1, "b": 2}, {"a": 2, "b": 3}])
        self.assertIs(df, dag_dag._replace_nodes_with_results(df))
        arr = np.array([["a", 1], ["b", 2]])
        self.assertIs(arr, dag_dag._replace_nodes_with_results(arr))

    def test_ref_equality(self):
        lst = ["a", _node("B"), "c"]
        got_val = dag_dag._replace_nodes_with_results([lst, lst])
        self.assertIs(got_val[0], got_val[1])
        self.assertIsNot(lst, got_val[0])

    def test_dont_replace_unnecessarily(self):
        structure = {
            "a": 1,
            "b": ["2", "3", "4", ("five",)],
            "c": 6.66,
        }
        structure["d"] = structure

        # Save a reference to the original "b" and its exact members.
        orig_b = structure["b"]
        b_ids = tuple(map(id, orig_b))

        got = Doubler().visit(structure)

        # check the primary result, first ensuring that the recursion
        # was handled correctly.
        self.assertIs(got, got["d"])
        del got["d"]
        # Ensure that the non-recursive part worked right.
        self.assertEqual({"a": 2, "b": ["2", "3", "4", ("five",)], "c": 6.66}, got)

        # Verify that the original "b" is used in the output and not modified.
        self.assertIs(orig_b, got["b"])
        self.assertEqual(b_ids, tuple(map(id, got["b"])))

    def test_replace_stored_params(self):
        # Since the corner cases of tree traversal are tested in the other
        # ReplaceNodesTests, this just tests the basics of stored params.
        got = dag_dag.replace_stored_params(
            [
                sp.StoredParam(_uid(0x1), decoder=decoders.Decoder("json")),
                {
                    "sub-dict": sp.StoredParam(
                        _uid(0x2), decoder=decoders.Decoder("native")
                    )
                },
                (sp.StoredParam(_uid(0x1), decoder=decoders.Decoder("json")),),
            ],
            sp.ParamLoader(
                {
                    "00000000-0000-0000-0000-000000000001": _b64(b'[true, "two", 3]'),
                    "00000000-0000-0000-0000-000000000002": _b64(cloudpickle.dumps(())),
                }
            ),
        )

        want = [
            [True, "two", 3],
            {"sub-dict": ()},
            ([True, "two", 3],),
        ]
        self.assertEqual(want, got)
        self.assertIs(got[0], got[2][0], "restored values must be same object")

    def test_replace_stored_params_pandas(self):
        arrow_pd, json_pd, json_raw = dag_dag.replace_stored_params(
            [
                sp.StoredParam(_uid(0x3), decoder=decoders.PandasDecoder("arrow")),
                # Ensure that we can restore the same source object
                # using multiple encodings.
                sp.StoredParam(_uid(0x4), decoder=decoders.PandasDecoder("json")),
                sp.StoredParam(_uid(0x4), decoder=decoders.Decoder("json")),
            ],
            sp.ParamLoader(
                {
                    "00000000-0000-0000-0000-000000000003": _ARROW_DATA,
                    "00000000-0000-0000-0000-000000000004": _b64(
                        b'[{"a": 1, "b": "x"}, {"a": 2, "b": "Y"}]'
                    ),
                }
            ),
        )

        want_arrow_pd = pd.DataFrame([[1, 1.1]], columns=("a", "param1"))
        self.assertTrue(want_arrow_pd.equals(arrow_pd))
        want_json_pd = pd.DataFrame([[1, "x"], [2, "Y"]], columns=("a", "b"))
        self.assertTrue(want_json_pd.equals(json_pd))
        self.assertEqual(
            [{"a": 1, "b": "x"}, {"a": 2, "b": "Y"}],
            json_raw,
        )


def _node(val):
    """Creates a completed node with the given value."""
    n = dag.Node(lambda: None)
    n._result = results.LocalResult(val)
    n._status = dag.Status.CANCELLED
    return n


def _uid(num: int) -> uuid.UUID:
    return uuid.UUID(int=num)


def _b64(x: bytes) -> str:
    return str(base64.b64encode(x), encoding="ascii")


# This is the base64 of the Arrow data returned by this query:
#   set @a = 1;
#   select @a a, ? param1;  -- params: [1.1]
_ARROW_DATA = """
/////8AAAAAQAAAAAAAKAAwACgAJAAQACgAAABAAAAAAAQQACAAIAAAABAAIAAAABAAAAAIAAABcAAAA
FAAAABAAFAAQAAAADwAIAAAABAAQAAAAEAAAABgAAAAAAAADGAAAAAAAAAAAAAYACAAGAAYAAAAAAAIA
BgAAAHBhcmFtMQAAEAAUABAADwAOAAgAAAAEABAAAAAQAAAAGAAAAAAAAgEcAAAAAAAAAAgADAAIAAcA
CAAAAAAAAAFAAAAAAQAAAGEAAAD/////yAAAABQAAAAAAAAADAAYABYAFQAQAAQADAAAAEAAAAAAAAAA
AAAAABQAAAAAAwQADAAcABAADAAIAAQADAAAABwAAAAcAAAAYAAAAAEAAAAAAAAAAAAAAAQABAAEAAAA
BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB8AAAAAAAAAIAAAAAAAAAAAAAAAAAAAACAAAAAAAAAA
HwAAAAAAAAAAAAAAAgAAAAEAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAEIk0Y
YECCCAAAgAEAAAAAAAAAAAAAAAAIAAAAAAAAAAQiTRhgQIIIAACAmpmZmZmZ8T8AAAAAAP////8AAAAA
"""
