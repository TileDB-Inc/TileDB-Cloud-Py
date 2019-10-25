import urllib
from . import rest_api
from . import config
from . import client

import cloudpickle
import base64
import sys


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


def build_dimension_coordinate(domain_type, val):
  """
  Build a dimension coordinate model
  :param domain_type: tiledb dimension type
  :param val: value to put as coordinate
  :return: rest_api.models.DimensionCoordinate: model
  """

  if domain_type == "int8":
    return rest_api.models.DimensionCoordinate(int8=int(val))
  elif domain_type == "uint8":
    return rest_api.models.DimensionCoordinate(uint8=int(val))
  elif domain_type == "int16":
    return rest_api.models.DimensionCoordinate(int16=int(val))
  elif domain_type == "uint16":
    return rest_api.models.DimensionCoordinate(uint16=int(val))
  elif domain_type == "int32":
    return rest_api.models.DimensionCoordinate(int32=int(val))
  elif domain_type == "uint32":
    return rest_api.models.DimensionCoordinate(uint32=int(val))
  elif domain_type == "int64":
    return rest_api.models.DimensionCoordinate(int64=int(val))
  elif domain_type == "uint64":
    return rest_api.models.DimensionCoordinate(uint64=int(val))
  elif domain_type == "float32":
    return rest_api.models.DimensionCoordinate(float32=float(val))
  elif domain_type == "float64":
    return rest_api.models.DimensionCoordinate(float64=float(val))
  else:
    raise Exception("Unsupported dimension type {} for apply udf".format(domain_type))

  return None


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

  def register(self, namespace=None, array_name=None, description=None, access_credentials_name=None):
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

    return api_instance.register_array(namespace=namespace, array=self.uri, array_metadata=rest_api.models.ArrayMetadataUpdate(description=description, name=array_name, uri=self.uri, access_credentials_name=access_credentials_name))

  def deregister(self):
    """
    Deregister the from the tiledb cloud service. This does not physically delete the array, it will remain
    in your bucket. All access to the array and cloud metadata will be removed.
    """
    (namespace, array_name) = split_uri(self.uri)

    api_instance = client.get_array_api()

    return api_instance.deregister_array(namespace=namespace, array=array_name)

  def apply(self, func, subarray, attrs=None, layout='R'):
    """
    Apply a user defined function to a udf

    **Example**
    >>> import tiledb, tiledb.cloud, numpy
    >>> def median(df):
    ...   return numpy.median(df["a"])
    >>> # Open the array then run the UDF
    >>> with tiledb.SparseArray("tiledb://user/myarray", ctx=tiledb.cloud.ctx()) as A:
    ...   A.apply(median, [(0,4)], attrs=["a", "b", "c"])
    2.0

    :param func: user function to run
    :return: results of applied udf
    """

    (namespace, array_name) = split_uri(self.uri)
    api_instance = client.get_udf_api()

    pickledUDF = cloudpickle.dumps(func)
    pickledUDF = base64.b64encode(pickledUDF).decode('ascii')

    ranges=[]
    idx = 0
    for dim in self.schema.domain:
      start = build_dimension_coordinate(dim.dtype, subarray[idx][0])
      end = build_dimension_coordinate(dim.dtype, subarray[idx][1])
      ranges.append(rest_api.models.UDFSubarrayRange(dimension_id=idx, range_start=start, range_end=end))
      idx = idx + 1

    ranges = rest_api.models.UDFSubarray(layout=layout, ranges=ranges)

    res = api_instance.submit_udf(namespace=namespace, array=array_name, udf=rest_api.models.UDF(type=rest_api.models.UDFType.PYTHON, _exec=pickledUDF, subarray=ranges, version="{}.{}.{}".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)))
    return cloudpickle.loads(res)