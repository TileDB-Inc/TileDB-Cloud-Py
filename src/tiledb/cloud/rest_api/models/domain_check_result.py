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


class DomainCheckResult(object):
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
    openapi_types = {"time": "datetime", "status": "DomainCheckStatus"}

    attribute_map = {"time": "time", "status": "status"}

    def __init__(
        self, time=None, status=None, local_vars_configuration=None
    ):  # noqa: E501
        """DomainCheckResult - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._time = None
        self._status = None
        self.discriminator = None

        if time is not None:
            self.time = time
        if status is not None:
            self.status = status

    @property
    def time(self):
        """Gets the time of this DomainCheckResult.  # noqa: E501

        The timestamp when the check was performed.  # noqa: E501

        :return: The time of this DomainCheckResult.  # noqa: E501
        :rtype: datetime
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this DomainCheckResult.

        The timestamp when the check was performed.  # noqa: E501

        :param time: The time of this DomainCheckResult.  # noqa: E501
        :type: datetime
        """

        self._time = time

    @property
    def status(self):
        """Gets the status of this DomainCheckResult.  # noqa: E501


        :return: The status of this DomainCheckResult.  # noqa: E501
        :rtype: DomainCheckStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DomainCheckResult.


        :param status: The status of this DomainCheckResult.  # noqa: E501
        :type: DomainCheckStatus
        """

        self._status = status

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
        if not isinstance(other, DomainCheckResult):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DomainCheckResult):
            return True

        return self.to_dict() != other.to_dict()
