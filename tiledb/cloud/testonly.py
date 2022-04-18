"""This module should only be imported from tests.

IT WILL NOT BE INCLUDED when installing TileDB Cloud.
"""

import contextlib
import random
import string
import uuid
from typing import Callable, Iterator

from tiledb.cloud import client
from tiledb.cloud import udf


def sequential_uuids(start: str) -> Iterator[uuid.UUID]:
    """Generator for sequential UUIDs for use in mocks."""
    current = uuid.UUID(hex=start)
    while True:
        yield current
        current = uuid.UUID(int=current.int + 1)


@contextlib.contextmanager
def register_udf(func: Callable) -> Iterator[str]:
    """Context manager to register a UDF for the duration of its block."""
    ns = client.default_user().username
    suffix = "".join(random.choices(string.ascii_letters, k=10))
    func_name = f"zzz_unittest_{func.__name__}_{suffix}"
    udf.register_udf(func, func_name, namespace=ns)
    try:
        yield f"{ns}/{func_name}"
    finally:
        udf.delete(func_name, ns)
