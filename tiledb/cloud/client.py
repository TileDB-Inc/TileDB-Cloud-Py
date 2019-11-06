from __future__ import absolute_import
from __future__ import print_function

from . import rest_api
from . import config
from . import tiledb_cloud_error
from .rest_api import ApiException as GenApiException
import urllib

import tiledb

TASK_ID_HEADER = "X-TILEDB-CLOUD-TASK-ID"


def Config():
    """
  Builds a tiledb config setting the login parameters that exist for the cloud service
  :return: tiledb.Config
  """
    host_parsed = urllib.parse.urlparse(config.config.host)
    cfg = tiledb.Config(
        {
            "rest.server_address": urllib.parse.urlunparse(
                (host_parsed.scheme, host_parsed.netloc, "", "", "", "")
            )
        }
    )
    if config.config.username != "" and config.config.password != "":
        cfg["rest.username"] = config.config.username
        cfg["rest.password"] = config.config.password
    else:
        cfg["rest.token"] = config.config.api_key["X-TILEDB-REST-API-KEY"]

    return cfg


def Ctx():
    """
    Builds a TileDB Context that has the tiledb config parameters for tiledb cloud set from stored login
    :return: tiledb.Ctx
    """
    return tiledb.Ctx(Config())


def get_array_api():
    if not isinstance(config.logged_in, bool):
        raise Exception(config.logged_in)
    return rest_api.ArrayApi(rest_api.ApiClient(config.config))


def get_user_api():
    if not isinstance(config.logged_in, bool):
        raise Exception(config.logged_in)
    return rest_api.UserApi(rest_api.ApiClient(config.config))


def get_organization_api():
    if not isinstance(config.logged_in, bool):
        raise Exception(config.logged_in)
    return rest_api.OrganizationApi(rest_api.ApiClient(config.config))


def get_udf_api():
    if not isinstance(config.logged_in, bool):
        raise Exception(config.logged_in)
    return rest_api.UdfApi(rest_api.ApiClient(config.config))


def get_tasks_api():
    if not isinstance(config.logged_in, bool):
        raise Exception(config.logged_in)
    return rest_api.TasksApi(rest_api.ApiClient(config.config))


def get_sql_api():
    if not isinstance(config.logged_in, bool):
        raise Exception(config.logged_in)
    return rest_api.SqlApi(rest_api.ApiClient(config.config))


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
        host = "https://api.tiledb.com/v1"

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
        user_api = get_user_api()
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


def list_arrays(include_public=False, namespace=None, permissions=None):
    """
    List arrays in a user account

    :param bool include_public: include publicly shared arrays or not, defaults to false
    :param str namespace: list arrays in single namespace
    :param list permissions: filter arrays for given permissions
    :return: list of all array metadata you have access to that meet the filter applied
    """

    api_instance = get_array_api()

    public_share = None
    if not include_public:
        public_share = "exclude"

    if permissions is not None and not isinstance(permissions, list):
        permissions = [permissions]

    try:
        final_arrays = []
        res = api_instance.get_all_array_metadata(public_share=public_share)

        # Loop through results and filter as appropriate
        for array in res:
            if namespace is not None and array.namespace != namespace:
                continue

            if permissions is not None and len(permissions) > 0:
                permission_found = any(
                    filter(lambda p: p in array.allowed_actions, permissions)
                )

                if not permission_found:
                    continue

            final_arrays.append(array)

        return final_arrays

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def user_profile():
    """

    :return: your user profile
    """

    api_instance = get_user_api()

    try:
        return api_instance.get_user()
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def organizations():
    """

    :return: list of all organizations user is part of
    """

    api_instance = get_organization_api()

    try:
        return api_instance.get_all_organizations()
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def organization(organization):
    """

    :param str organization: organization to fetct
    :return: details about organization
    """

    api_instance = get_organization_api()

    try:
        return api_instance.get_organization(organization=organization)
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None
