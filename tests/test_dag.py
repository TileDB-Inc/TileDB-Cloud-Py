import collections
import collections.abc as cabc
import os
import pickle
import time
import unittest

import numpy as np

import tiledb.cloud
from tiledb.cloud import dag
from tiledb.cloud.dag import dag as internal

tiledb.cloud.login(
    token=os.environ["TILEDB_CLOUD_HELPER_VAR"],
    host=os.environ.get("TILEDB_CLOUD_REST_HOST", None),
)


class DAGClassTest(unittest.TestCase):
    def test_simple_dag(self):
        d = dag.DAG()

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


status_updates = 0
done_updates = 0


class DAGCallbackTest(unittest.TestCase):
    def test_simple_dag(self):
        def status_callback_test(dag):
            global status_updates
            status_updates += 1

        def done_callback_test(dag):
            global done_updates
            done_updates += 1

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
        global status_updates
        global done_updates
        self.assertEqual(status_updates, 5)
        self.assertEqual(done_updates, 1)


def _node(val):
    """Creates a completed node with the given value."""
    n = dag.Node(lambda: None)
    n.status = dag.Status.COMPLETED
    n._results = val
    return n


class CustomSeq(cabc.MutableSequence):
    """Custom sequence implementation to test value replacement."""

    lst: list

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


class TestDAGInternals(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(5, internal._replace_nodes_with_results(5))
        self.assertEqual("hi", internal._replace_nodes_with_results(_node("hi")))

    def test_sequences(self):
        self.assertEqual(
            ["a", "b", "c"],
            internal._replace_nodes_with_results([_node("a"), "b", _node("c")]),
        )
        self.assertEqual(
            (1, 2, ["i", "ii"]),
            internal._replace_nodes_with_results((1, 2, [_node("i"), "ii"])),
        )

    def test_special_sequences(self):
        self.assertEqual(
            "some_string", internal._replace_nodes_with_results("some_string")
        )
        self.assertEqual(b"bytes", internal._replace_nodes_with_results(b"bytes"))

    def test_self_recursion(self):
        dct = {
            "nod": _node(("a", "b", "c")),
        }
        lst = [dct, _node("nod")]
        dct["lst"] = lst
        tup = (_node("lst"), lst, _node("dct"), dct)
        lst.append(tup)
        got_lst = internal._replace_nodes_with_results(lst)

        want_dct = {
            "nod": ("a", "b", "c"),
        }
        want_lst = [want_dct, "nod"]
        want_dct["lst"] = want_lst
        want_tup = ("lst", want_lst, "dct", want_dct)
        want_lst.append(want_tup)

        # assertEqual will blow up if you try to compare a recursive structure.
        # However, pickle handles recursion, so we just see if the results
        # have the same pickling.
        self.assertEqual(pickle.dumps(want_lst), pickle.dumps(got_lst))

    def test_custom_types(self):
        my_seq = CustomSeq("abcde")
        my_seq.append(CustomSeq(("F", _node("G"))))
        my_seq.append(_node("h"))

        self.assertEqual(
            CustomSeq(("a", "b", "c", "d", "e", CustomSeq("FG"), "h")),
            internal._replace_nodes_with_results(my_seq),
        )

        self.assertEqual(
            collections.OrderedDict(zero=0, one=1, two=2),
            internal._replace_nodes_with_results(
                collections.OrderedDict(
                    zero=_node(0),
                    one=_node(1),
                    two=2,
                )
            ),
        )
