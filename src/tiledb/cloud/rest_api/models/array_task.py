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


class ArrayTask(object):
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
        "id": "str",
        "name": "str",
        "username": "str",
        "description": "str",
        "array_metadata": "ArrayInfo",
        "subarray": "DomainArray",
        "memory": "int",
        "cpu": "int",
        "namespace": "str",
        "status": "ArrayTaskStatus",
        "status_message": "str",
        "start_time": "datetime",
        "finish_time": "datetime",
        "cost": "float",
        "egress_cost": "float",
        "access_cost": "float",
        "query_type": "Querytype",
        "udf_code": "str",
        "udf_language": "str",
        "sql_query": "str",
        "type": "ArrayTaskType",
        "activity": "list[ArrayActivityLog]",
        "logs": "str",
        "duration": "float",
        "sql_init_commands": "list[str]",
        "sql_parameters": "list[object]",
        "result_format": "ResultFormat",
        "task_graph_uuid": "str",
        "client_node_uuid": "str",
    }

    attribute_map = {
        "id": "id",
        "name": "name",
        "username": "username",
        "description": "description",
        "array_metadata": "array_metadata",
        "subarray": "subarray",
        "memory": "memory",
        "cpu": "cpu",
        "namespace": "namespace",
        "status": "status",
        "status_message": "status_message",
        "start_time": "start_time",
        "finish_time": "finish_time",
        "cost": "cost",
        "egress_cost": "egress_cost",
        "access_cost": "access_cost",
        "query_type": "query_type",
        "udf_code": "udf_code",
        "udf_language": "udf_language",
        "sql_query": "sql_query",
        "type": "type",
        "activity": "activity",
        "logs": "logs",
        "duration": "duration",
        "sql_init_commands": "sql_init_commands",
        "sql_parameters": "sql_parameters",
        "result_format": "result_format",
        "task_graph_uuid": "task_graph_uuid",
        "client_node_uuid": "client_node_uuid",
    }

    def __init__(
        self,
        id=None,
        name=None,
        username=None,
        description=None,
        array_metadata=None,
        subarray=None,
        memory=None,
        cpu=None,
        namespace=None,
        status=None,
        status_message=None,
        start_time=None,
        finish_time=None,
        cost=None,
        egress_cost=None,
        access_cost=None,
        query_type=None,
        udf_code=None,
        udf_language=None,
        sql_query=None,
        type=None,
        activity=None,
        logs=None,
        duration=None,
        sql_init_commands=None,
        sql_parameters=None,
        result_format=None,
        task_graph_uuid=None,
        client_node_uuid=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """ArrayTask - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._username = None
        self._description = None
        self._array_metadata = None
        self._subarray = None
        self._memory = None
        self._cpu = None
        self._namespace = None
        self._status = None
        self._status_message = None
        self._start_time = None
        self._finish_time = None
        self._cost = None
        self._egress_cost = None
        self._access_cost = None
        self._query_type = None
        self._udf_code = None
        self._udf_language = None
        self._sql_query = None
        self._type = None
        self._activity = None
        self._logs = None
        self._duration = None
        self._sql_init_commands = None
        self._sql_parameters = None
        self._result_format = None
        self._task_graph_uuid = None
        self._client_node_uuid = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if username is not None:
            self.username = username
        if description is not None:
            self.description = description
        if array_metadata is not None:
            self.array_metadata = array_metadata
        if subarray is not None:
            self.subarray = subarray
        if memory is not None:
            self.memory = memory
        if cpu is not None:
            self.cpu = cpu
        if namespace is not None:
            self.namespace = namespace
        if status is not None:
            self.status = status
        self.status_message = status_message
        self.start_time = start_time
        self.finish_time = finish_time
        if cost is not None:
            self.cost = cost
        if egress_cost is not None:
            self.egress_cost = egress_cost
        if access_cost is not None:
            self.access_cost = access_cost
        if query_type is not None:
            self.query_type = query_type
        if udf_code is not None:
            self.udf_code = udf_code
        if udf_language is not None:
            self.udf_language = udf_language
        if sql_query is not None:
            self.sql_query = sql_query
        if type is not None:
            self.type = type
        if activity is not None:
            self.activity = activity
        if logs is not None:
            self.logs = logs
        if duration is not None:
            self.duration = duration
        if sql_init_commands is not None:
            self.sql_init_commands = sql_init_commands
        if sql_parameters is not None:
            self.sql_parameters = sql_parameters
        if result_format is not None:
            self.result_format = result_format
        if task_graph_uuid is not None:
            self.task_graph_uuid = task_graph_uuid
        if client_node_uuid is not None:
            self.client_node_uuid = client_node_uuid

    @property
    def id(self):
        """Gets the id of this ArrayTask.  # noqa: E501

        task ID  # noqa: E501

        :return: The id of this ArrayTask.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ArrayTask.

        task ID  # noqa: E501

        :param id: The id of this ArrayTask.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this ArrayTask.  # noqa: E501

        Optional task name  # noqa: E501

        :return: The name of this ArrayTask.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ArrayTask.

        Optional task name  # noqa: E501

        :param name: The name of this ArrayTask.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def username(self):
        """Gets the username of this ArrayTask.  # noqa: E501

        username that executed this task  # noqa: E501

        :return: The username of this ArrayTask.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this ArrayTask.

        username that executed this task  # noqa: E501

        :param username: The username of this ArrayTask.  # noqa: E501
        :type: str
        """

        self._username = username

    @property
    def description(self):
        """Gets the description of this ArrayTask.  # noqa: E501

        Optional task description (Tasks purpose)  # noqa: E501

        :return: The description of this ArrayTask.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ArrayTask.

        Optional task description (Tasks purpose)  # noqa: E501

        :param description: The description of this ArrayTask.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def array_metadata(self):
        """Gets the array_metadata of this ArrayTask.  # noqa: E501


        :return: The array_metadata of this ArrayTask.  # noqa: E501
        :rtype: ArrayInfo
        """
        return self._array_metadata

    @array_metadata.setter
    def array_metadata(self, array_metadata):
        """Sets the array_metadata of this ArrayTask.


        :param array_metadata: The array_metadata of this ArrayTask.  # noqa: E501
        :type: ArrayInfo
        """

        self._array_metadata = array_metadata

    @property
    def subarray(self):
        """Gets the subarray of this ArrayTask.  # noqa: E501


        :return: The subarray of this ArrayTask.  # noqa: E501
        :rtype: DomainArray
        """
        return self._subarray

    @subarray.setter
    def subarray(self, subarray):
        """Sets the subarray of this ArrayTask.


        :param subarray: The subarray of this ArrayTask.  # noqa: E501
        :type: DomainArray
        """

        self._subarray = subarray

    @property
    def memory(self):
        """Gets the memory of this ArrayTask.  # noqa: E501

        memory allocated to task in bytes  # noqa: E501

        :return: The memory of this ArrayTask.  # noqa: E501
        :rtype: int
        """
        return self._memory

    @memory.setter
    def memory(self, memory):
        """Sets the memory of this ArrayTask.

        memory allocated to task in bytes  # noqa: E501

        :param memory: The memory of this ArrayTask.  # noqa: E501
        :type: int
        """

        self._memory = memory

    @property
    def cpu(self):
        """Gets the cpu of this ArrayTask.  # noqa: E501

        millicpu allocated to task  # noqa: E501

        :return: The cpu of this ArrayTask.  # noqa: E501
        :rtype: int
        """
        return self._cpu

    @cpu.setter
    def cpu(self, cpu):
        """Sets the cpu of this ArrayTask.

        millicpu allocated to task  # noqa: E501

        :param cpu: The cpu of this ArrayTask.  # noqa: E501
        :type: int
        """

        self._cpu = cpu

    @property
    def namespace(self):
        """Gets the namespace of this ArrayTask.  # noqa: E501

        namespace task is tied to  # noqa: E501

        :return: The namespace of this ArrayTask.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this ArrayTask.

        namespace task is tied to  # noqa: E501

        :param namespace: The namespace of this ArrayTask.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def status(self):
        """Gets the status of this ArrayTask.  # noqa: E501


        :return: The status of this ArrayTask.  # noqa: E501
        :rtype: ArrayTaskStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ArrayTask.


        :param status: The status of this ArrayTask.  # noqa: E501
        :type: ArrayTaskStatus
        """

        self._status = status

    @property
    def status_message(self):
        """Gets the status_message of this ArrayTask.  # noqa: E501

        The reason the array task status is in the state  # noqa: E501

        :return: The status_message of this ArrayTask.  # noqa: E501
        :rtype: str
        """
        return self._status_message

    @status_message.setter
    def status_message(self, status_message):
        """Sets the status_message of this ArrayTask.

        The reason the array task status is in the state  # noqa: E501

        :param status_message: The status_message of this ArrayTask.  # noqa: E501
        :type: str
        """

        self._status_message = status_message

    @property
    def start_time(self):
        """Gets the start_time of this ArrayTask.  # noqa: E501

        Start time RFC3339 for job  # noqa: E501

        :return: The start_time of this ArrayTask.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this ArrayTask.

        Start time RFC3339 for job  # noqa: E501

        :param start_time: The start_time of this ArrayTask.  # noqa: E501
        :type: datetime
        """

        self._start_time = start_time

    @property
    def finish_time(self):
        """Gets the finish_time of this ArrayTask.  # noqa: E501

        Finish time RFC3339 for job  # noqa: E501

        :return: The finish_time of this ArrayTask.  # noqa: E501
        :rtype: datetime
        """
        return self._finish_time

    @finish_time.setter
    def finish_time(self, finish_time):
        """Sets the finish_time of this ArrayTask.

        Finish time RFC3339 for job  # noqa: E501

        :param finish_time: The finish_time of this ArrayTask.  # noqa: E501
        :type: datetime
        """

        self._finish_time = finish_time

    @property
    def cost(self):
        """Gets the cost of this ArrayTask.  # noqa: E501

        Total accumulated for task in USD, example is $0.12  # noqa: E501

        :return: The cost of this ArrayTask.  # noqa: E501
        :rtype: float
        """
        return self._cost

    @cost.setter
    def cost(self, cost):
        """Sets the cost of this ArrayTask.

        Total accumulated for task in USD, example is $0.12  # noqa: E501

        :param cost: The cost of this ArrayTask.  # noqa: E501
        :type: float
        """

        self._cost = cost

    @property
    def egress_cost(self):
        """Gets the egress_cost of this ArrayTask.  # noqa: E501

        Total accumulated for egress task in USD, example is $0.12  # noqa: E501

        :return: The egress_cost of this ArrayTask.  # noqa: E501
        :rtype: float
        """
        return self._egress_cost

    @egress_cost.setter
    def egress_cost(self, egress_cost):
        """Sets the egress_cost of this ArrayTask.

        Total accumulated for egress task in USD, example is $0.12  # noqa: E501

        :param egress_cost: The egress_cost of this ArrayTask.  # noqa: E501
        :type: float
        """

        self._egress_cost = egress_cost

    @property
    def access_cost(self):
        """Gets the access_cost of this ArrayTask.  # noqa: E501

        Cost accumulated for access task in USD, example is $0.12  # noqa: E501

        :return: The access_cost of this ArrayTask.  # noqa: E501
        :rtype: float
        """
        return self._access_cost

    @access_cost.setter
    def access_cost(self, access_cost):
        """Sets the access_cost of this ArrayTask.

        Cost accumulated for access task in USD, example is $0.12  # noqa: E501

        :param access_cost: The access_cost of this ArrayTask.  # noqa: E501
        :type: float
        """

        self._access_cost = access_cost

    @property
    def query_type(self):
        """Gets the query_type of this ArrayTask.  # noqa: E501


        :return: The query_type of this ArrayTask.  # noqa: E501
        :rtype: Querytype
        """
        return self._query_type

    @query_type.setter
    def query_type(self, query_type):
        """Sets the query_type of this ArrayTask.


        :param query_type: The query_type of this ArrayTask.  # noqa: E501
        :type: Querytype
        """

        self._query_type = query_type

    @property
    def udf_code(self):
        """Gets the udf_code of this ArrayTask.  # noqa: E501

        Optional actual code that is going to be executed  # noqa: E501

        :return: The udf_code of this ArrayTask.  # noqa: E501
        :rtype: str
        """
        return self._udf_code

    @udf_code.setter
    def udf_code(self, udf_code):
        """Sets the udf_code of this ArrayTask.

        Optional actual code that is going to be executed  # noqa: E501

        :param udf_code: The udf_code of this ArrayTask.  # noqa: E501
        :type: str
        """

        self._udf_code = udf_code

    @property
    def udf_language(self):
        """Gets the udf_language of this ArrayTask.  # noqa: E501

        Optional actual language used to express udf_code  # noqa: E501

        :return: The udf_language of this ArrayTask.  # noqa: E501
        :rtype: str
        """
        return self._udf_language

    @udf_language.setter
    def udf_language(self, udf_language):
        """Sets the udf_language of this ArrayTask.

        Optional actual language used to express udf_code  # noqa: E501

        :param udf_language: The udf_language of this ArrayTask.  # noqa: E501
        :type: str
        """

        self._udf_language = udf_language

    @property
    def sql_query(self):
        """Gets the sql_query of this ArrayTask.  # noqa: E501

        Optional actual sql query that is going to be executed  # noqa: E501

        :return: The sql_query of this ArrayTask.  # noqa: E501
        :rtype: str
        """
        return self._sql_query

    @sql_query.setter
    def sql_query(self, sql_query):
        """Sets the sql_query of this ArrayTask.

        Optional actual sql query that is going to be executed  # noqa: E501

        :param sql_query: The sql_query of this ArrayTask.  # noqa: E501
        :type: str
        """

        self._sql_query = sql_query

    @property
    def type(self):
        """Gets the type of this ArrayTask.  # noqa: E501


        :return: The type of this ArrayTask.  # noqa: E501
        :rtype: ArrayTaskType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ArrayTask.


        :param type: The type of this ArrayTask.  # noqa: E501
        :type: ArrayTaskType
        """

        self._type = type

    @property
    def activity(self):
        """Gets the activity of this ArrayTask.  # noqa: E501

        Array activity logs for task  # noqa: E501

        :return: The activity of this ArrayTask.  # noqa: E501
        :rtype: list[ArrayActivityLog]
        """
        return self._activity

    @activity.setter
    def activity(self, activity):
        """Sets the activity of this ArrayTask.

        Array activity logs for task  # noqa: E501

        :param activity: The activity of this ArrayTask.  # noqa: E501
        :type: list[ArrayActivityLog]
        """

        self._activity = activity

    @property
    def logs(self):
        """Gets the logs of this ArrayTask.  # noqa: E501

        logs from array task  # noqa: E501

        :return: The logs of this ArrayTask.  # noqa: E501
        :rtype: str
        """
        return self._logs

    @logs.setter
    def logs(self, logs):
        """Sets the logs of this ArrayTask.

        logs from array task  # noqa: E501

        :param logs: The logs of this ArrayTask.  # noqa: E501
        :type: str
        """

        self._logs = logs

    @property
    def duration(self):
        """Gets the duration of this ArrayTask.  # noqa: E501

        duration in nanoseconds of an array task  # noqa: E501

        :return: The duration of this ArrayTask.  # noqa: E501
        :rtype: float
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this ArrayTask.

        duration in nanoseconds of an array task  # noqa: E501

        :param duration: The duration of this ArrayTask.  # noqa: E501
        :type: float
        """

        self._duration = duration

    @property
    def sql_init_commands(self):
        """Gets the sql_init_commands of this ArrayTask.  # noqa: E501

        SQL queries or commands to run before main sql query  # noqa: E501

        :return: The sql_init_commands of this ArrayTask.  # noqa: E501
        :rtype: list[str]
        """
        return self._sql_init_commands

    @sql_init_commands.setter
    def sql_init_commands(self, sql_init_commands):
        """Sets the sql_init_commands of this ArrayTask.

        SQL queries or commands to run before main sql query  # noqa: E501

        :param sql_init_commands: The sql_init_commands of this ArrayTask.  # noqa: E501
        :type: list[str]
        """

        self._sql_init_commands = sql_init_commands

    @property
    def sql_parameters(self):
        """Gets the sql_parameters of this ArrayTask.  # noqa: E501

        SQL query parameters  # noqa: E501

        :return: The sql_parameters of this ArrayTask.  # noqa: E501
        :rtype: list[object]
        """
        return self._sql_parameters

    @sql_parameters.setter
    def sql_parameters(self, sql_parameters):
        """Sets the sql_parameters of this ArrayTask.

        SQL query parameters  # noqa: E501

        :param sql_parameters: The sql_parameters of this ArrayTask.  # noqa: E501
        :type: list[object]
        """

        self._sql_parameters = sql_parameters

    @property
    def result_format(self):
        """Gets the result_format of this ArrayTask.  # noqa: E501


        :return: The result_format of this ArrayTask.  # noqa: E501
        :rtype: ResultFormat
        """
        return self._result_format

    @result_format.setter
    def result_format(self, result_format):
        """Sets the result_format of this ArrayTask.


        :param result_format: The result_format of this ArrayTask.  # noqa: E501
        :type: ResultFormat
        """

        self._result_format = result_format

    @property
    def task_graph_uuid(self):
        """Gets the task_graph_uuid of this ArrayTask.  # noqa: E501

        If set, the ID of the log for the task graph that this was part of.   # noqa: E501

        :return: The task_graph_uuid of this ArrayTask.  # noqa: E501
        :rtype: str
        """
        return self._task_graph_uuid

    @task_graph_uuid.setter
    def task_graph_uuid(self, task_graph_uuid):
        """Sets the task_graph_uuid of this ArrayTask.

        If set, the ID of the log for the task graph that this was part of.   # noqa: E501

        :param task_graph_uuid: The task_graph_uuid of this ArrayTask.  # noqa: E501
        :type: str
        """

        self._task_graph_uuid = task_graph_uuid

    @property
    def client_node_uuid(self):
        """Gets the client_node_uuid of this ArrayTask.  # noqa: E501

        If set, the client-defined ID of the node within this task's graph.   # noqa: E501

        :return: The client_node_uuid of this ArrayTask.  # noqa: E501
        :rtype: str
        """
        return self._client_node_uuid

    @client_node_uuid.setter
    def client_node_uuid(self, client_node_uuid):
        """Sets the client_node_uuid of this ArrayTask.

        If set, the client-defined ID of the node within this task's graph.   # noqa: E501

        :param client_node_uuid: The client_node_uuid of this ArrayTask.  # noqa: E501
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
        if not isinstance(other, ArrayTask):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ArrayTask):
            return True

        return self.to_dict() != other.to_dict()
