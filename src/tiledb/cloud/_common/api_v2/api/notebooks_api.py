# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

# python 2 and python 3 compatibility library
from tiledb.cloud._common.api_v2.api_client import ApiClient
from tiledb.cloud._common.api_v2.exceptions import ApiTypeError
from tiledb.cloud._common.api_v2.exceptions import ApiValueError


class NotebooksApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def handle_upload_notebook(self, namespace, array, filesize, notebook, **kwargs):
        """handle_upload_notebook

        Upload a notebook at the specified location and wrap it in TileDB Array
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.handle_upload_notebook(namespace, array, filesize, notebook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace of the notebook (required)
        :param str array: name/uri of array that is url-encoded (required)
        :param int filesize: size of the notebook to upload in bytes (required)
        :param file notebook: notebook to upload (required)
        :param str x_tiledb_cloud_access_credentials_name: Optional registered access credentials to use for creation
        :param str name: name of the TileDB array to create, if missing {array} is used
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: NotebookUploaded
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.handle_upload_notebook_with_http_info(
            namespace, array, filesize, notebook, **kwargs
        )

    def handle_upload_notebook_with_http_info(
        self, namespace, array, filesize, notebook, **kwargs
    ):
        """handle_upload_notebook

        Upload a notebook at the specified location and wrap it in TileDB Array
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.handle_upload_notebook_with_http_info(namespace, array, filesize, notebook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace of the notebook (required)
        :param str array: name/uri of array that is url-encoded (required)
        :param int filesize: size of the notebook to upload in bytes (required)
        :param file notebook: notebook to upload (required)
        :param str x_tiledb_cloud_access_credentials_name: Optional registered access credentials to use for creation
        :param str name: name of the TileDB array to create, if missing {array} is used
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(NotebookUploaded, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            "namespace",
            "array",
            "filesize",
            "notebook",
            "x_tiledb_cloud_access_credentials_name",
            "name",
        ]
        all_params.extend(
            [
                "async_req",
                "_return_http_data_only",
                "_preload_content",
                "_request_timeout",
            ]
        )

        for key, val in local_var_params["kwargs"].items():
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method handle_upload_notebook" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params or local_var_params["namespace"] is None
        ):
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `handle_upload_notebook`"
            )
        # verify the required parameter 'array' is set
        if self.api_client.client_side_validation and (
            "array" not in local_var_params or local_var_params["array"] is None
        ):
            raise ApiValueError(
                "Missing the required parameter `array` when calling `handle_upload_notebook`"
            )
        # verify the required parameter 'filesize' is set
        if self.api_client.client_side_validation and (
            "filesize" not in local_var_params or local_var_params["filesize"] is None
        ):
            raise ApiValueError(
                "Missing the required parameter `filesize` when calling `handle_upload_notebook`"
            )
        # verify the required parameter 'notebook' is set
        if self.api_client.client_side_validation and (
            "notebook" not in local_var_params or local_var_params["notebook"] is None
        ):
            raise ApiValueError(
                "Missing the required parameter `notebook` when calling `handle_upload_notebook`"
            )

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]
        if "array" in local_var_params:
            path_params["array"] = local_var_params["array"]

        query_params = []
        if "name" in local_var_params and local_var_params["name"] is not None:
            query_params.append(("name", local_var_params["name"]))
        if "filesize" in local_var_params and local_var_params["filesize"] is not None:
            query_params.append(("filesize", local_var_params["filesize"]))

        header_params = {}
        if "x_tiledb_cloud_access_credentials_name" in local_var_params:
            header_params["X-TILEDB-CLOUD-ACCESS-CREDENTIALS-NAME"] = local_var_params[
                "x_tiledb_cloud_access_credentials_name"
            ]

        form_params = []
        local_var_files = {}

        body_params = None
        if "notebook" in local_var_params:
            body_params = local_var_params["notebook"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # HTTP header `Content-Type`
        header_params["Content-Type"] = self.api_client.select_header_content_type(
            ["application/octet-stream"]
        )

        # Authentication setting
        auth_settings = ["ApiKeyAuth", "BasicAuth"]

        return self.api_client.call_api(
            "/v2/notebooks/{namespace}/{array}/upload",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="NotebookUploaded",
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )
