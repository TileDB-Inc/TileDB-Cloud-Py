from typing import Any

import attrs


@attrs.define(frozen=True, slots=True)
class Value:
    """Sentinel for a value that is known to be JSON-serializable.

    In cases where you know we're generating JSON-safe values where the
    generated API client does not need to recurse into this to look for more
    values that need to be converted into JSON, you can wrap the variable
    you're generating into this.
    """

    value: Any
