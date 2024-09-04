# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

# python 2 and python 3 compatibility library
import six

from tiledb.cloud.rest_api.api_client import ApiClient
from tiledb.cloud.rest_api.exceptions import ApiTypeError
from tiledb.cloud.rest_api.exceptions import ApiValueError


class RegisteredTaskGraphsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def delete_registered_task_graph(self, namespace, name, **kwargs):  # noqa: E501
        """delete_registered_task_graph  # noqa: E501

        Delete the given registered task graph.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_registered_task_graph(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace that owns this registered UDF. (required)
        :param str name: The name of the registered task graph. (required)
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
        return self.delete_registered_task_graph_with_http_info(
            namespace, name, **kwargs
        )  # noqa: E501

    def delete_registered_task_graph_with_http_info(
        self, namespace, name, **kwargs
    ):  # noqa: E501
        """delete_registered_task_graph  # noqa: E501

        Delete the given registered task graph.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_registered_task_graph_with_http_info(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace that owns this registered UDF. (required)
        :param str name: The name of the registered task graph. (required)
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
                    " to method delete_registered_task_graph" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `delete_registered_task_graph`"
            )  # noqa: E501
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and (
            "name" not in local_var_params
            or local_var_params["name"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `name` when calling `delete_registered_task_graph`"
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
            "/v1/taskgraphs/{namespace}/registered/{name}",
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

    def get_registered_task_graph(self, namespace, name, **kwargs):  # noqa: E501
        """get_registered_task_graph  # noqa: E501

        Fetch the contents of this registered task graph.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_registered_task_graph(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace that owns this registered UDF. (required)
        :param str name: The name of the registered task graph. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: RegisteredTaskGraph
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.get_registered_task_graph_with_http_info(
            namespace, name, **kwargs
        )  # noqa: E501

    def get_registered_task_graph_with_http_info(
        self, namespace, name, **kwargs
    ):  # noqa: E501
        """get_registered_task_graph  # noqa: E501

        Fetch the contents of this registered task graph.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_registered_task_graph_with_http_info(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace that owns this registered UDF. (required)
        :param str name: The name of the registered task graph. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(RegisteredTaskGraph, status_code(int), headers(HTTPHeaderDict))
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
                    " to method get_registered_task_graph" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `get_registered_task_graph`"
            )  # noqa: E501
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and (
            "name" not in local_var_params
            or local_var_params["name"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `name` when calling `get_registered_task_graph`"
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
            "/v1/taskgraphs/{namespace}/registered/{name}",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="RegisteredTaskGraph",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def get_registered_task_graph_sharing_policies(
        self, namespace, name, **kwargs
    ):  # noqa: E501
        """get_registered_task_graph_sharing_policies  # noqa: E501

        Get sharing policies for the task graph.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_registered_task_graph_sharing_policies(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace that owns the registered task graph. (required)
        :param str name: The name of the task graph. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[TaskGraphSharing]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.get_registered_task_graph_sharing_policies_with_http_info(
            namespace, name, **kwargs
        )  # noqa: E501

    def get_registered_task_graph_sharing_policies_with_http_info(
        self, namespace, name, **kwargs
    ):  # noqa: E501
        """get_registered_task_graph_sharing_policies  # noqa: E501

        Get sharing policies for the task graph.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_registered_task_graph_sharing_policies_with_http_info(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace that owns the registered task graph. (required)
        :param str name: The name of the task graph. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[TaskGraphSharing], status_code(int), headers(HTTPHeaderDict))
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
                    " to method get_registered_task_graph_sharing_policies" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `get_registered_task_graph_sharing_policies`"
            )  # noqa: E501
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and (
            "name" not in local_var_params
            or local_var_params["name"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `name` when calling `get_registered_task_graph_sharing_policies`"
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
            "/v1/taskgraphs/{namespace}/registered/{name}/share",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="list[TaskGraphSharing]",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get(
                "_return_http_data_only"
            ),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def register_registered_task_graph(self, namespace, name, **kwargs):  # noqa: E501
        """register_registered_task_graph  # noqa: E501

        Register a task graph in the given namespace, with the given name.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.register_registered_task_graph(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace that owns this registered UDF. (required)
        :param str name: The name of the registered task graph. (required)
        :param RegisteredTaskGraph graph: Task graph to register.
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
        return self.register_registered_task_graph_with_http_info(
            namespace, name, **kwargs
        )  # noqa: E501

    def register_registered_task_graph_with_http_info(
        self, namespace, name, **kwargs
    ):  # noqa: E501
        """register_registered_task_graph  # noqa: E501

        Register a task graph in the given namespace, with the given name.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.register_registered_task_graph_with_http_info(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace that owns this registered UDF. (required)
        :param str name: The name of the registered task graph. (required)
        :param RegisteredTaskGraph graph: Task graph to register.
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

        all_params = ["namespace", "name", "graph"]
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
                    " to method register_registered_task_graph" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `register_registered_task_graph`"
            )  # noqa: E501
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and (
            "name" not in local_var_params
            or local_var_params["name"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `name` when calling `register_registered_task_graph`"
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
        if "graph" in local_var_params:
            body_params = local_var_params["graph"]
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
            "/v1/taskgraphs/{namespace}/registered/{name}",
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

    def share_registered_task_graph(
        self, namespace, name, task_graph_sharing, **kwargs
    ):  # noqa: E501
        """share_registered_task_graph  # noqa: E501

        Share a task graph.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.share_registered_task_graph(namespace, name, task_graph_sharing, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace that owns the registered task graph. (required)
        :param str name: The name of the task graph. (required)
        :param TaskGraphSharing task_graph_sharing: Namespace and list of permissions to share with. An empty list of permissions will remove the namespace; if permissions already exist they will be deleted then new ones added. In the event of a failure, the new policies will be rolled back to prevent partial policies, and it's likely the UDF will not be shared with the namespace at all.  (required)
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
        return self.share_registered_task_graph_with_http_info(
            namespace, name, task_graph_sharing, **kwargs
        )  # noqa: E501

    def share_registered_task_graph_with_http_info(
        self, namespace, name, task_graph_sharing, **kwargs
    ):  # noqa: E501
        """share_registered_task_graph  # noqa: E501

        Share a task graph.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.share_registered_task_graph_with_http_info(namespace, name, task_graph_sharing, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace that owns the registered task graph. (required)
        :param str name: The name of the task graph. (required)
        :param TaskGraphSharing task_graph_sharing: Namespace and list of permissions to share with. An empty list of permissions will remove the namespace; if permissions already exist they will be deleted then new ones added. In the event of a failure, the new policies will be rolled back to prevent partial policies, and it's likely the UDF will not be shared with the namespace at all.  (required)
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

        all_params = ["namespace", "name", "task_graph_sharing"]
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
                    " to method share_registered_task_graph" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `share_registered_task_graph`"
            )  # noqa: E501
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and (
            "name" not in local_var_params
            or local_var_params["name"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `name` when calling `share_registered_task_graph`"
            )  # noqa: E501
        # verify the required parameter 'task_graph_sharing' is set
        if self.api_client.client_side_validation and (
            "task_graph_sharing" not in local_var_params
            or local_var_params["task_graph_sharing"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `task_graph_sharing` when calling `share_registered_task_graph`"
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
        if "task_graph_sharing" in local_var_params:
            body_params = local_var_params["task_graph_sharing"]
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
            "/v1/taskgraphs/{namespace}/registered/{name}/share",
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

    def update_registered_task_graph(self, namespace, name, **kwargs):  # noqa: E501
        """update_registered_task_graph  # noqa: E501

        Update the contents of an existing registered task graph.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_registered_task_graph(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace that owns this registered UDF. (required)
        :param str name: The name of the registered task graph. (required)
        :param RegisteredTaskGraph graph: The new contents of the task graph.
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
        return self.update_registered_task_graph_with_http_info(
            namespace, name, **kwargs
        )  # noqa: E501

    def update_registered_task_graph_with_http_info(
        self, namespace, name, **kwargs
    ):  # noqa: E501
        """update_registered_task_graph  # noqa: E501

        Update the contents of an existing registered task graph.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_registered_task_graph_with_http_info(namespace, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str namespace: The namespace that owns this registered UDF. (required)
        :param str name: The name of the registered task graph. (required)
        :param RegisteredTaskGraph graph: The new contents of the task graph.
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

        all_params = ["namespace", "name", "graph"]
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
                    " to method update_registered_task_graph" % key
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'namespace' is set
        if self.api_client.client_side_validation and (
            "namespace" not in local_var_params
            or local_var_params["namespace"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `namespace` when calling `update_registered_task_graph`"
            )  # noqa: E501
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and (
            "name" not in local_var_params
            or local_var_params["name"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError(
                "Missing the required parameter `name` when calling `update_registered_task_graph`"
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
        if "graph" in local_var_params:
            body_params = local_var_params["graph"]
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
            "/v1/taskgraphs/{namespace}/registered/{name}",
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
