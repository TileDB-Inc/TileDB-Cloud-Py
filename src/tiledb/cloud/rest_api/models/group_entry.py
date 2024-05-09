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


class GroupEntry(object):
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
    openapi_types = {"member_id": "str", "group": "GroupInfo", "array": "ArrayInfo"}

    attribute_map = {"member_id": "member_id", "group": "group", "array": "array"}

    def __init__(
        self, member_id=None, group=None, array=None, local_vars_configuration=None
    ):  # noqa: E501
        """GroupEntry - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._member_id = None
        self._group = None
        self._array = None
        self.discriminator = None

        if member_id is not None:
            self.member_id = member_id
        if group is not None:
            self.group = group
        if array is not None:
            self.array = array

    @property
    def member_id(self):
        """Gets the member_id of this GroupEntry.  # noqa: E501

        The unique member id for the entry  # noqa: E501

        :return: The member_id of this GroupEntry.  # noqa: E501
        :rtype: str
        """
        return self._member_id

    @member_id.setter
    def member_id(self, member_id):
        """Sets the member_id of this GroupEntry.

        The unique member id for the entry  # noqa: E501

        :param member_id: The member_id of this GroupEntry.  # noqa: E501
        :type: str
        """

        self._member_id = member_id

    @property
    def group(self):
        """Gets the group of this GroupEntry.  # noqa: E501


        :return: The group of this GroupEntry.  # noqa: E501
        :rtype: GroupInfo
        """
        return self._group

    @group.setter
    def group(self, group):
        """Sets the group of this GroupEntry.


        :param group: The group of this GroupEntry.  # noqa: E501
        :type: GroupInfo
        """

        self._group = group

    @property
    def array(self):
        """Gets the array of this GroupEntry.  # noqa: E501


        :return: The array of this GroupEntry.  # noqa: E501
        :rtype: ArrayInfo
        """
        return self._array

    @array.setter
    def array(self, array):
        """Sets the array of this GroupEntry.


        :param array: The array of this GroupEntry.  # noqa: E501
        :type: ArrayInfo
        """

        self._array = array

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
        if not isinstance(other, GroupEntry):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GroupEntry):
            return True

        return self.to_dict() != other.to_dict()
