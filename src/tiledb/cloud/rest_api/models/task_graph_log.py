# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint

from tiledb.cloud.rest_api.configuration import Configuration


class TaskGraphLog:
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
        "start_time": "datetime",
        "end_time": "datetime",
        "status": "TaskGraphLogStatus",
        "total_cost": "float",
        "access_cost": "float",
        "egress_cost": "float",
        "execution_time": "str",
        "status_count": "dict(str, float)",
        "nodes": "list[TaskGraphNodeMetadata]",
        "task_graph_type": "TaskGraphType",
        "task_graph_id": "str",
    }

    attribute_map = {
        "uuid": "uuid",
        "namespace": "namespace",
        "created_by": "created_by",
        "name": "name",
        "created_at": "created_at",
        "start_time": "start_time",
        "end_time": "end_time",
        "status": "status",
        "total_cost": "total_cost",
        "access_cost": "access_cost",
        "egress_cost": "egress_cost",
        "execution_time": "execution_time",
        "status_count": "status_count",
        "nodes": "nodes",
        "task_graph_type": "task_graph_type",
        "task_graph_id": "task_graph_id",
    }

    def __init__(
        self,
        uuid=None,
        namespace=None,
        created_by=None,
        name=None,
        created_at=None,
        start_time=None,
        end_time=None,
        status=None,
        total_cost=None,
        access_cost=None,
        egress_cost=None,
        execution_time=None,
        status_count=None,
        nodes=None,
        task_graph_type=None,
        task_graph_id=None,
        local_vars_configuration=None,
    ):
        """TaskGraphLog - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._uuid = None
        self._namespace = None
        self._created_by = None
        self._name = None
        self._created_at = None
        self._start_time = None
        self._end_time = None
        self._status = None
        self._total_cost = None
        self._access_cost = None
        self._egress_cost = None
        self._execution_time = None
        self._status_count = None
        self._nodes = None
        self._task_graph_type = None
        self._task_graph_id = None
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
        self.start_time = start_time
        self.end_time = end_time
        if status is not None:
            self.status = status
        self.total_cost = total_cost
        self.access_cost = access_cost
        self.egress_cost = egress_cost
        if execution_time is not None:
            self.execution_time = execution_time
        if status_count is not None:
            self.status_count = status_count
        if nodes is not None:
            self.nodes = nodes
        if task_graph_type is not None:
            self.task_graph_type = task_graph_type
        if task_graph_id is not None:
            self.task_graph_id = task_graph_id

    @property
    def uuid(self):
        """Gets the uuid of this TaskGraphLog.

        The server-generated UUID of the task graph.

        :return: The uuid of this TaskGraphLog.
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """Sets the uuid of this TaskGraphLog.

        The server-generated UUID of the task graph.

        :param uuid: The uuid of this TaskGraphLog.
        :type: str
        """

        self._uuid = uuid

    @property
    def namespace(self):
        """Gets the namespace of this TaskGraphLog.

        The namespace that owns this task graph log. When creating a task graph log, this is used as the namespace to create the log in; thereafter it is read-only.

        :return: The namespace of this TaskGraphLog.
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this TaskGraphLog.

        The namespace that owns this task graph log. When creating a task graph log, this is used as the namespace to create the log in; thereafter it is read-only.

        :param namespace: The namespace of this TaskGraphLog.
        :type: str
        """

        self._namespace = namespace

    @property
    def created_by(self):
        """Gets the created_by of this TaskGraphLog.

        The name of the user who created this task graph log.

        :return: The created_by of this TaskGraphLog.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this TaskGraphLog.

        The name of the user who created this task graph log.

        :param created_by: The created_by of this TaskGraphLog.
        :type: str
        """

        self._created_by = created_by

    @property
    def name(self):
        """Gets the name of this TaskGraphLog.

        A name for this task graph log, displayed in the UI. Does not need to be unique.

        :return: The name of this TaskGraphLog.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TaskGraphLog.

        A name for this task graph log, displayed in the UI. Does not need to be unique.

        :param name: The name of this TaskGraphLog.
        :type: str
        """

        self._name = name

    @property
    def created_at(self):
        """Gets the created_at of this TaskGraphLog.

        The date/time when this task graph log was originally created. This is distinct from the execution start_time.

        :return: The created_at of this TaskGraphLog.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this TaskGraphLog.

        The date/time when this task graph log was originally created. This is distinct from the execution start_time.

        :param created_at: The created_at of this TaskGraphLog.
        :type: datetime
        """

        self._created_at = created_at

    @property
    def start_time(self):
        """Gets the start_time of this TaskGraphLog.

        The start time of the task graph, recorded when the server starts executing the first node.

        :return: The start_time of this TaskGraphLog.
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this TaskGraphLog.

        The start time of the task graph, recorded when the server starts executing the first node.

        :param start_time: The start_time of this TaskGraphLog.
        :type: datetime
        """

        self._start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this TaskGraphLog.

        The end time of the task graph, recorded when the client reports completion.

        :return: The end_time of this TaskGraphLog.
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this TaskGraphLog.

        The end time of the task graph, recorded when the client reports completion.

        :param end_time: The end_time of this TaskGraphLog.
        :type: datetime
        """

        self._end_time = end_time

    @property
    def status(self):
        """Gets the status of this TaskGraphLog.


        :return: The status of this TaskGraphLog.
        :rtype: TaskGraphLogStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this TaskGraphLog.


        :param status: The status of this TaskGraphLog.
        :type: TaskGraphLogStatus
        """

        self._status = status

    @property
    def total_cost(self):
        """Gets the total_cost of this TaskGraphLog.

        If present, the total cost of executing all nodes in this task graph.

        :return: The total_cost of this TaskGraphLog.
        :rtype: float
        """
        return self._total_cost

    @total_cost.setter
    def total_cost(self, total_cost):
        """Sets the total_cost of this TaskGraphLog.

        If present, the total cost of executing all nodes in this task graph.

        :param total_cost: The total_cost of this TaskGraphLog.
        :type: float
        """

        self._total_cost = total_cost

    @property
    def access_cost(self):
        """Gets the access_cost of this TaskGraphLog.

        If present, the total cost of access from execution of the nodes in this task graph.

        :return: The access_cost of this TaskGraphLog.
        :rtype: float
        """
        return self._access_cost

    @access_cost.setter
    def access_cost(self, access_cost):
        """Sets the access_cost of this TaskGraphLog.

        If present, the total cost of access from execution of the nodes in this task graph.

        :param access_cost: The access_cost of this TaskGraphLog.
        :type: float
        """

        self._access_cost = access_cost

    @property
    def egress_cost(self):
        """Gets the egress_cost of this TaskGraphLog.

        If present, the total cost of access from execution of the nodes in this task graph.

        :return: The egress_cost of this TaskGraphLog.
        :rtype: float
        """
        return self._egress_cost

    @egress_cost.setter
    def egress_cost(self, egress_cost):
        """Sets the egress_cost of this TaskGraphLog.

        If present, the total cost of access from execution of the nodes in this task graph.

        :param egress_cost: The egress_cost of this TaskGraphLog.
        :type: float
        """

        self._egress_cost = egress_cost

    @property
    def execution_time(self):
        """Gets the execution_time of this TaskGraphLog.

        The total execution time of all the nodes in this graph, in ISO 8601 format with hours, minutes, and seconds.

        :return: The execution_time of this TaskGraphLog.
        :rtype: str
        """
        return self._execution_time

    @execution_time.setter
    def execution_time(self, execution_time):
        """Sets the execution_time of this TaskGraphLog.

        The total execution time of all the nodes in this graph, in ISO 8601 format with hours, minutes, and seconds.

        :param execution_time: The execution_time of this TaskGraphLog.
        :type: str
        """

        self._execution_time = execution_time

    @property
    def status_count(self):
        """Gets the status_count of this TaskGraphLog.

        A mapping from `ArrayTaskStatus` string value to the number of nodes in this graph that are in that status.

        :return: The status_count of this TaskGraphLog.
        :rtype: dict(str, float)
        """
        return self._status_count

    @status_count.setter
    def status_count(self, status_count):
        """Sets the status_count of this TaskGraphLog.

        A mapping from `ArrayTaskStatus` string value to the number of nodes in this graph that are in that status.

        :param status_count: The status_count of this TaskGraphLog.
        :type: dict(str, float)
        """

        self._status_count = status_count

    @property
    def nodes(self):
        """Gets the nodes of this TaskGraphLog.

        The structure of the graph. This is provided by the client when first setting up the task graph. Thereafter, it is read-only. This must be topographically sorted; that is, each node must appear after all nodes that it depends upon.

        :return: The nodes of this TaskGraphLog.
        :rtype: list[TaskGraphNodeMetadata]
        """
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        """Sets the nodes of this TaskGraphLog.

        The structure of the graph. This is provided by the client when first setting up the task graph. Thereafter, it is read-only. This must be topographically sorted; that is, each node must appear after all nodes that it depends upon.

        :param nodes: The nodes of this TaskGraphLog.
        :type: list[TaskGraphNodeMetadata]
        """

        self._nodes = nodes

    @property
    def task_graph_type(self):
        """Gets the task_graph_type of this TaskGraphLog.


        :return: The task_graph_type of this TaskGraphLog.
        :rtype: TaskGraphType
        """
        return self._task_graph_type

    @task_graph_type.setter
    def task_graph_type(self, task_graph_type):
        """Sets the task_graph_type of this TaskGraphLog.


        :param task_graph_type: The task_graph_type of this TaskGraphLog.
        :type: TaskGraphType
        """

        self._task_graph_type = task_graph_type

    @property
    def task_graph_id(self):
        """Gets the task_graph_id of this TaskGraphLog.

        The UUID of the task graph.

        :return: The task_graph_id of this TaskGraphLog.
        :rtype: str
        """
        return self._task_graph_id

    @task_graph_id.setter
    def task_graph_id(self, task_graph_id):
        """Sets the task_graph_id of this TaskGraphLog.

        The UUID of the task graph.

        :param task_graph_id: The task_graph_id of this TaskGraphLog.
        :type: str
        """

        self._task_graph_id = task_graph_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in self.openapi_types.items():
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
        if not isinstance(other, TaskGraphLog):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TaskGraphLog):
            return True

        return self.to_dict() != other.to_dict()
