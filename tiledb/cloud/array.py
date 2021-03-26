from . import rest_api
from . import config
from . import client
from . import tiledb_cloud_error
from .rest_api import ApiException as GenApiException
from .rest_api import rest
from . import udf
from . import utils

import zlib
import multiprocessing
import cloudpickle
import urllib
import base64
import sys
import numpy
import json

last_udf_task_id = None


class UDFResult(multiprocessing.pool.ApplyResult):
    def __init__(self, response, result_format, result_format_version=None):
        self.response = response
        self.task_id = None
        self.result_format = result_format
        self.result_format_version = result_format_version

    def get(self, timeout=None):
        try:
            response = rest.RESTResponse(self.response.get(timeout=timeout))
            global last_udf_task_id
            self.task_id = last_udf_task_id = response.getheader(client.TASK_ID_HEADER)
            res = response.data
        except GenApiException as exc:
            if exc.headers:
                self.task_id = exc.headers.get(client.TASK_ID_HEADER)
            raise tiledb_cloud_error.check_udf_exc(exc) from None
        except multiprocessing.TimeoutError as exc:
            raise tiledb_cloud_error.check_udf_exc(exc) from None

        if res[:2].hex() in ["7801", "785e", "789c", "78da"]:
            try:
                res = zlib.decompress(res)
            except zlib.error:
                raise tiledb_cloud_error.TileDBCloudError(
                    "Failed to decompress (zlib) result object"
                )

        try:
            if self.result_format == rest_api.models.UDFResultType.NATIVE:
                res = cloudpickle.loads(res)
            elif self.result_format == rest_api.models.UDFResultType.JSON:
                res = json.loads(res)
            elif self.result_format == rest_api.models.UDFResultType.ARROW:
                import pyarrow

                # Arrow optimized empty results by not serializing anything
                # We need to account for this and return None to the user instead of trying to read it (which will produce an error)
                if len(res) == 0:
                    return None

                reader = pyarrow.RecordBatchStreamReader(res)
                res = reader.read_all()
        except:
            raise tiledb_cloud_error.TileDBCloudError("Failed to load result object")

        return res


class ArrayList:
    def __init__(self):
        """
        This class incrementally builds a list of UDFArrayDetails for use in
        multi array UDFs
        """
        """list[UDFArrayDetails]"""
        self.arrayList = []

    def add(self, uri=None, ranges=None, buffers=None, layout=None):
        """
        Adds an array to list
        """
        if layout is None:
            converted_layout = None
        elif layout.upper() == "R":
            converted_layout = "row-major"
        elif layout.upper() == "C":
            converted_layout = "col-major"
        elif layout.upper() == "G":
            converted_layout = "global-order"
        elif layout.upper() == "U":
            converted_layout = "unordered"

        array_ranges = parse_ranges(ranges)
        udf_array_details = rest_api.models.UDFArrayDetails(
            uri=uri,
            ranges=rest_api.models.QueryRanges(layout=converted_layout, ranges=ranges),
            buffers=buffers,
        )
        self.arrayList.append(udf_array_details)

    def get(self):
        """
        Returns the list of UDFArrayDetails
        """
        return self.arrayList


