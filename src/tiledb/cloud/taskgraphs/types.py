"""User-facing types used in task graphs."""

import enum
from typing import Any, Dict, Optional, Union

import numpy as np

from .._results import types

# Re-exports of things that were previously in this module.
Arguments = types.Arguments
args = Arguments.of
NativeSequence = types.NativeSequence
NativeValue = types.NativeValue
TileDBJSONValue = types.TileDBJSONValue

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

# Re-export Arguments type.
