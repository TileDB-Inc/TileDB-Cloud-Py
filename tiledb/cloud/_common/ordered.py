"""Implementations of Python sets that remember their order."""

from typing import AbstractSet, Iterable, Iterator, MutableSet, TypeVar

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_Self = TypeVar("_Self", bound="FrozenSet")
"""Annotation for returning an object of your own type.

See https://peps.python.org/pep-0673/.
"""


class FrozenSet(AbstractSet[_T_co]):
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

    def copy(self: _Self) -> _Self:
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


class Set(FrozenSet[_T], MutableSet[_T]):
    """An :class:`_OrderedFrozenSet`, but this time it's mutable."""

    def copy(self: _Self) -> _Self:
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

    __hash__ = None  # type: ignore[assignment]
    """This is mutable, so it's not hashable."""
