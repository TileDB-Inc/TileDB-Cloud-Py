import json
from typing import Dict, Optional

import tiledb
from tiledb.cloud import rest_api


class TileDBCloudError(tiledb.TileDBError):
    def __init__(
        self,
        http_status: Optional[int] = None,
        *,
        json_data: Optional[Dict[str, object]] = None,
        body: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.json_data = json_data
        self.http_status = http_status
        self.body = body

    def __str__(self) -> str:
        if self.json_data:
            json_data = dict(self.json_data)
            msg = json_data.pop("message", None)
            code = json_data.pop("code", None)
            extra = f" - Extra details: {json_data!r}" if json_data else ""
            return f"{msg} - Code: {code}{extra}"
        if self.http_status == 404:
            return "HTTP 404: resource not found"
        return f"Unknown HTTP {self.http_status} error; response body: {self.body!r}"


def maybe_wrap(exc: Exception) -> TileDBCloudError:
    """Tries to extract useful information from an API exception."""
    if not isinstance(exc, rest_api.ApiException):
        # If this isn't an ApiException, something non–API-related happened.
        # We shouldn't try to wrap it.
        #
        # Bare "raise" here is OK because this function is already called from
        # within an exception handler.
        raise

    try:
        body_data = json.loads(exc.body)
    except Exception:
        raise TileDBCloudError(exc.status, body=exc.body) from exc
    return TileDBCloudError(exc.status, json_data=body_data)
