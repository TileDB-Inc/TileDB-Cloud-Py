from __future__ import print_function

import urllib
import tiledb.cloud.config as config
import tiledb.cloud.rest_api as rest_api
from tiledb.cloud.rest_api.rest import ApiException

def split_uri(uri):
    parsed = urllib.parse.urlparse(uri)
    if not parsed.scheme == "tiledb":
        raise Exception("Incorrect array uri, must be in tiledb:// scheme")
    return parsed.netloc, parsed.path[1:]


def login(token=None, username=None, password=None, host=None):
    """Login to cloud service"""
    if host is None:
        host = "https://api.tiledb.com/v1"

    if token is None and username is None and password is None:
        raise Exception("Username and Password OR token must be set")
    if (username is None and password is None) and token is None:
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


def array(uri):
    """Return array metadata"""
    (namespace, array_name) = split_uri(uri)
    if not isinstance(config.logged_in, bool):
        raise Exception(config.logged_in)
    api_instance = rest_api.ArrayApi(rest_api.ApiClient(config.config))

    return api_instance.get_array_metadata(namespace = namespace, array = array_name)
