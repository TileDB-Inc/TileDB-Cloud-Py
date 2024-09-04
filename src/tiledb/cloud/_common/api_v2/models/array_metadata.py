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


class ArrayMetadata(object):
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
    openapi_types = {"entries": "list[ArrayMetadataEntry]"}

    attribute_map = {"entries": "entries"}

    def __init__(self, entries=None, local_vars_configuration=None):
        """ArrayMetadata - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._entries = None
        self.discriminator = None

        if entries is not None:
            self.entries = entries

    @property
    def entries(self):
        """Gets the entries of this ArrayMetadata.

        List of metadata entries

        :return: The entries of this ArrayMetadata.
        :rtype: list[ArrayMetadataEntry]
        """
        return self._entries

    @entries.setter
    def entries(self, entries):
        """Sets the entries of this ArrayMetadata.

        List of metadata entries

        :param entries: The entries of this ArrayMetadata.
        :type: list[ArrayMetadataEntry]
        """

        self._entries = entries

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
        if not isinstance(other, ArrayMetadata):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ArrayMetadata):
            return True

        return self.to_dict() != other.to_dict()
