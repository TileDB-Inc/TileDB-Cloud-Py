import urllib
from . import rest_api
from . import config
from . import client
from . import tasks
from . import cloudarray
from . import tiledb_cloud_error
from .rest_api import ApiException as GenApiException
from .rest_api import rest


def info(uri):
    """
  Returns the cloud metadata

  :return: metadata object
  """
    (namespace, array_name) = cloudarray.split_uri(uri)
    api_instance = client.get_array_api()

    try:
        return api_instance.get_array_metadata(namespace=namespace, array=array_name)
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def list_shared_with(uri):
    """Return array sharing policies"""
    (namespace, array_name) = cloudarray.split_uri(uri)
    api_instance = client.get_array_api()

    try:
        return api_instance.get_array_sharing_policies(
            namespace=namespace, array=array_name
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def share_array(uri, namespace, permissions):
    """
  Shares array with give namespace and permissions

  :param str namespace:
  :param list(str) permissions:
  :return:
  """

    if not isinstance(permissions, list):
        permissions = [permissions]

    for perm in permissions:
        if (
            not perm.lower() == rest_api.models.ArrayActions.READ
            and not perm.lower() == rest_api.models.ArrayActions.WRITE
        ):
            raise Exception("Only read or write permissions are accepted")

    (array_namespace, array_name) = cloudarray.split_uri(uri)
    api_instance = client.get_array_api()

    try:
        return api_instance.share_array(
            namespace=array_namespace,
            array=array_name,
            array_sharing=rest_api.models.ArraySharing(
                namespace=namespace, actions=permissions
            ),
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def unshare_array(uri, namespace):
    """
  Removes sharing of an array from given namespace

  :param str namespace: namespace to remove shared access to the array
  :return:
  :raises: :py:exc:
  """
    return share_array(uri, namespace, list())


def register_array(
    uri, namespace=None, array_name=None, description=None, access_credentials_name=None
):
    """
  Register this array with the tiledb cloud service
  :param str namespace: optional username or organization array should be registered under. If unset will default to the user
  :param str array_name: name of array
  :param str description: optional description
  :param str access_credentials_name: optional name of access credentials to use, if left blank default for namespace will be used
  """
    api_instance = client.get_array_api()

    if namespace is None:
        if config.user is None:
            config.user = client.user_profile()

        namespace = config.user.username

    try:
        return api_instance.register_array(
            namespace=namespace,
            array=uri,
            array_metadata=rest_api.models.ArrayMetadataUpdate(
                description=description,
                name=array_name,
                uri=uri,
                access_credentials_name=access_credentials_name,
            ),
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def deregister_array(uri):
    """
  Deregister the from the tiledb cloud service. This does not physically delete the array, it will remain
  in your bucket. All access to the array and cloud metadata will be removed.
  """
    (namespace, array_name) = cloudarray.split_uri(uri)

    api_instance = client.get_array_api()

    try:
        return api_instance.deregister_array(namespace=namespace, array=array_name)
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None
