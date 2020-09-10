from __future__ import absolute_import
from __future__ import print_function

from . import rest_api
from . import config
from . import tiledb_cloud_error
from .rest_api import ApiException as GenApiException
import urllib

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
            raise ValueError("Unexpected config parameter '{r}' to cloud.Config")

    host_parsed = urllib.parse.urlparse(config.config.host)
    cfg_dict["rest.server_address"] = urllib.parse.urlunparse(
        (host_parsed.scheme, host_parsed.netloc, "", "", "", "")
    )
    cfg = tiledb.Config(cfg_dict)

    if config.config.username != "" and config.config.password != "":
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
    token="", username="", password="", host=None, verify_ssl=True, no_session=False
):
    """
    Login to cloud service

    :param token: api token for login
    :param username: username for login
    :param password: password for login
    :param host: host to login to
    :return:
    """
    if host is None:
        host = config.default_host
    elif host.endswith("/v1"):
        host = host[: -len("/v1")]
    elif host.endswith("/v1/"):
        host = host[: -len("/v1/")]

    if token == "" and username == "" and password == "":
        raise Exception("Username and Password OR token must be set")
    if (username == "" or password == "") and token == "":
        raise Exception("Username and Password are both required")

    # Is user logs in with username/password we need to create a session
    if token == "" and not no_session:
        config.setup_configuration(
            api_key={"X-TILEDB-REST-API-KEY": token},
            username=username,
            password=password,
            host=host,
            verify_ssl=verify_ssl,
        )
        client.update_clients()
        user_api = client.user_api
        session = user_api.get_session(remember_me=True)
        token = session.token
        username = ""
        password = ""

    config.setup_configuration(
        api_key={"X-TILEDB-REST-API-KEY": token},
        username=username,
        password=password,
        host=host,
        verify_ssl=verify_ssl,
    )
    config.save_configuration(config.default_config_file)
    config.logged_in = True
    client.update_clients()


def list_public_arrays(
    namespace=None, permissions=None, tag=None, search=None, page=None, per_page=None
):
    """
    List public arrays

    :param str namespace: list arrays in single namespace
    :param list permissions: filter arrays for given permissions
    :param list tag: zero or more tags to filter on
    :param str search: search string
    :param int page: optional page for pagination
    :param int per_page: optional per_page for pagination
    :return: list of all array metadata you have access to that meet the filter applied
    """

    api_instance = client.array_api
    if permissions is not None and not isinstance(permissions, list):
        permissions = [permissions]

    try:
        kwargs = {}
        if namespace is not None:
            kwargs["namespace"] = namespace
        if search is not None:
            kwargs["search"] = search
        if tag is not None:
            kwargs["tag"] = tag
        if permissions is not None:
            kwargs["permissions"] = permissions
        if page is not None:
            kwargs["page"] = page
        if per_page is not None:
            kwargs["per_page"] = per_page
        res = api_instance.arrays_browser_public_get(**kwargs)

        # if the user didn't ask for pagination just return raw array list
        if page is None:
            return res.arrays
        return res

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def list_shared_arrays(
    namespace=None, permissions=None, tag=None, search=None, page=None, per_page=None
):
    """
    List shared arrays

    :param str namespace: list arrays in single namespace
    :param list permissions: filter arrays for given permissions
    :param list tag: zero or more tags to filter on
    :param str search: search string
    :param int page: optional page for pagination
    :param int per_page: optional per_page for pagination
    :return: list of all array metadata you have access to that meet the filter applied
    """

    api_instance = client.array_api
    if permissions is not None and not isinstance(permissions, list):
        permissions = [permissions]

    try:
        kwargs = {}
        if namespace is not None:
            kwargs["namespace"] = namespace
        if search is not None:
            kwargs["search"] = search
        if tag is not None:
            kwargs["tag"] = tag
        if permissions is not None:
            kwargs["permissions"] = permissions
        if page is not None:
            kwargs["page"] = page
        if per_page is not None:
            kwargs["per_page"] = per_page
        res = api_instance.arrays_browser_shared_get(**kwargs)

        # if the user didn't ask for pagination just return raw array list
        if page is None:
            return res.arrays
        return res

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def list_arrays(
    namespace=None, permissions=None, tag=None, search=None, page=None, per_page=None
):
    """
    List arrays in a user account

    :param str namespace: list arrays in single namespace
    :param list permissions: filter arrays for given permissions
    :param list tag: zero or more tags to filter on
    :param str search: search string
    :param int page: optional page for pagination
    :param int per_page: optional per_page for pagination
    :return: list of all array metadata you have access to that meet the filter applied
    """

    api_instance = client.array_api
    if permissions is not None and not isinstance(permissions, list):
        permissions = [permissions]

    try:
        kwargs = {}
        if namespace is not None:
            kwargs["namespace"] = namespace
        if search is not None:
            kwargs["search"] = search
        if tag is not None:
            kwargs["tag"] = tag
        if permissions is not None:
            kwargs["permissions"] = permissions
        if page is not None:
            kwargs["page"] = page
        if per_page is not None:
            kwargs["per_page"] = per_page

        res = api_instance.arrays_browser_owned_get(**kwargs)

        # if the user didn't ask for pagination just return raw array list
        if page is None:
            return res.arrays
        return res

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def user_profile():
    """

    :return: your user profile
    """

    api_instance = client.user_api

    try:
        return api_instance.get_user()
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def organizations():
    """

    :return: list of all organizations user is part of
    """

    api_instance = client.organization_api

    try:
        return api_instance.get_all_organizations()
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def organization(organization):
    """

    :param str organization: organization to fetct
    :return: details about organization
    """

    api_instance = client.organization_api

    try:
        return api_instance.get_organization(organization=organization)
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def find_organization_or_user_for_default_charges(user):
    """
    Takes a user model and finds either the first non public organization or the user itself
    :param user:
    :return: namespace name to charge by default (organization or user if not part of any organization)
    """

    namespace_to_charge = user.username
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

    def __init__(self):
        self.update_clients()

    def __get_array_api(self):
        return rest_api.ArrayApi(rest_api.ApiClient(config.config))

    def __get_user_api(self):
        return rest_api.UserApi(rest_api.ApiClient(config.config))

    def __get_organization_api(self):
        return rest_api.OrganizationApi(rest_api.ApiClient(config.config))

    def __get_udf_api(self):
        return rest_api.UdfApi(rest_api.ApiClient(config.config))

    def __get_tasks_api(self):
        return rest_api.TasksApi(rest_api.ApiClient(config.config))

    def __get_sql_api(self):
        return rest_api.SqlApi(rest_api.ApiClient(config.config))


client = Client()
