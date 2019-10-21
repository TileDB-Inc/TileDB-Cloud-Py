from __future__ import absolute_import
from __future__ import print_function

from . import rest_api
from . import config


def login(token="", username="", password="", host=None):
    """Login to cloud service"""
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
    """List arrays in a user account"""
    if not isinstance(config.logged_in, bool):
        raise Exception(config.logged_in)
    api_instance = rest_api.ArrayApi(rest_api.ApiClient(config.config))

    return api_instance.get_all_array_metadata()

