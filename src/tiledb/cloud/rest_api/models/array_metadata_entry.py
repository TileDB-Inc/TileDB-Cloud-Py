# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class ArrayMetadataEntry(object):
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
        "key": "str",
        "type": "str",
        "value_num": "int",
        "value": "list[int]",
        "_del": "bool",
    }

    attribute_map = {
        "key": "key",
        "type": "type",
        "value_num": "valueNum",
        "value": "value",
        "_del": "del",
    }

    def __init__(
        self,
        key=None,
        type=None,
        value_num=None,
        value=None,
        _del=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """ArrayMetadataEntry - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._key = None
        self._type = None
        self._value_num = None
        self._value = None
        self.__del = None
        self.discriminator = None

        if key is not None:
            self.key = key
        if type is not None:
            self.type = type
        if value_num is not None:
            self.value_num = value_num
        if value is not None:
            self.value = value
        if _del is not None:
            self._del = _del

    @property
    def key(self):
        """Gets the key of this ArrayMetadataEntry.  # noqa: E501


        :return: The key of this ArrayMetadataEntry.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this ArrayMetadataEntry.


        :param key: The key of this ArrayMetadataEntry.  # noqa: E501
        :type: str
        """

        self._key = key

    @property
    def type(self):
        """Gets the type of this ArrayMetadataEntry.  # noqa: E501


        :return: The type of this ArrayMetadataEntry.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ArrayMetadataEntry.


        :param type: The type of this ArrayMetadataEntry.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def value_num(self):
        """Gets the value_num of this ArrayMetadataEntry.  # noqa: E501


        :return: The value_num of this ArrayMetadataEntry.  # noqa: E501
        :rtype: int
        """
        return self._value_num

    @value_num.setter
    def value_num(self, value_num):
        """Sets the value_num of this ArrayMetadataEntry.


        :param value_num: The value_num of this ArrayMetadataEntry.  # noqa: E501
        :type: int
        """

        self._value_num = value_num

    @property
    def value(self):
        """Gets the value of this ArrayMetadataEntry.  # noqa: E501


        :return: The value of this ArrayMetadataEntry.  # noqa: E501
        :rtype: list[int]
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this ArrayMetadataEntry.


        :param value: The value of this ArrayMetadataEntry.  # noqa: E501
        :type: list[int]
        """

        self._value = value

    @property
    def _del(self):
        """Gets the _del of this ArrayMetadataEntry.  # noqa: E501


        :return: The _del of this ArrayMetadataEntry.  # noqa: E501
        :rtype: bool
        """
        return self.__del

    @_del.setter
    def _del(self, _del):
        """Sets the _del of this ArrayMetadataEntry.


        :param _del: The _del of this ArrayMetadataEntry.  # noqa: E501
        :type: bool
        """

        self.__del = _del

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
        if not isinstance(other, ArrayMetadataEntry):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ArrayMetadataEntry):
            return True

        return self.to_dict() != other.to_dict()
