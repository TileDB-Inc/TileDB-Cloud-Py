# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint

import six

from tiledb.cloud.rest_api.configuration import Configuration


class TaskGraph(object):
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
        "uuid": "str",
        "namespace": "str",
        "created_by": "str",
        "name": "str",
        "created_at": "datetime",
        "nodes": "list[TaskGraphNode]",
        "parallelism": "int",
        "retry_strategy": "RetryStrategy",
        "deadline": "int",
        "task_graph_type": "TaskGraphType",
    }

    attribute_map = {
        "uuid": "uuid",
        "namespace": "namespace",
        "created_by": "created_by",
        "name": "name",
        "created_at": "created_at",
        "nodes": "nodes",
        "parallelism": "parallelism",
        "retry_strategy": "retry_strategy",
        "deadline": "deadline",
        "task_graph_type": "task_graph_type",
    }

    def __init__(
        self,
        uuid=None,
        namespace=None,
        created_by=None,
        name=None,
        created_at=None,
        nodes=None,
        parallelism=None,
        retry_strategy=None,
        deadline=None,
        task_graph_type=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """TaskGraph - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._uuid = None
        self._namespace = None
        self._created_by = None
        self._name = None
        self._created_at = None
        self._nodes = None
        self._parallelism = None
        self._retry_strategy = None
        self._deadline = None
        self._task_graph_type = None
        self.discriminator = None

        if uuid is not None:
            self.uuid = uuid
        if namespace is not None:
            self.namespace = namespace
        if created_by is not None:
            self.created_by = created_by
        if name is not None:
            self.name = name
        if created_at is not None:
            self.created_at = created_at
        if nodes is not None:
            self.nodes = nodes
        self.parallelism = parallelism
        if retry_strategy is not None:
            self.retry_strategy = retry_strategy
        self.deadline = deadline
        if task_graph_type is not None:
            self.task_graph_type = task_graph_type

    @property
    def uuid(self):
        """Gets the uuid of this TaskGraph.  # noqa: E501

        The server-generated UUID of the task graph.  # noqa: E501

        :return: The uuid of this TaskGraph.  # noqa: E501
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this TaskGraph.

        The server-generated UUID of the task graph.  # noqa: E501

        :param uuid: The uuid of this TaskGraph.  # noqa: E501
        :type: str
        """

        self._uuid = uuid

    @property
    def namespace(self):
        """Gets the namespace of this TaskGraph.  # noqa: E501

        The namespace that owns this task graph. When creating a task graph log, this is used as the namespace to create the log in; thereafter it is read-only.   # noqa: E501

        :return: The namespace of this TaskGraph.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this TaskGraph.

        The namespace that owns this task graph. When creating a task graph log, this is used as the namespace to create the log in; thereafter it is read-only.   # noqa: E501

        :param namespace: The namespace of this TaskGraph.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def created_by(self):
        """Gets the created_by of this TaskGraph.  # noqa: E501

        The name of the user who created this task graph log.  # noqa: E501

        :return: The created_by of this TaskGraph.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this TaskGraph.

        The name of the user who created this task graph log.  # noqa: E501

        :param created_by: The created_by of this TaskGraph.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def name(self):
        """Gets the name of this TaskGraph.  # noqa: E501

        A name for this task graph, displayed in the UI. Does not need to be unique.   # noqa: E501

        :return: The name of this TaskGraph.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TaskGraph.

        A name for this task graph, displayed in the UI. Does not need to be unique.   # noqa: E501

        :param name: The name of this TaskGraph.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def created_at(self):
        """Gets the created_at of this TaskGraph.  # noqa: E501

        The date/time when this task graph was originally created.   # noqa: E501

        :return: The created_at of this TaskGraph.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this TaskGraph.

        The date/time when this task graph was originally created.   # noqa: E501

        :param created_at: The created_at of this TaskGraph.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def nodes(self):
        """Gets the nodes of this TaskGraph.  # noqa: E501

        The structure of the graph. This is provided by the client when first setting up the task graph. This must be topographically sorted; that is, each node must appear after all nodes that it depends upon.   # noqa: E501

        :return: The nodes of this TaskGraph.  # noqa: E501
        :rtype: list[TaskGraphNode]
        """
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        """Sets the nodes of this TaskGraph.

        The structure of the graph. This is provided by the client when first setting up the task graph. This must be topographically sorted; that is, each node must appear after all nodes that it depends upon.   # noqa: E501

        :param nodes: The nodes of this TaskGraph.  # noqa: E501
        :type: list[TaskGraphNode]
        """

        self._nodes = nodes

    @property
    def parallelism(self):
        """Gets the parallelism of this TaskGraph.  # noqa: E501

        Parallelism limits the max total parallel pods that can execute at the same time in a workflow.   # noqa: E501

        :return: The parallelism of this TaskGraph.  # noqa: E501
        :rtype: int
        """
        return self._parallelism

    @parallelism.setter
    def parallelism(self, parallelism):
        """Sets the parallelism of this TaskGraph.

        Parallelism limits the max total parallel pods that can execute at the same time in a workflow.   # noqa: E501

        :param parallelism: The parallelism of this TaskGraph.  # noqa: E501
        :type: int
        """

        self._parallelism = parallelism

    @property
    def retry_strategy(self):
        """Gets the retry_strategy of this TaskGraph.  # noqa: E501


        :return: The retry_strategy of this TaskGraph.  # noqa: E501
        :rtype: RetryStrategy
        """
        return self._retry_strategy

    @retry_strategy.setter
    def retry_strategy(self, retry_strategy):
        """Sets the retry_strategy of this TaskGraph.


        :param retry_strategy: The retry_strategy of this TaskGraph.  # noqa: E501
        :type: RetryStrategy
        """

        self._retry_strategy = retry_strategy

    @property
    def deadline(self):
        """Gets the deadline of this TaskGraph.  # noqa: E501

        Duration in seconds relative to the workflow start time which the workflow is allowed to run before it gets terminated.   # noqa: E501

        :return: The deadline of this TaskGraph.  # noqa: E501
        :rtype: int
        """
        return self._deadline

    @deadline.setter
    def deadline(self, deadline):
        """Sets the deadline of this TaskGraph.

        Duration in seconds relative to the workflow start time which the workflow is allowed to run before it gets terminated.   # noqa: E501

        :param deadline: The deadline of this TaskGraph.  # noqa: E501
        :type: int
        """

        self._deadline = deadline

    @property
    def task_graph_type(self):
        """Gets the task_graph_type of this TaskGraph.  # noqa: E501


        :return: The task_graph_type of this TaskGraph.  # noqa: E501
        :rtype: TaskGraphType
        """
        return self._task_graph_type

    @task_graph_type.setter
    def task_graph_type(self, task_graph_type):
        """Sets the task_graph_type of this TaskGraph.


        :param task_graph_type: The task_graph_type of this TaskGraph.  # noqa: E501
        :type: TaskGraphType
        """

        self._task_graph_type = task_graph_type

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
        if not isinstance(other, TaskGraph):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TaskGraph):
            return True

        return self.to_dict() != other.to_dict()
