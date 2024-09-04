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
    openapi_types = {
        "namespace": "str",
        "name": "str",
        "member_type": "GroupMemberType",
    }

    attribute_map = {
        "namespace": "namespace",
        "name": "name",
        "member_type": "member_type",
    }

    def __init__(
        self, namespace=None, name=None, member_type=None, local_vars_configuration=None
    ):  # noqa: E501
        """GroupMember - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._namespace = None
        self._name = None
        self._member_type = None
        self.discriminator = None

        if namespace is not None:
            self.namespace = namespace
        if name is not None:
            self.name = name
        if member_type is not None:
            self.member_type = member_type

    @property
    def namespace(self):
        """Gets the namespace of this GroupMember.  # noqa: E501

        The namespace of the asset.  # noqa: E501

        :return: The namespace of this GroupMember.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this GroupMember.

        The namespace of the asset.  # noqa: E501

        :param namespace: The namespace of this GroupMember.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def name(self):
        """Gets the name of this GroupMember.  # noqa: E501

        The name or id of the asset.  # noqa: E501

        :return: The name of this GroupMember.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GroupMember.

        The name or id of the asset.  # noqa: E501

        :param name: The name of this GroupMember.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def member_type(self):
        """Gets the member_type of this GroupMember.  # noqa: E501


        :return: The member_type of this GroupMember.  # noqa: E501
        :rtype: GroupMemberType
        """
        return self._member_type

    @member_type.setter
    def member_type(self, member_type):
        """Sets the member_type of this GroupMember.


        :param member_type: The member_type of this GroupMember.  # noqa: E501
        :type: GroupMemberType
        """

        self._member_type = member_type

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
