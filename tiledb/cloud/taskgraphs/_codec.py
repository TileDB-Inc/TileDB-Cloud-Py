import base64
import json
from typing import Any, Dict, Optional, TypeVar, Union

import cloudpickle

from tiledb.cloud._results import decoders
from tiledb.cloud._results import visitor

_T = TypeVar("_T")
TOrDict = Union[_T, Dict[str, Any]]
_SENTINEL_KEY = "__tdbudf__"
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
        sentinel_name = arg[_SENTINEL_KEY]
        return self._replace_sentinel(sentinel_name, arg)

    def _replace_sentinel(
        self,
        kind: str,
        value: Dict[str, Any],
    ) -> Optional[visitor.Replacement]:
        """The base implementation of a sentinel-replacer.

        It is passed the kind and value of a ``__tdbudf__``–containing object::

            # Given this:
            the_object = {"__tdbudf__": "node_data", "data": "abc"}
            # This will be called:
            self._replace_sentinel("node_data", the_object)

        This implementation handles replacing values that do not require any
        external information. Derived implementations should handle their own
        keys and end with a call to
        ``return super()._replace_sentinel(kind, value)``.
        """
        if kind == _ESCAPE_CODE:
            # An escaped value.
            inner_value = value[_ESCAPE_CODE]
            return visitor.Replacement(
                {k: self.visit(v) for (k, v) in inner_value.items()}
            )
        if kind == "immediate":
            fmt = value["format"]
            base64d = value["base64_data"]
            data = base64.b64decode(base64d)
            return visitor.Replacement(_LOADERS[fmt](data))
        raise ValueError(f"Unknown sentinel type {kind!r}")


# TODO: Move these to decoders._DECODE_FNS functions once our API is firmed up.
_LOADERS = {
    "arrow": decoders._load_arrow,
    "bytes": bytes,
    "json": json.loads,
    "native": cloudpickle.loads,
    "python_pickle": cloudpickle.loads,
}
