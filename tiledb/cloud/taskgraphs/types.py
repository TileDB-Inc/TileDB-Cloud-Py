"""User-facing types used in task graphs."""

from typing import Any, Dict, List, Tuple, TypeVar, Union

import attrs

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


@attrs.define(frozen=True, slots=True)
class Arguments:
    """The arguments and keyword arguments that can be sent to a function.

    You usually shouldn't call the constructor directly; instead use
    :meth:``of``.
    """

    args: tuple = ()
    kwargs: Dict[str, Any] = attrs.Factory(dict)

    @classmethod
    def of(cls, *args, **kwargs) -> "Arguments":
        """Creates an Arguments object representing the given call."""
        return cls(args, kwargs)


args = Arguments.of
