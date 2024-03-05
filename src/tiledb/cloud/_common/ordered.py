"""Implementations of Python sets that remember their order."""

from typing import AbstractSet as _AbstractSet
from typing import Iterable, Iterator, TypeVar
from typing import MutableSet as _MutableSet

from typing_extensions import Self

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)


class FrozenSet(_AbstractSet[_T_co]):
    """A frozenset that remembers the insertion order of elements.

    Unlike dicts, Python sets don't remember insertion order. This class
    is useful for situations where you want to have a consistent order
    of set elements, like when iteration order is important or to make
    tests consistent.

    The ordering this set has is the order that elements were inserted,
    just like a dict has insertion order. Apart from this, it behaves
    exactly as a frozenset. This notably includes that *comparisons are
    order-independent*. Two differently-ordered OrderedFrozenSets are
    considered equal.
    """

    def __init__(self, source: Iterable[_T_co] = ()):
        self._dict = {x: None for x in source}

    def copy(self) -> Self:
        """Returns itself, because it's immutable."""
        return self

    def __len__(self) -> int:
        return len(self._dict)

    def __contains__(self, item) -> bool:
        return item in self._dict

    def __iter__(self) -> Iterator[_T_co]:
        return iter(self._dict)

    def __hash__(self) -> int:
        return self._hash()  # type: ignore[attr-defined] # (false alarm)

    def __repr__(self) -> str:
        contents = ", ".join(map(repr, self))
        if len(self) == 1:
            contents += ","
        return f"{type(self).__name__}(({contents}))"


class Set(FrozenSet[_T], _MutableSet[_T]):
    """An :class:`_OrderedFrozenSet`, but this time it's mutable.

    Not guaranteed to be thread-safe.
    """

    def copy(self) -> Self:
        """Returns a shallow copy of this set. Equivalent to ``set.copy()``."""
        return type(self)(self)

    def add(self, val: _T) -> None:
        self._dict[val] = None

    def discard(self, val: _T) -> None:
        try:
            self.remove(val)
        except KeyError:
            pass

    def remove(self, val: _T) -> None:
        del self._dict[val]

    def pop(self) -> _T:
        """Drops and returns the most recently-added item."""
        return self._dict.popitem()[0]

    def clear(self) -> None:
        self._dict.clear()

    def popleft(self) -> _T:
        """Drops and returns the least recently-added item. New!"""
        try:
            start = next(iter(self))
        except StopIteration:
            raise KeyError("pop from an empty ordered set")
        self._dict.pop(start)
        return start

    def update(self, *others: Iterable[_T]) -> None:
        """Adds every element from the ``others`` iterables to this one."""
        for oth in others:
            for item in oth:
                self.add(item)

    __hash__ = None  # type: ignore[assignment]
    """This is mutable, so it's not hashable."""


__all__ = ("FrozenSet", "Set")
