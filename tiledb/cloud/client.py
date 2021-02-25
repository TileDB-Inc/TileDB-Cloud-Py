from __future__ import absolute_import
from __future__ import print_function

from . import rest_api
from . import config
from . import tiledb_cloud_error
from .rest_api import ApiException as GenApiException
import urllib
import os
from urllib3 import Retry

import tiledb

TASK_ID_HEADER = "X-TILEDB-CLOUD-TASK-ID"


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

    host_parsed = urllib.parse.urlparse(config.config.host)
    cfg_dict["rest.server_address"] = urllib.parse.urlunparse(
        (host_parsed.scheme, host_parsed.netloc, "", "", "", "")
    )
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
    verify_ssl=True,
    no_session=False,
    threads=os.cpu_count() * 2,
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
    elif host.endswith("/v1"):
        host = host[: -len("/v1")]
    elif host.endswith("/v1/"):
        host = host[: -len("/v1/")]

    if (token is None or token == "") and (
        (username is None or username == "") and (password is None or password == "")
    ):
        raise Exception("Username and Password OR token must be set")
    if (username is None or username == "" or password is None or password == "") and (
        token is None or token == ""
    ):
        raise Exception("Username and Password are both required")

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
        client.pool_threads = threads
        client.update_clients()
        user_api = client.user_api
        session = user_api.get_session(remember_me=True)
        token = session.token

    if token is not None and token != "":
        kwargs["api_key"] = {"X-TILEDB-REST-API-KEY": token}
        del kwargs["username"]
        del kwargs["password"]

    config.setup_configuration(**kwargs)
    config.save_configuration(config.default_config_file)
    config.logged_in = True
    client.pool_threads = threads
    client.update_clients()


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
    :param list permissions: filter arrays for given permissions
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

    api_instance = client.array_api
    if permissions is not None and not isinstance(permissions, list):
        permissions = [permissions]

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
    :param list permissions: filter arrays for given permissions
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

    api_instance = client.array_api
    if permissions is not None and not isinstance(permissions, list):
        permissions = [permissions]

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
    :param list permissions: filter arrays for given permissions
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

    api_instance = client.array_api
    if permissions is not None and not isinstance(permissions, list):
        permissions = [permissions]

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

    api_instance = client.user_api

    try:
        return api_instance.get_user(async_req=async_req)
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def organizations(async_req=False):
    """

    :param async_req: return future instead of results for async support
    :return: list of all organizations user is part of
    """

    api_instance = client.organization_api

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

    api_instance = client.organization_api

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


class Client:
    def update_clients(self):
        self.array_api = self.__get_array_api()
        self.organization_api = self.__get_organization_api()
        self.sql_api = self.__get_sql_api()
        self.tasks_api = self.__get_tasks_api()
        self.udf_api = self.__get_udf_api()
        self.user_api = self.__get_user_api()
        self.notebook_api = self.__get_notebook_api()

    def __init__(self, pool_threads=os.cpu_count() * 2, retry_mode="default"):
        """

        :param pool_threads: Number of threads to use for http requests
        :param retry_mode: Retry mode ["default", "forceful", "disabled"]
        """
        self.pool_threads = pool_threads
        self.retry_mode(retry_mode)
        self.update_clients()

    def set_disable_retries(self):
        config.config.retries = False
        self.update_clients()

    def set_default_retries(self):
        config.config.retries = Retry(
            total=10,
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
        )
        self.update_clients()

    def set_forceful_retries(self):
        config.config.retries = Retry(
            total=10,
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
        )
        self.update_clients()

    def retry_mode(self, mode="default"):
        """

        :param mode: Retry mode ["default", "forceful", "disabled"]
        :return:
        """
        if mode == "default":
            self.set_default_retries()
        elif mode == "forceful":
            self.set_forceful_retries()
        elif mode == "disabled":
            self.set_disable_retries()
        else:
            raise Exception(
                "unsupported retry mode %s. Valid options are default, forceful or disabled".format(
                    model
                )
            )

        self.update_clients()

    def set_threads(self, threads=os.cpu_count() * 2):
        """
        Update thread pool sizes for async functionality
        :param threads:
        :return:
        """
        self.pool_threads = threads
        self.update_clients()

    def __get_array_api(self):
        return rest_api.ArrayApi(
            rest_api.ApiClient(
                configuration=config.config, pool_threads=self.pool_threads
            )
        )

    def __get_user_api(self):
        return rest_api.UserApi(
            rest_api.ApiClient(
                configuration=config.config, pool_threads=self.pool_threads
            )
        )

    def __get_organization_api(self):
        return rest_api.OrganizationApi(
            rest_api.ApiClient(
                configuration=config.config, pool_threads=self.pool_threads
            )
        )

    def __get_udf_api(self):
        return rest_api.UdfApi(
            rest_api.ApiClient(
                configuration=config.config, pool_threads=self.pool_threads
            )
        )

    def __get_tasks_api(self):
        return rest_api.TasksApi(
            rest_api.ApiClient(
                configuration=config.config, pool_threads=self.pool_threads
            )
        )

    def __get_sql_api(self):
        return rest_api.SqlApi(
            rest_api.ApiClient(
                configuration=config.config, pool_threads=self.pool_threads
            )
        )

    def __get_notebook_api(self):
        return rest_api.NotebookApi(
            rest_api.ApiClient(
                configuration=config.config, pool_threads=self.pool_threads
            )
        )


client = Client()
