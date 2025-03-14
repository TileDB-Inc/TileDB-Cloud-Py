import json
import os.path
import warnings
from pathlib import Path
from typing import Optional

from urllib3 import Retry

from tiledb.cloud.rest_api import configuration
from tiledb.cloud.rest_api import models

default_host = "https://api.tiledb.com"
default_config_file = Path.joinpath(Path.home(), ".tiledb", "cloud.json")

# Starting with version 0.12.30, "config" is a dynamic attribute of
# this module. The actual state of the attribute is bound to "_config",
# which begins uninitialized. Looking up "config" from
# tiledb.cloud.config causes our stored configuration to be loaded
# just as needed.
_config = configuration.Configuration()


def __getattr__(name):
    global logged_in
    if name == "config":
        if not logged_in:
            logged_in = load_configuration(default_config_file)
        return _config
    else:
        raise AttributeError


def parse_bool(s: str) -> bool:
    return s.lower() in ["true", "1", "on"]


def save_configuration(config_file):
    config_path = os.path.dirname(config_file)
    if not os.path.exists(config_path):
        os.makedirs(config_path)

    with open(config_file, "w") as f:
        host = _config.host

        config_to_save = {
            "host": host,
            "verify_ssl": _config.verify_ssl,
        }

        if _config.api_key is not None and _config.api_key != "":
            config_to_save["api_key"] = _config.api_key

        if _config.username is not None and _config.username != "":
            config_to_save["username"] = _config.username

        if _config.password is not None and _config.password != "":
            config_to_save["password"] = _config.password

        json.dump(config_to_save, f, indent=4, sort_keys=True)


def load_configuration(config_path):
    logged_in = True
    # Look for env variables
    token = os.getenv("TILEDB_REST_TOKEN", None)
    if token is not None and token != "":
        token = {"X-TILEDB-REST-API-KEY": token}
    host = os.getenv("TILEDB_REST_HOST")
    # default username/password to empty strings
    username = os.getenv("TILEDB_REST_USERNAME", None)
    password = os.getenv("TILEDB_REST_PASSWORD", None)
    verify_ssl = not parse_bool(os.getenv("TILEDB_REST_IGNORE_SSL_VALIDATION", "False"))

    if os.path.isfile(config_path):
        with open(config_path, "r") as f:
            # Parse JSON into an object with attributes corresponding to dict keys.
            config_obj = json.loads(f.read())
            if (
                "username" in config_obj
                and config_obj["username"] is not None
                and config_obj["username"] != ""
            ):
                username = config_obj["username"]
            if (
                "password" in config_obj
                and config_obj["password"] is not None
                and config_obj["password"] != ""
            ):
                password = config_obj["password"]

            # Don't override user env variables
            if host is None or host == "":
                host = config_obj["host"]

            # Don't override user env variables
            if (
                (token is None or token == "")
                and "api_key" in config_obj
                and config_obj["api_key"] is not None
                and config_obj["api_key"] != ""
            ):
                token = config_obj["api_key"]

            if "verify_ssl" in config_obj:
                verify_ssl = config_obj["verify_ssl"]

    if (token is None or token == "") and (username is None or username == ""):
        warnings.warn(
            "You must first login before you can run commands."
            " Please run tiledb.cloud.login."
        )
        logged_in = False

    if host is None or host == "":
        global default_host
        host = default_host

    setup_configuration(
        api_key=token,
        username=username,
        password=password,
        host=host,
        verify_ssl=verify_ssl,
    )
    return logged_in


def setup_configuration(
    api_key=None, host="", username=None, password=None, verify_ssl=True
):
    if api_key is None:
        api_key = {}
    _config.api_key = api_key
    _config.host = host
    _config.username = username
    _config.password = password
    _config.verify_ssl = verify_ssl
    _config.retries = Retry(
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
    # Set logged in at this point
    global logged_in
    logged_in = True


# Loading of the default configuration file and determination of
# whether we are logged in or not is now deferred to the first access
# of this module's "config" attribute.
logged_in = None
user: Optional[models.User] = None
"""The default user to use.

You should probably access this through ``client.default_user()`` rather than
doing so directly.
"""
