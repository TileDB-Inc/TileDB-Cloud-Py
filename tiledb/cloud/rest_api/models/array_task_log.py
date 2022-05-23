# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec

import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class ArrayTaskLog(object):
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
    openapi_types = {"array_task_id": "str", "logs": "str"}

    attribute_map = {"array_task_id": "array_task_id", "logs": "logs"}

    def __init__(
        self, array_task_id=None, logs=None, local_vars_configuration=None
    ):  # noqa: E501
        """ArrayTaskLog - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._array_task_id = None
        self._logs = None
        self.discriminator = None

        if array_task_id is not None:
            self.array_task_id = array_task_id
        if logs is not None:
            self.logs = logs

    @property
    def array_task_id(self):
        """Gets the array_task_id of this ArrayTaskLog.  # noqa: E501

        ID of associated task  # noqa: E501

        :return: The array_task_id of this ArrayTaskLog.  # noqa: E501
        :rtype: str
        """
        return self._array_task_id

    @array_task_id.setter
    def array_task_id(self, array_task_id):
        """Sets the array_task_id of this ArrayTaskLog.

        ID of associated task  # noqa: E501

        :param array_task_id: The array_task_id of this ArrayTaskLog.  # noqa: E501
        :type array_task_id: str
        """

        self._array_task_id = array_task_id

    @property
    def logs(self):
        """Gets the logs of this ArrayTaskLog.  # noqa: E501

        logs from array task  # noqa: E501

        :return: The logs of this ArrayTaskLog.  # noqa: E501
        :rtype: str
        """
        return self._logs

    @logs.setter
    def logs(self, logs):
        """Sets the logs of this ArrayTaskLog.

        logs from array task  # noqa: E501

        :param logs: The logs of this ArrayTaskLog.  # noqa: E501
        :type logs: str
        """

        self._logs = logs

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(lambda x: convert(x), value))
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(lambda item: (item[0], convert(item[1])), value.items())
                )
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ArrayTaskLog):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ArrayTaskLog):
            return True

        return self.to_dict() != other.to_dict()
