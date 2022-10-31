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


class ArrayTasksApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_array_tasks_sidebar(self, **kwargs):  # noqa: E501
        """get_array_tasks_sidebar  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_array_tasks_sidebar(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int start: Fetch tasks created after this time, unix epoch in seconds, default 7 days ago
        :param int end: Fetch tasks created before this time, unix epoch in seconds, default now
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ArrayTaskBrowserSidebar
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.get_array_tasks_sidebar_with_http_info(**kwargs)  # noqa: E501

    def get_array_tasks_sidebar_with_http_info(self, **kwargs):  # noqa: E501
        """get_array_tasks_sidebar  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_array_tasks_sidebar_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int start: Fetch tasks created after this time, unix epoch in seconds, default 7 days ago
        :param int end: Fetch tasks created before this time, unix epoch in seconds, default now
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ArrayTaskBrowserSidebar, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["start", "end"]
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
                    " to method get_array_tasks_sidebar" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]

        collection_formats = {}

        path_params = {}

        query_params = []
        if (
            "start" in local_var_params and local_var_params["start"] is not None
        ):  # noqa: E501
            query_params.append(("start", local_var_params["start"]))  # noqa: E501
        if (
            "end" in local_var_params and local_var_params["end"] is not None
        ):  # noqa: E501
            query_params.append(("end", local_var_params["end"]))  # noqa: E501

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
            "/v1/tasks/sidebar",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="ArrayTaskBrowserSidebar",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )
