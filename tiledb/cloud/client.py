import enum
import os
import threading
from concurrent import futures
from typing import Callable, Optional, Sequence, TypeVar, Union

import urllib3

import tiledb
from tiledb.cloud import config
from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud.pool_manager_wrapper import _PoolManagerWrapper
from tiledb.cloud.rest_api import ApiException as GenApiException
from tiledb.cloud.rest_api import models

_T = TypeVar("_T")


def Config(cfg_dict=None):
    """
    Builds a tiledb config setting the login parameters that exist for the cloud service
    :return: tiledb.Config
    """
    restricted = ("rest.server_address", "rest.username", "rest.password")

    if not cfg_dict:
        cfg_dict = dict()

    for r in restricted:
        if r in cfg_dict:
            raise ValueError(f"Unexpected config parameter '{r}' to cloud.Config")

    host = config.config.host

    cfg_dict["rest.server_address"] = host
    cfg = tiledb.Config(cfg_dict)

    if (
        config.config.username is not None
        and config.config.username != ""
        and config.config.password is not None
        and config.config.password != ""
    ):
        cfg["rest.username"] = config.config.username
        cfg["rest.password"] = config.config.password
    else:
        cfg["rest.token"] = config.config.api_key["X-TILEDB-REST-API-KEY"]

    return cfg


def Ctx(config=None):
    """
    Builds a TileDB Context that has the tiledb config parameters for tiledb cloud set from stored login
    :return: tiledb.Ctx
    """
    return tiledb.Ctx(Config(config))


def login(
    token=None,
    username=None,
    password=None,
    host=None,
    verify_ssl=None,
    no_session=False,
    threads=None,
):
    """
    Login to cloud service

    :param token: api token for login
    :param username: username for login
    :param password: password for login
    :param host: host to login to
    :param verify_ssl: Enable strict SSL verification
    :param no_session: don't create a session token on login, store instead username/password
    :param threads: number of threads to enable for concurrent requests
    :return:
    """
    if host is None:
        host = config.default_host

    if (token is None or token == "") and (
        (username is None or username == "") and (password is None or password == "")
    ):
        raise Exception("Username and Password OR token must be set")
    if (username is None or username == "" or password is None or password == "") and (
        token is None or token == ""
    ):
        raise Exception("Username and Password are both required")

    if verify_ssl is None:
        verify_ssl = not config.parse_bool(
            os.getenv("TILEDB_REST_IGNORE_SSL_VALIDATION", "False")
        )

        kwargs = {
            "username": username,
            "password": password,
            "host": host,
            "verify_ssl": verify_ssl,
            "api_key": {},
        }
    # Is user logs in with username/password we need to create a session
    if (token is None or token == "") and not no_session:
        config.setup_configuration(**kwargs)
        client.set_threads(threads)
        user_api = build(rest_api.UserApi)
        session = user_api.get_session(remember_me=True)
        token = session.token

    if token is not None and token != "":
        kwargs["api_key"] = {"X-TILEDB-REST-API-KEY": token}
        del kwargs["username"]
        del kwargs["password"]

    config.setup_configuration(**kwargs)
    config.save_configuration(config.default_config_file)
    config.logged_in = True
    client.set_threads(threads)


def default_user() -> models.User:
    """Returns the default user to be used.

    If :data:`config.user` is set, that is the default user. If unset, we fetch
    the currently logged-in user with :func:`user_profile` and store that in
    :data:`config.user`.
    """
    if not config.user:
        # No locks. It's fine if we fetch this twice.
        config.user = user_profile()
    assert config.user
    return config.user


def default_charged_namespace() -> str:
    """Returns the namespace :func:`default_user` charges to by default."""
    return find_organization_or_user_for_default_charges(default_user())


