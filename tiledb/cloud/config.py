import os.path
from pathlib import Path
import json
from . import rest_api

config = rest_api.configuration.Configuration()
default_config_file = Path.joinpath(Path.home(), ".tiledb", "cloud.json")

def save_configuration(config_file):
    config_path = os.path.dirname(config_file)
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    with open(config_file, 'w') as f:
        global config
        config_to_save={'host': config.host, 'username': config.username, 'password': config.password, 'api_key':  config.api_key, 'verify_ssl': config.verify_ssl}
        json.dump(config_to_save, f, indent=4, sort_keys=True)


def load_configuration(config_path):
    if not os.path.isfile(config_path):
        return "You must first login before you can run commands"
    with open(config_path, 'r') as f:
        global config
        # Parse JSON into an object with attributes corresponding to dict keys.
        config_obj = json.loads(f.read())
        setup_configuration(api_key=config_obj['api_key'], username=config_obj['username'], password=config_obj['password'], host=config_obj['host'], verify_ssl=config_obj['verify_ssl'])
    return True


def setup_configuration(api_key, username, password, host, verify_ssl=True):
    global config
    config.api_key = api_key
    config.host = host
    config.username = username
    config.password = password
    config.verify_ssl = verify_ssl

# Load default config file if it exists
logged_in = load_configuration(default_config_file)
user = None
