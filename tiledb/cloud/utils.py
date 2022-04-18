import base64
import inspect
import logging
import sys
import urllib
from typing import Any, Callable, Optional, TypeVar

import cloudpickle

TILEDB_CLOUD_PROTOCOL = 4

# General-use logger for TileDB Cloud.
logger = logging.getLogger("tiledb.cloud")


_builtin_function = type(len)
"""The type of functions implemented in C."""


def split_uri(uri):
    """
    Split a URI into namespace and array name

    :param uri: uri to split into namespace and array name
    :param async_req: return future instead of results for async support
    :return: tuple (namespace, array_name)
    """
    parsed = urllib.parse.urlparse(uri)
    if not parsed.scheme == "tiledb":
        raise Exception("Incorrect array uri, must be in tiledb:// scheme")
    return parsed.netloc, parsed.path[1:]


def getsourcelines(func: Callable) -> Optional[str]:
    """Attempt to extract the source code of ``func``, but accept failure."""
    if isinstance(func, _builtin_function):
        # Built-in functions have no accessible source code.
        return None
    try:
        # Attempt to find and serialize the original source...
        return "".join(inspect.getsourcelines(func)[0])
    except Exception as exc:
        pass
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


def b64_pickle(obj: Any) -> str:
    """Pickles the given object, then base64 encodes the pickle."""
    pickle = cloudpickle.dumps(obj, protocol=TILEDB_CLOUD_PROTOCOL)
    return base64.b64encode(pickle).decode("ascii")


PYTHON_VERSION = ".".join(map(str, sys.version_info[:3]))
"""The Python version as an ``X.Y.Z`` string."""
