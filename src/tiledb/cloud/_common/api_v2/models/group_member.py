# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


import pprint

import six

from tiledb.cloud._common.api_v2.configuration import Configuration


class GroupMember(object):
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
    openapi_types = {"name": "str", "uri": "str", "type": "GroupMemberType"}

    attribute_map = {"name": "name", "uri": "uri", "type": "type"}

    def __init__(self, name=None, uri=None, type=None, local_vars_configuration=None):
        """GroupMember - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._uri = None
        self._type = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if uri is not None:
            self.uri = uri
        if type is not None:
            self.type = type

    @property
    def name(self):
        """Gets the name of this GroupMember.

        The name of the member

        :return: The name of this GroupMember.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GroupMember.

        The name of the member

        :param name: The name of this GroupMember.
        :type: str
        """

        self._name = name

    @property
    def uri(self):
        """Gets the uri of this GroupMember.

        The uri of the member

        :return: The uri of this GroupMember.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this GroupMember.

        The uri of the member

        :param uri: The uri of this GroupMember.
        :type: str
        """

        self._uri = uri

    @property
    def type(self):
        """Gets the type of this GroupMember.


        :return: The type of this GroupMember.
        :rtype: GroupMemberType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this GroupMember.


        :param type: The type of this GroupMember.
        :type: GroupMemberType
        """

        self._type = type

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
        if not isinstance(other, GroupMember):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GroupMember):
            return True

        return self.to_dict() != other.to_dict()
