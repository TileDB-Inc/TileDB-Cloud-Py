import json
from typing import Any, Dict, List, Optional, Sequence, cast

from .._common import visitor
from . import codecs
from . import types

SENTINEL_KEY = "__tdbudf__"
ESCAPE_CODE = "__escape__"
_RAW_JSON = "raw_json"


class Encoder(visitor.ReplacingVisitor):
    """Turns arbitrary Python values into TileDB JSON.

    This escapes arbitrary native values so that they can be JSON-serialized.
    It should only be used with ``NativeValue``s—that is, values that are
    already JSON-serializable, like ``RegisteredArg``s or ``CallArg``s, should
    *not* be passed to an ``Escaper``. The base implementation will return
    fully self-contained JSON-serializable objects, i.e. ``CallArg``s.
    """

    def encode_arguments(
        self, arguments: types.Arguments
    ) -> Sequence[types.TileDBJSONValue]:
        """Encodes Python arguments as TileDB JSON.

        This is a convenience method to encode a whole set of ``Arguments`` into
        the TileDB JSON arguments format. This includes both basic encoding
        as well as adding the ``raw_json`` sentinel to arguments that do not
        include any TileDB JSON data (to avoid descending into them).
        """
        encoded: List[Dict[str, object]] = []
        encoded.extend({"value": self._encode_arg(val)} for val in arguments.args)
        encoded.extend(
            {"name": name, "value": self._encode_arg(val)}
            for (name, val) in arguments.kwargs.items()
        )
        return cast(Sequence[types.TileDBJSONValue], encoded)

    def _encode_arg(self, val: object) -> types.TileDBJSONValue:
        encoded = self.visit(val)
        if encoded is val and encoded and isinstance(encoded, (dict, list, tuple)):
            # If we get here, then there is no TileDB-specific data, since
            # the object we got out of encoding is the same object we passed in.
            # Using the _RAW_JSON sentinel, we can avoid descending into this
            # object on the decoding side.
            return types.TileDBJSONValue({SENTINEL_KEY: _RAW_JSON, _RAW_JSON: encoded})
        return types.TileDBJSONValue(encoded)

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
        if kind == _RAW_JSON:
            # `raw_json` is a special sentinel indicating that the value in
            # the `raw_json` field is pure JSON with no TileDB values inside it.
            # This means we can avoid descending into it. For example:
            #
            #   {"__tdbudf__": "raw_json", "raw_json": [some huge matrix]}
            #
            # Initially we only use it to write parameters and not results.
            return visitor.Replacement(value[_RAW_JSON])
        if kind == "immediate":
            # "immediate" values are values of the format
            #   {fmt: format name, base64_data: data_string}
            # where the format name is one of the codecs in codecs.py
            # and the base64_data is the encoded data.
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
