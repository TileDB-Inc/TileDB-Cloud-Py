import itertools
import unittest

from tiledb.cloud._common import ordered


class TestSets(unittest.TestCase):
    def test_frozen(self):
        s = ordered.FrozenSet(
            ("one", "two", "three", "two", "three", "four", "a billion")
        )
        self.assertEqual(5, len(s))
        self.assertEqual(("one", "two", "three", "four", "a billion"), tuple(s))
        self.assertIn("one", s)
        self.assertNotIn("threeve", s)

        other = ordered.FrozenSet(("one", "three", "two", "four", "a billion"))
        # For compatibility, ordering is not considered when comparing OFSs.
        self.assertEqual(other, s)
        self.assertEqual(hash(other), hash(s))
        # You can also compare an OrderedFrozenSet with a regular frozenset.
        self.assertEqual(frozenset(("one", "two", "three", "four", "a billion")), s)

        self.assertIs(s, s.copy())

        self.assertEqual(
            "FrozenSet(('one', 'two', 'three', 'four', 'a billion'))",
            repr(s),
        )
        self.assertEqual("FrozenSet((1,))", repr(ordered.FrozenSet((1,))))

    def test_mutable(self):
        s = ordered.Set((b"bytes", b"MORE BYTES"))
        self.assertEqual(2, len(s))
        s.add(b"bytes")
        s.add(b"different")
        self.assertEqual(3, len(s))
        self.assertEqual((b"bytes", b"MORE BYTES", b"different"), tuple(s))
        self.assertEqual({b"bytes", b"different", b"MORE BYTES"}, s)

        self.assertEqual(
            "Set((b'bytes', b'MORE BYTES', b'different'))",
            repr(s),
        )

        s.remove(b"MORE BYTES")
        with self.assertRaises(KeyError):
            s.remove(b"bogus")
        s.discard(b"bogus")  # doesn't error
        self.assertEqual(2, len(s))
        self.assertEqual((b"bytes", b"different"), tuple(s))

        self.assertEqual(b"different", s.pop())
        self.assertIn(b"bytes", s)
        self.assertNotIn(b"missing", s)

        s.clear()
        self.assertEqual(0, len(s))
        self.assertEqual((), tuple(s))

        with self.assertRaises(TypeError):
            hash(s)

        s2 = s.copy()
        s2.add(b"hello")
        self.assertEqual((), tuple(s))
        self.assertEqual((b"hello",), tuple(s2))
        self.assertEqual("Set((b'hello',))", repr(s2))

    def test_permutations(self):
        """Detailed insertion order test."""
        for cls in (ordered.FrozenSet, ordered.Set):
            with self.subTest(cls):
                for perm in itertools.permutations((1, 2, 3, 4)):
                    with self.subTest(perm):
                        perm_set = cls(perm)
                        self.assertEqual(perm, tuple(perm_set))