def list_public_arrays(
    namespace=None,
    permissions=None,
    tag=None,
    exclude_tag=None,
    search=None,
    file_type=None,
    exclude_file_type=None,
    page=None,
    per_page=None,
    async_req=False,
):
    """
    List public arrays

    :param str namespace: list arrays in single namespace
    :param str permissions: filter arrays for given permissions
    :param list tag: zero or more tags to filter on
    :param list exclude_tag: zero or more tags to filter on
    :param str search: search string
    :param list file_type: zero or more file_types to filter on
    :param list exclude_file_type: zero or more file_types to filter on
    :param int page: optional page for pagination
    :param int per_page: optional per_page for pagination
    :param async_req: return future instead of results for async support
    :return: list of all array metadata you have access to that meet the filter applied
    """

    api_instance = build(rest_api.ArrayApi)
    permissions = _maybe_unwrap(permissions)

    try:
        kwargs = {"async_req": async_req}
        if namespace is not None:
            kwargs["namespace"] = namespace
        if search is not None:
            kwargs["search"] = search
        if tag is not None:
            kwargs["tag"] = tag
        if exclude_tag is not None:
            kwargs["exclude_tag"] = exclude_tag
        if permissions is not None:
            kwargs["permissions"] = permissions
        if file_type is not None:
            kwargs["file_type"] = file_type
        if exclude_file_type is not None:
            kwargs["exclude_file_type"] = exclude_file_type
        if page is not None:
            kwargs["page"] = page
        if per_page is not None:
            kwargs["per_page"] = per_page
        res = api_instance.arrays_browser_public_get(**kwargs)

        # if the user didn't ask for pagination just return raw array list
        return res

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def list_shared_arrays(
    namespace=None,
    permissions=None,
    tag=None,
    exclude_tag=None,
    search=None,
    file_type=None,
    exclude_file_type=None,
    page=None,
    per_page=None,
    async_req=False,
):
    """
    List shared arrays

    :param str namespace: list arrays in single namespace
    :param str permissions: filter arrays for given permissions
    :param list tag: zero or more tags to filter on
    :param list exclude_tag: zero or more tags to filter on
    :param str search: search string
    :param list file_type: zero or more file_types to filter on
    :param list exclude_file_type: zero or more file_types to filter on
    :param int page: optional page for pagination
    :param int per_page: optional per_page for pagination
    :param async_req: return future instead of results for async support
    :return: list of all array metadata you have access to that meet the filter applied
    """

    api_instance = build(rest_api.ArrayApi)
    permissions = _maybe_unwrap(permissions)

    try:
        kwargs = {"async_req": async_req}
        if namespace is not None:
            kwargs["namespace"] = namespace
        if search is not None:
            kwargs["search"] = search
        if tag is not None:
            kwargs["tag"] = tag
        if exclude_tag is not None:
            kwargs["exclude_tag"] = exclude_tag
        if permissions is not None:
            kwargs["permissions"] = permissions
        if file_type is not None:
            kwargs["file_type"] = file_type
        if exclude_file_type is not None:
            kwargs["exclude_file_type"] = exclude_file_type
        if page is not None:
            kwargs["page"] = page
        if per_page is not None:
            kwargs["per_page"] = per_page
        res = api_instance.arrays_browser_shared_get(**kwargs)

        # if the user didn't ask for pagination just return raw array list
        return res

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def list_arrays(
    namespace=None,
    permissions=None,
    tag=None,
    exclude_tag=None,
    search=None,
    file_type=None,
    exclude_file_type=None,
    page=None,
    per_page=None,
    async_req=False,
):
    """
    List arrays in a user account

    :param str namespace: list arrays in single namespace
    :param str permissions: filter arrays for given permissions
    :param list tag: zero or more tags to filter on
    :param list exclude_tag: zero or more tags to filter on
    :param str search: search string
    :param list file_type: zero or more file_types to filter on
    :param list exclude_file_type: zero or more file_types to filter on
    :param int page: optional page for pagination
    :param int per_page: optional per_page for pagination
    :param async_req: return future instead of results for async support
    :return: list of all array metadata you have access to that meet the filter applied
    """

    api_instance = build(rest_api.ArrayApi)
    permissions = _maybe_unwrap(permissions)

    try:
        kwargs = {"async_req": async_req}
        if namespace is not None:
            kwargs["namespace"] = namespace
        if search is not None:
            kwargs["search"] = search
        if tag is not None:
            kwargs["tag"] = tag
        if exclude_tag is not None:
            kwargs["exclude_tag"] = exclude_tag
        if permissions is not None:
            kwargs["permissions"] = permissions
        if file_type is not None:
            kwargs["file_type"] = file_type
        if exclude_file_type is not None:
            kwargs["exclude_file_type"] = exclude_file_type
        if page is not None:
            kwargs["page"] = page
        if per_page is not None:
            kwargs["per_page"] = per_page

        res = api_instance.arrays_browser_owned_get(**kwargs)

        # if the user didn't ask for pagination just return raw array list
        return res

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def user_profile(async_req=False):
    """
    :param async_req: return future instead of results for async support

    :return: your user profile
    """

    api_instance = build(rest_api.UserApi)

    try:
        return api_instance.get_user(async_req=async_req)
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def organizations(async_req=False):
    """

    :param async_req: return future instead of results for async support
    :return: list of all organizations user is part of
    """

    api_instance = build(rest_api.OrganizationApi)

    try:
        return api_instance.get_all_organizations(async_req=async_req)
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def organization(organization, async_req=False):
    """

    :param str organization: organization to fetct
    :param async_req: return future instead of results for async support
    :return: details about organization
    """

    api_instance = build(rest_api.OrganizationApi)

    try:
        return api_instance.get_organization(
            organization=organization, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def find_organization_or_user_for_default_charges(user):
    """
    Takes a user model and finds either the first non public organization or the user itself
    :param user:
    :return: namespace name to charge by default (organization or user if not part of any organization)
    """

    namespace_to_charge = user.username

    if (
        user.default_namespace_charged is not None
        and user.default_namespace_charged != ""
    ):
        return user.default_namespace_charged

    for org in user.organizations:
        if org.organization_name != "public":
            namespace_to_charge = org.organization_name
            break

    return namespace_to_charge


class RetryMode(enum.Enum):
    DEFAULT = "default"
    FORCEFUL = "forceful"
    DISABLED = "disabled"

    def maybe_from(v: "RetryOrStr") -> "RetryMode":
        if isinstance(v, RetryMode):
            return v
        return RetryMode(v)


RetryOrStr = Union[RetryMode, str]


_RETRY_CONFIGS = {
    RetryMode.DEFAULT: urllib3.Retry(
        total=100,
        backoff_factor=0.25,
        status_forcelist=[503],
        allowed_methods=[
            "HEAD",
            "GET",
            "PUT",
            "DELETE",
            "OPTIONS",
            "TRACE",
            "POST",
            "PATCH",
        ],
        raise_on_status=False,
        # Don't remove any headers on redirect
        remove_headers_on_redirect=[],
    ),
    RetryMode.FORCEFUL: urllib3.Retry(
        total=100,
        backoff_factor=0.25,
        status_forcelist=[400, 500, 501, 502, 503],
        allowed_methods=[
            "HEAD",
            "GET",
            "PUT",
            "DELETE",
            "OPTIONS",
            "TRACE",
            "POST",
            "PATCH",
        ],
        raise_on_status=False,
        # Don't remove any headers on redirect
        remove_headers_on_redirect=[],
    ),
    RetryMode.DISABLED: False,
}


class Client:
    def __init__(
        self,
        pool_threads: Optional[int] = None,
        retry_mode: RetryOrStr = RetryMode.DEFAULT,
    ):
        """

        :param pool_threads: Number of threads to use for http requests
        :param retry_mode: Retry mode ["default", "forceful", "disabled"]
        """
        self._pool_lock = threading.Lock()
        self._set_threads(pool_threads)
        self._retry_mode(retry_mode)
        self._client = self._rebuild_client()

    def build(self, builder: Callable[[rest_api.ApiClient], _T]) -> _T:
        """Builds an API client with the given config."""
        return builder(self._client)

    def set_disable_retries(self):
        self.retry_mode(RetryMode.DISABLED)

    def set_default_retries(self):
        self.retry_mode(RetryMode.DEFAULT)

    def set_forceful_retries(self):
        self.retry_mode(RetryMode.FORCEFUL)

    def retry_mode(self, mode: RetryOrStr = RetryMode.DEFAULT) -> None:
        """Sets how we should retry requests and updates API instances."""
        self._retry_mode(mode)
        self._client = self._rebuild_client()

    def set_threads(self, threads: Optional[int] = None) -> None:
        """Updates the number of threads in the async thread pool."""
        self._set_threads(threads)
        self._client = self._rebuild_client()

    def _retry_mode(self, mode: RetryOrStr) -> None:
        mode = RetryMode.maybe_from(mode)
        config.config.retries = _RETRY_CONFIGS[mode]

    def _rebuild_client(self):
        """
        Initialize api clients
        """
        # If users increase the size of the thread pool, increase the size
        # of the connection pool to match. (The internal members of
        # ThreadPoolExecutor are not exposed in the .pyi files, so we silence
        # mypy's warning here.)
        pool_size = self._thread_pool._max_workers  # type: ignore[attr-defined]
        config.config.connection_pool_maxsize = pool_size
        client = rest_api.ApiClient(config.config)
        client.rest_client.pool_manager = _PoolManagerWrapper(
            client.rest_client.pool_manager
        )
        return client

    def _set_threads(self, threads) -> None:
        with self._pool_lock:
            old_pool = getattr(self, "_thread_pool", None)
            self._thread_pool = futures.ThreadPoolExecutor(
                threads, thread_name_prefix="tiledb-async-"
            )
        if old_pool:
            old_pool.shutdown(wait=False)

    def _pool_submit(
        self,
        func: Callable[..., _T],
        *args,
        **kwargs,
    ) -> "futures.Future[_T]":
        with self._pool_lock:
            return self._thread_pool.submit(func, *args, **kwargs)


client = Client()

build = client.build


def _maybe_unwrap(param: Union[None, str, Sequence[str]]) -> Optional[str]:
    """Unwraps the first value if passed a sequence of strings."""
    if param is None or isinstance(param, str):
        return param
    try:
        return param[0]
    except IndexError:
        # If we're passed an empty sequence, treat it as no parameter.
        return None
