# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint

from tiledb.cloud.rest_api.configuration import Configuration


class NotebookStatus(object):
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
        "namespace": "str",
        "uptime": "int",
        "cpu_usage": "int",
        "gpu_usage": "int",
        "memory_usage": "int",
        "gpu_limit": "int",
        "memory_limit": "int",
        "storage_usage": "int",
        "storage_limit": "int",
        "cpu_count": "int",
        "cost": "float",
        "pod_status": "PodStatus",
    }

    attribute_map = {
        "namespace": "namespace",
        "uptime": "uptime",
        "cpu_usage": "cpu_usage",
        "gpu_usage": "gpu_usage",
        "memory_usage": "memory_usage",
        "gpu_limit": "gpu_limit",
        "memory_limit": "memory_limit",
        "storage_usage": "storage_usage",
        "storage_limit": "storage_limit",
        "cpu_count": "cpu_count",
        "cost": "cost",
        "pod_status": "pod_status",
    }

    def __init__(
        self,
        namespace=None,
        uptime=None,
        cpu_usage=None,
        gpu_usage=None,
        memory_usage=None,
        gpu_limit=None,
        memory_limit=None,
        storage_usage=None,
        storage_limit=None,
        cpu_count=None,
        cost=None,
        pod_status=None,
        local_vars_configuration=None,
    ):
        """NotebookStatus - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._namespace = None
        self._uptime = None
        self._cpu_usage = None
        self._gpu_usage = None
        self._memory_usage = None
        self._gpu_limit = None
        self._memory_limit = None
        self._storage_usage = None
        self._storage_limit = None
        self._cpu_count = None
        self._cost = None
        self._pod_status = None
        self.discriminator = None

        if namespace is not None:
            self.namespace = namespace
        if uptime is not None:
            self.uptime = uptime
        if cpu_usage is not None:
            self.cpu_usage = cpu_usage
        if gpu_usage is not None:
            self.gpu_usage = gpu_usage
        if memory_usage is not None:
            self.memory_usage = memory_usage
        if gpu_limit is not None:
            self.gpu_limit = gpu_limit
        if memory_limit is not None:
            self.memory_limit = memory_limit
        if storage_usage is not None:
            self.storage_usage = storage_usage
        if storage_limit is not None:
            self.storage_limit = storage_limit
        if cpu_count is not None:
            self.cpu_count = cpu_count
        self.cost = cost
        if pod_status is not None:
            self.pod_status = pod_status

    @property
    def namespace(self):
        """Gets the namespace of this NotebookStatus.

        namespace of notebook

        :return: The namespace of this NotebookStatus.
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this NotebookStatus.

        namespace of notebook

        :param namespace: The namespace of this NotebookStatus.
        :type: str
        """

        self._namespace = namespace

    @property
    def uptime(self):
        """Gets the uptime of this NotebookStatus.

        duration notebook has been running in seconds

        :return: The uptime of this NotebookStatus.
        :rtype: int
        """
        return self._uptime

    @uptime.setter
    def uptime(self, uptime):
        """Sets the uptime of this NotebookStatus.

        duration notebook has been running in seconds

        :param uptime: The uptime of this NotebookStatus.
        :type: int
        """

        self._uptime = uptime

    @property
    def cpu_usage(self):
        """Gets the cpu_usage of this NotebookStatus.

        current cpu usage in millicpu

        :return: The cpu_usage of this NotebookStatus.
        :rtype: int
        """
        return self._cpu_usage

    @cpu_usage.setter
    def cpu_usage(self, cpu_usage):
        """Sets the cpu_usage of this NotebookStatus.

        current cpu usage in millicpu

        :param cpu_usage: The cpu_usage of this NotebookStatus.
        :type: int
        """

        self._cpu_usage = cpu_usage

    @property
    def gpu_usage(self):
        """Gets the gpu_usage of this NotebookStatus.

        gpu usage in milligpu

        :return: The gpu_usage of this NotebookStatus.
        :rtype: int
        """
        return self._gpu_usage

    @gpu_usage.setter
    def gpu_usage(self, gpu_usage):
        """Sets the gpu_usage of this NotebookStatus.

        gpu usage in milligpu

        :param gpu_usage: The gpu_usage of this NotebookStatus.
        :type: int
        """

        self._gpu_usage = gpu_usage

    @property
    def memory_usage(self):
        """Gets the memory_usage of this NotebookStatus.

        memory usage in bytes

        :return: The memory_usage of this NotebookStatus.
        :rtype: int
        """
        return self._memory_usage

    @memory_usage.setter
    def memory_usage(self, memory_usage):
        """Sets the memory_usage of this NotebookStatus.

        memory usage in bytes

        :param memory_usage: The memory_usage of this NotebookStatus.
        :type: int
        """

        self._memory_usage = memory_usage

    @property
    def gpu_limit(self):
        """Gets the gpu_limit of this NotebookStatus.

        gpu limit in milligpu

        :return: The gpu_limit of this NotebookStatus.
        :rtype: int
        """
        return self._gpu_limit

    @gpu_limit.setter
    def gpu_limit(self, gpu_limit):
        """Sets the gpu_limit of this NotebookStatus.

        gpu limit in milligpu

        :param gpu_limit: The gpu_limit of this NotebookStatus.
        :type: int
        """

        self._gpu_limit = gpu_limit

    @property
    def memory_limit(self):
        """Gets the memory_limit of this NotebookStatus.

        memory allocated to notebook server in bytes

        :return: The memory_limit of this NotebookStatus.
        :rtype: int
        """
        return self._memory_limit

    @memory_limit.setter
    def memory_limit(self, memory_limit):
        """Sets the memory_limit of this NotebookStatus.

        memory allocated to notebook server in bytes

        :param memory_limit: The memory_limit of this NotebookStatus.
        :type: int
        """

        self._memory_limit = memory_limit

    @property
    def storage_usage(self):
        """Gets the storage_usage of this NotebookStatus.

        storage usage in bytes

        :return: The storage_usage of this NotebookStatus.
        :rtype: int
        """
        return self._storage_usage

    @storage_usage.setter
    def storage_usage(self, storage_usage):
        """Sets the storage_usage of this NotebookStatus.

        storage usage in bytes

        :param storage_usage: The storage_usage of this NotebookStatus.
        :type: int
        """

        self._storage_usage = storage_usage

    @property
    def storage_limit(self):
        """Gets the storage_limit of this NotebookStatus.

        storage allocated to notebook server in bytes

        :return: The storage_limit of this NotebookStatus.
        :rtype: int
        """
        return self._storage_limit

    @storage_limit.setter
    def storage_limit(self, storage_limit):
        """Sets the storage_limit of this NotebookStatus.

        storage allocated to notebook server in bytes

        :param storage_limit: The storage_limit of this NotebookStatus.
        :type: int
        """

        self._storage_limit = storage_limit

    @property
    def cpu_count(self):
        """Gets the cpu_count of this NotebookStatus.

        millicpu allocated to notebook server

        :return: The cpu_count of this NotebookStatus.
        :rtype: int
        """
        return self._cpu_count

    @cpu_count.setter
    def cpu_count(self, cpu_count):
        """Sets the cpu_count of this NotebookStatus.

        millicpu allocated to notebook server

        :param cpu_count: The cpu_count of this NotebookStatus.
        :type: int
        """

        self._cpu_count = cpu_count

    @property
    def cost(self):
        """Gets the cost of this NotebookStatus.

        cost in USD for the current notebook session

        :return: The cost of this NotebookStatus.
        :rtype: float
        """
        return self._cost

    @cost.setter
    def cost(self, cost):
        """Sets the cost of this NotebookStatus.

        cost in USD for the current notebook session

        :param cost: The cost of this NotebookStatus.
        :type: float
        """

        self._cost = cost

    @property
    def pod_status(self):
        """Gets the pod_status of this NotebookStatus.


        :return: The pod_status of this NotebookStatus.
        :rtype: PodStatus
        """
        return self._pod_status

    @pod_status.setter
    def pod_status(self, pod_status):
        """Sets the pod_status of this NotebookStatus.


        :param pod_status: The pod_status of this NotebookStatus.
        :type: PodStatus
        """

        self._pod_status = pod_status

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
        if not isinstance(other, NotebookStatus):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NotebookStatus):
            return True

        return self.to_dict() != other.to_dict()
