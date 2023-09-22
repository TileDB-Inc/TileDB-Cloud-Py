from typing import List, NewType, Tuple, TypeVar, Union

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
