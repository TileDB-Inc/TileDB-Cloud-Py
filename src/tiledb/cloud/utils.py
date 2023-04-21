"""General utilities that don't fit anywhere else."""

# This currently only exports split_uri, which was the only externally-usable
# code from the previous utils module.

from tiledb.cloud._common.utils import split_uri

__all__ = ("split_uri",)
