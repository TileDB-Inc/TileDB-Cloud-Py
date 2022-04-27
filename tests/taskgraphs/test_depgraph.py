import pickle
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
        self.assertEqual(("root", "floater"), g.roots())
        self.assertEqual(("last", "floater"), g.leaves())

        g.add_edge(child="child", parent="child 2")
        self.assertEqual(
            ("root", "floater", "child 2", "child", "grandchild", "last"),
            g.topo_sorted,
        )
        self.assertEqual(("root", "floater"), g.roots())
        self.assertEqual(("last", "floater"), g.leaves())

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
        self.assertEqual(("root", "floater"), g.roots())
        self.assertEqual(("last", "floater"), g.leaves())

        expected_parents_children = {
            "root": ([], ["child", "child 2", "last"]),
            "child": (["root", "child 2"], ["last"]),
            "child 2": (["root"], ["last", "child"]),
            "last": (["root", "child", "child 2"], []),
            "floater": ([], []),
        }
        for node, (parents, children) in expected_parents_children.items():
            with self.subTest(f"{node!r} relationships"):
                # Order is important here.
                self.assertEqual(parents, list(g.parents_of(node)))
                self.assertEqual(children, list(g.children_of(node)))

        with self.assertRaises(KeyError):
            g.children_of("no")
        with self.assertRaises(KeyError):
            g.parents_of("no")

    def test_tinys(self):
        g = depgraph.DepGraph[int]()
        self.assertEqual((), g.topo_sorted)
        self.assertEqual((), g.roots())
        self.assertEqual((), g.leaves())

        g.add_new_node(1, ())
        self.assertEqual((1,), g.topo_sorted)
        self.assertEqual((1,), g.roots())
        self.assertEqual((1,), g.leaves())

        g.remove(1)
        self.assertEqual((), g.topo_sorted)
        self.assertEqual((), g.roots())
        self.assertEqual((), g.leaves())

    def test_diamond(self):
        g = depgraph.DepGraph[bytes]()
        g.add_new_node(b"root", ())
        g.add_new_node(b"left", [b"root"])
        g.add_new_node(b"right", [b"root"])
        g.add_new_node(b"end", [b"left", b"right"])

        self.assertEqual((b"root", b"left", b"right", b"end"), g.topo_sorted)
        self.assertEqual((b"root",), g.roots())
        self.assertEqual((b"end",), g.leaves())

        g.add_edge(child=b"left", parent=b"right")

        self.assertEqual((b"root", b"right", b"left", b"end"), g.topo_sorted)
        self.assertEqual((b"root",), g.roots())
        self.assertEqual((b"end",), g.leaves())

    def test_line(self):
        g = depgraph.DepGraph()
        g.add_new_node(True, ())
        g.add_new_node("FileNotFound", (True,))
        g.add_new_node(False, ("FileNotFound",))

        self.assertEqual((True, "FileNotFound", False), g.topo_sorted)
        self.assertEqual((True,), g.roots())
        self.assertEqual((False,), g.leaves())

        g.remove("FileNotFound")

        self.assertEqual((True, False), g.topo_sorted)
        for relatives in (g.parents_of, g.children_of):
            for value in (True, False):
                self.assertEqual(frozenset(), relatives(value))
        self.assertEqual((True, False), g.roots())
        self.assertEqual((True, False), g.leaves())

    def test_copy(self):
        old: depgraph.DepGraph[int] = depgraph.DepGraph()
        old.add_new_node(1, ())
        old.add_new_node(2, ())
        old.add_new_node(3, (1, 2))
        old.add_new_node(4, ())
        old.add_new_node(5, (1, 2, 3))

        # The easiest way to test that a complex structure is to ensure that
        # the pickle remains unchanged.
        canonical = pickle.dumps(old)

        new = old.copy()
        self.assertEqual(new.topo_sorted, old.topo_sorted)
        for n in (1, 2, 3, 4, 5):
            self.assertEqual(new.parents_of(n), old.parents_of(n))
            self.assertEqual(new.children_of(n), old.children_of(n))

        new.add_edge(child=4, parent=1)
        self.assertEqual(canonical, pickle.dumps(old))
        new.add_new_node(6, (4,))
        self.assertEqual(canonical, pickle.dumps(old))
        new.remove(2)
        self.assertEqual(canonical, pickle.dumps(old))
