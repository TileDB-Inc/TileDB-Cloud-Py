from enum import Enum
from typing import Any, Dict, Optional

import requests

from tiledb.cloud import config
from tiledb.services import errors


class AllowedMethods(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


def _prepare_headers(
    *, acn: Optional[str] = None, extra_headers: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-TILEDB-REST-API-KEY": config.config.api_key["X-TILEDB-REST-API-KEY"],
    }

    if acn:
        headers["X-TILEDB-CLOUD-ACCESS-CREDENTIALS-NAME"] = acn
    if extra_headers:
        headers.update(extra_headers)

    return headers


def perform_request(
    method: AllowedMethods,
    url: str,
    *,
    # Common
    acn: Optional[str] = None,
    headers: Optional[Dict[str, Any]] = None,
    # GET
    params: Optional[Dict[str, Any]] = None,
    # POST
    body: Optional[Dict[str, Any]] = None,
    # Session
    request_session: Optional[requests.Session] = None,
) -> requests.Response:
    """
    Performs a request of a given Allowed Action to the provided endpoint.

    :param method: An AllowedMethod from:
        ["GET", "POST", "PUT", "PATCH", "DELETE"]
    :param url: Endpoint's url.
    :param acn: Cloud Access Credentials Name, defaults to None.
    :param headers: Request headers, defaults to None
    :param params: Request path parameters, defaults to None.
    :param body: Request body dictionary, defaults to None.
    :param request_session: A requests.Session instance, defaults to None
    :raises errors.Unavailable: In case of Connection or Timeout errors.
    :return requests.Response: The endpoint response
    """

    headers = _prepare_headers(acn=acn, extra_headers=headers)
    try:
        actor = request_session or requests
        response = actor.request(
            method=method.value, url=url, params=params, json=body, headers=headers
        )
    except (requests.ConnectionError, requests.Timeout) as exc:
        raise errors.Unavailable("Endpoint '{}' is unavailable".format(url)) from exc

    response.raise_for_status()
    return response


def perform_post_request(
    url: str,
    body: Dict[str, Any],
    *,
    acn: Optional[str] = None,
    headers: Optional[Dict[str, Any]] = None,
    request_session: Optional[requests.Session] = None,
) -> requests.Response:
    """
    Performs a PATCH request to the provided endpoint.

    :param url: Endpoint's url.
    :param body: Request body dictionary.
    :param acn: Cloud Access Credentials Name, defaults to None.
    :param headers: Request headers, defaults to None
    :param request_session: A requests.Session instance, defaults to None
    :raises errors.Unavailable: In case of Connection or Timeout errors.
    :return requests.Response: The endpoint response
    """
    headers = _prepare_headers(acn=acn, **headers)
    try:
        if request_session:
            response = request_session.post(url, json=body, headers=headers)
        else:
            response = requests.post(url, json=body, headers=headers)
    except (requests.ConnectionError, requests.Timeout) as exc:
        raise errors.Unavailable("Endpoint '{}' is unavailable".format(url)) from exc

    response.raise_for_status()
    return response


def perform_patch_request(
    url: str,
    body: Dict[str, Any],
    *,
    acn: Optional[str] = None,
    headers: Optional[Dict[str, Any]] = None,
    request_session: Optional[requests.Session] = None,
) -> requests.Response:
    """
    Performs a PATCH request to the provided endpoint.

    :param url: Endpoint's url.
    :param body: Request body dictionary.
    :param acn: Cloud Access Credentials Name, defaults to None.
    :param headers: Request headers, defaults to None
    :param request_session: A requests.Session instance, defaults to None
    :raises errors.Unavailable: In case of Connection or Timeout errors.
    :return requests.Response: The endpoint response
    """
    headers = _prepare_headers(acn=acn, **headers)
    try:
        if request_session:
            response = request_session.patch(url, json=body, headers=headers)
        else:
            response = requests.patch(url, json=body, headers=headers)
    except (requests.ConnectionError, requests.Timeout) as exc:
        raise errors.Unavailable("Endpoint '{}' is unavailable".format(url)) from exc

    response.raise_for_status()
    return response
