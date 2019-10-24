from __future__ import absolute_import
from __future__ import print_function

from . import rest_api
from . import config

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

def login(token="", username="", password="", host=None):
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
    if (username == "" and password == "") and token == "":
        raise Exception("Username and Password are both required")

    config.setup_configuration({"X-TILEDB-REST-API-KEY": token}, username, password, host)
    config.save_configuration(config.default_config_file)
    config.logged_in = True


def list_arrays():
    """
    List arrays in a user account

    :return: list of all array metadata you have access to
    """
    api_instance = get_array_api()

    return api_instance.get_all_array_metadata()


def user_profile():
    """

    :return: your user profile
    """

    api_instance = get_user_api()

    return api_instance.get_user()


def organizations():
    """

    :return: list of all organizations user is part of
    """

    api_instance = get_organization_api()

    return api_instance.get_all_organizations()


def organization(organization):
    """

    :param str organization: organization to fetct
    :return: details about organization
    """

    api_instance = get_organization_api()

    return api_instance.get_organization(organization=organization)