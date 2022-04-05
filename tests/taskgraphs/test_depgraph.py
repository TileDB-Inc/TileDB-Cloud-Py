import unittest

from tiledb.cloud.taskgraphs import depgraph


class TestDepGraph(unittest.TestCase):
    def test_it(self):
        g = depgraph.DepGraph[str]()
        g.add_new_node("a", "")
        g.add_new_node("b", "a")
        g.add_new_node("c", "b")
        g.add_new_node("d", "a")
        g.add_new_node("e", "abcd")
        self.assertEqual(tuple("abcde"), g.topo_sorted)
        g.add_edge(child="b", parent="d")
        self.assertEqual(tuple("adbce"), g.topo_sorted)
        with self.assertRaises(depgraph.CyclicGraphError):
            g.add_edge(child="a", parent="e")
        with self.assertRaises(depgraph.CyclicGraphError):
            g.add_edge(child="b", parent="b")
        with self.assertRaises(KeyError):
            g.add_new_node("b", "")
        with self.assertRaises(KeyError):
            g.add_new_node("f", "gh")
        with self.assertRaises(KeyError):
            g.add_edge(child="a", parent="q")

        g.remove("c")
        self.assertEqual(tuple("adbe"), g.topo_sorted)
