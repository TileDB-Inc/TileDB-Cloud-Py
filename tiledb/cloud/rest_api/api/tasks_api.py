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


class TasksApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def run_sql(self, namespace, sql, **kwargs):  # noqa: E501
        """run_sql  # noqa: E501

        Run a sql query  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_sql(namespace, sql, async_req=True)
        >>> result = thread.get()

        :param namespace: namespace to run task under is in (an organization name or user's username) (required)
        :type namespace: str
        :param sql: sql being submitted (required)
        :type sql: SQLParameters
        :param accept_encoding: Encoding to use
        :type accept_encoding: str
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
        :rtype: list[object]
        """
        kwargs["_return_http_data_only"] = True
        return self.run_sql_with_http_info(namespace, sql, **kwargs)  # noqa: E501

    def run_sql_with_http_info(self, namespace, sql, **kwargs):  # noqa: E501
        """run_sql  # noqa: E501

        Run a sql query  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_sql_with_http_info(namespace, sql, async_req=True)
        >>> result = thread.get()

        :param namespace: namespace to run task under is in (an organization name or user's username) (required)
        :type namespace: str
        :param sql: sql being submitted (required)
        :type sql: SQLParameters
        :param accept_encoding: Encoding to use
        :type accept_encoding: str
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
        :rtype: tuple(list[object], status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = ["namespace", "sql", "accept_encoding"]
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
                    "Got an unexpected keyword argument '%s'" " to method run_sql" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `run_sql`"
            )  # noqa: E501
        # verify the required parameter 'sql' is set
        if self.api_client.client_side_validation and (
            "sql" not in local_var_params
            or local_var_params["sql"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `sql` when calling `run_sql`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "namespace" in local_var_params:
            path_params["namespace"] = local_var_params["namespace"]  # noqa: E501

        query_params = []

        header_params = {}
        if "accept_encoding" in local_var_params:
            header_params["Accept-Encoding"] = local_var_params[
                "accept_encoding"
            ]  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if "sql" in local_var_params:
            body_params = local_var_params["sql"]
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
            200: "list[object]",
            204: None,
        }

        return self.api_client.call_api(
            "/sql/{namespace}",
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

    def task_id_get(self, id, **kwargs):  # noqa: E501
        """task_id_get  # noqa: E501

        Fetch an array task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.task_id_get(id, async_req=True)
        >>> result = thread.get()

        :param id: task ID to fetch (required)
        :type id: str
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
        :rtype: ArrayTask
        """
        kwargs["_return_http_data_only"] = True
        return self.task_id_get_with_http_info(id, **kwargs)  # noqa: E501

    def task_id_get_with_http_info(self, id, **kwargs):  # noqa: E501
        """task_id_get  # noqa: E501

        Fetch an array task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.task_id_get_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: task ID to fetch (required)
        :type id: str
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
        :rtype: tuple(ArrayTask, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = ["id"]
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
                    " to method task_id_get" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'id' is set
        if self.api_client.client_side_validation and (
            "id" not in local_var_params or local_var_params["id"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `id` when calling `task_id_get`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "id" in local_var_params:
            path_params["id"] = local_var_params["id"]  # noqa: E501

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
            200: "ArrayTask",
        }

        return self.api_client.call_api(
            "/task/{id}",
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

    def task_id_result_get(self, id, **kwargs):  # noqa: E501
        """task_id_result_get  # noqa: E501

        Retrieve results of an array task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.task_id_result_get(id, async_req=True)
        >>> result = thread.get()

        :param id: task ID to retrieve stored results (required)
        :type id: str
        :param accept_encoding: Encoding to use
        :type accept_encoding: str
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
        :rtype: str
        """
        kwargs["_return_http_data_only"] = True
        return self.task_id_result_get_with_http_info(id, **kwargs)  # noqa: E501

    def task_id_result_get_with_http_info(self, id, **kwargs):  # noqa: E501
        """task_id_result_get  # noqa: E501

        Retrieve results of an array task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.task_id_result_get_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param id: task ID to retrieve stored results (required)
        :type id: str
        :param accept_encoding: Encoding to use
        :type accept_encoding: str
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
        :rtype: tuple(str, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = ["id", "accept_encoding"]
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
                    " to method task_id_result_get" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'id' is set
        if self.api_client.client_side_validation and (
            "id" not in local_var_params or local_var_params["id"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `id` when calling `task_id_result_get`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "id" in local_var_params:
            path_params["id"] = local_var_params["id"]  # noqa: E501

        query_params = []

        header_params = {}
        if "accept_encoding" in local_var_params:
            header_params["Accept-Encoding"] = local_var_params[
                "accept_encoding"
            ]  # noqa: E501

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
            200: "str",
            202: None,
            404: "Error",
        }

        return self.api_client.call_api(
            "/task/{id}/result",
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

    def tasks_get(self, **kwargs):  # noqa: E501
        """tasks_get  # noqa: E501

        Fetch a list of all array tasks a user has access to  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tasks_get(async_req=True)
        >>> result = thread.get()

        :param namespace: namespace to filter
        :type namespace: str
        :param created_by: username to filter
        :type created_by: str
        :param array: name/uri of array that is url-encoded to filter
        :type array: str
        :param start: start time for tasks to filter by
        :type start: int
        :param end: end time for tasks to filter by
        :type end: int
        :param page: pagination offset
        :type page: int
        :param per_page: pagination limit
        :type per_page: int
        :param type: task type, \"QUERY\", \"SQL\", \"UDF\", \"GENERIC_UDF\"
        :type type: str
        :param exclude_type: task_type to exclude matching array in results, more than one can be included
        :type exclude_type: list[str]
        :param file_type: match file_type of task array, more than one can be included
        :type file_type: list[str]
        :param exclude_file_type: exclude file_type of task arrays, more than one can be included
        :type exclude_file_type: list[str]
        :param status: Filter to only return these statuses
        :type status: str
        :param search: search string that will look at name, namespace or description fields
        :type search: str
        :param orderby: sort by which field valid values include start_time, name
        :type orderby: str
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
        :rtype: ArrayTaskData
        """
        kwargs["_return_http_data_only"] = True
        return self.tasks_get_with_http_info(**kwargs)  # noqa: E501

    def tasks_get_with_http_info(self, **kwargs):  # noqa: E501
        """tasks_get  # noqa: E501

        Fetch a list of all array tasks a user has access to  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tasks_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param namespace: namespace to filter
        :type namespace: str
        :param created_by: username to filter
        :type created_by: str
        :param array: name/uri of array that is url-encoded to filter
        :type array: str
        :param start: start time for tasks to filter by
        :type start: int
        :param end: end time for tasks to filter by
        :type end: int
        :param page: pagination offset
        :type page: int
        :param per_page: pagination limit
        :type per_page: int
        :param type: task type, \"QUERY\", \"SQL\", \"UDF\", \"GENERIC_UDF\"
        :type type: str
        :param exclude_type: task_type to exclude matching array in results, more than one can be included
        :type exclude_type: list[str]
        :param file_type: match file_type of task array, more than one can be included
        :type file_type: list[str]
        :param exclude_file_type: exclude file_type of task arrays, more than one can be included
        :type exclude_file_type: list[str]
        :param status: Filter to only return these statuses
        :type status: str
        :param search: search string that will look at name, namespace or description fields
        :type search: str
        :param orderby: sort by which field valid values include start_time, name
        :type orderby: str
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
        :rtype: tuple(ArrayTaskData, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            "namespace",
            "created_by",
            "array",
            "start",
            "end",
            "page",
            "per_page",
            "type",
            "exclude_type",
            "file_type",
            "exclude_file_type",
            "status",
            "search",
            "orderby",
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
                    " to method tasks_get" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]

        collection_formats = {}

        path_params = {}

        query_params = []
        if (
            "namespace" in local_var_params
            and local_var_params["namespace"] is not None
        ):  # noqa: E501
            query_params.append(
                ("namespace", local_var_params["namespace"])
            )  # noqa: E501
        if (
            "created_by" in local_var_params
            and local_var_params["created_by"] is not None
        ):  # noqa: E501
            query_params.append(
                ("created_by", local_var_params["created_by"])
            )  # noqa: E501
        if (
            "array" in local_var_params and local_var_params["array"] is not None
        ):  # noqa: E501
            query_params.append(("array", local_var_params["array"]))  # noqa: E501
        if (
            "start" in local_var_params and local_var_params["start"] is not None
        ):  # noqa: E501
            query_params.append(("start", local_var_params["start"]))  # noqa: E501
        if (
            "end" in local_var_params and local_var_params["end"] is not None
        ):  # noqa: E501
            query_params.append(("end", local_var_params["end"]))  # noqa: E501
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
        if (
            "type" in local_var_params and local_var_params["type"] is not None
        ):  # noqa: E501
            query_params.append(("type", local_var_params["type"]))  # noqa: E501
        if (
            "exclude_type" in local_var_params
            and local_var_params["exclude_type"] is not None
        ):  # noqa: E501
            query_params.append(
                ("exclude_type", local_var_params["exclude_type"])
            )  # noqa: E501
            collection_formats["exclude_type"] = "csv"  # noqa: E501
        if (
            "file_type" in local_var_params
            and local_var_params["file_type"] is not None
        ):  # noqa: E501
            query_params.append(
                ("file_type", local_var_params["file_type"])
            )  # noqa: E501
            collection_formats["file_type"] = "multi"  # noqa: E501
        if (
            "exclude_file_type" in local_var_params
            and local_var_params["exclude_file_type"] is not None
        ):  # noqa: E501
            query_params.append(
                ("exclude_file_type", local_var_params["exclude_file_type"])
            )  # noqa: E501
            collection_formats["exclude_file_type"] = "multi"  # noqa: E501
        if (
            "status" in local_var_params and local_var_params["status"] is not None
        ):  # noqa: E501
            query_params.append(("status", local_var_params["status"]))  # noqa: E501
        if (
            "search" in local_var_params and local_var_params["search"] is not None
        ):  # noqa: E501
            query_params.append(("search", local_var_params["search"]))  # noqa: E501
        if (
            "orderby" in local_var_params and local_var_params["orderby"] is not None
        ):  # noqa: E501
            query_params.append(("orderby", local_var_params["orderby"]))  # noqa: E501

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
            200: "ArrayTaskData",
        }

        return self.api_client.call_api(
            "/tasks",
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
