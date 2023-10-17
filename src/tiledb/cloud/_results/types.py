import itertools
from typing import Callable, Dict, List, NewType, Tuple, TypeVar, Union

import attrs

_T = TypeVar("_T")
NativeSequence = Union[Tuple[_T, ...], List[_T]]
"""Either of Python's built-in sequences."""

# Aliases to clarify how data is managed through the lifecycle of building
# and executing a task graph.

NativeValue = object
"""Any *native* Python value, as opposed to one encoded into JSON."""

TileDBJSONValue = NewType("TileDBJSONValue", object)
"""JSON-encoded value with enough data to fully reconstruct it.

For instance, this will not include stored parameter references, or node output
values.
"""


@attrs.define(frozen=True, slots=True)
class Arguments:
    """The arguments and keyword arguments that can be sent to a function.

    You usually shouldn't call the constructor directly; instead use
    :meth:``of``.
    """

    args: Tuple[object, ...] = attrs.field(converter=tuple, default=())
    kwargs: Dict[str, object] = attrs.Factory(dict)

    @classmethod
    def of(cls, *args: object, **kwargs: object) -> "Arguments":
        """Creates an Arguments object representing the given call.

        Calling this with any parameters will give you an ``Arguments``
        representing that call:

        >>> Arguments.of(1, 2, a=1, b="two", **{"c": b"four"})
        args(1, 2, a=1, b="two", c=b"four")

        """
        return cls(args, kwargs)

    def apply(self, to: Callable[..., _T]) -> _T:
        return to(*self.args, **self.kwargs)

    def __repr__(self):
        """A representation of this which looks like a function call."""
        parts = itertools.chain(
            map(repr, self.args),
            (f"{k}={v!r}" for (k, v) in self.kwargs.items()),
        )
        joined = ", ".join(parts)
        return f"args({joined})"
