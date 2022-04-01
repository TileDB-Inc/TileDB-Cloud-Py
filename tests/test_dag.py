import base64
import collections
import collections.abc as cabc
import itertools
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
from tiledb.cloud import tasks
from tiledb.cloud._results import decoders
from tiledb.cloud._results import results
from tiledb.cloud._results import stored_params as sp
from tiledb.cloud._results import visitor
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
                namespace=client.default_charged_namespace(),
                nodes=[
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_1.id),
                        name="node_1",
                        depends_on=[],
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_2.id),
                        name="node_2",
                        depends_on=[str(node_1.id)],
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_3.id),
                        name="node_3",
                        depends_on=[str(node_2.id)],
                    ),
                ],
            ),
        )

    def test_simple_cloud_dag(self):
        d = dag.DAG()

        node_1 = d.submit(np.median, [1, 2, 3])
        node_2 = d.submit(lambda x: x * 2, node_1)
        node_3 = d.submit(lambda x: x * 2, node_2)

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

    def _remote_result(self, node: dag_dag.Node) -> results.RemoteResult:
        """Extracts the RemoteResult out of the Node's future."""
        result = node._future.result()  # type: ignore
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
        l = lambda x: x * 2
        node_2 = d.add_node(l, node_1)
        node_2.name = "multi_node_2"
        node_3 = d.add_node(l, node_2)
        node_3.name = "multi_node_3"
        node_4 = d.add_node(l, node_2)
        node_4.name = "multi_node_4"
        node_5 = d.add_node(l, node_2)
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
                namespace=client.default_charged_namespace(),
                nodes=[
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_1.id),
                        name="multi_node_1",
                        depends_on=[],
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_2.id),
                        name="multi_node_2",
                        depends_on=[str(node_1.id)],
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_5.id),
                        name="multi_node_5",
                        depends_on=[str(node_2.id)],
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_4.id),
                        name="multi_node_4",
                        depends_on=[str(node_2.id)],
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_3.id),
                        name="multi_node_3",
                        depends_on=[str(node_2.id)],
                    ),
                    models.TaskGraphNodeMetadata(
                        client_node_uuid=str(node_6.id),
                        name="multi_node_6",
                        depends_on=[
                            str(node_3.id),
                            str(node_4.id),
                            str(node_5.id),
                        ],
                    ),
                ],
            ),
        )

    def test_end_nodes_dag(self):
        d = dag.DAG()

        node_1 = d.add_node(np.median, [1, 2, 3])
        node_1.name = "multi_node_1"
        l = lambda x: x * 2
        node_2 = d.add_node(l, node_1)
        node_2.name = "multi_node_2"
        node_3 = d.add_node(l, node_2)
        node_3.name = "multi_node_3"
        node_4 = d.add_node(l, node_2)
        node_4.name = "multi_node_4"
        node_5 = d.add_node(l, node_2)
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

        self.assertEqual(node2.status, dag.Status.CANCELLED)
        self.assertEqual(node2.result(), None)


class DAGCancelTest(unittest.TestCase):
    def test_dag_cancel(self):
        d = dag.DAG()
        node = d.add_node(time.sleep, 1)
        node_2 = d.add_node(np.mean, [1, 1])
        node_2.depends_on(node)

        d.compute()
        # Cancel DAG
        d.cancel()

        self.assertEqual(d.status, dag.Status.CANCELLED)

        self.assertEqual(node.status, dag.Status.CANCELLED)
        self.assertEqual(node.result(), None)

        self.assertEqual(node_2.status, dag.Status.CANCELLED)
        self.assertEqual(node_2.result(), None)


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
        self.assertEqual(self.status_updates, 5)
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
    n._future = futures.Future()
    n._future.set_result(results.LocalResult(val))
    n.status = dag.Status.COMPLETED
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
