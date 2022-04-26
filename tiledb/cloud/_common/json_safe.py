from typing import Generic, TypeVar

import attrs

_T_co = TypeVar("_T_co", covariant=True)


# This really should be a `slots` class, but setting `slots=True` breaks things
# in python 3.6.
@attrs.define(frozen=True, slots=False)
class Value(Generic[_T_co]):
    """Sentinel for a value that is known to be JSON-serializable.

    In cases where you know we're generating JSON-safe values where the
    generated API client does not need to recurse into this to look for more
    values that need to be converted into JSON, you can wrap the variable
    you're generating into this.
    """

    value: _T_co
