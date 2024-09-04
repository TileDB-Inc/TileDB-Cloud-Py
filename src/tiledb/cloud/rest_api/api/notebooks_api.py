# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

# python 2 and python 3 compatibility library
import six

from tiledb.cloud.rest_api.api_client import ApiClient
from tiledb.cloud.rest_api.exceptions import ApiTypeError
from tiledb.cloud.rest_api.exceptions import ApiValueError


class NotebooksApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def notebooks_namespace_array_end_timestamps_get(self, namespace, array, **kwargs):
        """notebooks_namespace_array_end_timestamps_get

        retrieve a list of timestamps from the array fragment info listing in milliseconds, paginated
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.notebooks_namespace_array_end_timestamps_get(namespace, array, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace array is in (an organization name or user's username) (required)
        :param str array: name/uri of array that is url-encoded (required)
        :param int page: pagination offset
        :param int per_page: pagination limit
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ArrayEndTimestampData
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.notebooks_namespace_array_end_timestamps_get_with_http_info(
            namespace, array, **kwargs
        )

    def notebooks_namespace_array_end_timestamps_get_with_http_info(
        self, namespace, array, **kwargs
    ):
        """notebooks_namespace_array_end_timestamps_get

        retrieve a list of timestamps from the array fragment info listing in milliseconds, paginated
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.notebooks_namespace_array_end_timestamps_get_with_http_info(namespace, array, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace array is in (an organization name or user's username) (required)
        :param str array: name/uri of array that is url-encoded (required)
        :param int page: pagination offset
        :param int per_page: pagination limit
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ArrayEndTimestampData, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["namespace", "array", "page", "per_page"]
        all_params.extend(
            [
                "async_req",
                "_return_http_data_only",
                "_preload_content",
                "_request_timeout",
            ]
        )

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method notebooks_namespace_array_end_timestamps_get" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params or local_var_params["namespace"] is None
        ):
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `notebooks_namespace_array_end_timestamps_get`"
            )
        # verify the required parameter 'array' is set
        if self.api_client.client_side_validation and (
            "array" not in local_var_params or local_var_params["array"] is None
        ):
            raise ApiValueError(
                "Missing the required parameter `array` when calling `notebooks_namespace_array_end_timestamps_get`"
            )

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]
        if "array" in local_var_params:
            path_params["array"] = local_var_params["array"]

        query_params = []
        if "page" in local_var_params and local_var_params["page"] is not None:
            query_params.append(("page", local_var_params["page"]))
        if "per_page" in local_var_params and local_var_params["per_page"] is not None:
            query_params.append(("per_page", local_var_params["per_page"]))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # Authentication setting
        auth_settings = ["ApiKeyAuth", "BasicAuth"]

        return self.api_client.call_api(
            "/v1/notebooks/{namespace}/{array}/end_timestamps",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="ArrayEndTimestampData",
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def notebooks_namespace_array_prune_post(self, namespace, array, **kwargs):
        """notebooks_namespace_array_prune_post

        prune fragments of the notebook
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.notebooks_namespace_array_prune_post(namespace, array, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace array is in (an organization name or user's username) (required)
        :param str array: name/uri of array that is url-encoded (required)
        :param int keep_versions: The number of most recents fragment to preserve
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.notebooks_namespace_array_prune_post_with_http_info(
            namespace, array, **kwargs
        )

    def notebooks_namespace_array_prune_post_with_http_info(
        self, namespace, array, **kwargs
    ):
        """notebooks_namespace_array_prune_post

        prune fragments of the notebook
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.notebooks_namespace_array_prune_post_with_http_info(namespace, array, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace array is in (an organization name or user's username) (required)
        :param str array: name/uri of array that is url-encoded (required)
        :param int keep_versions: The number of most recents fragment to preserve
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["namespace", "array", "keep_versions"]
        all_params.extend(
            [
                "async_req",
                "_return_http_data_only",
                "_preload_content",
                "_request_timeout",
            ]
        )

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method notebooks_namespace_array_prune_post" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params or local_var_params["namespace"] is None
        ):
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `notebooks_namespace_array_prune_post`"
            )
        # verify the required parameter 'array' is set
        if self.api_client.client_side_validation and (
            "array" not in local_var_params or local_var_params["array"] is None
        ):
            raise ApiValueError(
                "Missing the required parameter `array` when calling `notebooks_namespace_array_prune_post`"
            )

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]
        if "array" in local_var_params:
            path_params["array"] = local_var_params["array"]

        query_params = []
        if (
            "keep_versions" in local_var_params
            and local_var_params["keep_versions"] is not None
        ):
            query_params.append(("keep_versions", local_var_params["keep_versions"]))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # Authentication setting
        auth_settings = ["ApiKeyAuth", "BasicAuth"]

        return self.api_client.call_api(
            "/v1/notebooks/{namespace}/{array}/prune",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )
