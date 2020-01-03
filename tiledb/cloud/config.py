import os.path, sys
from pathlib import Path
import json
from . import rest_api
from urllib3 import Retry

config = rest_api.configuration.Configuration()
default_config_file = Path.joinpath(Path.home(), ".tiledb", "cloud.json")
if sys.version_info < (3, 6):
    default_config_file = str(default_config_file)


def save_configuration(config_file):
    config_path = os.path.dirname(config_file)
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    with open(config_file, "w") as f:
        global config
        config_to_save = {
            "host": config.host,
            "api_key": config.api_key,
            "verify_ssl": config.verify_ssl,
        }

        if config.username is not None and config.username != "":
            config_to_save["username"] = config.username

        if config.password is not None and config.password != "":
            config_to_save["password"] = config.password

        json.dump(config_to_save, f, indent=4, sort_keys=True)


def load_configuration(config_path):
    if not os.path.isfile(config_path):
        return "You must first login before you can run commands"
    with open(config_path, "r") as f:
        global config
        # Parse JSON into an object with attributes corresponding to dict keys.
        config_obj = json.loads(f.read())
        username = ""
        password = ""
        if "username" in config_obj:
            username = config_obj["username"]
        if "password" in config_obj:
            password = config_obj["password"]

        host = config_obj["host"]
        if host.endswith("/v1"):
            host = host[: -len("/v1")]
        elif host.endswith("/v1/"):
            host = host[: -len("/v1/")]

        setup_configuration(
            api_key=config_obj["api_key"],
            username=username,
            password=password,
            host=host,
            verify_ssl=config_obj["verify_ssl"],
        )
    return True


def setup_configuration(api_key, host, username="", password="", verify_ssl=True):
    host = host + "/v1"
    global config
    config.api_key = api_key
    config.host = host
    config.username = username
    config.password = password
    config.verify_ssl = verify_ssl
    config.retries = Retry(
        total=10,
        backoff_factor=0.25,
        status_forcelist=[503],
        method_whitelist=False,
        raise_on_status=False,
    )


# Load default config file if it exists
logged_in = load_configuration(default_config_file)
user = None
