# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from tiledb.cloud._common.api_v2.api_client import ApiClient
from tiledb.cloud._common.api_v2.exceptions import ApiTypeError  # noqa: F401
from tiledb.cloud._common.api_v2.exceptions import ApiValueError  # noqa: F401


class UserApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def add_credential(self, namespace, access_credential, **kwargs):  # noqa: E501
        """add_credential  # noqa: E501

        Create a new credential for the namespace  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_credential(namespace, access_credential, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace (required)
        :param AccessCredential access_credential: The new credentials to be created. (required)
        :param str provider: Show only the credentials from this provider. This should be one of the CloudProvider enum values.
        :param str type: Show only the credentials of this type. This should be one of the AccessCredentialType enum values.
        :param int page: pagination offset
        :param int per_page: pagination limit
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
        return self.add_credential_with_http_info(
            namespace, access_credential, **kwargs
        )  # noqa: E501

    def add_credential_with_http_info(
        self, namespace, access_credential, **kwargs
    ):  # noqa: E501
        """add_credential  # noqa: E501

        Create a new credential for the namespace  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.add_credential_with_http_info(namespace, access_credential, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace (required)
        :param AccessCredential access_credential: The new credentials to be created. (required)
        :param str provider: Show only the credentials from this provider. This should be one of the CloudProvider enum values.
        :param str type: Show only the credentials of this type. This should be one of the AccessCredentialType enum values.
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
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            "namespace",
            "access_credential",
            "provider",
            "type",
            "page",
            "per_page",
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
                    " to method add_credential" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `add_credential`"
            )  # noqa: E501
        # verify the required parameter 'access_credential' is set
        if self.api_client.client_side_validation and (
            "access_credential" not in local_var_params
            or local_var_params["access_credential"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `access_credential` when calling `add_credential`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]  # noqa: E501

        query_params = []
        if (
            "provider" in local_var_params and local_var_params["provider"] is not None
        ):  # noqa: E501
            query_params.append(
                ("provider", local_var_params["provider"])
            )  # noqa: E501
        if (
            "type" in local_var_params and local_var_params["type"] is not None
        ):  # noqa: E501
            query_params.append(("type", local_var_params["type"]))  # noqa: E501
        if (
            "page" in local_var_params and local_var_params["page"] is not None
        ):  # noqa: E501
            query_params.append(("page", local_var_params["page"]))  # noqa: E501
        if (
            "per_page" in local_var_params and local_var_params["per_page"] is not None
        ):  # noqa: E501
            query_params.append(
                ("per_page", local_var_params["per_page"])
            )  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "access_credential" in local_var_params:
            body_params = local_var_params["access_credential"]
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

        return self.api_client.call_api(
            "/v2/credentials/{namespace}",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def delete_credential(self, namespace, name, **kwargs):  # noqa: E501
        """delete_credential  # noqa: E501

        Delete the named access credential. Any arrays still set to use this credential will use the namespace's default and may become unreachable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_credential(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace (required)
        :param str name: A URL-safe version of the credential's user-provided name (required)
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
        return self.delete_credential_with_http_info(
            namespace, name, **kwargs
        )  # noqa: E501

    def delete_credential_with_http_info(self, namespace, name, **kwargs):  # noqa: E501
        """delete_credential  # noqa: E501

        Delete the named access credential. Any arrays still set to use this credential will use the namespace's default and may become unreachable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_credential_with_http_info(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace (required)
        :param str name: A URL-safe version of the credential's user-provided name (required)
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

        all_params = ["namespace", "name"]
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
                    " to method delete_credential" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `delete_credential`"
            )  # noqa: E501
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and (
            "name" not in local_var_params
            or local_var_params["name"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `name` when calling `delete_credential`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]  # noqa: E501
        if "name" in local_var_params:
            path_params["name"] = local_var_params["name"]  # noqa: E501

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

        return self.api_client.call_api(
            "/v2/credentials/{namespace}/{name}",
            "DELETE",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def get_credential(self, namespace, name, **kwargs):  # noqa: E501
        """get_credential  # noqa: E501

        Retrieve an access credential by name  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_credential(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace (required)
        :param str name: A URL-safe version of the credential's user-provided name (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AccessCredential
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.get_credential_with_http_info(
            namespace, name, **kwargs
        )  # noqa: E501

    def get_credential_with_http_info(self, namespace, name, **kwargs):  # noqa: E501
        """get_credential  # noqa: E501

        Retrieve an access credential by name  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_credential_with_http_info(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace (required)
        :param str name: A URL-safe version of the credential's user-provided name (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AccessCredential, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["namespace", "name"]
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
                    " to method get_credential" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `get_credential`"
            )  # noqa: E501
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and (
            "name" not in local_var_params
            or local_var_params["name"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `name` when calling `get_credential`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]  # noqa: E501
        if "name" in local_var_params:
            path_params["name"] = local_var_params["name"]  # noqa: E501

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

        return self.api_client.call_api(
            "/v2/credentials/{namespace}/{name}",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="AccessCredential",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def list_credentials(self, namespace, **kwargs):  # noqa: E501
        """list_credentials  # noqa: E501

        List the credentials available in the namespace  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_credentials(namespace, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace (required)
        :param str provider: Show only the credentials from this provider. This should be one of the CloudProvider enum values.
        :param str type: Show only the credentials of this type. This should be one of the AccessCredentialType enum values.
        :param int page: pagination offset
        :param int per_page: pagination limit
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AccessCredentialsData
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.list_credentials_with_http_info(namespace, **kwargs)  # noqa: E501

    def list_credentials_with_http_info(self, namespace, **kwargs):  # noqa: E501
        """list_credentials  # noqa: E501

        List the credentials available in the namespace  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_credentials_with_http_info(namespace, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace (required)
        :param str provider: Show only the credentials from this provider. This should be one of the CloudProvider enum values.
        :param str type: Show only the credentials of this type. This should be one of the AccessCredentialType enum values.
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
        :return: tuple(AccessCredentialsData, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["namespace", "provider", "type", "page", "per_page"]
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
                    " to method list_credentials" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `list_credentials`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]  # noqa: E501

        query_params = []
        if (
            "provider" in local_var_params and local_var_params["provider"] is not None
        ):  # noqa: E501
            query_params.append(
                ("provider", local_var_params["provider"])
            )  # noqa: E501
        if (
            "type" in local_var_params and local_var_params["type"] is not None
        ):  # noqa: E501
            query_params.append(("type", local_var_params["type"]))  # noqa: E501
        if (
            "page" in local_var_params and local_var_params["page"] is not None
        ):  # noqa: E501
            query_params.append(("page", local_var_params["page"]))  # noqa: E501
        if (
            "per_page" in local_var_params and local_var_params["per_page"] is not None
        ):  # noqa: E501
            query_params.append(
                ("per_page", local_var_params["per_page"])
            )  # noqa: E501

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

        return self.api_client.call_api(
            "/v2/credentials/{namespace}",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="AccessCredentialsData",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def update_credential(
        self, namespace, name, access_credential, **kwargs
    ):  # noqa: E501
        """update_credential  # noqa: E501

        Update the named access credential. This will also update the information used to access arrays set to use this credential.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_credential(namespace, name, access_credential, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace (required)
        :param str name: A URL-safe version of the credential's user-provided name (required)
        :param AccessCredential access_credential: Changes to make to this credential (required)
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
        return self.update_credential_with_http_info(
            namespace, name, access_credential, **kwargs
        )  # noqa: E501

    def update_credential_with_http_info(
        self, namespace, name, access_credential, **kwargs
    ):  # noqa: E501
        """update_credential  # noqa: E501

        Update the named access credential. This will also update the information used to access arrays set to use this credential.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_credential_with_http_info(namespace, name, access_credential, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace (required)
        :param str name: A URL-safe version of the credential's user-provided name (required)
        :param AccessCredential access_credential: Changes to make to this credential (required)
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

        all_params = ["namespace", "name", "access_credential"]
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
                    " to method update_credential" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `update_credential`"
            )  # noqa: E501
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and (
            "name" not in local_var_params
            or local_var_params["name"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `name` when calling `update_credential`"
            )  # noqa: E501
        # verify the required parameter 'access_credential' is set
        if self.api_client.client_side_validation and (
            "access_credential" not in local_var_params
            or local_var_params["access_credential"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `access_credential` when calling `update_credential`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]  # noqa: E501
        if "name" in local_var_params:
            path_params["name"] = local_var_params["name"]  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "access_credential" in local_var_params:
            body_params = local_var_params["access_credential"]
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

        return self.api_client.call_api(
            "/v2/credentials/{namespace}/{name}",
            "PATCH",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )
