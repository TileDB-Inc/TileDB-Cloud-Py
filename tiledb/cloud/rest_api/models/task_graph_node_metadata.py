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


class TaskGraphNodeMetadata(object):
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
        "client_node_uuid": "str",
        "name": "str",
        "depends_on": "list[str]",
        "executions": "list[ArrayTask]",
    }

    attribute_map = {
        "client_node_uuid": "client_node_uuid",
        "name": "name",
        "depends_on": "depends_on",
        "executions": "executions",
    }

    def __init__(
        self,
        client_node_uuid=None,
        name=None,
        depends_on=None,
        executions=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """TaskGraphNodeMetadata - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._client_node_uuid = None
        self._name = None
        self._depends_on = None
        self._executions = None
        self.discriminator = None

        if client_node_uuid is not None:
            self.client_node_uuid = client_node_uuid
        if name is not None:
            self.name = name
        if depends_on is not None:
            self.depends_on = depends_on
        if executions is not None:
            self.executions = executions

    @property
    def client_node_uuid(self):
        """Gets the client_node_uuid of this TaskGraphNodeMetadata.  # noqa: E501

        The client-generated UUID of the given graph node.  # noqa: E501

        :return: The client_node_uuid of this TaskGraphNodeMetadata.  # noqa: E501
        :rtype: str
        """
        return self._client_node_uuid

    @client_node_uuid.setter
    def client_node_uuid(self, client_node_uuid):
        """Sets the client_node_uuid of this TaskGraphNodeMetadata.

        The client-generated UUID of the given graph node.  # noqa: E501

        :param client_node_uuid: The client_node_uuid of this TaskGraphNodeMetadata.  # noqa: E501
        :type: str
        """

        self._client_node_uuid = client_node_uuid

    @property
    def name(self):
        """Gets the name of this TaskGraphNodeMetadata.  # noqa: E501

        The client-generated name of the node. This is not guaranteed to be unique.   # noqa: E501

        :return: The name of this TaskGraphNodeMetadata.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TaskGraphNodeMetadata.

        The client-generated name of the node. This is not guaranteed to be unique.   # noqa: E501

        :param name: The name of this TaskGraphNodeMetadata.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def depends_on(self):
        """Gets the depends_on of this TaskGraphNodeMetadata.  # noqa: E501

        The client_node_uuid of each node that this node depends upon. Used to define the structure of the graph.   # noqa: E501

        :return: The depends_on of this TaskGraphNodeMetadata.  # noqa: E501
        :rtype: list[str]
        """
        return self._depends_on

    @depends_on.setter
    def depends_on(self, depends_on):
        """Sets the depends_on of this TaskGraphNodeMetadata.

        The client_node_uuid of each node that this node depends upon. Used to define the structure of the graph.   # noqa: E501

        :param depends_on: The depends_on of this TaskGraphNodeMetadata.  # noqa: E501
        :type: list[str]
        """

        self._depends_on = depends_on

    @property
    def executions(self):
        """Gets the executions of this TaskGraphNodeMetadata.  # noqa: E501

        ArrayTasks representing each execution attempt for this node. For nodes that have never been submitted, this will be empty. For nodes that have been retried, this may have multiple entries. The last one in the list represents the most recent execution. This is read-only and generated by the server based on the tasks it has actually executed.   # noqa: E501

        :return: The executions of this TaskGraphNodeMetadata.  # noqa: E501
        :rtype: list[ArrayTask]
        """
        return self._executions

    @executions.setter
    def executions(self, executions):
        """Sets the executions of this TaskGraphNodeMetadata.

        ArrayTasks representing each execution attempt for this node. For nodes that have never been submitted, this will be empty. For nodes that have been retried, this may have multiple entries. The last one in the list represents the most recent execution. This is read-only and generated by the server based on the tasks it has actually executed.   # noqa: E501

        :param executions: The executions of this TaskGraphNodeMetadata.  # noqa: E501
        :type: list[ArrayTask]
        """

        self._executions = executions

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
        if not isinstance(other, TaskGraphNodeMetadata):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TaskGraphNodeMetadata):
            return True

        return self.to_dict() != other.to_dict()
