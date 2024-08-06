import base64
import datetime
import functools
import logging
import sys
import threading
from enum import Enum
from typing import Any, Callable, Optional, Tuple, Type, TypeVar, Union

import cloudpickle
import urllib3

from tiledb.cloud._common import functions

TILEDB_CLOUD_PROTOCOL = 4
PYTHON_VERSION = ".".join(map(str, sys.version_info[:3]))
"""The Python version as an ``X.Y.Z`` string."""

# General-use logger for TileDB Cloud.
logger = logging.getLogger("tiledb.cloud")


def canonicalize_ns_name_uri(
    **ns_name_uri: Optional[str],
) -> Tuple[Optional[str], Optional[str]]:
    """Canonicalizes the namespace/name pair for functions also accepting URIs.

    Pass three named arguments to this function (in the order namespace, name,
    URI) and it will return a tuple of (namespace, name) to actually use.
    The arguments are named to generate relevant error messages for the caller::

        def some_func(
            namespace: Optional[str] = None,
            array_name: Optional[str] = None,
            destination_uri: Optional[str] = None,
            # ...
        ) -> ...:
            ns, name = canonicalize_ns_name_uri(
                namespace=namespace,
                array_name=array_name,
                destination_uri=destination_uri,
            )

    If ``destination_uri`` is set, but ``namespace`` or ``array_name`` is too,
    the user will get a :class:`ValueError` with the correct parameter names
    in the message.

    This works because keyword-argument dicts (and dicts in general) in Python
    remember insertion order.
    """
    try:
        ns_pair, name_pair, uri_pair = ns_name_uri.items()
    except ValueError as ve:
        # This is an internal error that should never be hit by users;
        # we only call this function directly ourselves.
        raise AssertionError(
            f"Internal error: canonicalize only got {len(ns_name_uri)} params"
        ) from ve
    ns_param, ns = ns_pair
    name_param, name = name_pair
    uri_param, uri = uri_pair
    if uri:
        if ns or name:
            raise ValueError(
                f"{ns_param}/{name_param} or {uri_param} may be set, but not both"
            )
        return split_uri(uri)
    return ns, name


def canonicalize_nameuri_namespace(
    name: str, namespace: Optional[str]
) -> Tuple[Optional[str], str]:
    """Returns the canonical namespace and name given a name/uri and namespace.

    This takes a ``name`` parameter which may be either a bare array name
    or a ``tiledb://`` URI, and a ``namespace`` parameter and returns the
    actual namespace and name to use.
    """
    try:
        namespace, name = split_uri(name)
    except ValueError:
        pass  # It's not a URI. Just use the params as-is.
    else:
        if namespace:
            raise ValueError("If `name` is a URI, `namespace` must not be set.")
    return namespace, name


def split_uri(uri: str) -> Tuple[str, str]:
    """
    Split a URI into namespace and array name

    :param uri: uri to split into namespace and array name
    :return: tuple (namespace, array_name)
    """
    post_tiledb = uri.removeprefix("tiledb://")
    if post_tiledb == uri:  # prefix was not removed
        raise ValueError("Incorrect array uri, must be in tiledb:// scheme")
    ns, _, name = post_tiledb.partition("/")
    return ns, name


def b64_pickle(obj: Any) -> str:
    """Pickles the given object, then base64 encodes the pickle."""
    pickle = cloudpickle.dumps(obj, protocol=TILEDB_CLOUD_PROTOCOL)
    return base64.b64encode(pickle).decode("ascii")


_CT = TypeVar("_CT", bound=Callable)


def ephemeral_thread(func: _CT, name: Optional[str] = None) -> _CT:
    """Wraps the function to be called on an ephemeral (but non-daemon) thread.

    Unlike a ``concurrent.futures.Executor``, this runs the things as a
    non-daemon thread, so it's useful for things you don't want to block on,
    but also don't want to get interrupted if the main thread exits.

    Exceptions are ignored.
    """

    name = name or f"ephemeral {functions.full_name(func)}"

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


def release_connection(resp: "urllib3.BaseHTTPResponse") -> None:
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


def datetime_to_msec(t: Union[datetime.datetime, int, None]) -> Optional[int]:
    return int(t.timestamp() * 1000) if isinstance(t, datetime.datetime) else t


def sanitize_enum_argument(enum_class: Type[Enum], value: str) -> Type[Enum]:
    try:
        return enum_class(value)
    except ValueError as exc:
        raise ValueError(f"{value} is not a valid {enum_class.__name__}") from exc
