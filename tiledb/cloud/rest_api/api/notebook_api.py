# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from tiledb.cloud.rest_api.api_client import ApiClient
from tiledb.cloud.rest_api.exceptions import ApiTypeError  # noqa: F401
from tiledb.cloud.rest_api.exceptions import ApiValueError


class NotebookApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_notebook_server_status(self, namespace, **kwargs):  # noqa: E501
        """get_notebook_server_status  # noqa: E501

        Get status of the notebook server  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_notebook_server_status(namespace, async_req=True)
        >>> result = thread.get()

        :param namespace: namespace notebook is in (an organization name or user's username) (required)
        :type namespace: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: NotebookStatus
        """
        kwargs["_return_http_data_only"] = True
        return self.get_notebook_server_status_with_http_info(
            namespace, **kwargs
        )  # noqa: E501

    def get_notebook_server_status_with_http_info(
        self, namespace, **kwargs
    ):  # noqa: E501
        """get_notebook_server_status  # noqa: E501

        Get status of the notebook server  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_notebook_server_status_with_http_info(namespace, async_req=True)
        >>> result = thread.get()

        :param namespace: namespace notebook is in (an organization name or user's username) (required)
        :type namespace: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(NotebookStatus, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = ["namespace"]
        all_params.extend(
            [
                "async_req",
                "_return_http_data_only",
                "_preload_content",
                "_request_timeout",
                "_request_auth",
            ]
        )

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_notebook_server_status" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `get_notebook_server_status`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )  # noqa: E501

        # Authentication setting
        auth_settings = ["ApiKeyAuth", "BasicAuth"]  # noqa: E501

        response_types_map = {
            200: "NotebookStatus",
            202: None,
            402: "Error",
            404: None,
        }

        return self.api_client.call_api(
            "/notebooks/server/{namespace}/status",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get("_request_auth"),
        )

    def handle_copy_notebook(
        self, namespace, array, notebook_copy, **kwargs
    ):  # noqa: E501
        """handle_copy_notebook  # noqa: E501

        Copy a tiledb notebook at the specified location  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.handle_copy_notebook(namespace, array, notebook_copy, async_req=True)
        >>> result = thread.get()

        :param namespace: The namespace of the notebook (required)
        :type namespace: str
        :param array: The name of the notebook (required)
        :type array: str
        :param notebook_copy: Input/Output information to create a new TileDB file (required)
        :type notebook_copy: NotebookCopy
        :param x_tiledb_cloud_access_credentials_name: Optional registered access credentials to use for creation
        :type x_tiledb_cloud_access_credentials_name: str
        :param end_timestamp: Milliseconds since Unix epoch, copy will use open_at functionality to copy notebook created at the specific timestamp
        :type end_timestamp: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: NotebookCopied
        """
        kwargs["_return_http_data_only"] = True
        return self.handle_copy_notebook_with_http_info(
            namespace, array, notebook_copy, **kwargs
        )  # noqa: E501

    def handle_copy_notebook_with_http_info(
        self, namespace, array, notebook_copy, **kwargs
    ):  # noqa: E501
        """handle_copy_notebook  # noqa: E501

        Copy a tiledb notebook at the specified location  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.handle_copy_notebook_with_http_info(namespace, array, notebook_copy, async_req=True)
        >>> result = thread.get()

        :param namespace: The namespace of the notebook (required)
        :type namespace: str
        :param array: The name of the notebook (required)
        :type array: str
        :param notebook_copy: Input/Output information to create a new TileDB file (required)
        :type notebook_copy: NotebookCopy
        :param x_tiledb_cloud_access_credentials_name: Optional registered access credentials to use for creation
        :type x_tiledb_cloud_access_credentials_name: str
        :param end_timestamp: Milliseconds since Unix epoch, copy will use open_at functionality to copy notebook created at the specific timestamp
        :type end_timestamp: int
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(NotebookCopied, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            "namespace",
            "array",
            "notebook_copy",
            "x_tiledb_cloud_access_credentials_name",
            "end_timestamp",
        ]
        all_params.extend(
            [
                "async_req",
                "_return_http_data_only",
                "_preload_content",
                "_request_timeout",
                "_request_auth",
            ]
        )

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method handle_copy_notebook" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `handle_copy_notebook`"
            )  # noqa: E501
        # verify the required parameter 'array' is set
        if self.api_client.client_side_validation and (
            "array" not in local_var_params
            or local_var_params["array"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `array` when calling `handle_copy_notebook`"
            )  # noqa: E501
        # verify the required parameter 'notebook_copy' is set
        if self.api_client.client_side_validation and (
            "notebook_copy" not in local_var_params
            or local_var_params["notebook_copy"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `notebook_copy` when calling `handle_copy_notebook`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]  # noqa: E501
        if "array" in local_var_params:
            path_params["array"] = local_var_params["array"]  # noqa: E501

        query_params = []
        if (
            "end_timestamp" in local_var_params
            and local_var_params["end_timestamp"] is not None
        ):  # noqa: E501
            query_params.append(
                ("end_timestamp", local_var_params["end_timestamp"])
            )  # noqa: E501

        header_params = {}
        if "x_tiledb_cloud_access_credentials_name" in local_var_params:
            header_params["X-TILEDB-CLOUD-ACCESS-CREDENTIALS-NAME"] = local_var_params[
                "x_tiledb_cloud_access_credentials_name"
            ]  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if "notebook_copy" in local_var_params:
            body_params = local_var_params["notebook_copy"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )  # noqa: E501

        # HTTP header `Content-Type`
        header_params[
            "Content-Type"
        ] = self.api_client.select_header_content_type(  # noqa: E501
            ["application/json"]
        )  # noqa: E501

        # Authentication setting
        auth_settings = ["ApiKeyAuth", "BasicAuth"]  # noqa: E501

        response_types_map = {
            201: "NotebookCopied",
        }

        return self.api_client.call_api(
            "/notebooks/{namespace}/{array}/copy",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get("_request_auth"),
        )

    def handle_upload_notebook(self, namespace, input_file, **kwargs):  # noqa: E501
        """handle_upload_notebook  # noqa: E501

        Upload a notebook at the specified location  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.handle_upload_notebook(namespace, input_file, async_req=True)
        >>> result = thread.get()

        :param namespace: The namespace of the notebook (required)
        :type namespace: str
        :param input_file: the notebook to upload (required)
        :type input_file: file
        :param x_tiledb_cloud_access_credentials_name: Optional registered access credentials to use for creation
        :type x_tiledb_cloud_access_credentials_name: str
        :param output_uri: output location of the TileDB File
        :type output_uri: str
        :param name: name to set for registered file
        :type name: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: FileUploaded
        """
        kwargs["_return_http_data_only"] = True
        return self.handle_upload_notebook_with_http_info(
            namespace, input_file, **kwargs
        )  # noqa: E501

    def handle_upload_notebook_with_http_info(
        self, namespace, input_file, **kwargs
    ):  # noqa: E501
        """handle_upload_notebook  # noqa: E501

        Upload a notebook at the specified location  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.handle_upload_notebook_with_http_info(namespace, input_file, async_req=True)
        >>> result = thread.get()

        :param namespace: The namespace of the notebook (required)
        :type namespace: str
        :param input_file: the notebook to upload (required)
        :type input_file: file
        :param x_tiledb_cloud_access_credentials_name: Optional registered access credentials to use for creation
        :type x_tiledb_cloud_access_credentials_name: str
        :param output_uri: output location of the TileDB File
        :type output_uri: str
        :param name: name to set for registered file
        :type name: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(FileUploaded, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            "namespace",
            "input_file",
            "x_tiledb_cloud_access_credentials_name",
            "output_uri",
            "name",
        ]
        all_params.extend(
            [
                "async_req",
                "_return_http_data_only",
                "_preload_content",
                "_request_timeout",
                "_request_auth",
            ]
        )

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method handle_upload_notebook" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `handle_upload_notebook`"
            )  # noqa: E501
        # verify the required parameter 'input_file' is set
        if self.api_client.client_side_validation and (
            "input_file" not in local_var_params
            or local_var_params["input_file"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `input_file` when calling `handle_upload_notebook`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]  # noqa: E501

        query_params = []

        header_params = {}
        if "x_tiledb_cloud_access_credentials_name" in local_var_params:
            header_params["X-TILEDB-CLOUD-ACCESS-CREDENTIALS-NAME"] = local_var_params[
                "x_tiledb_cloud_access_credentials_name"
            ]  # noqa: E501

        form_params = []
        local_var_files = {}
        if "input_file" in local_var_params:
            local_var_files["input_file"] = local_var_params["input_file"]  # noqa: E501
        if "output_uri" in local_var_params:
            form_params.append(
                ("output_uri", local_var_params["output_uri"])
            )  # noqa: E501
        if "name" in local_var_params:
            form_params.append(("name", local_var_params["name"]))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )  # noqa: E501

        # HTTP header `Content-Type`
        header_params[
            "Content-Type"
        ] = self.api_client.select_header_content_type(  # noqa: E501
            ["multipart/form-data"]
        )  # noqa: E501

        # Authentication setting
        auth_settings = ["ApiKeyAuth", "BasicAuth"]  # noqa: E501

        response_types_map = {
            201: "FileUploaded",
        }

        return self.api_client.call_api(
            "/notebooks/{namespace}/upload",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get("_request_auth"),
        )

    def shutdown_notebook_server(self, namespace, **kwargs):  # noqa: E501
        """shutdown_notebook_server  # noqa: E501

        Shutdown a notebook server  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.shutdown_notebook_server(namespace, async_req=True)
        >>> result = thread.get()

        :param namespace: namespace notebook is in (an organization name or user's username) (required)
        :type namespace: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs["_return_http_data_only"] = True
        return self.shutdown_notebook_server_with_http_info(
            namespace, **kwargs
        )  # noqa: E501

    def shutdown_notebook_server_with_http_info(
        self, namespace, **kwargs
    ):  # noqa: E501
        """shutdown_notebook_server  # noqa: E501

        Shutdown a notebook server  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.shutdown_notebook_server_with_http_info(namespace, async_req=True)
        >>> result = thread.get()

        :param namespace: namespace notebook is in (an organization name or user's username) (required)
        :type namespace: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        local_var_params = locals()

        all_params = ["namespace"]
        all_params.extend(
            [
                "async_req",
                "_return_http_data_only",
                "_preload_content",
                "_request_timeout",
                "_request_auth",
            ]
        )

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method shutdown_notebook_server" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `shutdown_notebook_server`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )  # noqa: E501

        # Authentication setting
        auth_settings = ["ApiKeyAuth", "BasicAuth"]  # noqa: E501

        response_types_map = {}

        return self.api_client.call_api(
            "/notebooks/server/{namespace}",
            "DELETE",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get("_request_auth"),
        )

    def update_notebook_name(
        self, namespace, array, notebook_metadata, **kwargs
    ):  # noqa: E501
        """update_notebook_name  # noqa: E501

        update name on a notebok, moving related S3 object to new location  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.update_notebook_name(namespace, array, notebook_metadata, async_req=True)
        >>> result = thread.get()

        :param namespace: namespace array is in (an organization name or user's username) (required)
        :type namespace: str
        :param array: name/uri of notebook (array) that is url-encoded (required)
        :type array: str
        :param notebook_metadata: notebook (array) metadata to update (required)
        :type notebook_metadata: ArrayInfoUpdate
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs["_return_http_data_only"] = True
        return self.update_notebook_name_with_http_info(
            namespace, array, notebook_metadata, **kwargs
        )  # noqa: E501

    def update_notebook_name_with_http_info(
        self, namespace, array, notebook_metadata, **kwargs
    ):  # noqa: E501
        """update_notebook_name  # noqa: E501

        update name on a notebok, moving related S3 object to new location  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.update_notebook_name_with_http_info(namespace, array, notebook_metadata, async_req=True)
        >>> result = thread.get()

        :param namespace: namespace array is in (an organization name or user's username) (required)
        :type namespace: str
        :param array: name/uri of notebook (array) that is url-encoded (required)
        :type array: str
        :param notebook_metadata: notebook (array) metadata to update (required)
        :type notebook_metadata: ArrayInfoUpdate
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        local_var_params = locals()

        all_params = ["namespace", "array", "notebook_metadata"]
        all_params.extend(
            [
                "async_req",
                "_return_http_data_only",
                "_preload_content",
                "_request_timeout",
                "_request_auth",
            ]
        )

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_notebook_name" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `update_notebook_name`"
            )  # noqa: E501
        # verify the required parameter 'array' is set
        if self.api_client.client_side_validation and (
            "array" not in local_var_params
            or local_var_params["array"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `array` when calling `update_notebook_name`"
            )  # noqa: E501
        # verify the required parameter 'notebook_metadata' is set
        if self.api_client.client_side_validation and (
            "notebook_metadata" not in local_var_params
            or local_var_params["notebook_metadata"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `notebook_metadata` when calling `update_notebook_name`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]  # noqa: E501
        if "array" in local_var_params:
            path_params["array"] = local_var_params["array"]  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "notebook_metadata" in local_var_params:
            body_params = local_var_params["notebook_metadata"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )  # noqa: E501

        # HTTP header `Content-Type`
        header_params[
            "Content-Type"
        ] = self.api_client.select_header_content_type(  # noqa: E501
            ["application/json"]
        )  # noqa: E501

        # Authentication setting
        auth_settings = ["ApiKeyAuth", "BasicAuth"]  # noqa: E501

        response_types_map = {}

        return self.api_client.call_api(
            "/notebooks/{namespace}/{array}/rename",
            "PATCH",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get("_request_auth"),
        )
