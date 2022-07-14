"""This module should only be imported from tests.

IT WILL NOT BE INCLUDED when installing TileDB Cloud.
"""

import contextlib
import random
import string
import time
import uuid
from typing import Callable, Iterator, Optional

from tiledb.cloud import client
from tiledb.cloud import udf


def sequential_uuids(start: str) -> Iterator[uuid.UUID]:
    """Generator for sequential UUIDs for use in mocks."""
    current = uuid.UUID(hex=start)
    while True:
        yield current
        current = uuid.UUID(int=current.int + 1)


@contextlib.contextmanager
def register_udf(func: Callable, func_name: Optional[str] = None) -> Iterator[str]:
    """Context manager to register a UDF for the duration of its block."""
    ns = client.default_user().username
    func_name = func_name or random_name(func.__name__)
    udf.register_udf(func, func_name, namespace=ns)
    time.sleep(1)  # Sometimes permissions take a bit to propagate.
    try:
        yield f"{ns}/{func_name}"
    finally:
        udf.delete(func_name, ns)


def random_name(name: str) -> str:
    suffix = "".join(random.choices(string.ascii_letters, k=10))
    return f"zzz_unittest_{name}_{suffix}"


def is_unittest_user() -> bool:
    """Used to skip tests that depend upon the state of the unittest user."""
    return client.default_user().username == "unittest"
