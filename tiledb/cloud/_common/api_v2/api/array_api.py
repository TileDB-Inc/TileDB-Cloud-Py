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
from tiledb.cloud._common.api_v2.exceptions import ApiValueError


class ArrayApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def array_activity_log(self, namespace, array, **kwargs):  # noqa: E501
        """array_activity_log  # noqa: E501

        get array activity logs  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.array_activity_log(namespace, array, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace array is in (an organization name or user's username) (required)
        :param str array: name/uri of array that is url-encoded (required)
        :param int start: Start time of window of fetch logs, unix epoch in seconds (default: seven days ago)
        :param int end: End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp)
        :param list[str] event_types: Event values can be one or more of the following read, write, create, delete, register, deregister, comma separated
        :param str task_id: Array task id To filter activity to
        :param bool has_task_id: Excludes activity log results that does not contain an array task uuid
        :param int page: pagination offset
        :param int per_page: pagination limit
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ArrayActivityLogData
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.array_activity_log_with_http_info(
            namespace, array, **kwargs
        )  # noqa: E501

    def array_activity_log_with_http_info(
        self, namespace, array, **kwargs
    ):  # noqa: E501
        """array_activity_log  # noqa: E501

        get array activity logs  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.array_activity_log_with_http_info(namespace, array, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: namespace array is in (an organization name or user's username) (required)
        :param str array: name/uri of array that is url-encoded (required)
        :param int start: Start time of window of fetch logs, unix epoch in seconds (default: seven days ago)
        :param int end: End time of window of fetch logs, unix epoch in seconds (default: current utc timestamp)
        :param list[str] event_types: Event values can be one or more of the following read, write, create, delete, register, deregister, comma separated
        :param str task_id: Array task id To filter activity to
        :param bool has_task_id: Excludes activity log results that does not contain an array task uuid
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
        :return: tuple(ArrayActivityLogData, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            "namespace",
            "array",
            "start",
            "end",
            "event_types",
            "task_id",
            "has_task_id",
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
                    " to method array_activity_log" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `array_activity_log`"
            )  # noqa: E501
        # verify the required parameter 'array' is set
        if self.api_client.client_side_validation and (
            "array" not in local_var_params
            or local_var_params["array"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `array` when calling `array_activity_log`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]  # noqa: E501
        if "array" in local_var_params:
            path_params["array"] = local_var_params["array"]  # noqa: E501

        query_params = []
        if (
            "start" in local_var_params and local_var_params["start"] is not None
        ):  # noqa: E501
            query_params.append(("start", local_var_params["start"]))  # noqa: E501
        if (
            "end" in local_var_params and local_var_params["end"] is not None
        ):  # noqa: E501
            query_params.append(("end", local_var_params["end"]))  # noqa: E501
        if (
            "event_types" in local_var_params
            and local_var_params["event_types"] is not None
        ):  # noqa: E501
            query_params.append(
                ("event_types", local_var_params["event_types"])
            )  # noqa: E501
            collection_formats["event_types"] = "multi"  # noqa: E501
        if (
            "task_id" in local_var_params and local_var_params["task_id"] is not None
        ):  # noqa: E501
            query_params.append(("task_id", local_var_params["task_id"]))  # noqa: E501
        if (
            "has_task_id" in local_var_params
            and local_var_params["has_task_id"] is not None
        ):  # noqa: E501
            query_params.append(
                ("has_task_id", local_var_params["has_task_id"])
            )  # noqa: E501
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
            "/v2/arrays/{namespace}/{array}/activity",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="ArrayActivityLogData",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )
