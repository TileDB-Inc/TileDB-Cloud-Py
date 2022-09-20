"""User-facing types used in task graphs."""

import enum
import itertools
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union

import attrs
import numpy as np

_T = TypeVar("_T")
NativeSequence = Union[Tuple[_T, ...], List[_T]]
"""Either of Python's built-in sequences."""

# Aliases to clarify how data is managed through the lifecycle of building
# and executing a task graph.

NativeValue = Any
"""Any *native* Python value, as opposed to one encoded into JSON."""

RegisteredArg = Any
"""JSON-encodable values ready for writing into a registered task graph.

These values are JSON-encodable and may contain
``{"__tdbudf__": "node_output"}`` dictionaries as references to upstream nodes
in their graph.
"""

CallArgStoredParams = Any
"""JSON-encodable params ready for calling the server (with stored params).

These values are JSON-encodable and may contain
``{"__tdbudf__": "stored_param"}`` dictionaries as references to
previously-executed task graph nodes.
"""

CallArg = Any
"""JSON-encodable params ready for calling the server (with values).

These values are JSON-encoded but will have all the information necessary
to decode them contained within their data.
"""

ArrayMultiIndex = Dict[str, np.ndarray]
"""Type returned from an array query."""


class Layout(enum.Enum):
    """The layout of a TileDB query."""

    ROW_MAJOR = "R"
    COL_MAJOR = "C"
    GLOBAL_ORDER = "G"
    UNORDERED = "U"

    @classmethod
    def parse(cls, val: Optional["LayoutOrStr"]) -> Optional["Layout"]:
        if not val:  # Specifically so we support "" as a null layout.
            return None
        if isinstance(val, Layout):
            return val
        upval = val.upper()
        try:
            return cls(upval)
        except ValueError:
            pass
        upval = upval.replace("-", "_")
        try:
            return cls[upval]
        except KeyError:
            raise ValueError(f"{val!r} is not a valid layout")

    def to_json(self) -> str:
        return self.name.lower().replace("_", "-")


LayoutOrStr = Union[Layout, str]


@attrs.define(frozen=True, slots=True)
class Arguments:
    """The arguments and keyword arguments that can be sent to a function.

    You usually shouldn't call the constructor directly; instead use
    :meth:``of``.
    """

    args: Tuple[Any, ...] = attrs.field(converter=tuple, default=())
    kwargs: Dict[str, Any] = attrs.Factory(dict)

    @classmethod
    def of(cls, *args, **kwargs) -> "Arguments":
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


args = Arguments.of
