import tiledb
import urllib
from . import rest_api
from . import config


def split_uri(uri):
  """Split a URI into namespace and array name"""
  parsed = urllib.parse.urlparse(uri)
  if not parsed.scheme == "tiledb":
    raise Exception("Incorrect array uri, must be in tiledb:// scheme")
  return parsed.netloc, parsed.path[1:]


class CloudArray(object):
  def sharing_list(self):
    """Return array sharing policies"""
    (namespace, array_name) = split_uri(self.uri)
    if not isinstance(config.logged_in, bool):
      raise Exception(config.logged_in)
    api_instance = rest_api.ArrayApi(rest_api.ApiClient(config.config))

    return api_instance.get_array_sharing_policies(namespace=namespace, array=array_name)

  def cloud_metadata(self):
    """Return array metadata"""
    (namespace, array_name) = split_uri(self.uri)
    if not isinstance(config.logged_in, bool):
      raise Exception(config.logged_in)
    api_instance = rest_api.ArrayApi(rest_api.ApiClient(config.config))

    return api_instance.get_array_metadata(namespace = namespace, array = array_name)
