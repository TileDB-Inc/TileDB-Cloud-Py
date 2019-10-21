import tiledb
import urllib

def split_uri(uri):
  parsed = urllib.parse.urlparse(uri)
  if not parsed.scheme == "tiledb":
    raise Exception("Incorrect array uri, must be in tiledb:// scheme")
  return parsed.netloc, parsed.path[1:]

class CloudArray(object):
  def array_sharing_list(self):
    """Return array metadata"""
    (namespace, array_name) = split_uri(self.uri)
    if not isinstance(config.logged_in, bool):
      raise Exception(config.logged_in)
    api_instance = rest_api.ArrayApi(rest_api.ApiClient(config.config))

    return api_instance.get_array_sharing_policies(namespace=namespace, array=array_name)

class DenseCloudArray(CloudArray, tiledb.DenseArray):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class SparseCloudArray(CloudArray, tiledb.SparseArray):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)


