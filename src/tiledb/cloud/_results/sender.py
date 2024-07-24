import uuid
from typing import Any, Callable, Dict, Optional, TypeVar

import urllib3

from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error as tce
from tiledb.cloud._common import utils
from tiledb.cloud._results import decoders
from tiledb.cloud._results import results

_T = TypeVar("_T")
IDCallback = Callable[[Optional[uuid.UUID]], Any]
"""Type of the callback function we pass the response UUID to."""


def send_udf_call(
    api_func: Callable[..., urllib3.HTTPResponse],
    api_kwargs: Dict[str, Any],
    decoder: decoders.AbstractDecoder,
    id_callback: Optional[IDCallback] = None,
    *,
    results_stored: bool,
    results_downloaded: bool,
) -> "results.RemoteResult[_T]":
    """Synchronously sends a request to the given API.

    This handles the boilerplate parts (exception handling, parsing, response
    construction) of calling one of the generated API functions for UDFs.
    It runs synchronously and will return a :class:`results.RemoteResult`.
    To run the same function asychronously, use
    :func:`wrap_async_base_call` around the function that calls this
    (by convention, the ``whatever_api_base`` functions).

    This should only be used by callers *inside* this package.

    :param api_func: The UDF API function that we want to call from here.
        For instance, this might be :meth:`rest_api.SqlApi.run_sql`.
    :param api_kwargs: The arguments to pass to the API function as a dict.
        This should only include the parameters you want to send to the server,
        *not* any of the “meta” parameters that are mixed in with them (e.g.
        ``_preload_content``; this function will correctly set up the request).
    :param decoder: The Decoder to use to decode the response.
    :param id_callback: When the request completes (either by success or
        failure), this will be called with the UUID from the HTTP response,
        or None if the UUID could not be parsed.
    :param results_stored: A boolean indicating whether the results were stored.
        This does *not affect* the request; the ``store_results`` parameter of
        whatever API message the call uses must be set, and this must match
        that value.
    :return: A response containing the parsed result and metadata about it.
    """
    try:
        http_response = api_func(_preload_content=False, **api_kwargs)
    except rest_api.ApiException as exc:
        if id_callback:
            id_callback(results.extract_task_id(exc))
        raise tce.maybe_wrap(exc) from None

    try:
        task_id = results.extract_task_id(http_response)
        if id_callback:
            id_callback(task_id)

        return results.RemoteResult(
            body=http_response.data if results_downloaded else None,
            decoder=decoder,
            task_id=task_id,
            results_stored=results_stored,
        )
    finally:
        utils.release_connection(http_response)


def wrap_async_base_call(
    func: Callable[..., results.Result[_T]],
    *args: Any,
    **kwargs: Any,
) -> results.AsyncResult[_T]:
    """Makes a call to some `whatever_base` UDF call asynchronous."""
    ft = client.client._pool_submit(func, *args, **kwargs)
    return results.AsyncResult(ft)