def info(uri, async_req=False):
    """
    Returns the cloud metadata

    :param async_req: return future instead of results for async support

    :return: metadata object
    """
    (namespace, array_name) = split_uri(uri)
    api_instance = client.client.array_api

    try:
        return api_instance.get_array_metadata(
            namespace=namespace, array=array_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def list_shared_with(uri, async_req=False):
    """Return array sharing policies"""
    (namespace, array_name) = split_uri(uri)
    api_instance = client.client.array_api

    try:
        return api_instance.get_array_sharing_policies(
            namespace=namespace, array=array_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def share_array(uri, namespace, permissions, async_req=False):
    """
    Shares array with give namespace and permissions

    :param str namespace:
    :param list(str) permissions:
    :param async_req: return future instead of results for async support
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

    (array_namespace, array_name) = split_uri(uri)
    api_instance = client.client.array_api

    try:
        return api_instance.share_array(
            namespace=array_namespace,
            array=array_name,
            array_sharing=rest_api.models.ArraySharing(
                namespace=namespace, actions=permissions
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def unshare_array(uri, namespace, async_req=False):
    """
    Removes sharing of an array from given namespace

    :param str namespace: namespace to remove shared access to the array
    :param async_req: return future instead of results for async support
    :return:
    :raises: :py:exc:
    """
    return share_array(uri, namespace, list(), async_req=async_req)


def update_info(
    uri,
    array_name=None,
    description=None,
    access_credentials_name=None,
    tags=None,
    async_req=False,
):
    """
    Update an array's info
    :param str namespace: optional username or organization array should be registered under. If unset will default to the user
    :param str array_name: name of array to rename to
    :param str description: optional description
    :param str access_credentials_name: optional name of access credentials to use, if left blank default for namespace will be used
    :param list tags: to update to
    :param str file_type: array represents give file type
    :param str file_properties: set file properties on array
    :param async_req: return future instead of results for async support
    """
    api_instance = client.client.array_api
    (namespace, current_array_name) = split_uri(uri)

    try:
        return api_instance.update_array_metadata(
            namespace=namespace,
            array=current_array_name,
            array_metadata=rest_api.models.ArrayInfoUpdate(
                description=description,
                name=array_name,
                uri=uri,
                access_credentials_name=access_credentials_name,
                tags=tags,
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def update_file_properties(uri, file_type=None, file_properties=None, async_req=False):
    """
    Update an Array to indicate its a file and has given properties. Any properties set are returned with the array info
    :param str uri: uri of array to update
    :param str file_type: file type to set
    :param dict file_properties: dictionary of properties to set
    :return:
    """

    api_instance = client.client.array_api
    (namespace, current_array_name) = split_uri(uri)

    try:
        return api_instance.update_array_metadata(
            namespace=namespace,
            array=current_array_name,
            array_metadata=rest_api.models.ArrayInfoUpdate(
                file_type=file_type, file_properties=file_properties
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def register_array(
    uri,
    namespace=None,
    array_name=None,
    description=None,
    access_credentials_name=None,
    async_req=False,
):
    """
    Register this array with the tiledb cloud service
    :param str namespace: optional username or organization array should be registered under. If unset will default to the user
    :param str array_name: name of array
    :param str description: optional description
    :param str access_credentials_name: optional name of access credentials to use, if left blank default for namespace will be used
    :param async_req: return future instead of results for async support
    """
    api_instance = client.client.array_api

    if namespace is None:
        if config.user is None:
            config.user = client.user_profile()

        namespace = config.user.username

    try:
        return api_instance.register_array(
            namespace=namespace,
            array=uri,
            array_metadata=rest_api.models.ArrayInfoUpdate(
                description=description,
                name=array_name,
                uri=uri,
                access_credentials_name=access_credentials_name,
            ),
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def deregister_array(uri, async_req=False):
    """
    Deregister the from the tiledb cloud service. This does not physically delete the array, it will remain
    in your bucket. All access to the array and cloud metadata will be removed.

    :param async_req: return future instead of results for async support

    :return success or error
    """
    (namespace, array_name) = split_uri(uri)

    api_instance = client.client.array_api

    try:
        return api_instance.deregister_array(
            namespace=namespace, array=array_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def delete_array(uri, content_type, async_req=False):
    """
    Deregister the array from the tiledb cloud service, then deletes physical array from disk.
    All access to the array and cloud metadata will be removed.

    :param async_req: return future instead of results for async support

    :return success or error
    """
    (namespace, array_name) = split_uri(uri)

    api_instance = client.client.array_api

    try:
        return api_instance.delete_array(
            namespace=namespace,
            array=array_name,
            content_type=content_type,
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def array_activity(uri, async_req=False):
    """
    Fetch array activity
    :param uri:
    :param async_req: return future instead of results for async support
    :return:
    """
    (namespace, array_name) = split_uri(uri)

    api_instance = client.client.array_api

    try:
        return api_instance.array_activity_log(
            namespace=namespace, array=array_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def split_uri(uri):
    """
    Split a URI into namespace and array name

    :param uri: uri to split into namespace and array name
    :param async_req: return future instead of results for async support
    :return: tuple (namespace, array_name)
    """
    parsed = urllib.parse.urlparse(uri)
    if not parsed.scheme == "tiledb":
        raise Exception("Incorrect array uri, must be in tiledb:// scheme")
    return parsed.netloc, parsed.path[1:]


def parse_ranges(ranges):
    """
    Takes a list of the following objects per dimension:

    - scalar index
    - (start,end) tuple
    - list of either of the above types

    :param ranges: list of (scalar, tuple, list)
    :param builder: function taking arguments (dim_idx, start, end)
    :return:
    """

    def make_range(dim_range):
        if isinstance(dim_range, (int, float, numpy.datetime64, numpy.timedelta64)):
            start, end = dim_range, dim_range
        elif isinstance(dim_range, (tuple, list)):
            if len(dim_range) == 0:
                return []
            elif len(dim_range) == 1:
                start, end = dim_range[0]
            elif len(dim_range) == 2:
                start, end = dim_range[0], dim_range[1]
            else:
                raise ValueError("List or tuple has count greater than 2 element")
        elif isinstance(dim_range, slice):
            assert dim_range.step is None, "slice steps are not supported!"
            start, end = dim_range.start, dim_range.stop
        elif dim_range is None:
            return []
        else:
            raise ValueError("Unknown index type! (type: '{}')".format(type(dim_range)))

        # Convert datetimes to int64
        if type(start) == numpy.datetime64 or type(start) == numpy.timedelta64:
            start = start.astype("int64").item()
        if type(end) == numpy.datetime64 or type(end) == numpy.timedelta64:
            end = end.astype("int64").item()

        return [start, end]

    result = list()
    for dim_idx, dim_range in enumerate(ranges):
        dim_list = []
        # TODO handle numpy scalars here?
        if isinstance(
            dim_range, (int, float, tuple, slice, numpy.datetime64, numpy.timedelta64)
        ):
            dim_list.extend(make_range(dim_range))
        elif isinstance(dim_range, list):
            for r in dim_range:
                dim_list.extend(make_range(r))
        elif dim_range is None:
            pass
        else:
            raise ValueError(
                "Unknown subarray/index type! (type: '{}', "
                ", idx: '{}', value: '{}')".format(type(dim_range), dim_idx, dim_range)
            )
        result.append(dim_list)

    return result


def apply_async(
    uri,
    func=None,
    ranges=None,
    name=None,
    attrs=None,
    layout=None,
    image_name=None,
    http_compressor="deflate",
    include_source_lines=True,
    task_name=None,
    v2=True,
    result_format=rest_api.models.UDFResultType.NATIVE,
    result_format_version=None,
    **kwargs
):
    """
    Apply a user defined function to an array asynchronous

    :param uri: array to apply on
    :param func: user function to run
    :param ranges: ranges to issue query on
    :param attrs: list of attributes or dimensions to fetch in query
    :param layout: tiledb query layout
    :param image_name: udf image name to use, useful for testing beta features
    :param http_compressor: set http compressor for results
    :param include_source_lines: disables sending sources lines of function along with udf
    :param str task_name: optional name to assign the task for logging and audit purposes
    :param bool v2: use v2 array udfs
    :param UDFResultType result_format: result serialization format
    :param str result_format_version: set a format version for cloudpickle or arrow IPC
    :param kwargs: named arguments to pass to function
    :return: UDFResult object which is a future containing the results of the UDF

    **Example**
    >>> import tiledb, tiledb.cloud, numpy
    >>> def median(df):
    ...   return numpy.median(df["a"])
    >>> # Open the array then run the UDF
    >>> tiledb.cloud.array.apply_async("tiledb://TileDB-Inc/quickstart_dense", median, [(0,5), (0,5)], attrs=["a", "b", "c"]).get()
    2.0
    """

    (namespace, array_name) = split_uri(uri)
    api_instance = client.client.udf_api

    if func is not None and not callable(func):
        raise TypeError("func argument to `apply` must be callable!")
    elif func is None and name is None or name == "":
        raise TypeError("name argument to `apply` must be set if no function is passed")

    pickledUDF = None
    source_lines = None
    if func is not None:
        source_lines = utils.getsourcelines(func) if include_source_lines else None
        pickledUDF = cloudpickle.dumps(func, protocol=udf.tiledb_cloud_protocol)
        pickledUDF = base64.b64encode(pickledUDF).decode("ascii")

    ranges = parse_ranges(ranges)

    if layout is None:
        converted_layout = None
    elif layout.upper() == "R":
        converted_layout = "row-major"
    elif layout.upper() == "C":
        converted_layout = "col-major"
    elif layout.upper() == "G":
        converted_layout = "global-order"
    elif layout.upper() == "U":
        converted_layout = "unordered"

    ranges = rest_api.models.QueryRanges(layout=converted_layout, ranges=ranges)

    arguments = None
    if kwargs is not None and len(kwargs) > 0:
        arguments = []
        if len(kwargs) > 0:
            arguments.append(kwargs)
        arguments = tuple(arguments)
        arguments = cloudpickle.dumps(arguments, protocol=udf.tiledb_cloud_protocol)
        arguments = base64.b64encode(arguments).decode("ascii")

    if image_name is None:
        image_name = "default"
    try:

        kwargs = {"_preload_content": False, "async_req": True}
        if http_compressor is not None:
            kwargs["accept_encoding"] = http_compressor

        kwargs["v2"] = v2

        udf_model = rest_api.models.MultiArrayUDF(
            language=rest_api.models.UDFLanguage.PYTHON,
            _exec=pickledUDF,
            ranges=ranges,
            buffers=attrs,
            version="{}.{}.{}".format(
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
            ),
            image_name=image_name,
            task_name=task_name,
            argument=arguments,
            result_format=result_format,
            result_format_version=result_format_version,
        )

        if pickledUDF is not None:
            udf_model._exec = pickledUDF
        elif name is not None:
            udf_model.udf_info_name = name

        if source_lines is not None:
            udf_model.exec_raw = source_lines

        # _preload_content must be set to false to avoid trying to decode binary data
        response = api_instance.submit_udf(
            namespace=namespace, array=array_name, udf=udf_model, **kwargs
        )

        return UDFResult(response, result_format=result_format)

    except GenApiException as exc:
        raise tiledb_cloud_error.check_udf_exc(exc) from None


def apply(
    uri,
    func=None,
    ranges=None,
    name=None,
    attrs=None,
    layout=None,
    image_name=None,
    http_compressor="deflate",
    task_name=None,
    v2=True,
    result_format=rest_api.models.UDFResultType.NATIVE,
    result_format_version=None,
    **kwargs
):
    """
    Apply a user defined function to an array synchronous

    :param uri: array to apply on
    :param func: user function to run
    :param ranges: ranges to issue query on
    :param attrs: list of attributes or dimensions to fetch in query
    :param layout: tiledb query layout
    :param image_name: udf image name to use, useful for testing beta features
    :param http_compressor: set http compressor for results
    :param str task_name: optional name to assign the task for logging and audit purposes
    :param bool v2: use v2 array udfs
    :param UDFResultType result_format: result serialization format
    :param str result_format_version: set a format version for cloudpickle or arrow IPC
    :param kwargs: named arguments to pass to function
    :return: UDFResult object which is a future containing the results of the UDF

    **Example**
    >>> import tiledb, tiledb.cloud, numpy
    >>> def median(df):
    ...   return numpy.median(df["a"])
    >>> # Open the array then run the UDF
    >>> tiledb.cloud.array.apply("tiledb://TileDB-Inc/quickstart_dense", median, [(0,5), (0,5)], attrs=["a", "b", "c"])
    2.0
    """
    return apply_async(
        uri=uri,
        func=func,
        ranges=ranges,
        name=name,
        attrs=attrs,
        layout=layout,
        image_name=image_name,
        http_compressor=http_compressor,
        task_name=task_name,
        v2=v2,
        result_format=result_format,
        result_format_version=result_format_version,
        **kwargs,
    ).get()


def exec_multi_array_udf_async(
    func=None,
    array_list=None,
    namespace=None,
    name=None,
    layout=None,
    image_name=None,
    http_compressor="deflate",
    include_source_lines=True,
    task_name=None,
    result_format=rest_api.models.UDFResultType.NATIVE,
    result_format_version=None,
    **kwargs
):
    """
    Apply a user defined function to multiple arrays
    :param func: user function to run
    :param namespace: namespace to run udf under
    :param array_list: ArrayList object build incrementally to contain list of UDFArrayDetails for use in multi array UDFs
    :param layout: tiledb query layout
    :param image_name: udf image name to use, useful for testing beta features
    :param http_compressor: set http compressor for results
    :param str task_name: optional name to assign the task for logging and audit purposes
    :param UDFResultType result_format: result serialization format
    :param str result_format_version: set a format version for cloudpickle or arrow IPC
    :param kwargs: named arguments to pass to function
    :return: UDFResult object which is a future containing the results of the UDF
    >>> import numpy as np
    >>> from tiledb.cloud import array
    >>> import tiledb.cloud
    >>> dense_array = "tiledb://andreas/quickstart_dense_local"
    >>> sparse_array = "tiledb://andreas/quickstart_sparse_local"
    >>> def median(numpy_ordered_dictionary):
    ...    return np.median(numpy_ordered_dictionary[0]["a"]) + np.median(numpy_ordered_dictionary[1]["a"])
    >>> array_list = array.ArrayList()
    >>> array_list.add(dense_array, [(1, 4), (1, 4)], ["a"])
    >>> array_list.add(sparse_array, [(1, 2), (1, 4)], ["a"])
    >>> namespace = "namespace"
    >>> res = array.exec_multi_array_udf(median, array_list, namespace)
    >>> print("Median Multi UDF:\n{}\n".format(res))
    """

    api_instance = client.client.udf_api

    # If the namespace is not set, we will default to the user's namespace
    if namespace is None:
        # Fetch the client profile for username if it is not already cached
        if config.user is None:
            config.user = client.user_profile()

        namespace = client.find_organization_or_user_for_default_charges(config.user)

    if func is not None and not callable(func):
        raise TypeError("func argument to `exec_multi_array_udf` must be callable!")
    elif func is None and name is None or name == "":
        raise TypeError("name argument to `apply` must be set if no function is passed")

    pickledUDF = None
    source_lines = None
    if func is not None:
        source_lines = utils.getsourcelines(func) if include_source_lines else None
        pickledUDF = cloudpickle.dumps(func, protocol=udf.tiledb_cloud_protocol)
        pickledUDF = base64.b64encode(pickledUDF).decode("ascii")

    if array_list is None:
        raise TypeError("arrays need to have passed in order to call multi array udfs")

    if type(array_list) is not ArrayList:
        raise TypeError("array details passed not of correct type (ArrayList)")

    # Get the list of arrays
    arrays = array_list.get()

    if len(arrays) == 0:
        raise TypeError("arrays need to have passed in order to call multi array udfs")

    arguments = None
    if kwargs is not None and len(kwargs) > 0:
        arguments = []
        if len(kwargs) > 0:
            arguments.append(kwargs)
        arguments = tuple(arguments)
        arguments = cloudpickle.dumps(arguments, protocol=udf.tiledb_cloud_protocol)
        arguments = base64.b64encode(arguments).decode("ascii")

    if image_name is None:
        image_name = "default"
    try:

        kwargs = {"_preload_content": False, "async_req": True}
        if http_compressor is not None:
            kwargs["accept_encoding"] = http_compressor

        udf_model = rest_api.models.MultiArrayUDF(
            language=rest_api.models.UDFLanguage.PYTHON,
            _exec=pickledUDF,
            arrays=arrays,
            version="{}.{}.{}".format(
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
            ),
            image_name=image_name,
            task_name=task_name,
            argument=arguments,
            result_format=result_format,
            result_format_version=result_format_version,
        )

        if pickledUDF is not None:
            udf_model._exec = pickledUDF
        elif name is not None:
            udf_model.udf_info_name = name

        if source_lines is not None:
            udf_model.exec_raw = source_lines

        response = api_instance.submit_multi_array_udf(
            namespace=namespace, udf=udf_model, **kwargs
        )

        return UDFResult(response, result_format=result_format)

    except GenApiException as exc:
        raise tiledb_cloud_error.check_udf_exc(exc) from None


def exec_multi_array_udf(
    func=None,
    array_list=None,
    namespace=None,
    name=None,
    layout=None,
    image_name=None,
    http_compressor="deflate",
    include_source_lines=True,
    task_name=None,
    result_format=rest_api.models.UDFResultType.NATIVE,
    result_format_version=None,
    **kwargs
):
    return exec_multi_array_udf_async(
        func=func,
        array_list=array_list,
        namespace=namespace,
        name=name,
        layout=layout,
        image_name=image_name,
        http_compressor=http_compressor,
        include_source_lines=include_source_lines,
        task_name=task_name,
        result_format=result_format,
        result_format_version=result_format_version,
        **kwargs,
    ).get()
