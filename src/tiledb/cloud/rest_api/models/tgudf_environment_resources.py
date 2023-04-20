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


class TGUDFEnvironmentResources(object):
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
    openapi_types = {"cpu": "str", "memory": "str", "gpu": "int"}

    attribute_map = {"cpu": "cpu", "memory": "memory", "gpu": "gpu"}

    def __init__(
        self, cpu=None, memory=None, gpu=None, local_vars_configuration=None
    ):  # noqa: E501
        """TGUDFEnvironmentResources - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._cpu = None
        self._memory = None
        self._gpu = None
        self.discriminator = None

        if cpu is not None:
            self.cpu = cpu
        if memory is not None:
            self.memory = memory
        if gpu is not None:
            self.gpu = gpu

    @property
    def cpu(self):
        """Gets the cpu of this TGUDFEnvironmentResources.  # noqa: E501


        :return: The cpu of this TGUDFEnvironmentResources.  # noqa: E501
        :rtype: str
        """
        return self._cpu

    @cpu.setter
    def cpu(self, cpu):
        """Sets the cpu of this TGUDFEnvironmentResources.


        :param cpu: The cpu of this TGUDFEnvironmentResources.  # noqa: E501
        :type: str
        """

        self._cpu = cpu

    @property
    def memory(self):
        """Gets the memory of this TGUDFEnvironmentResources.  # noqa: E501


        :return: The memory of this TGUDFEnvironmentResources.  # noqa: E501
        :rtype: str
        """
        return self._memory

    @memory.setter
    def memory(self, memory):
        """Sets the memory of this TGUDFEnvironmentResources.


        :param memory: The memory of this TGUDFEnvironmentResources.  # noqa: E501
        :type: str
        """

        self._memory = memory

    @property
    def gpu(self):
        """Gets the gpu of this TGUDFEnvironmentResources.  # noqa: E501


        :return: The gpu of this TGUDFEnvironmentResources.  # noqa: E501
        :rtype: int
        """
        return self._gpu

    @gpu.setter
    def gpu(self, gpu):
        """Sets the gpu of this TGUDFEnvironmentResources.


        :param gpu: The gpu of this TGUDFEnvironmentResources.  # noqa: E501
        :type: int
        """

        self._gpu = gpu

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
        if not isinstance(other, TGUDFEnvironmentResources):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TGUDFEnvironmentResources):
            return True

        return self.to_dict() != other.to_dict()
