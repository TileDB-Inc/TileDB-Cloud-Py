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


class QueryReader(object):
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
        "layout": "Layout",
        "subarray": "Subarray",
        "read_state": "ReadState",
        "var_offsets_mode": "str",
        "var_offsets_add_extra_element": "bool",
        "var_offsets_bitsize": "int",
    }

    attribute_map = {
        "layout": "layout",
        "subarray": "subarray",
        "read_state": "readState",
        "var_offsets_mode": "varOffsetsMode",
        "var_offsets_add_extra_element": "varOffsetsAddExtraElement",
        "var_offsets_bitsize": "varOffsetsBitsize",
    }

    def __init__(
        self,
        layout=None,
        subarray=None,
        read_state=None,
        var_offsets_mode=None,
        var_offsets_add_extra_element=None,
        var_offsets_bitsize=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """QueryReader - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._layout = None
        self._subarray = None
        self._read_state = None
        self._var_offsets_mode = None
        self._var_offsets_add_extra_element = None
        self._var_offsets_bitsize = None
        self.discriminator = None

        if layout is not None:
            self.layout = layout
        if subarray is not None:
            self.subarray = subarray
        if read_state is not None:
            self.read_state = read_state
        if var_offsets_mode is not None:
            self.var_offsets_mode = var_offsets_mode
        if var_offsets_add_extra_element is not None:
            self.var_offsets_add_extra_element = var_offsets_add_extra_element
        if var_offsets_bitsize is not None:
            self.var_offsets_bitsize = var_offsets_bitsize

    @property
    def layout(self):
        """Gets the layout of this QueryReader.  # noqa: E501


        :return: The layout of this QueryReader.  # noqa: E501
        :rtype: Layout
        """
        return self._layout

    @layout.setter
    def layout(self, layout):
        """Sets the layout of this QueryReader.


        :param layout: The layout of this QueryReader.  # noqa: E501
        :type: Layout
        """

        self._layout = layout

    @property
    def subarray(self):
        """Gets the subarray of this QueryReader.  # noqa: E501


        :return: The subarray of this QueryReader.  # noqa: E501
        :rtype: Subarray
        """
        return self._subarray

    @subarray.setter
    def subarray(self, subarray):
        """Sets the subarray of this QueryReader.


        :param subarray: The subarray of this QueryReader.  # noqa: E501
        :type: Subarray
        """

        self._subarray = subarray

    @property
    def read_state(self):
        """Gets the read_state of this QueryReader.  # noqa: E501


        :return: The read_state of this QueryReader.  # noqa: E501
        :rtype: ReadState
        """
        return self._read_state

    @read_state.setter
    def read_state(self, read_state):
        """Sets the read_state of this QueryReader.


        :param read_state: The read_state of this QueryReader.  # noqa: E501
        :type: ReadState
        """

        self._read_state = read_state

    @property
    def var_offsets_mode(self):
        """Gets the var_offsets_mode of this QueryReader.  # noqa: E501

        The offsets format (bytes or elements) to be used.  # noqa: E501

        :return: The var_offsets_mode of this QueryReader.  # noqa: E501
        :rtype: str
        """
        return self._var_offsets_mode

    @var_offsets_mode.setter
    def var_offsets_mode(self, var_offsets_mode):
        """Sets the var_offsets_mode of this QueryReader.

        The offsets format (bytes or elements) to be used.  # noqa: E501

        :param var_offsets_mode: The var_offsets_mode of this QueryReader.  # noqa: E501
        :type: str
        """

        self._var_offsets_mode = var_offsets_mode

    @property
    def var_offsets_add_extra_element(self):
        """Gets the var_offsets_add_extra_element of this QueryReader.  # noqa: E501

        True if an extra element will be added to the end of the offsets buffer.  # noqa: E501

        :return: The var_offsets_add_extra_element of this QueryReader.  # noqa: E501
        :rtype: bool
        """
        return self._var_offsets_add_extra_element

    @var_offsets_add_extra_element.setter
    def var_offsets_add_extra_element(self, var_offsets_add_extra_element):
        """Sets the var_offsets_add_extra_element of this QueryReader.

        True if an extra element will be added to the end of the offsets buffer.  # noqa: E501

        :param var_offsets_add_extra_element: The var_offsets_add_extra_element of this QueryReader.  # noqa: E501
        :type: bool
        """

        self._var_offsets_add_extra_element = var_offsets_add_extra_element

    @property
    def var_offsets_bitsize(self):
        """Gets the var_offsets_bitsize of this QueryReader.  # noqa: E501

        The offsets bitsize (32 or 64) to be used.  # noqa: E501

        :return: The var_offsets_bitsize of this QueryReader.  # noqa: E501
        :rtype: int
        """
        return self._var_offsets_bitsize

    @var_offsets_bitsize.setter
    def var_offsets_bitsize(self, var_offsets_bitsize):
        """Sets the var_offsets_bitsize of this QueryReader.

        The offsets bitsize (32 or 64) to be used.  # noqa: E501

        :param var_offsets_bitsize: The var_offsets_bitsize of this QueryReader.  # noqa: E501
        :type: int
        """

        self._var_offsets_bitsize = var_offsets_bitsize

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
        if not isinstance(other, QueryReader):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, QueryReader):
            return True

        return self.to_dict() != other.to_dict()
