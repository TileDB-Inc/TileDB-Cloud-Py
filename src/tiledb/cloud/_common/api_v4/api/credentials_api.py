# coding: utf-8

"""
    Specification file for tiledb-server v4 API

    This spec is exposed to the public under /v4 route group  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Contact: info@tiledb.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from tiledb.cloud._common.api_v4.api_client import ApiClient
from tiledb.cloud._common.api_v4.exceptions import ApiTypeError  # noqa: F401
from tiledb.cloud._common.api_v4.exceptions import ApiValueError  # noqa: F401


class CredentialsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_credential(self, credential_create_request, **kwargs):  # noqa: E501
        """Create a credential  # noqa: E501

        create a new credential, the user will create a new credential to access assets  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_credential(credential_create_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param CredentialCreateRequest credential_create_request: the new credentials to be created (required)
        :param str teamspace_id: Teamspace id should be empty, if the request is about an action on workspace level
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
        return self.create_credential_with_http_info(
            credential_create_request, **kwargs
        )  # noqa: E501

    def create_credential_with_http_info(
        self, credential_create_request, **kwargs
    ):  # noqa: E501
        """Create a credential  # noqa: E501

        create a new credential, the user will create a new credential to access assets  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_credential_with_http_info(credential_create_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param CredentialCreateRequest credential_create_request: the new credentials to be created (required)
        :param str teamspace_id: Teamspace id should be empty, if the request is about an action on workspace level
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

        all_params = ["credential_create_request", "teamspace_id"]
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
                    " to method create_credential" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'credential_create_request' is set
        if self.api_client.client_side_validation and (
            "credential_create_request" not in local_var_params
            or local_var_params["credential_create_request"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `credential_create_request` when calling `create_credential`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if (
            "teamspace_id" in local_var_params
            and local_var_params["teamspace_id"] is not None
        ):  # noqa: E501
            query_params.append(
                ("teamspace_id", local_var_params["teamspace_id"])
            )  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "credential_create_request" in local_var_params:
            body_params = local_var_params["credential_create_request"]
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
        auth_settings = ["ApiKeyAuth", "BasicAuth", "OAuth2"]  # noqa: E501

        return self.api_client.call_api(
            "/credentials",
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

    def delete_credential_by_name(self, name, **kwargs):  # noqa: E501
        """Delete user credential  # noqa: E501

        Delete the named access credential. Any arrays still set to use this credential will use the user's default and may become unreachable  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_credential_by_name(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: The name of the credentials to run CRUD operations against (required)
        :param str teamspace_id: Teamspace id should be empty, if the request is about an action on workspace level
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
        return self.delete_credential_by_name_with_http_info(
            name, **kwargs
        )  # noqa: E501

    def delete_credential_by_name_with_http_info(self, name, **kwargs):  # noqa: E501
        """Delete user credential  # noqa: E501

        Delete the named access credential. Any arrays still set to use this credential will use the user's default and may become unreachable  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_credential_by_name_with_http_info(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: The name of the credentials to run CRUD operations against (required)
        :param str teamspace_id: Teamspace id should be empty, if the request is about an action on workspace level
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

        all_params = ["name", "teamspace_id"]
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
                    " to method delete_credential_by_name" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and (
            "name" not in local_var_params
            or local_var_params["name"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `name` when calling `delete_credential_by_name`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "name" in local_var_params:
            path_params["name"] = local_var_params["name"]  # noqa: E501

        query_params = []
        if (
            "teamspace_id" in local_var_params
            and local_var_params["teamspace_id"] is not None
        ):  # noqa: E501
            query_params.append(
                ("teamspace_id", local_var_params["teamspace_id"])
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
        auth_settings = ["ApiKeyAuth", "BasicAuth", "OAuth2"]  # noqa: E501

        return self.api_client.call_api(
            "/credentials/{name}",
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

    def get_credential_by_name(self, name, **kwargs):  # noqa: E501
        """Get user credential  # noqa: E501

        get information about user credential by name  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_credential_by_name(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: The name of the credentials to run CRUD operations against (required)
        :param str teamspace_id: Teamspace id should be empty, if the request is about an action on workspace level
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: CredentialGetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.get_credential_by_name_with_http_info(name, **kwargs)  # noqa: E501

    def get_credential_by_name_with_http_info(self, name, **kwargs):  # noqa: E501
        """Get user credential  # noqa: E501

        get information about user credential by name  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_credential_by_name_with_http_info(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: The name of the credentials to run CRUD operations against (required)
        :param str teamspace_id: Teamspace id should be empty, if the request is about an action on workspace level
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(CredentialGetResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["name", "teamspace_id"]
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
                    " to method get_credential_by_name" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and (
            "name" not in local_var_params
            or local_var_params["name"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `name` when calling `get_credential_by_name`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "name" in local_var_params:
            path_params["name"] = local_var_params["name"]  # noqa: E501

        query_params = []
        if (
            "teamspace_id" in local_var_params
            and local_var_params["teamspace_id"] is not None
        ):  # noqa: E501
            query_params.append(
                ("teamspace_id", local_var_params["teamspace_id"])
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
        auth_settings = ["ApiKeyAuth", "BasicAuth", "OAuth2"]  # noqa: E501

        return self.api_client.call_api(
            "/credentials/{name}",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="CredentialGetResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def get_credentials(self, **kwargs):  # noqa: E501
        """Get user credentials  # noqa: E501

        list the credentials available for the user  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_credentials(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str teamspace_id: Teamspace id should be empty, if the request is about an action on workspace level
        :param CloudProvider provider: Show only the credentials from this provider. This should be one of the CloudProvider enum values.
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
        :return: CredentialsListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.get_credentials_with_http_info(**kwargs)  # noqa: E501

    def get_credentials_with_http_info(self, **kwargs):  # noqa: E501
        """Get user credentials  # noqa: E501

        list the credentials available for the user  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_credentials_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str teamspace_id: Teamspace id should be empty, if the request is about an action on workspace level
        :param CloudProvider provider: Show only the credentials from this provider. This should be one of the CloudProvider enum values.
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
        :return: tuple(CredentialsListResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["teamspace_id", "provider", "type", "page", "per_page"]
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
                    " to method get_credentials" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]

        collection_formats = {}

        path_params = {}

        query_params = []
        if (
            "teamspace_id" in local_var_params
            and local_var_params["teamspace_id"] is not None
        ):  # noqa: E501
            query_params.append(
                ("teamspace_id", local_var_params["teamspace_id"])
            )  # noqa: E501
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
        auth_settings = ["ApiKeyAuth", "BasicAuth", "OAuth2"]  # noqa: E501

        return self.api_client.call_api(
            "/credentials",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="CredentialsListResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def patch_credential_by_name(
        self, name, credential_update_request, **kwargs
    ):  # noqa: E501
        """Update user credential  # noqa: E501

        update user credential given by the user  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.patch_credential_by_name(name, credential_update_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: The name of the credentials to run CRUD operations against (required)
        :param CredentialUpdateRequest credential_update_request: credential update details (required)
        :param str teamspace_id: Teamspace id should be empty, if the request is about an action on workspace level
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
        return self.patch_credential_by_name_with_http_info(
            name, credential_update_request, **kwargs
        )  # noqa: E501

    def patch_credential_by_name_with_http_info(
        self, name, credential_update_request, **kwargs
    ):  # noqa: E501
        """Update user credential  # noqa: E501

        update user credential given by the user  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.patch_credential_by_name_with_http_info(name, credential_update_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: The name of the credentials to run CRUD operations against (required)
        :param CredentialUpdateRequest credential_update_request: credential update details (required)
        :param str teamspace_id: Teamspace id should be empty, if the request is about an action on workspace level
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

        all_params = ["name", "credential_update_request", "teamspace_id"]
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
                    " to method patch_credential_by_name" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and (
            "name" not in local_var_params
            or local_var_params["name"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `name` when calling `patch_credential_by_name`"
            )  # noqa: E501
        # verify the required parameter 'credential_update_request' is set
        if self.api_client.client_side_validation and (
            "credential_update_request" not in local_var_params
            or local_var_params["credential_update_request"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `credential_update_request` when calling `patch_credential_by_name`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "name" in local_var_params:
            path_params["name"] = local_var_params["name"]  # noqa: E501

        query_params = []
        if (
            "teamspace_id" in local_var_params
            and local_var_params["teamspace_id"] is not None
        ):  # noqa: E501
            query_params.append(
                ("teamspace_id", local_var_params["teamspace_id"])
            )  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "credential_update_request" in local_var_params:
            body_params = local_var_params["credential_update_request"]
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
        auth_settings = ["ApiKeyAuth", "BasicAuth", "OAuth2"]  # noqa: E501

        return self.api_client.call_api(
            "/credentials/{name}",
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

    def verify_credential(self, credentials_verify_request, **kwargs):  # noqa: E501
        """Verify a given credential  # noqa: E501

        verify the credentials connection for a namespace  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.verify_credential(credentials_verify_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param CredentialsVerifyRequest credentials_verify_request: credential to verify (required)
        :param str teamspace_id: Teamspace id should be empty, if the request is about an action on workspace level
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
        return self.verify_credential_with_http_info(
            credentials_verify_request, **kwargs
        )  # noqa: E501

    def verify_credential_with_http_info(
        self, credentials_verify_request, **kwargs
    ):  # noqa: E501
        """Verify a given credential  # noqa: E501

        verify the credentials connection for a namespace  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.verify_credential_with_http_info(credentials_verify_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param CredentialsVerifyRequest credentials_verify_request: credential to verify (required)
        :param str teamspace_id: Teamspace id should be empty, if the request is about an action on workspace level
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

        all_params = ["credentials_verify_request", "teamspace_id"]
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
                    " to method verify_credential" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'credentials_verify_request' is set
        if self.api_client.client_side_validation and (
            "credentials_verify_request" not in local_var_params
            or local_var_params["credentials_verify_request"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `credentials_verify_request` when calling `verify_credential`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if (
            "teamspace_id" in local_var_params
            and local_var_params["teamspace_id"] is not None
        ):  # noqa: E501
            query_params.append(
                ("teamspace_id", local_var_params["teamspace_id"])
            )  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "credentials_verify_request" in local_var_params:
            body_params = local_var_params["credentials_verify_request"]
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
        auth_settings = ["ApiKeyAuth", "BasicAuth", "OAuth2"]  # noqa: E501

        return self.api_client.call_api(
            "/credentials/verify",
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
