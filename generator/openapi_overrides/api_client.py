"""Re-exporting the ``api_client`` namespace."""

from tiledb.cloud.rest_api.api_client import *  # noqa: F401,F403

_ApiClientCls = ApiClient  # noqa: F405


def ApiClient(*args, **kwargs) -> _ApiClientCls:
    """Returns an ``ApiClient`` suitable for the v2 API models."""
    from . import models

    return _ApiClientCls(*args, **kwargs, _tdb_models_module=models)
