import unittest

from tiledb.cloud.taskgraphs.delayed import _graph


class DummyNode(_graph.Node):
    @classmethod
    def create(cls, *parents: _graph.Node):
        mgr = _graph.Merger()
        mgr.visit(parents)
        new_owner = mgr.merge_visited()
        new = cls(new_owner)
        new_owner._add(new, parents=mgr.unexecuted_nodes)
        return new


class TestBuild(unittest.TestCase):
    def test_merge(self):
        node_0 = DummyNode.create()
        owner_0 = node_0._owner
        self.assertIsNotNone(owner_0)
        node_1 = DummyNode.create()

        node_merged = DummyNode.create(node_0, node_1)

        self.assertIs(owner_0, node_0._owner)
        self.assertIs(owner_0, node_1._owner)
        self.assertIs(owner_0, node_merged._owner)

    def test_split_merge(self):
        start = DummyNode.create()
        start_owner = start._owner
        left = DummyNode.create(start)
        right = DummyNode.create(start)
        merge = DummyNode.create(left, right)

        for n in (start, left, right, merge):
            self.assertIs(start_owner, n._owner)

    def test_already_running(self):
        running = DummyNode.create()
        running._owner._execution = object()  # enough to make it truthy
        other = DummyNode.create(running)
        self.assertIsNot(running._owner, other._owner)
