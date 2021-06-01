import inspect
import logging
from typing import Callable, Optional, TypeVar

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


_T = TypeVar("_T")


def signature_of(src: Callable) -> Callable[[_T], _T]:
    """Decorator that applies the signature of ``func`` to the wrapped function.

    This allows autocomplete tools, like in Jupyter notebooks or IPython,
    to use function signature information from the source function when
    providing help for users about the destination function.

    In this example, users will be able to see prompts for ``b`` or ``c``
    when they press ``Tab`` while writing a call to  ``iter_a``:

    >>> def a(b, c):
    ...   return f'Hello, {b}! I am {c}.'
    >>> @signature_of(a)
    ... def iter_a(*args, **kwargs):
    ...   yield a(*args, **kwargs)
    """

    def copy_to(dst):
        dst.__signature__ = inspect.signature(src)
        return dst

    return copy_to
