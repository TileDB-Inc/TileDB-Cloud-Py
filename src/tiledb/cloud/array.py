import uuid
import warnings
from typing import Any, Callable, Iterable, List, Optional, Sequence, Union

import numpy

from . import client
from . import rest_api
from . import tiledb_cloud_error
from . import udf
from ._common import functions
from ._common import json_safe
from ._common import utils
from ._results import decoders
from ._results import results
from ._results import sender
from ._results import types
from .rest_api import ApiException as GenApiException
from .rest_api import models

last_udf_task_id: Optional[str] = None

# Re-export for compatibility.
split_uri = utils.split_uri


class ArrayList:
    """
    This class incrementally builds a list of UDFArrayDetails
    for use in multi array UDFs `list[UDFArrayDetails]`
    """

    def __init__(self):
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

        parsed = parse_ranges(ranges)  # check that the ranges are parseable.
        udf_array_details = models.UDFArrayDetails(
            uri=uri,
            ranges=models.QueryRanges(layout=converted_layout, ranges=parsed),
            buffers=buffers,
            parameter_id=str(uuid.uuid4()),
        )
        self.arrayList.append(udf_array_details)

    def get(self):
        """
        Returns the list of UDFArrayDetails
        """
        return self.arrayList

    def _to_tgudf_args(self) -> Sequence[object]:
        tgudf_ified = tuple(
            {
                "__tdbudf__": "udf_array_details",
                "udf_array_details": entry,
            }
            for entry in self.arrayList
        )
        if not tgudf_ified:
            # If there are no arrays, nothing is prepended.
            return ()
        if len(tgudf_ified) == 1:
            # If there is one array, it is prepended as a single value.
            return ({"value": tgudf_ified[0]},)
        # Otherwise, the list of arrays is passed as a single parameter.
        return ({"value": tgudf_ified},)


