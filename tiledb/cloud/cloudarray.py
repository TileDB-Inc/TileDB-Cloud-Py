import urllib
from . import rest_api
from . import config
from . import client
from . import tasks
from . import tiledb_cloud_error
from .rest_api import ApiException as GenApiException
from .rest_api import rest

import cloudpickle

tiledb_cloud_protocol = 4

import base64
import sys
import numpy as np

last_udf_task_id = None


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

    if domain_type == np.dtype("int8"):
        return rest_api.models.DimensionCoordinate(int8=int(val))
    elif domain_type == np.dtype("uint8"):
        return rest_api.models.DimensionCoordinate(uint8=int(val))
    elif domain_type == np.dtype("int16"):
        return rest_api.models.DimensionCoordinate(int16=int(val))
    elif domain_type == np.dtype("uint16"):
        return rest_api.models.DimensionCoordinate(uint16=int(val))
    elif domain_type == np.dtype("int32"):
        return rest_api.models.DimensionCoordinate(int32=int(val))
    elif domain_type == np.dtype("uint32"):
        return rest_api.models.DimensionCoordinate(uint32=int(val))
    elif domain_type == np.dtype("int64"):
        return rest_api.models.DimensionCoordinate(int64=int(val))
    elif domain_type == np.dtype("uint64"):
        return rest_api.models.DimensionCoordinate(uint64=int(val))
    elif domain_type == np.dtype("float32"):
        return rest_api.models.DimensionCoordinate(float32=float(val))
    elif domain_type == np.dtype("float64"):
        return rest_api.models.DimensionCoordinate(float64=float(val))
    else:
        raise Exception(
            "Unsupported dimension type {} for apply udf".format(domain_type)
        )

    return None


def parse_ranges(ranges, builder):
    """
    Takes a list of the following objects per dimension:

    - scalar index
    - (start,end) tuple
    - list of either of the above types

    :param ranges: list of (scalar, tuple, list)
    :param builder: function taking arguments (dim_idx, start, end)
    :return:
    """

    def make_range(dim_idx, dim_range):
        if isinstance(dim_range, (int, float)):
            start, end = dim_range, dim_range
        elif isinstance(dim_range, (tuple, list)):
            start, end = dim_range[0], dim_range[1]
        elif isinstance(dim_range, slice):
            assert dim_range.step is None, "slice steps are not supported!"
            start, end = dim_range.start, dim_range.stop
        else:
            raise ValueError("Unknown index type! (type: '{}')".format(type(dim_range)))

        return builder(dim_idx, start, end)

    result = list()
    for dim_idx, dim_range in enumerate(ranges):
        # TODO handle numpy scalars here?
        if isinstance(dim_range, (int, float, tuple, slice)):
            result.append(make_range(dim_idx, dim_range))
        elif isinstance(dim_range, list):
            result.extend([make_range(dim_idx, r) for r in dim_range])
        else:
            raise ValueError(
                "Unknown subarray/index type! (type: '{}', "
                ", idx: '{}', value: '{}')".format(type(dim_range), dim_idx, dim_range)
            )

    return result


class CloudArray(object):
    def apply(self, func, subarray, attrs=None, layout=None):
        """
    Apply a user defined function to a udf

    **Example**
    >>> import tiledb, tiledb.cloud, numpy
    >>> def median(df):
    ...   return numpy.median(df["a"])
    >>> # Open the array then run the UDF
    >>> with tiledb.SparseArray("tiledb://TileDB-Inc/quickstart_dense", ctx=tiledb.cloud.ctx()) as A:
    ...   A.apply(median, [(0,5), (0,5)], attrs=["a", "b", "c"])
    2.0

    :param func: user function to run
    :return: results of applied udf
    """

        (namespace, array_name) = split_uri(self.uri)
        api_instance = client.get_udf_api()

        if not callable(func):
            raise TypeError("First argument to `apply` must be callable!")

        pickledUDF = cloudpickle.dumps(func, protocol=tiledb_cloud_protocol)
        pickledUDF = base64.b64encode(pickledUDF).decode("ascii")

        dtypes = list(
            self.schema.domain.dim(idx).dtype
            for idx in range(0, self.schema.domain.ndim)
        )

        def build_rest_udfrange(dim_idx, start, end):
            xstart = build_dimension_coordinate(dtypes[dim_idx], start)
            xend = build_dimension_coordinate(dtypes[dim_idx], end)
            return rest_api.models.UDFSubarrayRange(
                dimension_id=dim_idx, range_start=xstart, range_end=xend
            )

        ranges = parse_ranges(subarray, build_rest_udfrange)

        converted_layout = "row-major"

        if layout is None:
            converted_layout = "unordered"
        elif layout.upper() == "R":
            converted_layout = "row-major"
        elif layout.upper() == "C":
            converted_layout = "col-major"
        elif layout.upper() == "G":
            converted_layout = "global-order"

        ranges = rest_api.models.UDFSubarray(layout=converted_layout, ranges=ranges)

        try:
            # _preload_content must be set to false to avoid trying to decode binary data
            response = api_instance.submit_udf(
                namespace=namespace,
                array=array_name,
                udf=rest_api.models.UDF(
                    type=rest_api.models.UDFType.PYTHON,
                    _exec=pickledUDF,
                    subarray=ranges,
                    version="{}.{}.{}".format(
                        sys.version_info.major,
                        sys.version_info.minor,
                        sys.version_info.micro,
                    ),
                ),
                _preload_content=False,
            )
            response = rest.RESTResponse(response)

            global last_udf_task_id
            last_udf_task_id = response.getheader(client.TASK_ID_HEADER)

            res = response.data
        except GenApiException as exc:
            raise tiledb_cloud_error.check_udf_exc(exc) from None
        return cloudpickle.loads(res)
