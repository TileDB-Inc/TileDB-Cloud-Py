import base64
import functools
import inspect
import logging
import sys
import threading
import urllib
from typing import Any, Callable, Optional, TypeVar, Union

import cloudpickle
import urllib3

TILEDB_CLOUD_PROTOCOL = 4

# General-use logger for TileDB Cloud.
logger = logging.getLogger("tiledb.cloud")

_T = TypeVar("_T")
Funcable = Union[str, Callable[..., _T]]
"""Either a Python function or the name of a registered UDF."""
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


def func_name(f: Funcable) -> str:
    """Generates a "full name" to the given function for human reference."""
    if isinstance(f, str):
        return f"registered UDF {f!r}"
    try:
        if f.__module__:
            return f"{f.__module__}.{f.__qualname__}"
        return f.__qualname__
    except AttributeError:
        return str(f)


def getsourcelines(func: Callable) -> Optional[str]:
    """Attempt to extract the source code of ``func``, but accept failure."""
    if isinstance(func, _builtin_function):
        # Built-in functions have no accessible source code.
        return None
    try:
        # Attempt to find and serialize the original source...
        return "".join(inspect.getsourcelines(func)[0])
    except Exception:
        pass
    return None


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


def check_funcable(**kwargs) -> None:
    """Checks whether the given parameter can be treated as a function.

    For a function like::

        def process(some_func: Funcable, more, params):
            utils.check_funcable(some_func=some_func)
            # ...

    If it's a Funcable, then execution continues as normal. If not, then
    it raises an informative exception.
    """
    name, func = kwargs.popitem()
    assert not kwargs, "Too many args passed to _check_funcable"
    if callable(func) or type(func) == str:
        return
    raise TypeError(
        f"{name} argument must be a callable or the registered name of a UDF, "
        f"not {type(func)}"
    )


_CT = TypeVar("_CT", bound=Callable)


def ephemeral_thread(func: _CT, name: Optional[str] = None) -> _CT:
    """Wraps the function to be called on an ephemeral (but non-daemon) thread.

    Unlike a ``concurrent.futures.Executor``, this runs the things as a
    non-daemon thread, so it's useful for things you don't want to block on,
    but also don't want to get interrupted if the main thread exits.

    Exceptions are ignored.
    """

    name = name or f"ephemeral {func_name(func)}"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Kick off a non-daemonic thread to report completion so that we don't
        # block on the server call when reporting doneness to the caller,
        # but also we don't let the process terminate while we're still
        # reporting.
        #
        # ┄: blocked, ═: running, •: synchronization point, ×: termination
        # [d] = daemon thread
        #
        # main:  ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄╒══════×
        # us[d]: ═════════════•═╕┄┄┄┄╒══•══×   main terminates
        # ephemeral:          ┊ ┊   ═•══╪═══════════×
        #       start ephemeral ┊    ┊  ┊           ephemeral terminates
        #            running.wait    ┊  ┊
        #                  running.set  (client code) main/us sync point
        #
        # Without this non-daemon reporter, the Python interpreter could stop
        # as soon as main terminates, meaning that the ephemeral call would not
        # get the chance to run to completion.
        started = threading.Event()

        def run():
            started.set()
            try:
                func(*args, **kwargs)
            except Exception:
                pass  # Drop it on the floor.

        thread = threading.Thread(name=name, target=run, daemon=False)
        thread.start()
        started.wait()

    return wrapper  # type: ignore[return-value]


def release_connection(resp: urllib3.HTTPResponse) -> None:
    """Release the backing connection of this HTTPResponse to the pool.

    When a call is made with ``preload_content=False``, the response body is not
    eagerly read, and because of this, urllib3 does not know that the connection
    can be returned to the pool. This means that both (a) we may use the results
    of a request before it has fully finished (sometimes desirable, sometimes
    undesirable), and (b) as time goes on, we will have more and more dangling
    sockets open but unusable.

    This function drains those connections (i.e. reads the data and throws it
    on the floor) and releases the connection back to the pool, in a blocking
    manner (since we may wish to wait until all the contents are received).
    Consider combining this with :func:`ephemeral_thread` for an async call.
    """
    resp.drain_conn()
    resp.release_conn()