def info(uri, async_req=False):
    """
    Returns the cloud metadata

    :param async_req: return future instead of results for async support

    :return: metadata object
    """
    (namespace, array_name) = split_uri(uri)
    api_instance = client.build(rest_api.ArrayApi)

    try:
        return api_instance.get_array_metadata(
            namespace=namespace, array=array_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def list_shared_with(uri, async_req=False):
    """Return array sharing policies"""
    (namespace, array_name) = split_uri(uri)
    api_instance = client.build(rest_api.ArrayApi)

    try:
        return api_instance.get_array_sharing_policies(
            namespace=namespace, array=array_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


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
            not perm.lower() == models.ArrayActions.READ
            and not perm.lower() == models.ArrayActions.WRITE
        ):
            raise Exception("Only read or write permissions are accepted")

    (array_namespace, array_name) = split_uri(uri)
    api_instance = client.build(rest_api.ArrayApi)

    try:
        return api_instance.share_array(
            namespace=array_namespace,
            array=array_name,
            array_sharing=models.ArraySharing(namespace=namespace, actions=permissions),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


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
    :param str namespace: The username or organization that owns the array.
        If unset, will use the logged-in user.
    :param str array_name: name of array to rename to
    :param str description: optional description
    :param str access_credentials_name: The access credentials to use when
        accessing the backing array. Leave unset to not change.
    :param list tags: to update to
    :param str file_type: array represents give file type
    :param str file_properties: set file properties on array
    :param async_req: return future instead of results for async support
    """
    api_instance = client.build(rest_api.ArrayApi)
    (namespace, current_array_name) = split_uri(uri)

    try:
        return api_instance.update_array_metadata(
            namespace=namespace,
            array=current_array_name,
            array_metadata=models.ArrayInfoUpdate(
                description=description,
                name=array_name,
                uri=uri,
                access_credentials_name=access_credentials_name,
                tags=tags,
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def update_file_properties(uri, file_type=None, file_properties=None, async_req=False):
    """
    Update an Array to indicate its a file and has given properties.
    Any properties set are returned with the array info.
    :param str uri: uri of array to update
    :param str file_type: file type to set
    :param dict file_properties: dictionary of properties to set
    :return:
    """

    api_instance = client.build(rest_api.ArrayApi)
    (namespace, current_array_name) = split_uri(uri)

    try:
        return api_instance.update_array_metadata(
            namespace=namespace,
            array=current_array_name,
            array_metadata=models.ArrayInfoUpdate(
                file_type=file_type, file_properties=file_properties
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


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
    :param str namespace: The user or organization to register the array under.
        If unset will default to the user
    :param str array_name: name of array
    :param str description: optional description
    :param str access_credentials_name: optional name of access credentials to use,
        if left blank default for namespace will be used
    :param async_req: return future instead of results for async support
    """
    api_instance = client.build(rest_api.ArrayApi)

    namespace = namespace or client.default_user().username

    try:
        return api_instance.register_array(
            namespace=namespace,
            array=uri,
            array_metadata=models.ArrayInfoUpdate(
                description=description,
                name=array_name,
                uri=uri,
                access_credentials_name=access_credentials_name,
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def deregister_array(uri, async_req=False):
    """
    Deregister the from the tiledb cloud service.
    This does not physically delete the array, it will remain in your bucket.
    All access to the array and cloud metadata will be removed.

    :param async_req: return future instead of results for async support

    :return success or error
    """
    (namespace, array_name) = split_uri(uri)

    api_instance = client.build(rest_api.ArrayApi)

    try:
        return api_instance.deregister_array(
            namespace=namespace, array=array_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def delete_array(uri, *, async_req=False):
    """
    Deregister the array from the tiledb cloud service,
    then deletes physical array from disk.

    All access to the array and cloud metadata will be removed.

    :param async_req: return future instead of results for async support

    :return success or error
    """
    (namespace, array_name) = split_uri(uri)

    api_instance = client.build(rest_api.ArrayApi)

    try:
        return api_instance.delete_array(
            namespace=namespace,
            array=array_name,
            content_type="application/json",
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def array_activity(uri, async_req=False):
    """
    Fetch array activity
    :param uri:
    :param async_req: return future instead of results for async support
    :return:
    """
    (namespace, array_name) = split_uri(uri)

    api_instance = client.build(rest_api.ArrayApi)

    try:
        return api_instance.array_activity_log(
            namespace=namespace, array=array_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


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
        if isinstance(dim_range, numpy.ndarray):
            dim_list = dim_range.tolist()
        elif isinstance(
            dim_range, (int, float, tuple, slice, numpy.datetime64, numpy.timedelta64)
        ):
            dim_list = make_range(dim_range)
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

    return json_safe.Value(result)


def apply_base(
    uri: str,
    func: Union[str, Callable, None] = None,
    ranges: Sequence = (),
    name: Optional[str] = None,
    attrs: Sequence = (),
    layout: Optional[str] = None,
    image_name: str = "default",
    http_compressor: str = "deflate",
    include_source_lines: bool = True,
    task_name: Optional[str] = None,
    v2=None,
    result_format: str = models.ResultFormat.NATIVE,
    result_format_version=None,
    store_results: bool = False,
    stored_param_uuids: Iterable[uuid.UUID] = (),
    timeout: int = None,
    resource_class: Optional[str] = None,
    _download_results: bool = True,
    namespace: Optional[str] = None,
    _server_graph_uuid: Optional[uuid.UUID] = None,
    _client_node_uuid: Optional[uuid.UUID] = None,
    **kwargs: Any,
) -> results.RemoteResult:
    """Apply a user-defined function to an array, and return data and metadata.

    :param uri: The ``tiledb://...`` URI of the array to apply the function to.
    :param func: The function to run. This can be either a callable function,
        or the name of a registered user-defined function
    :param ranges: ranges to issue query on
    :param name: Deprecated. If ``func`` is ``None``, the name of the registered
        user-defined function to call.
    :param attrs: list of attributes or dimensions to fetch in query
    :param layout: tiledb query layout
    :param image_name: udf image name to use, useful for testing beta features
    :param http_compressor: set http compressor for results
    :param include_source_lines: True to send the source code of your UDF to
        the server with your request. (This means it can be shown to you
        in stack traces if an error occurs.) False to send only compiled Python
        bytecode.
    :param str task_name: optional name to assign the task
        for logging and audit purposes
    :param v2: Ignored.
    :param ResultFormat result_format: result serialization format
    :param result_format_version: Deprecated and ignored.
    :param store_results: True to temporarily store results on the server side
        for later retrieval (in addition to downloading them).
    :param timeout: Timeout for UDF in seconds
    :param resource_class: The name of the resource class to use. Resource classes
        define maximum limits for cpu and memory usage.
    :param _download_results: True to download and parse results eagerly.
        False to not download results by default and only do so lazily
        (e.g. for an intermediate node in a graph).
    :param namespace: The namespace to execute the UDF under.
    :param _server_graph_uuid: If this function is being executed within a DAG,
        the server-generated ID of the graph's log. Otherwise, None.
    :param _client_node_uuid: If this function is being executed within a DAG,
        the ID of this function's node within the graph. Otherwise, None.
    :param kwargs: named arguments to pass to function

    **Example**
    >>> import tiledb, tiledb.cloud, numpy
    >>> def median(df):
    ...   return numpy.median(df["a"])
    >>> # Open the array then run the UDF
    >>> tiledb.cloud.array.apply_base("tiledb://TileDB-Inc/quickstart_dense", median, [(0,5), (0,5)], attrs=["a", "b", "c"]).result
    2.0
    """  # noqa: E501
    del v2  # unused

    if result_format_version:
        warnings.warn(DeprecationWarning("result_format_version is unused."))

    api_instance = client.build(rest_api.UdfApi)

    if name:
        warnings.warn(
            DeprecationWarning(
                "Use of `name` to set a function name is deprecated. "
                "Pass the function name in `func` instead."
            )
        )
    user_func = _pick_func(func=func, name=name)

    array_list = ArrayList()
    array_list.add(
        uri=uri,
        layout=layout,
        ranges=ranges,
        buffers=attrs,
    )

    udf_model = models.MultiArrayUDF(
        language=models.UDFLanguage.PYTHON,
        arrays=array_list.get(),
        version=utils.PYTHON_VERSION,
        image_name=image_name,
        task_name=task_name,
        result_format=result_format,
        store_results=store_results,
        stored_param_uuids=list(str(uuid) for uuid in stored_param_uuids),
        resource_class=resource_class,
        dont_download_results=not _download_results,
        task_graph_uuid=_server_graph_uuid and str(_server_graph_uuid),
        client_node_uuid=_client_node_uuid and str(_client_node_uuid),
    )

    if timeout is not None:
        udf_model.timeout = timeout

    if callable(user_func):
        udf_model._exec = utils.b64_pickle(user_func)
        if include_source_lines:
            udf_model.exec_raw = functions.getsourcelines(user_func)
    else:
        udf_model.udf_info_name = user_func

    json_arguments: List[object] = []
    json_arguments.extend(array_list._to_tgudf_args())
    json_arguments.extend(
        udf._StoredParamJSONer().encode_arguments(types.Arguments((), kwargs))
    )
    udf_model.arguments_json = json_arguments

    if kwargs:
        udf_model.argument = utils.b64_pickle((kwargs,))

    submit_kwargs = dict(
        namespace=namespace or client.default_charged_namespace(),
        udf=udf_model,
    )

    if http_compressor:
        submit_kwargs["accept_encoding"] = http_compressor

    return sender.send_udf_call(
        api_instance.submit_multi_array_udf,
        submit_kwargs,
        decoders.Decoder(result_format),
        id_callback=_maybe_set_last_udf_id,
        results_stored=store_results,
        results_downloaded=_download_results,
    )


@functions.signature_of(apply_base)
def apply(*args, **kwargs) -> Any:
    """
    Apply a user defined function to an array, synchronously.

    All arguments are exactly as in :func:`apply_base`, but this returns
    the data only.

    **Example:**

    >>> import tiledb, tiledb.cloud, numpy
    >>> def median(df):
    ...   return numpy.median(df["a"])
    >>> # Open the array then run the UDF
    >>> tiledb.cloud.array.apply("tiledb://TileDB-Inc/quickstart_dense", median, [(0,5), (0,5)], attrs=["a", "b", "c"])
    2.0
    """  # noqa: E501
    return apply_base(*args, **kwargs).get()


def apply_async(*args, **kwargs) -> results.AsyncResult:
    """Apply a user-defined function to an array, asynchronously.

    All arguments are exactly as in :func:`apply_base`, but this returns
    the data as a future-like AsyncResponse.
    """
    return sender.wrap_async_base_call(apply_base, *args, **kwargs)


def exec_multi_array_udf_base(
    func: Union[str, Callable, None] = None,
    array_list: ArrayList = None,
    namespace: Optional[str] = None,
    name: Optional[str] = None,
    layout=None,
    image_name: str = "default",
    http_compressor: Optional[str] = "deflate",
    include_source_lines: bool = True,
    task_name: Optional[str] = None,
    result_format: str = models.ResultFormat.NATIVE,
    result_format_version=None,
    store_results: bool = False,
    stored_param_uuids: Iterable[uuid.UUID] = (),
    resource_class: Optional[str] = None,
    _download_results: bool = True,
    _server_graph_uuid: Optional[uuid.UUID] = None,
    _client_node_uuid: Optional[uuid.UUID] = None,
    **kwargs,
) -> results.RemoteResult:
    """
    Apply a user defined function to multiple arrays.

    :param func: The function to run. This can be either a callable function,
        or the name of a registered user-defined function
    :param array_list: The list of arrays to run the function on,
        as an already-built ArrayList object.
    :param namespace: namespace to run udf under
    :param layout: Ignored.
    :param image_name: udf image name to use, useful for testing beta features
    :param http_compressor: set http compressor for results
    :param str task_name: optional name to assign the task
        for logging and audit purposes
    :param ResultFormat result_format: result serialization format
    :param str result_format_version: Deprecated and ignored.
    :param store_results: True to temporarily store results on the server side
        for later retrieval (in addition to downloading them).
    :param _server_graph_uuid: If this function is being executed within a DAG,
        the server-generated ID of the graph's log. Otherwise, None.
    :param _client_node_uuid: If this function is being executed within a DAG,
        the ID of this function's node within the graph. Otherwise, None.
    :param resource_class: The name of the resource class to use. Resource classes
        define maximum limits for cpu and memory usage.
    :param kwargs: named arguments to pass to function
    :return: A future containing the results of the UDF.
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
    """  # noqa: E501
    if layout:
        warnings.warn(DeprecationWarning("layout is unused."))
    if result_format_version:
        warnings.warn(DeprecationWarning("result_format_version is unused."))

    api_instance = client.build(rest_api.UdfApi)

    namespace = namespace or client.default_charged_namespace()

    if type(array_list) is not ArrayList:
        raise TypeError(
            f"array_list must be passed as an ArrayList, not {type(array_list)}"
        )
    assert array_list
    arrays = array_list.get()
    if not arrays:
        raise ValueError("must pass at least 1 array to a multi-array UDF")

    user_func = _pick_func(func=func, name=name)
    del name, func

    udf_model = models.MultiArrayUDF(
        language=models.UDFLanguage.PYTHON,
        arrays=arrays,
        version=utils.PYTHON_VERSION,
        image_name=image_name,
        task_name=task_name,
        result_format=result_format,
        store_results=store_results,
        stored_param_uuids=list(str(uuid) for uuid in stored_param_uuids),
        resource_class=resource_class,
        dont_download_results=not _download_results,
        task_graph_uuid=_server_graph_uuid and str(_server_graph_uuid),
        client_node_uuid=_client_node_uuid and str(_client_node_uuid),
    )

    if callable(user_func):
        udf_model._exec = utils.b64_pickle(user_func)
        if include_source_lines:
            udf_model.exec_raw = functions.getsourcelines(user_func)
    else:
        udf_model.udf_info_name = user_func

    json_arguments: List[object] = []
    json_arguments.extend(array_list._to_tgudf_args())
    json_arguments.extend(
        udf._StoredParamJSONer().encode_arguments(types.Arguments((), kwargs))
    )
    if kwargs:
        udf_model.argument = utils.b64_pickle((kwargs,))

    submit_kwargs = dict(
        namespace=namespace,
        udf=udf_model,
    )
    if http_compressor:
        submit_kwargs["accept_encoding"] = http_compressor

    return sender.send_udf_call(
        api_instance.submit_multi_array_udf,
        submit_kwargs,
        decoders.Decoder(result_format),
        id_callback=_maybe_set_last_udf_id,
        results_stored=store_results,
        results_downloaded=_download_results,
    )


@functions.signature_of(exec_multi_array_udf_base)
def exec_multi_array_udf(*args, **kwargs) -> Any:
    """Apply a user-defined function to multiple arrays, synchronously.

    All arguments are exactly as in :func:`exec_multi_array_udf_base`.
    """
    return exec_multi_array_udf_base(*args, **kwargs).get()


@functions.signature_of(exec_multi_array_udf_base)
def exec_multi_array_udf_async(*args, **kwargs) -> results.AsyncResult:
    """Apply a user-defined function to multiple arrays, asynchronously.

    All arguments are exactly as in :func:`exec_multi_array_udf_base`.
    """
    return sender.wrap_async_base_call(exec_multi_array_udf_base, *args, **kwargs)


def _pick_func(**kwargs: Union[str, Callable, None]) -> Union[str, Callable]:
    """Extracts the exactly *one* function from the provided arguments.

    Raises an error if either zero or more than one functions is passed.
    Uses the names of the arguments as part of the error message.
    """

    result: Union[str, Callable, None] = None
    count = 0

    for val in kwargs.values():
        if val:
            result = val
            count += 1

    if count != 1:
        names = ", ".join(kwargs)
        raise TypeError(f"exactly 1 of [{names}] must be provided")
    if not callable(result) and type(result) != str or not result:
        raise TypeError(
            "provided function must be a callable or the str name of a UDF, "
            f"not {type(result)}"
        )
    return result


def _maybe_set_last_udf_id(task_id: Optional[uuid.UUID]) -> None:
    """Tries to set the last_udf_id from the exception, if present."""
    global last_udf_task_id
    if task_id:
        last_udf_task_id = str(task_id)
