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


class GroupBrowserFilterData(object):
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
    openapi_types = {"namespaces": "list[str]", "group_types": "list[GroupType]"}

    attribute_map = {"namespaces": "namespaces", "group_types": "group_types"}

    def __init__(
        self, namespaces=None, group_types=None, local_vars_configuration=None
    ):  # noqa: E501
        """GroupBrowserFilterData - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._namespaces = None
        self._group_types = None
        self.discriminator = None

        if namespaces is not None:
            self.namespaces = namespaces
        if group_types is not None:
            self.group_types = group_types

    @property
    def namespaces(self):
        """Gets the namespaces of this GroupBrowserFilterData.  # noqa: E501

        list of all unique namespaces to display  # noqa: E501

        :return: The namespaces of this GroupBrowserFilterData.  # noqa: E501
        :rtype: list[str]
        """
        return self._namespaces

    @namespaces.setter
    def namespaces(self, namespaces):
        """Sets the namespaces of this GroupBrowserFilterData.

        list of all unique namespaces to display  # noqa: E501

        :param namespaces: The namespaces of this GroupBrowserFilterData.  # noqa: E501
        :type: list[str]
        """

        self._namespaces = namespaces

    @property
    def group_types(self):
        """Gets the group_types of this GroupBrowserFilterData.  # noqa: E501

        list of all available group types to display  # noqa: E501

        :return: The group_types of this GroupBrowserFilterData.  # noqa: E501
        :rtype: list[GroupType]
        """
        return self._group_types

    @group_types.setter
    def group_types(self, group_types):
        """Sets the group_types of this GroupBrowserFilterData.

        list of all available group types to display  # noqa: E501

        :param group_types: The group_types of this GroupBrowserFilterData.  # noqa: E501
        :type: list[GroupType]
        """

        self._group_types = group_types

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
        if not isinstance(other, GroupBrowserFilterData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GroupBrowserFilterData):
            return True

        return self.to_dict() != other.to_dict()
