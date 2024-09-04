# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

# python 2 and python 3 compatibility library
import six

from tiledb.cloud._common.api_v2.api_client import ApiClient
from tiledb.cloud._common.api_v2.exceptions import ApiTypeError
from tiledb.cloud._common.api_v2.exceptions import ApiValueError


class FilesApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def handle_upload_file(
        self, namespace, array, content_type, filesize, file, **kwargs
    ):
        """handle_upload_file

        Upload a file at the specified location and wrap it in TileDB Array
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.handle_upload_file(namespace, array, content_type, filesize, file, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace of the file (required)
        :param str array: name/uri of array that is url-encoded (required)
        :param str content_type: Content Type of input (required)
        :param int filesize: size of the file to upload in bytes (required)
        :param file file: file to upload (required)
        :param str x_tiledb_cloud_access_credentials_name: Optional registered access credentials to use for creation
        :param str name: name of the TileDB array to create, if missing {array} is used
        :param str filename: original file name
        :param str mimetype: Mime type of the uploaded file. Autogenerated clients do not always support changing the content type param. Server will always use mimetype query param to set mimetype for file, if it is not set Content-Type will be used
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: FileUploaded
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.handle_upload_file_with_http_info(
            namespace, array, content_type, filesize, file, **kwargs
        )

    def handle_upload_file_with_http_info(
        self, namespace, array, content_type, filesize, file, **kwargs
    ):
        """handle_upload_file

        Upload a file at the specified location and wrap it in TileDB Array
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.handle_upload_file_with_http_info(namespace, array, content_type, filesize, file, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace of the file (required)
        :param str array: name/uri of array that is url-encoded (required)
        :param str content_type: Content Type of input (required)
        :param int filesize: size of the file to upload in bytes (required)
        :param file file: file to upload (required)
        :param str x_tiledb_cloud_access_credentials_name: Optional registered access credentials to use for creation
        :param str name: name of the TileDB array to create, if missing {array} is used
        :param str filename: original file name
        :param str mimetype: Mime type of the uploaded file. Autogenerated clients do not always support changing the content type param. Server will always use mimetype query param to set mimetype for file, if it is not set Content-Type will be used
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(FileUploaded, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            "namespace",
            "array",
            "content_type",
            "filesize",
            "file",
            "x_tiledb_cloud_access_credentials_name",
            "name",
            "filename",
            "mimetype",
        ]
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
                    " to method handle_upload_file" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params or local_var_params["namespace"] is None
        ):
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `handle_upload_file`"
            )
        # verify the required parameter 'array' is set
        if self.api_client.client_side_validation and (
            "array" not in local_var_params or local_var_params["array"] is None
        ):
            raise ApiValueError(
                "Missing the required parameter `array` when calling `handle_upload_file`"
            )
        # verify the required parameter 'content_type' is set
        if self.api_client.client_side_validation and (
            "content_type" not in local_var_params
            or local_var_params["content_type"] is None
        ):
            raise ApiValueError(
                "Missing the required parameter `content_type` when calling `handle_upload_file`"
            )
        # verify the required parameter 'filesize' is set
        if self.api_client.client_side_validation and (
            "filesize" not in local_var_params or local_var_params["filesize"] is None
        ):
            raise ApiValueError(
                "Missing the required parameter `filesize` when calling `handle_upload_file`"
            )
        # verify the required parameter 'file' is set
        if self.api_client.client_side_validation and (
            "file" not in local_var_params or local_var_params["file"] is None
        ):
            raise ApiValueError(
                "Missing the required parameter `file` when calling `handle_upload_file`"
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
        if "filename" in local_var_params and local_var_params["filename"] is not None:
            query_params.append(("filename", local_var_params["filename"]))
        if "filesize" in local_var_params and local_var_params["filesize"] is not None:
            query_params.append(("filesize", local_var_params["filesize"]))
        if "mimetype" in local_var_params and local_var_params["mimetype"] is not None:
            query_params.append(("mimetype", local_var_params["mimetype"]))

        header_params = {}
        if "x_tiledb_cloud_access_credentials_name" in local_var_params:
            header_params["X-TILEDB-CLOUD-ACCESS-CREDENTIALS-NAME"] = local_var_params[
                "x_tiledb_cloud_access_credentials_name"
            ]
        if "content_type" in local_var_params:
            header_params["Content-Type"] = local_var_params["content_type"]

        form_params = []
        local_var_files = {}

        body_params = None
        if "file" in local_var_params:
            body_params = local_var_params["file"]
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
            "/v2/files/{namespace}/{array}/upload",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="FileUploaded",
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )
