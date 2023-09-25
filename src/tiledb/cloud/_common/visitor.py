"""Module containing the base abstract replacing visitor and shared logic."""

import abc
from typing import Any, Dict, Generic, Iterable, Optional, TypeVar

import attrs

_T_co = TypeVar("_T_co", covariant=True)


# This really should be a `slots` class, but setting `slots=True` breaks things
# in python 3.6.
@attrs.define(frozen=True, slots=False)
class Replacement(Generic[_T_co]):
    """A sentinel return value to indicate that the value should be replaced.

    This wrapper ensures that we are able to replace nodes with `None`
    or other falsey values if needed.
    """

    value: _T_co


class ReplacingVisitor(metaclass=abc.ABCMeta):
    """An abstract class to descend through data structure, replacing values.

    An instance of this class should be used in a one-shot manner to descend
    into a data structure and return a new, equivalent structure, but with
    nodes (specified by :meth:`maybe_replace`) replaced in the output.

    See implementations immediately below, or Doubler in the tests.
    """

    def __init__(self) -> None:
        # A dictionary mapping the ID of every object we have seen in our
        # traversal to the object it is replaced with, to avoid duplicating
        # work or getting caught in self-referential structures.
        self.seen: Dict[int, object] = {}
        # A dictionary mapping IDs of every object we have probed in our
        # pre-traversal to:
        # - True, if it or a child node needs to be replaced.
        # - False, if nothing in its subtree needs replacement and it can be
        #   used as-is.
        # - None, if we are still descending through this object.
        self._needs_replacement: Dict[int, Optional[bool]] = {}

    def visit(self, arg: object) -> object:
        """Visits a single node of the data structure and returns its new value.

        This function recursively descends through a data structure to transform
        it into a new value. It is both the entry point (i.e., the caller
        passes in the value it wants to transform) and the internal recursive
        step (i.e., each sub-node of that value is passed here to be transformed
        as well).

        It returns the value that the input is transformed into, which may be
        the same value as was passed in.
        """
        original_id = id(arg)
        try:
            # If we have already seen this exact instance,
            # return the one we calculated before.
            return self.seen[original_id]
        except KeyError:
            pass  # We haven't seen this object yet; continue.

        # First, handle if this is something to replace directly.
        replacement = self.maybe_replace(arg)
        if replacement:
            self._needs_replacement[original_id] = True
            self.seen[original_id] = replacement.value
            return replacement.value

        deep_needs_replacement = self._probe(arg)
        if not deep_needs_replacement:
            # Sanity-check to ensure that the invariants we maintain are held.
            assert deep_needs_replacement is not None, "probe did not complete properly"
            # If this node and its children do not need to be replaced,
            # just return the original object.
            self.seen[original_id] = arg
            return arg

        # Descend into built-in sequence and mapping types.
        # We only descend into the built-in types that directly serialize to
        # JSON.

        if isinstance(arg, list):
            # Mutable types may contain self references, so we create one and
            # store it as the canonical substitution for this instance in case
            # we see this original again.

            # Still call `type(arg)()` rather than `list()` or `[]` in case
            # this is a custom list subtype.
            new_list = type(arg)()
            self.seen[original_id] = new_list
            new_list.extend(map(self.visit, arg))
            return new_list
        if isinstance(arg, tuple):
            # We assume that calling an immutable tuple subtype with an
            # iterable argument returns that sequence, initialized with
            # the values from that iterable (like `tuple(some_iterable)`).
            new_tuple = type(arg)(map(self.visit, arg))
            self.seen[original_id] = new_tuple
            return new_tuple
        if isinstance(arg, dict):
            # As before, create the mapping in advance to allow self references.

            # Similar to sequences, we assume that an empty call to a mapping
            # type gives us an empty version we can then update, like `dict()`.
            new_dict = type(arg)()
            self.seen[original_id] = new_dict
            new_dict.update((k, self.visit(v)) for k, v in arg.items())
            return new_dict

        # Otherwise, we just return the original thing.
        self.seen[original_id] = arg
        return arg

    def _probe(self, arg: object) -> Optional[bool]:
        """Probes a node and finds if anything in its tree needs replacement."""
        original_id = id(arg)
        try:
            return self._needs_replacement[original_id]
        except KeyError:
            pass  # We still need to probe this object.

        # Find out if we have to replace this directly.
        replacement = self.maybe_replace(arg)
        if replacement:
            self.seen[original_id] = replacement.value
            self._needs_replacement[original_id] = True
            return True

        # Set this so that we don't get lost in a recursive structure.
        self._needs_replacement[original_id] = None

        # Figure out what the children we may need to iterate over are.
        children: Iterable[Any] = ()
        if isinstance(arg, (list, tuple)):
            children = arg
        elif isinstance(arg, dict):
            children = arg.values()

        # Probe every child of this object to see if we need to replace it.
        for child in children:
            if self._probe(child):
                self._needs_replacement[original_id] = True
                return True

        # If we got here, none of the children needed to be replaced either,
        # so this node does not need to be replaced.
        self._needs_replacement[original_id] = False
        return False

    @abc.abstractmethod
    def maybe_replace(self, arg: object) -> Optional[Replacement]:
        """Abstract function returning a value if it should be replaced.

        This will be called as the visitor visits every node of the data
        structure. If the node should be replaced with some value, it should
        return that value wrapped in a :class:`_Replacement`. If it returns
        None, the replacer will visit the node as normal.
        """
        raise NotImplementedError()
