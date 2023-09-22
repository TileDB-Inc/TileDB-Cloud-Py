import json
from typing import Any, Dict, Optional

from .._common import visitor
from . import codecs

SENTINEL_KEY = "__tdbudf__"
ESCAPE_CODE = "__escape__"


class Encoder(visitor.ReplacingVisitor):
    """Turns arbitrary Python values into TileDB JSON.

    This escapes arbitrary native values so that they can be JSON-serialized.
    It should only be used with ``NativeValue``s—that is, values that are
    already JSON-serializable, like ``RegisteredArg``s or ``CallArg``s, should
    *not* be passed to an ``Escaper``. The base implementation will return
    fully self-contained JSON-serializable objects, i.e. ``CallArg``s.
    """

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if is_jsonable_shallow(arg):
            if isinstance(arg, dict):
                if SENTINEL_KEY in arg:
                    return visitor.Replacement(
                        {
                            SENTINEL_KEY: ESCAPE_CODE,
                            ESCAPE_CODE: {k: self.visit(v) for (k, v) in arg.items()},
                        }
                    )
            return None
        return visitor.Replacement(codecs.BinaryBlob.of(arg)._tdb_to_json())


class Decoder(visitor.ReplacingVisitor):
    """A general-purpose replacer to decode sentinel-containing structures.

    This descends through data structures and replaces dictionaries containing
    ``__tdbudf__`` values with the unescaped values. This base implementation
    handles only the basics; you can create a derived version to handle specific
    situations (building arguments, replacing values, etc.).

    The data that is returned from this is generally a ``types.NativeValue``.
    """

    def maybe_replace(self, arg) -> Optional[visitor.Replacement]:
        if not isinstance(arg, dict):
            return None
        try:
            sentinel_name = arg[SENTINEL_KEY]
        except KeyError:
            return None
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
        if kind == ESCAPE_CODE:
            # An escaped value.
            inner_value = value[ESCAPE_CODE]
            # We can't just visit `inner_value` here, since `inner_value`
            # is the thing which has the ESCAPE_CODE key that is being escaped.
            return visitor.Replacement(
                {k: self.visit(v) for (k, v) in inner_value.items()}
            )
        if kind == "immediate":
            # "immediate" values are values of the format
            fmt = value["format"]
            base64d = value["base64_data"]
            return visitor.Replacement(
                codecs.CODECS_BY_FORMAT[fmt].decode_base64(base64d)
            )
        raise ValueError(f"Unknown sentinel type {kind!r}")


def dumps(obj: object) -> bytes:
    """Dumps an object to TileDB UDF–encoded JSON."""
    enc = Encoder()
    result_json = enc.visit(obj)
    return json.dumps(result_json).encode("utf-8")


def loads(data: bytes) -> object:
    """Loads TileDB UDF–encoded JSON to an object."""
    data_json = json.loads(data)
    dec = Decoder()
    return dec.visit(data_json)


_NATIVE_JSONABLE = (
    str,
    int,
    bool,
    float,
    type(None),
    list,
    tuple,
)
"""Types whose direct values can always be turned into JSON."""


def is_jsonable_shallow(obj) -> bool:
    if isinstance(obj, _NATIVE_JSONABLE):
        return True
    if not isinstance(obj, dict):
        # Apart from the above types, only dicts are JSONable.
        return False
    # For a dict to be JSONable, all keys must be strings.
    return all(isinstance(key, str) for key in obj)
