from types import MappingProxyType

from . import indexing
from . import ingestion
from . import udfs
from . import utils

DEFAULT_MIN_RESOURCES = MappingProxyType({"cpu": "1", "memory": "2Gi"})


__all__ = (
    "indexing",
    "ingestion",
    "udfs",
    "utils",
)
