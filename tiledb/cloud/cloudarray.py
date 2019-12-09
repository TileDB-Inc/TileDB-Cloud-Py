import urllib
from . import rest_api
from . import config
from . import client
from . import tasks
from . import tiledb_cloud_error
from .rest_api import ApiException as GenApiException
from .rest_api import rest

from tiledb import libtiledb, multirange_indexing

import cloudpickle

tiledb_cloud_protocol = 4

import base64
import sys

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
        raise Exception(
            "Unsupported dimension type {} for apply udf".format(domain_type)
        )

    return None


class MultiIndexRanges(object):
    def __init__(self, ranges):
        self.ranges = ranges


class MultiIndexer(object):
    def __init__(self, array):
        self.schema = array.schema

    def __getitem__(self, idx):
        # adapted from libtiledb.multi_index `getitem_ranges`
        dom = self.schema.domain
        ndim = dom.ndim
        idx = libtiledb._index_as_tuple(idx)

        ranges = list()
        for i, sel in enumerate(idx):
            subranges = multirange_indexing.sel_to_subranges(sel)
            ranges.append(subranges)

        # extend the list to ndim
        if len(ranges) < ndim:
            ranges.extend([tuple() for _ in range(ndim - len(ranges))])

        return MultiIndexRanges(ranges)


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

        ranges = self._calculate_ranges(subarray)

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

    def _calculate_ranges(self, subarray):
        ranges = list()
        if isinstance(subarray, MultiIndexRanges):
            for dim_idx, dim_rng in enumerate(subarray.ranges):
                dim = self.schema.domain.dim(dim_idx)
                for idx, rng in enumerate(dim_rng):
                    start = build_dimension_coordinate(dim.dtype, rng[0])
                    end = build_dimension_coordinate(dim.dtype, rng[1] + 1)
                    ranges.append(
                        rest_api.models.UDFSubarrayRange(
                            dimension_id=dim_idx, range_start=start, range_end=end
                        )
                    )
        else:
            for idx, dim in enumerate(self.schema.domain):
                start = build_dimension_coordinate(dim.dtype, subarray[idx][0])
                end = build_dimension_coordinate(dim.dtype, subarray[idx][1])
                ranges.append(
                    rest_api.models.UDFSubarrayRange(
                        dimension_id=idx, range_start=start, range_end=end
                    )
                )

        return ranges

    @property
    def MI(self):
        return MultiIndexer(self)
