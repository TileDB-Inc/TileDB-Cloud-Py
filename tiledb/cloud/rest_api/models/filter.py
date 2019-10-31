# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 0.6.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class Filter(object):
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
        'type': 'FilterType',
        'data': 'FilterData'
    }

    attribute_map = {
        'type': 'type',
        'data': 'data'
    }

    def __init__(self, type=None, data=None):  # noqa: E501
        """Filter - a model defined in OpenAPI"""  # noqa: E501

        self._type = None
        self._data = None
        self.discriminator = None

        self.type = type
        if data is not None:
            self.data = data

    @property
    def type(self):
        """Gets the type of this Filter.  # noqa: E501


        :return: The type of this Filter.  # noqa: E501
        :rtype: FilterType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Filter.


        :param type: The type of this Filter.  # noqa: E501
        :type: FilterType
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def data(self):
        """Gets the data of this Filter.  # noqa: E501


        :return: The data of this Filter.  # noqa: E501
        :rtype: FilterData
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this Filter.


        :param data: The data of this Filter.  # noqa: E501
        :type: FilterData
        """

        self._data = data

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
        if not isinstance(other, Filter):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
