import base64
import json
from typing import Any, Dict, Optional, TypeVar, Union

import cloudpickle

from tiledb.cloud._results import decoders
from tiledb.cloud._results import visitor

_T = TypeVar("_T")
TOrDict = Union[_T, Dict[str, Any]]
_SENTINEL_KEY = "__tiledb_sentinel__"
_ESCAPE_CODE = "__escape__"


class Unescaper(visitor.ReplacingVisitor):
    """A general-purpose replacer to unescape sentinel-containing structures.

    This descends through data structures and replaces dictionaries containing
    ``__tiledb_sentinel__`` values with the unescaped values. This base
    implementation handles only the basics; you can create a derived version
    to handle specific situations (building arguments, replacing values, etc.).s
    """

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if not isinstance(arg, dict):
            return None
        if _SENTINEL_KEY not in arg:
            return None
        sentinel_value: Dict[str, Any] = arg[_SENTINEL_KEY]
        count = len(sentinel_value)
        if count != 1:
            entries = tuple(sentinel_value)
            raise ValueError(
                f"A sentinel value may have only one key. Had {count}: {entries!r}"
            )
        key, value = next(iter(sentinel_value.items()))
        return self._replace_sentinel(key, value)

    def _replace_sentinel(
        self,
        inner_key: str,
        inner_value: Any,
    ) -> Optional[visitor.Replacement]:
        """The base implementation of a sentinel-replacer.

        It is passed the ``inner_key`` and ``inner_value`` of a
        ``__tiledb_sentinel__``–containing object::

            # Given this:
            {"__tiledb_sentinel__": {"node_data": "qwerty"}}
            # This will be called:
            self._replace_sentinel("node_data", "qwerty")

        This implementation handles replacing values that do not require any
        external information. Derived implementations should handle their own
        keys and end with a call to
        ``return super()._replace_sentinel(inner_key, inner_value)``.
        """
        if inner_key == _ESCAPE_CODE:
            # A value that looks like {sentinel: {escape: [something]}}
            return visitor.Replacement(
                {k: self.visit(v) for (k, v) in inner_value.items()}
            )
        if inner_key == "immediate":
            fmt = inner_value["format"]
            base64d = inner_value["base64_data"]
            data = base64.b64decode(base64d)
            return visitor.Replacement(_LOADERS[fmt](data))
        raise ValueError(f"Unknown sentinel key {inner_key!r}")


# TODO: Move these to decoders._DECODE_FNS functions once our API is firmed up.
_LOADERS = {
    "arrow": decoders._load_arrow,
    "bytes": bytes,
    "json": json.loads,
    "python_pickle": cloudpickle.loads,
}
