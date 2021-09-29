"""Alias for pre-release compatibility with UDF environment."""

from tiledb.cloud._results import stored_params


class StoredParam(stored_params.StoredParam):
    pass
