from . import rest_api
from . import client
from . import cloudarray

import tiledb

import cloudpickle
import base64
import sys

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


class UDF(object):
  def __init__(self, array, func):
    """

    :param array: udf will be run on
    :param func: udf function
    """
    self._array = array
    self._func = func

  def apply_function(self, selection, func, layout=rest_api.models.Layout.ROW_MAJOR):
    """
    Apply function on an array
    :param selection: subarray to slice
    :param func: func to run
    :param layout: layout for query
    :return: results of udf
    """

    (namespace, array_name) = cloudarray.split_uri(self._array.uri)
    api_instance = client.get_udf_api()

    pickledUDF = cloudpickle.dumps(func)
    pickledUDF = base64.b64encode(pickledUDF).decode('ascii')

    ranges=[]
    idx = 0
    for dim in self._array.schema.domain:
      start = build_dimension_coordinate(dim.dtype, selection[idx][0])
      end = build_dimension_coordinate(dim.dtype, selection[idx][1])
      ranges.append(rest_api.models.UDFSubarrayRange(dimension_id=idx, range_start=start, range_end=end))
      idx = idx + 1

    ranges = rest_api.models.UDFSubarray(layout=layout, ranges=ranges)

    api_instance.submit_udf(namespace=namespace, array=array_name, udf=rest_api.models.UDF(type=rest_api.models.UDFType.PYTHON, _exec=pickledUDF, subarray=ranges, version="{}.{}.{}".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)))


  def __getitem__(self, selection):
    """
    Slice a array to apply a udf
    :param selection: subarray
    :return:
    """
    # Make sure selection is a tuple
    if not isinstance(selection, tuple):
      selection = (selection,)

    selection = tiledb.libtiledb.index_as_tuple(selection)
    idx = tiledb.libtiledb.replace_ellipsis(self._array.schema.domain.ndim, selection)
    idx, drop_axes = tiledb.libtiledb.replace_scalars_slice(self._array.schema.domain, idx)
    subarray = tiledb.libtiledb.index_domain_subarray(self._array.schema.domain, idx)

    return self.apply_function(subarray, self._func)

  @property
  def func(self):
      """Gets the func of this UDF.  # noqa: E501


      :return: The func of this UDF.  # noqa: E501
      :rtype: func
      """
      return self._func

  @func.setter
  def func(self, func):
      """Sets the func of this UDF.


      :param func: The func of this UDF.  # noqa: E501
      :type: func
      """

      self._func =func
