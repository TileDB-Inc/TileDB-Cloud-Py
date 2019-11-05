# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 0.6.3
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class SubarrayRanges(object):
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
        'type': 'Datatype',
        'has_default_range': 'bool',
        'buffer': 'list[int]'
    }

    attribute_map = {
        'type': 'type',
        'has_default_range': 'hasDefaultRange',
        'buffer': 'buffer'
    }

    def __init__(self, type=None, has_default_range=None, buffer=None):  # noqa: E501
        """SubarrayRanges - a model defined in OpenAPI"""  # noqa: E501

        self._type = None
        self._has_default_range = None
        self._buffer = None
        self.discriminator = None

        if type is not None:
            self.type = type
        if has_default_range is not None:
            self.has_default_range = has_default_range
        if buffer is not None:
            self.buffer = buffer

    @property
    def type(self):
        """Gets the type of this SubarrayRanges.  # noqa: E501


        :return: The type of this SubarrayRanges.  # noqa: E501
        :rtype: Datatype
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this SubarrayRanges.


        :param type: The type of this SubarrayRanges.  # noqa: E501
        :type: Datatype
        """

        self._type = type

    @property
    def has_default_range(self):
        """Gets the has_default_range of this SubarrayRanges.  # noqa: E501

        True if the range is the default range  # noqa: E501

        :return: The has_default_range of this SubarrayRanges.  # noqa: E501
        :rtype: bool
        """
        return self._has_default_range

    @has_default_range.setter
    def has_default_range(self, has_default_range):
        """Sets the has_default_range of this SubarrayRanges.

        True if the range is the default range  # noqa: E501

        :param has_default_range: The has_default_range of this SubarrayRanges.  # noqa: E501
        :type: bool
        """

        self._has_default_range = has_default_range

    @property
    def buffer(self):
        """Gets the buffer of this SubarrayRanges.  # noqa: E501

        The bytes of the ranges  # noqa: E501

        :return: The buffer of this SubarrayRanges.  # noqa: E501
        :rtype: list[int]
        """
        return self._buffer

    @buffer.setter
    def buffer(self, buffer):
        """Sets the buffer of this SubarrayRanges.

        The bytes of the ranges  # noqa: E501

        :param buffer: The buffer of this SubarrayRanges.  # noqa: E501
        :type: list[int]
        """

        self._buffer = buffer

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
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
        if not isinstance(other, SubarrayRanges):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
