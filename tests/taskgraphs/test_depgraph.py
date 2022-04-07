import unittest

from tiledb.cloud.taskgraphs import depgraph


class TestDepGraph(unittest.TestCase):
    def test_it(self):
        g = depgraph.DepGraph[str]()
        g.add_new_node("root", "")
        g.add_new_node("child", ["root"])
        g.add_new_node("grandchild", ["child"])
        g.add_new_node("child 2", ["root"])
        g.add_new_node("last", ["root", "child", "grandchild", "child 2"])
        g.add_new_node("floater", ())
        self.assertEqual(
            ("root", "child", "grandchild", "child 2", "last", "floater"),
            g.topo_sorted,
        )
        g.add_edge(child="child", parent="child 2")
        self.assertEqual(
            ("root", "floater", "child 2", "child", "grandchild", "last"),
            g.topo_sorted,
        )
        with self.assertRaises(depgraph.CyclicGraphError):
            g.add_edge(child="root", parent="last")
        with self.assertRaises(depgraph.CyclicGraphError):
            g.add_edge(child="child", parent="child")
        with self.assertRaises(KeyError):
            g.add_new_node("root", [])
        with self.assertRaises(KeyError):
            g.add_new_node("new-node", ["missing", "existing"])
        with self.assertRaises(KeyError):
            g.add_edge(child="last", parent="missing")
        with self.assertRaises(KeyError):
            g.add_edge(child="missing", parent="root")

        g.remove("grandchild")
        self.assertEqual(
            ("root", "floater", "child 2", "child", "last"),
            g.topo_sorted,
        )

        expected_parents_children = {
            "root": ([], ["child", "child 2", "last"]),
            "child": (["root", "child 2"], ["last"]),
            "child 2": (["root"], ["child", "last"]),
            "last": (["root", "child", "child 2"], []),
            "floater": ([], []),
        }
        for node, (parents, children) in expected_parents_children.items():
            with self.subTest(f"{node!r} relationships"):
                self.assertEqual(frozenset(parents), g.parents_of(node))
                self.assertEqual(frozenset(children), g.children_of(node))

        with self.assertRaises(KeyError):
            g.children_of("no")
        with self.assertRaises(KeyError):
            g.parents_of("no")

    def test_tinys(self):
        g = depgraph.DepGraph[int]()
        self.assertEqual((), g.topo_sorted)
        g.add_new_node(1, ())
        self.assertEqual((1,), g.topo_sorted)
        g.remove(1)
        self.assertEqual((), g.topo_sorted)

    def test_diamond(self):
        g = depgraph.DepGraph[bytes]()
        g.add_new_node(b"root", ())
        g.add_new_node(b"left", [b"root"])
        g.add_new_node(b"right", [b"root"])
        g.add_new_node(b"end", [b"left", b"right"])

        self.assertEqual((b"root", b"left", b"right", b"end"), g.topo_sorted)

        g.add_edge(child=b"left", parent=b"right")

        self.assertEqual((b"root", b"right", b"left", b"end"), g.topo_sorted)

    def test_line(self):
        g = depgraph.DepGraph()
        g.add_new_node(True, ())
        g.add_new_node("FileNotFound", (True,))
        g.add_new_node(False, ("FileNotFound",))

        self.assertEqual((True, "FileNotFound", False), g.topo_sorted)
        g.remove("FileNotFound")
        self.assertEqual((True, False), g.topo_sorted)
        for relatives in (g.parents_of, g.children_of):
            for value in (True, False):
                self.assertEqual(frozenset(), relatives(value))
