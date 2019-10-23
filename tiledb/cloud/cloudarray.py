import urllib
from . import rest_api
from . import config
from . import client

def split_uri(uri):
  """
  Split a URI into namespace and array name

  :param uri: uri to split into namespace and array name
  :return: tuple (namespace, array_name)
  """
  parsed = urllib.parse.urlparse(uri)
  if not parsed.scheme == "tiledb":
    raise Exception("Incorrect array uri, must be in tiledb:// scheme")
  return parsed.netloc, parsed.path[1:]


class CloudArray(object):
  def sharing_list(self):
    """Return array sharing policies"""
    (namespace, array_name) = split_uri(self.uri)
    api_instance = client.get_array_api()

    return api_instance.get_array_sharing_policies(namespace=namespace, array=array_name)

  def cloud_metadata(self):
    """
    Returns the cloud metadata

    :return: metadata object
    """
    (namespace, array_name) = split_uri(self.uri)
    api_instance = client.get_array_api()

    return api_instance.get_array_metadata(namespace = namespace, array = array_name)

  def share(self, namespace, permissions):
    """
    Shares array with give namespace and permissions

    :param str namespace:
    :param list(str) permissions:
    :return:
    """

    if not isinstance(permissions, list):
      permissions = [permissions]

    for perm in permissions:
      if not perm.lower() == rest_api.models.ArrayActions.READ and not perm.lower() == rest_api.models.ArrayActions.WRITE:
        raise Exception("Only read or write permissions are accepted")

    (array_namespace, array_name) = split_uri(self.uri)
    api_instance = client.get_array_api()

    return api_instance.share_array(namespace=array_namespace, array=array_name, array_sharing=rest_api.models.ArraySharing(namespace=namespace, actions=permissions))

  def unshare(self, namespace):
    """
    Removes sharing of an array from given namespace

    :param str namespace: namespace to remove shared access to the array
    :return:
    :raises: :py:exc:
    """
    return self.share(namespace, list())

  def register(self, namespace=None, array_name=None, description=None):
    """
    Register this array with the tiledb cloud service
    :param str array_name: name of array
    :param str description: optional description
    :param str namespace: optional username or organization array should be registered under. If unset will default to the user
    """
    api_instance = client.get_array_api()

    if namespace is None:
      if config.user is None:
        config.user = client.user_profile()

      namespace = config.user.username

    return api_instance.register_array(namespace=namespace, array=self.uri, array_metadata=rest_api.models.ArrayMetadataUpdate(description=description, name=array_name, uri=self.uri))

  def deregister(self):
    """
    Deregister the from the tiledb cloud service. This does not physically delete the array, it will remain
    in your bucket. All access to the array and cloud metadata will be removed.
    """
    (namespace, array_name) = split_uri(self.uri)

    api_instance = client.get_array_api()

    return api_instance.deregister_array(namespace=namespace, array=array_name)