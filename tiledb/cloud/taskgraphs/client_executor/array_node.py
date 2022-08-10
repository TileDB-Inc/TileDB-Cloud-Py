import itertools
import uuid
from typing import Any, Dict, Optional, TypeVar

import numpy as np

from tiledb.cloud import rest_api
from tiledb.cloud.taskgraphs.client_executor import _base
from tiledb.cloud.taskgraphs.client_executor import _replacers

_T = TypeVar("_T")


class ArrayNode(_base.Node[_base.ET, _T]):
    """A node representing a read from a TileDB Array.

    This node is not executed by itself; instead, it only appears as an input
    to TileDB UDF nodes.
    """

    def __init__(
        self,
        uid: uuid.UUID,
        owner: _base.ET,
        name: Optional[str],
        json_data: Dict[str, Any],
    ):
        super().__init__(uid, owner, name)
        self._array_data = json_data["array_node"]
        self._details: Optional[Dict[str, Any]] = None

    def _exec_impl(
        self,
        parents: Dict[uuid.UUID, _base.Node],
        input_value: Any,
    ) -> None:
        assert input_value is _base.NOTHING
        uri = self._array_data["uri"]
        ranges_dict: Dict[str, Any] = self._array_data.get("ranges")
        buffers = self._array_data.get("buffers")
        replacer = _replacers.NodeOutputValueReplacer(parents)
        # We unconditionally visit ranges_dict because that may always contain
        # encoded data (e.g., slices), even if the node has no parents.
        ranges_dict = replacer.visit(ranges_dict)
        if parents:
            # ...whereas uri and buffers are always guaranteed to be pure JSON.
            uri = replacer.visit(uri)
            buffers = replacer.visit(buffers)

        request_ranges = {}
        friendly_ranges = ranges_dict.get("friendly_ranges")
        raw_ranges = ranges_dict.get("ranges")
        if friendly_ranges is not None:
            if raw_ranges is not None:
                raise ValueError("either ranges or friendly_ranges must be set, not both")
            request_ranges["ranges"] = _canonicalize_ranges(friendly_ranges)
        else:
            request_ranges["ranges"] = raw_ranges
        # Fix needed to work around deserialization problems on the server side.
        # We don't use setdefault here because `None` is also an invalid value.
        # TODO: remove this.
        ranges_dict["ranges"] = ranges_dict.get("ranges") or ()
        self._details = dict(
            parameter_id=str(self.id),
            uri=uri,
            ranges=request_ranges,
            buffers=buffers,
        )

    def task_id(self, timeout: Optional[float] = None) -> Optional[uuid.UUID]:
        return None

    def _result_impl(self):
        raise TypeError("ArrayNode is a virtual node and does not have results.")

    def _udf_array_details(self) -> Dict[str, Any]:
        self._assert_succeeded()
        assert self._details
        return self._details

    def _encode_for_param(self, mode: _base.ParamFormat):
        del mode  # unused
        self._assert_succeeded()
        return {
            "__tdbudf__": "udf_array_details",
            "udf_array_details": self._udf_array_details(),
        }

    def _run_location(self) -> str:
        return rest_api.TaskGraphLogRunLocation.VIRTUAL


def _canonicalize_ranges(rangeses):
    return tuple(_canonicalize_dimension_ranges(r) for r in rangeses)


def _canonicalize_dimension_ranges(ranges):
    """Builds the canonical range index for a single value."""
    if ranges is None:
        return ()

    # Scalar values specify exactly one entry
    single_span = _unambiguous_span_from(ranges)
    if single_span is not None:
        return single_span

    # Otherwise, this means that we have a sequence.
    if not isinstance(ranges, (list, tuple)):
        raise TypeError(
            "Ranges over a single dimension must be a list or tuple,"
            f" not {type(ranges)}."
        )

    return tuple(itertools.chain.from_iterable(map(_entry_to_span, ranges)))


def _entry_to_span(it) -> tuple:
    single_span = _unambiguous_span_from(it)
    if single_span is not None:
        return single_span
    if not isinstance(it, (list, tuple)):
        raise TypeError(
            "A span in a range must be a scalar value or a"
            f" 1- or 2-entry list, not {type(it)}."
        )
    if not it:
        return ()
    if len(it) == 1:
        canon = _canonicalize_scalar(it[0], fail_loudly=True)
        return (canon, canon)
    if len(it) == 2:
        return tuple(_canonicalize_scalar(x, fail_loudly=True) for x in it)
    raise ValueError(f"A span in a range must be a 1- or 2-entry list; got {len(it)}.")


def _unambiguous_span_from(it) -> Optional[tuple]:
    """Converts an entry of a scalar value or a slice to a span, if possible.

    Returns None if the value is not a scalar.
    """
    if isinstance(it, slice):
        if it.step is not None:
            raise ValueError("Slices with steps are not supported.")
        if it.start is it.stop is None:
            return ()
        if it.start is None or it.stop is None:
            raise ValueError("Both start and stop of a slice must be specified.")
        return (
            _canonicalize_scalar(it.start, fail_loudly=True),
            _canonicalize_scalar(it.stop, fail_loudly=True),
        )
    # This will be None if `it` is not a scalar.
    canon = _canonicalize_scalar(it)
    return None if canon is None else (canon, canon)


_SCALARS = (float, int, str, np.datetime64, np.timedelta64)


def _canonicalize_scalar(it, *, fail_loudly: bool = False):
    if not isinstance(it, _SCALARS):
        if fail_loudly:
            raise TypeError(
                f"A range cannot be of type {type(it)}; only {_SCALARS} are supported."
            )
        return None
    if isinstance(it, (np.datetime64, np.timedelta64)):
        return int(it.astype("int64"))
    return it
