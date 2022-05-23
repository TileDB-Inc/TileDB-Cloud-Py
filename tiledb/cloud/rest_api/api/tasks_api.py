"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from tiledb.cloud.rest_api.api_client import ApiClient
from tiledb.cloud.rest_api.api_client import Endpoint as _Endpoint
from tiledb.cloud.rest_api.model.array_task import ArrayTask
from tiledb.cloud.rest_api.model.array_task_data import ArrayTaskData
from tiledb.cloud.rest_api.model.error import Error
from tiledb.cloud.rest_api.model.sql_parameters import SQLParameters
from tiledb.cloud.rest_api.model_utils import check_allowed_values  # noqa: F401
from tiledb.cloud.rest_api.model_utils import check_validations
from tiledb.cloud.rest_api.model_utils import date
from tiledb.cloud.rest_api.model_utils import datetime
from tiledb.cloud.rest_api.model_utils import file_type
from tiledb.cloud.rest_api.model_utils import none_type
from tiledb.cloud.rest_api.model_utils import validate_and_convert_types


class TasksApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.run_sql_endpoint = _Endpoint(
            settings={
                "response_type": (
                    [bool, date, datetime, dict, float, int, list, str, none_type],
                ),
                "auth": ["ApiKeyAuth", "BasicAuth"],
                "endpoint_path": "/sql/{namespace}",
                "operation_id": "run_sql",
                "http_method": "POST",
                "servers": None,
            },
            params_map={
                "all": [
                    "namespace",
                    "sql",
                    "accept_encoding",
                ],
                "required": [
                    "namespace",
                    "sql",
                ],
                "nullable": [],
                "enum": [],
                "validation": [],
            },
            root_map={
                "validations": {},
                "allowed_values": {},
                "openapi_types": {
                    "namespace": (str,),
                    "sql": (SQLParameters,),
                    "accept_encoding": (str,),
                },
                "attribute_map": {
                    "namespace": "namespace",
                    "accept_encoding": "Accept-Encoding",
                },
                "location_map": {
                    "namespace": "path",
                    "sql": "body",
                    "accept_encoding": "header",
                },
                "collection_format_map": {},
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": ["application/json"],
            },
            api_client=api_client,
        )
        self.task_id_get_endpoint = _Endpoint(
            settings={
                "response_type": (ArrayTask,),
                "auth": ["ApiKeyAuth", "BasicAuth"],
                "endpoint_path": "/task/{id}",
                "operation_id": "task_id_get",
                "http_method": "GET",
                "servers": None,
            },
            params_map={
                "all": [
                    "id",
                ],
                "required": [
                    "id",
                ],
                "nullable": [],
                "enum": [],
                "validation": [],
            },
            root_map={
                "validations": {},
                "allowed_values": {},
                "openapi_types": {
                    "id": (str,),
                },
                "attribute_map": {
                    "id": "id",
                },
                "location_map": {
                    "id": "path",
                },
                "collection_format_map": {},
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )
        self.task_id_result_get_endpoint = _Endpoint(
            settings={
                "response_type": (str,),
                "auth": ["ApiKeyAuth", "BasicAuth"],
                "endpoint_path": "/task/{id}/result",
                "operation_id": "task_id_result_get",
                "http_method": "GET",
                "servers": None,
            },
            params_map={
                "all": [
                    "id",
                    "accept_encoding",
                ],
                "required": [
                    "id",
                ],
                "nullable": [],
                "enum": [],
                "validation": [],
            },
            root_map={
                "validations": {},
                "allowed_values": {},
                "openapi_types": {
                    "id": (str,),
                    "accept_encoding": (str,),
                },
                "attribute_map": {
                    "id": "id",
                    "accept_encoding": "Accept-Encoding",
                },
                "location_map": {
                    "id": "path",
                    "accept_encoding": "header",
                },
                "collection_format_map": {},
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )
        self.tasks_get_endpoint = _Endpoint(
            settings={
                "response_type": (ArrayTaskData,),
                "auth": ["ApiKeyAuth", "BasicAuth"],
                "endpoint_path": "/tasks",
                "operation_id": "tasks_get",
                "http_method": "GET",
                "servers": None,
            },
            params_map={
                "all": [
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
                ],
                "required": [],
                "nullable": [],
                "enum": [],
                "validation": [],
            },
            root_map={
                "validations": {},
                "allowed_values": {},
                "openapi_types": {
                    "namespace": (str,),
                    "created_by": (str,),
                    "array": (str,),
                    "start": (int,),
                    "end": (int,),
                    "page": (int,),
                    "per_page": (int,),
                    "type": (str,),
                    "exclude_type": ([str],),
                    "file_type": ([str],),
                    "exclude_file_type": ([str],),
                    "status": (str,),
                    "search": (str,),
                    "orderby": (str,),
                },
                "attribute_map": {
                    "namespace": "namespace",
                    "created_by": "created_by",
                    "array": "array",
                    "start": "start",
                    "end": "end",
                    "page": "page",
                    "per_page": "per_page",
                    "type": "type",
                    "exclude_type": "exclude_type",
                    "file_type": "file_type",
                    "exclude_file_type": "exclude_file_type",
                    "status": "status",
                    "search": "search",
                    "orderby": "orderby",
                },
                "location_map": {
                    "namespace": "query",
                    "created_by": "query",
                    "array": "query",
                    "start": "query",
                    "end": "query",
                    "page": "query",
                    "per_page": "query",
                    "type": "query",
                    "exclude_type": "query",
                    "file_type": "query",
                    "exclude_file_type": "query",
                    "status": "query",
                    "search": "query",
                    "orderby": "query",
                },
                "collection_format_map": {
                    "exclude_type": "csv",
                    "file_type": "multi",
                    "exclude_file_type": "multi",
                },
            },
            headers_map={
                "accept": ["application/json"],
                "content_type": [],
            },
            api_client=api_client,
        )

    def run_sql(self, namespace, sql, **kwargs):
        """run_sql  # noqa: E501

        Run a sql query  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.run_sql(namespace, sql, async_req=True)
        >>> result = thread.get()

        Args:
            namespace (str): namespace to run task under is in (an organization name or user's username)
            sql (SQLParameters): sql being submitted

        Keyword Args:
            accept_encoding (str): Encoding to use. [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            [bool, date, datetime, dict, float, int, list, str, none_type]
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs["async_req"] = kwargs.get("async_req", False)
        kwargs["_return_http_data_only"] = kwargs.get("_return_http_data_only", True)
        kwargs["_preload_content"] = kwargs.get("_preload_content", True)
        kwargs["_request_timeout"] = kwargs.get("_request_timeout", None)
        kwargs["_check_input_type"] = kwargs.get("_check_input_type", True)
        kwargs["_check_return_type"] = kwargs.get("_check_return_type", True)
        kwargs["_host_index"] = kwargs.get("_host_index")
        kwargs["namespace"] = namespace
        kwargs["sql"] = sql
        return self.run_sql_endpoint.call_with_http_info(**kwargs)

    def task_id_get(self, id, **kwargs):
        """task_id_get  # noqa: E501

        Fetch an array task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.task_id_get(id, async_req=True)
        >>> result = thread.get()

        Args:
            id (str): task ID to fetch

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            ArrayTask
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs["async_req"] = kwargs.get("async_req", False)
        kwargs["_return_http_data_only"] = kwargs.get("_return_http_data_only", True)
        kwargs["_preload_content"] = kwargs.get("_preload_content", True)
        kwargs["_request_timeout"] = kwargs.get("_request_timeout", None)
        kwargs["_check_input_type"] = kwargs.get("_check_input_type", True)
        kwargs["_check_return_type"] = kwargs.get("_check_return_type", True)
        kwargs["_host_index"] = kwargs.get("_host_index")
        kwargs["id"] = id
        return self.task_id_get_endpoint.call_with_http_info(**kwargs)

    def task_id_result_get(self, id, **kwargs):
        """task_id_result_get  # noqa: E501

        Retrieve results of an array task  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.task_id_result_get(id, async_req=True)
        >>> result = thread.get()

        Args:
            id (str): task ID to retrieve stored results

        Keyword Args:
            accept_encoding (str): Encoding to use. [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            str
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs["async_req"] = kwargs.get("async_req", False)
        kwargs["_return_http_data_only"] = kwargs.get("_return_http_data_only", True)
        kwargs["_preload_content"] = kwargs.get("_preload_content", True)
        kwargs["_request_timeout"] = kwargs.get("_request_timeout", None)
        kwargs["_check_input_type"] = kwargs.get("_check_input_type", True)
        kwargs["_check_return_type"] = kwargs.get("_check_return_type", True)
        kwargs["_host_index"] = kwargs.get("_host_index")
        kwargs["id"] = id
        return self.task_id_result_get_endpoint.call_with_http_info(**kwargs)

    def tasks_get(self, **kwargs):
        """tasks_get  # noqa: E501

        Fetch a list of all array tasks a user has access to  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.tasks_get(async_req=True)
        >>> result = thread.get()


        Keyword Args:
            namespace (str): namespace to filter. [optional]
            created_by (str): username to filter. [optional]
            array (str): name/uri of array that is url-encoded to filter. [optional]
            start (int): start time for tasks to filter by. [optional]
            end (int): end time for tasks to filter by. [optional]
            page (int): pagination offset. [optional]
            per_page (int): pagination limit. [optional]
            type (str): task type, \"QUERY\", \"SQL\", \"UDF\", \"GENERIC_UDF\". [optional]
            exclude_type ([str]): task_type to exclude matching array in results, more than one can be included. [optional]
            file_type ([str]): match file_type of task array, more than one can be included. [optional]
            exclude_file_type ([str]): exclude file_type of task arrays, more than one can be included. [optional]
            status (str): Filter to only return these statuses. [optional]
            search (str): search string that will look at name, namespace or description fields. [optional]
            orderby (str): sort by which field valid values include start_time, name. [optional]
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            ArrayTaskData
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs["async_req"] = kwargs.get("async_req", False)
        kwargs["_return_http_data_only"] = kwargs.get("_return_http_data_only", True)
        kwargs["_preload_content"] = kwargs.get("_preload_content", True)
        kwargs["_request_timeout"] = kwargs.get("_request_timeout", None)
        kwargs["_check_input_type"] = kwargs.get("_check_input_type", True)
        kwargs["_check_return_type"] = kwargs.get("_check_return_type", True)
        kwargs["_host_index"] = kwargs.get("_host_index")
        return self.tasks_get_endpoint.call_with_http_info(**kwargs)
