import unittest

import numpy as np
from tiledb.cloud import dag


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
    def test_simple_dag(self):
        d = dag.DAG()

        node = d.add_node(lambda x: x * 2, np.median)
        node.name = "node"

        d.exec()

        self.assertEqual(node.results(), None)
        self.assertEqual(node.status, dag.Status.FAILED)
        self.assertEqual(
            str(node.error), "unsupported operand type(s) for *: 'function' and 'int'"
        )

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
