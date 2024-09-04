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


class FragmentInfo(object):
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
        "array_schema_all": "dict(str, ArraySchema)",
        "fragment_info": "list[SingleFragmentInfo]",
        "to_vacuum": "list[str]",
    }

    attribute_map = {
        "array_schema_all": "arraySchemaAll",
        "fragment_info": "fragmentInfo",
        "to_vacuum": "toVacuum",
    }

    def __init__(
        self,
        array_schema_all=None,
        fragment_info=None,
        to_vacuum=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """FragmentInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._array_schema_all = None
        self._fragment_info = None
        self._to_vacuum = None
        self.discriminator = None

        if array_schema_all is not None:
            self.array_schema_all = array_schema_all
        if fragment_info is not None:
            self.fragment_info = fragment_info
        if to_vacuum is not None:
            self.to_vacuum = to_vacuum

    @property
    def array_schema_all(self):
        """Gets the array_schema_all of this FragmentInfo.  # noqa: E501

        map of all array schemas  # noqa: E501

        :return: The array_schema_all of this FragmentInfo.  # noqa: E501
        :rtype: dict(str, ArraySchema)
        """
        return self._array_schema_all

    @array_schema_all.setter
    def array_schema_all(self, array_schema_all):
        """Sets the array_schema_all of this FragmentInfo.

        map of all array schemas  # noqa: E501

        :param array_schema_all: The array_schema_all of this FragmentInfo.  # noqa: E501
        :type: dict(str, ArraySchema)
        """

        self._array_schema_all = array_schema_all

    @property
    def fragment_info(self):
        """Gets the fragment_info of this FragmentInfo.  # noqa: E501

        information about fragments in the array  # noqa: E501

        :return: The fragment_info of this FragmentInfo.  # noqa: E501
        :rtype: list[SingleFragmentInfo]
        """
        return self._fragment_info

    @fragment_info.setter
    def fragment_info(self, fragment_info):
        """Sets the fragment_info of this FragmentInfo.

        information about fragments in the array  # noqa: E501

        :param fragment_info: The fragment_info of this FragmentInfo.  # noqa: E501
        :type: list[SingleFragmentInfo]
        """

        self._fragment_info = fragment_info

    @property
    def to_vacuum(self):
        """Gets the to_vacuum of this FragmentInfo.  # noqa: E501

        the URIs of the fragments to vacuum  # noqa: E501

        :return: The to_vacuum of this FragmentInfo.  # noqa: E501
        :rtype: list[str]
        """
        return self._to_vacuum

    @to_vacuum.setter
    def to_vacuum(self, to_vacuum):
        """Sets the to_vacuum of this FragmentInfo.

        the URIs of the fragments to vacuum  # noqa: E501

        :param to_vacuum: The to_vacuum of this FragmentInfo.  # noqa: E501
        :type: list[str]
        """

        self._to_vacuum = to_vacuum

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
        if not isinstance(other, FragmentInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FragmentInfo):
            return True

        return self.to_dict() != other.to_dict()
