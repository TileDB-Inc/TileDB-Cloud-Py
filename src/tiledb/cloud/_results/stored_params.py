"""Handles stored parameters for clients and the UDF environment."""

import base64
import dataclasses
import uuid
from typing import Any, Dict, Generic, TypeVar

from . import decoders

_T = TypeVar("_T")


@dataclasses.dataclass(frozen=True)
class StoredParam(Generic[_T]):
    """The information needed to identify and decode a stored parameter.

    This type is used as a sentinel for stored params in Python UDF parameters.
    When the UDF execution environment unpacks its parameters, if it runs into
    a StoredParam value, it will unpack it from the server-side stored parameter
    dictionary, replacing the StoredParam instance with the actual value that
    should be replaced.

    The exact name and location of this class is important, because instances
    are sent as pickles when making UDF requests.
    """

    # The server-generated UUID included in the X-TileDB-Cloud-Task-ID header.
    task_id: uuid.UUID

    # The Decoder that will be used to turn the bytes into a useful value.
    decoder: decoders.AbstractDecoder[_T]

    def decode(self, binary_data: bytes) -> _T:
        return self.decoder.decode(binary_data)


class MissingError(KeyError):
    """Subclass of KeyError raised when there's a missing stored parameter."""


class ParamLoader:
    """A class to load server-side params while reusing loaded instances."""

    def __init__(self, raw_params: Dict[str, str]):
        """Sets up a new ParamLoader.

        :param raw_params: A dictionary of UUID-as-hex-string (no ``{}``s)
          to base64-encoded binary data.
        """
        self._raw_params = raw_params
        self._loaded: Dict[StoredParam, Any] = {}

    def load(self, param: StoredParam) -> Any:
        """Loads the given parameter from the input, reusing instances.

        This is not guaranteed to be thread-safe since we expect to restore
        server-side parameters on one thread.
        """
        try:
            return self._loaded[param]
        except KeyError:
            pass  # not cached yet.
        try:
            b64_data = self._raw_params[str(param.task_id)].encode("ascii")
        except KeyError as ke:
            actual_key = ke.args[0]
            present = self._raw_params.keys()
            raise MissingError(
                actual_key,
                f"Stored parameter {actual_key!r} was not found."
                f" All available parameters: {set(present)}",
            ) from None
        binary_data = base64.standard_b64decode(b64_data)
        real_data = param.decode(binary_data)
        self._loaded[param] = real_data
        return real_data
