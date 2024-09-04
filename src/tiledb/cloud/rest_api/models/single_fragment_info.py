# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint

import six

from tiledb.cloud.rest_api.configuration import Configuration


class SingleFragmentInfo(object):
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
    openapi_types = {"array_schema_name": "str", "meta": "FragmentMetadata"}

    attribute_map = {"array_schema_name": "ArraySchemaName", "meta": "meta"}

    def __init__(
        self, array_schema_name=None, meta=None, local_vars_configuration=None
    ):
        """SingleFragmentInfo - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._array_schema_name = None
        self._meta = None
        self.discriminator = None

        if array_schema_name is not None:
            self.array_schema_name = array_schema_name
        if meta is not None:
            self.meta = meta

    @property
    def array_schema_name(self):
        """Gets the array_schema_name of this SingleFragmentInfo.

        array schema name

        :return: The array_schema_name of this SingleFragmentInfo.
        :rtype: str
        """
        return self._array_schema_name

    @array_schema_name.setter
    def array_schema_name(self, array_schema_name):
        """Sets the array_schema_name of this SingleFragmentInfo.

        array schema name

        :param array_schema_name: The array_schema_name of this SingleFragmentInfo.
        :type: str
        """

        self._array_schema_name = array_schema_name

    @property
    def meta(self):
        """Gets the meta of this SingleFragmentInfo.


        :return: The meta of this SingleFragmentInfo.
        :rtype: FragmentMetadata
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """Sets the meta of this SingleFragmentInfo.


        :param meta: The meta of this SingleFragmentInfo.
        :type: FragmentMetadata
        """

        self._meta = meta

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
        if not isinstance(other, SingleFragmentInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SingleFragmentInfo):
            return True

        return self.to_dict() != other.to_dict()
