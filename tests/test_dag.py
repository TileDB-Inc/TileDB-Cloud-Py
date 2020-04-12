import unittest
import os

import numpy as np
from tiledb.cloud import dag
import tiledb.cloud

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

        d.exec()

        self.assertEqual(node_1.results(), 2)
        self.assertEqual(node_2.results(), 4)
        self.assertEqual(node_3.results(), 8)

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

        d.exec()

        self.assertEqual(node_1.results(), 2)
        self.assertEqual(node_2.results(), 4)
        self.assertEqual(node_3.results(), "aaaa")

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

        d.exec()

        self.assertEqual(node_1.results(), 2)
        self.assertEqual(node_2.results(), 4)
        self.assertEqual(node_3.results(), 8)
        self.assertEqual(node_4.results(), 8)
        self.assertEqual(node_5.results(), 8)
        self.assertEqual(node_6.results(), 24)


class DAGFailureTest(unittest.TestCase):
    def test_dag_failure(self):
        d = dag.DAG()

        node = d.add_node(lambda x: x * 2, np.median)
        node.name = "node"

        d.exec()

        self.assertEqual(node.results(), None)
        self.assertEqual(node.status, dag.Status.FAILED)
        self.assertEqual(
            str(node.error), "unsupported operand type(s) for *: 'function' and 'int'"
        )

    def test_dag_dependency_fail_early(self):

        d = dag.DAG()

        node = d.add_node(lambda x: x * 2, np.median)
        node.name = "node"
        node2 = d.add_node(lambda x: x * 2, 10)
        node2.name = "node2"
        node2.depends_on(node)

        d.exec()

        self.assertEqual(node.results(), None)
        self.assertEqual(node.status, dag.Status.FAILED)
        self.assertEqual(
            str(node.error), "unsupported operand type(s) for *: 'function' and 'int'"
        )
        self.assertEqual(node2.results(), None)
        self.assertEqual(node2.status, dag.Status.NOT_STARTED)
        self.assertEqual(d.status, dag.Status.FAILED)


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

        d.exec()

        self.assertEqual(node.results(), numpy.sum(orig["a"]))

    def test_dag_udf_exec(self):
        import numpy

        d = dag.DAG()

        node = d.add_node(
            tiledb.cloud.udf.exec, lambda x: numpy.sum(x), arguments=[1, 4, 10, 40]
        )
        node.name = "node"

        d.exec()

        self.assertEqual(node.results(), 55)

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

        d.exec()

        self.assertEqual(node.results()["a"][0], numpy.sum(orig["a"]))

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
            func=mean,
            arguments=[node_array_apply, node_sql],
            name="node_exec",
        )

        d.exec()

        self.assertEqual(node_array_apply.results(), numpy.sum(orig["a"]))
        self.assertEqual(node_sql.results()["a"][0], numpy.sum(orig_dense["a"]))
        self.assertEqual(
            node_exec.results(),
            numpy.mean([numpy.sum(orig["a"]), numpy.sum(orig_dense["a"])]),
        )
        self.assertEqual(d.status, dag.Status.COMPLETED)
