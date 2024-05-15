# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class SQLParameters(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        "name": "str",
        "query": "str",
        "output_uri": "str",
        "store_results": "bool",
        "dont_download_results": "bool",
        "resource_class": "str",
        "result_format": "ResultFormat",
        "init_commands": "list[str]",
        "parameters": "list[object]",
        "task_graph_uuid": "str",
        "client_node_uuid": "str",
    }

    attribute_map = {
        "name": "name",
        "query": "query",
        "output_uri": "output_uri",
        "store_results": "store_results",
        "dont_download_results": "dont_download_results",
        "resource_class": "resource_class",
        "result_format": "result_format",
        "init_commands": "init_commands",
        "parameters": "parameters",
        "task_graph_uuid": "task_graph_uuid",
        "client_node_uuid": "client_node_uuid",
    }

    def __init__(
        self,
        name=None,
        query=None,
        output_uri=None,
        store_results=None,
        dont_download_results=None,
        resource_class=None,
        result_format=None,
        init_commands=None,
        parameters=None,
        task_graph_uuid=None,
        client_node_uuid=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """SQLParameters - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._query = None
        self._output_uri = None
        self._store_results = None
        self._dont_download_results = None
        self._resource_class = None
        self._result_format = None
        self._init_commands = None
        self._parameters = None
        self._task_graph_uuid = None
        self._client_node_uuid = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if query is not None:
            self.query = query
        if output_uri is not None:
            self.output_uri = output_uri
        if store_results is not None:
            self.store_results = store_results
        if dont_download_results is not None:
            self.dont_download_results = dont_download_results
        if resource_class is not None:
            self.resource_class = resource_class
        if result_format is not None:
            self.result_format = result_format
        if init_commands is not None:
            self.init_commands = init_commands
        if parameters is not None:
            self.parameters = parameters
        if task_graph_uuid is not None:
            self.task_graph_uuid = task_graph_uuid
        if client_node_uuid is not None:
            self.client_node_uuid = client_node_uuid

    @property
    def name(self):
        """Gets the name of this SQLParameters.  # noqa: E501

        name of task, optional  # noqa: E501

        :return: The name of this SQLParameters.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SQLParameters.

        name of task, optional  # noqa: E501

        :param name: The name of this SQLParameters.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def query(self):
        """Gets the query of this SQLParameters.  # noqa: E501

        query to run  # noqa: E501

        :return: The query of this SQLParameters.  # noqa: E501
        :rtype: str
        """
        return self._query

    @query.setter
    def query(self, query):
        """Sets the query of this SQLParameters.

        query to run  # noqa: E501

        :param query: The query of this SQLParameters.  # noqa: E501
        :type: str
        """

        self._query = query

    @property
    def output_uri(self):
        """Gets the output_uri of this SQLParameters.  # noqa: E501

        Output array uri  # noqa: E501

        :return: The output_uri of this SQLParameters.  # noqa: E501
        :rtype: str
        """
        return self._output_uri

    @output_uri.setter
    def output_uri(self, output_uri):
        """Sets the output_uri of this SQLParameters.

        Output array uri  # noqa: E501

        :param output_uri: The output_uri of this SQLParameters.  # noqa: E501
        :type: str
        """

        self._output_uri = output_uri

    @property
    def store_results(self):
        """Gets the store_results of this SQLParameters.  # noqa: E501

        store results for later retrieval  # noqa: E501

        :return: The store_results of this SQLParameters.  # noqa: E501
        :rtype: bool
        """
        return self._store_results

    @store_results.setter
    def store_results(self, store_results):
        """Sets the store_results of this SQLParameters.

        store results for later retrieval  # noqa: E501

        :param store_results: The store_results of this SQLParameters.  # noqa: E501
        :type: bool
        """

        self._store_results = store_results

    @property
    def dont_download_results(self):
        """Gets the dont_download_results of this SQLParameters.  # noqa: E501

        Set to true to avoid downloading the results of this UDF. Useful for intermediate nodes in a task graph where you will not be using the results of your function. Defaults to false (\"yes download results\").  # noqa: E501

        :return: The dont_download_results of this SQLParameters.  # noqa: E501
        :rtype: bool
        """
        return self._dont_download_results

    @dont_download_results.setter
    def dont_download_results(self, dont_download_results):
        """Sets the dont_download_results of this SQLParameters.

        Set to true to avoid downloading the results of this UDF. Useful for intermediate nodes in a task graph where you will not be using the results of your function. Defaults to false (\"yes download results\").  # noqa: E501

        :param dont_download_results: The dont_download_results of this SQLParameters.  # noqa: E501
        :type: bool
        """

        self._dont_download_results = dont_download_results

    @property
    def resource_class(self):
        """Gets the resource_class of this SQLParameters.  # noqa: E501

        The resource class to use for the SQL execution. Resource classes define resource limits for memory and CPUs. If this is empty, then the SQL will execute in the standard resource class of the TileDB Cloud provider.   # noqa: E501

        :return: The resource_class of this SQLParameters.  # noqa: E501
        :rtype: str
        """
        return self._resource_class

    @resource_class.setter
    def resource_class(self, resource_class):
        """Sets the resource_class of this SQLParameters.

        The resource class to use for the SQL execution. Resource classes define resource limits for memory and CPUs. If this is empty, then the SQL will execute in the standard resource class of the TileDB Cloud provider.   # noqa: E501

        :param resource_class: The resource_class of this SQLParameters.  # noqa: E501
        :type: str
        """

        self._resource_class = resource_class

    @property
    def result_format(self):
        """Gets the result_format of this SQLParameters.  # noqa: E501


        :return: The result_format of this SQLParameters.  # noqa: E501
        :rtype: ResultFormat
        """
        return self._result_format

    @result_format.setter
    def result_format(self, result_format):
        """Sets the result_format of this SQLParameters.


        :param result_format: The result_format of this SQLParameters.  # noqa: E501
        :type: ResultFormat
        """

        self._result_format = result_format

    @property
    def init_commands(self):
        """Gets the init_commands of this SQLParameters.  # noqa: E501

        Queries or commands to run before main query  # noqa: E501

        :return: The init_commands of this SQLParameters.  # noqa: E501
        :rtype: list[str]
        """
        return self._init_commands

    @init_commands.setter
    def init_commands(self, init_commands):
        """Sets the init_commands of this SQLParameters.

        Queries or commands to run before main query  # noqa: E501

        :param init_commands: The init_commands of this SQLParameters.  # noqa: E501
        :type: list[str]
        """

        self._init_commands = init_commands

    @property
    def parameters(self):
        """Gets the parameters of this SQLParameters.  # noqa: E501

        SQL query parameters  # noqa: E501

        :return: The parameters of this SQLParameters.  # noqa: E501
        :rtype: list[object]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this SQLParameters.

        SQL query parameters  # noqa: E501

        :param parameters: The parameters of this SQLParameters.  # noqa: E501
        :type: list[object]
        """

        self._parameters = parameters

    @property
    def task_graph_uuid(self):
        """Gets the task_graph_uuid of this SQLParameters.  # noqa: E501

        If set, the ID of the log for the task graph that this was part of.   # noqa: E501

        :return: The task_graph_uuid of this SQLParameters.  # noqa: E501
        :rtype: str
        """
        return self._task_graph_uuid

    @task_graph_uuid.setter
    def task_graph_uuid(self, task_graph_uuid):
        """Sets the task_graph_uuid of this SQLParameters.

        If set, the ID of the log for the task graph that this was part of.   # noqa: E501

        :param task_graph_uuid: The task_graph_uuid of this SQLParameters.  # noqa: E501
        :type: str
        """

        self._task_graph_uuid = task_graph_uuid

    @property
    def client_node_uuid(self):
        """Gets the client_node_uuid of this SQLParameters.  # noqa: E501

        If set, the client-defined ID of the node within this task's graph.   # noqa: E501

        :return: The client_node_uuid of this SQLParameters.  # noqa: E501
        :rtype: str
        """
        return self._client_node_uuid

    @client_node_uuid.setter
    def client_node_uuid(self, client_node_uuid):
        """Sets the client_node_uuid of this SQLParameters.

        If set, the client-defined ID of the node within this task's graph.   # noqa: E501

        :param client_node_uuid: The client_node_uuid of this SQLParameters.  # noqa: E501
        :type: str
        """

        self._client_node_uuid = client_node_uuid

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SQLParameters):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SQLParameters):
            return True

        return self.to_dict() != other.to_dict()
