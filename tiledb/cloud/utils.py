import inspect
import logging
from typing import Callable, Optional

logger = logging.getLogger("tiledb.cloud")


def getsourcelines(func: Callable) -> Optional[str]:
    """Attempt to extract the source code of ``func``, but accept failure."""
    try:
        # Attempt to find and serialize the original source...
        return "".join(inspect.getsourcelines(func)[0])
    except OSError as exc:
        # ...but if it's not available, don't panic; just go on without it.
        logger.warning(
            "Failed to serialize function source text, "
            "proceeding with bytecode only: %s",
            exc,
        )
    return None
