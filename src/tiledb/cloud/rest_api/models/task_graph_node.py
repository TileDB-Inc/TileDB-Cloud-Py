# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class TaskGraphNode(object):
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
        "client_node_id": "str",
        "name": "str",
        "depends_on": "list[str]",
        "array_node": "UDFArrayDetails",
        "input_node": "TGInputNodeData",
        "sql_node": "TGSQLNodeData",
        "udf_node": "TGUDFNodeData",
    }

    attribute_map = {
        "client_node_id": "client_node_id",
        "name": "name",
        "depends_on": "depends_on",
        "array_node": "array_node",
        "input_node": "input_node",
        "sql_node": "sql_node",
        "udf_node": "udf_node",
    }

    def __init__(
        self,
        client_node_id=None,
        name=None,
        depends_on=None,
        array_node=None,
        input_node=None,
        sql_node=None,
        udf_node=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """TaskGraphNode - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._client_node_id = None
        self._name = None
        self._depends_on = None
        self._array_node = None
        self._input_node = None
        self._sql_node = None
        self._udf_node = None
        self.discriminator = None

        if client_node_id is not None:
            self.client_node_id = client_node_id
        self.name = name
        if depends_on is not None:
            self.depends_on = depends_on
        if array_node is not None:
            self.array_node = array_node
        self.input_node = input_node
        self.sql_node = sql_node
        self.udf_node = udf_node

    @property
    def client_node_id(self):
        """Gets the client_node_id of this TaskGraphNode.  # noqa: E501

        The client-generated UUID of the given graph node.  # noqa: E501

        :return: The client_node_id of this TaskGraphNode.  # noqa: E501
        :rtype: str
        """
        return self._client_node_id

    @client_node_id.setter
    def client_node_id(self, client_node_id):
        """Sets the client_node_id of this TaskGraphNode.

        The client-generated UUID of the given graph node.  # noqa: E501

        :param client_node_id: The client_node_id of this TaskGraphNode.  # noqa: E501
        :type: str
        """

        self._client_node_id = client_node_id

    @property
    def name(self):
        """Gets the name of this TaskGraphNode.  # noqa: E501

        A client-specified name for the node. If provided, this must be unique.   # noqa: E501

        :return: The name of this TaskGraphNode.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TaskGraphNode.

        A client-specified name for the node. If provided, this must be unique.   # noqa: E501

        :param name: The name of this TaskGraphNode.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def depends_on(self):
        """Gets the depends_on of this TaskGraphNode.  # noqa: E501

        The client_node_uuid of each node that this node depends upon. Used to define the structure of the graph.   # noqa: E501

        :return: The depends_on of this TaskGraphNode.  # noqa: E501
        :rtype: list[str]
        """
        return self._depends_on

    @depends_on.setter
    def depends_on(self, depends_on):
        """Sets the depends_on of this TaskGraphNode.

        The client_node_uuid of each node that this node depends upon. Used to define the structure of the graph.   # noqa: E501

        :param depends_on: The depends_on of this TaskGraphNode.  # noqa: E501
        :type: list[str]
        """

        self._depends_on = depends_on

    @property
    def array_node(self):
        """Gets the array_node of this TaskGraphNode.  # noqa: E501


        :return: The array_node of this TaskGraphNode.  # noqa: E501
        :rtype: UDFArrayDetails
        """
        return self._array_node

    @array_node.setter
    def array_node(self, array_node):
        """Sets the array_node of this TaskGraphNode.


        :param array_node: The array_node of this TaskGraphNode.  # noqa: E501
        :type: UDFArrayDetails
        """

        self._array_node = array_node

    @property
    def input_node(self):
        """Gets the input_node of this TaskGraphNode.  # noqa: E501


        :return: The input_node of this TaskGraphNode.  # noqa: E501
        :rtype: TGInputNodeData
        """
        return self._input_node

    @input_node.setter
    def input_node(self, input_node):
        """Sets the input_node of this TaskGraphNode.


        :param input_node: The input_node of this TaskGraphNode.  # noqa: E501
        :type: TGInputNodeData
        """

        self._input_node = input_node

    @property
    def sql_node(self):
        """Gets the sql_node of this TaskGraphNode.  # noqa: E501


        :return: The sql_node of this TaskGraphNode.  # noqa: E501
        :rtype: TGSQLNodeData
        """
        return self._sql_node

    @sql_node.setter
    def sql_node(self, sql_node):
        """Sets the sql_node of this TaskGraphNode.


        :param sql_node: The sql_node of this TaskGraphNode.  # noqa: E501
        :type: TGSQLNodeData
        """

        self._sql_node = sql_node

    @property
    def udf_node(self):
        """Gets the udf_node of this TaskGraphNode.  # noqa: E501


        :return: The udf_node of this TaskGraphNode.  # noqa: E501
        :rtype: TGUDFNodeData
        """
        return self._udf_node

    @udf_node.setter
    def udf_node(self, udf_node):
        """Sets the udf_node of this TaskGraphNode.


        :param udf_node: The udf_node of this TaskGraphNode.  # noqa: E501
        :type: TGUDFNodeData
        """

        self._udf_node = udf_node

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
        if not isinstance(other, TaskGraphNode):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TaskGraphNode):
            return True

        return self.to_dict() != other.to_dict()