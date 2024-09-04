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


class UDFArrayDetails(object):
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
        "parameter_id": "str",
        "uri": "str",
        "ranges": "QueryRanges",
        "buffers": "list[str]",
    }

    attribute_map = {
        "parameter_id": "parameter_id",
        "uri": "uri",
        "ranges": "ranges",
        "buffers": "buffers",
    }

    def __init__(
        self,
        parameter_id=None,
        uri=None,
        ranges=None,
        buffers=None,
        local_vars_configuration=None,
    ):
        """UDFArrayDetails - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._parameter_id = None
        self._uri = None
        self._ranges = None
        self._buffers = None
        self.discriminator = None

        self.parameter_id = parameter_id
        if uri is not None:
            self.uri = uri
        if ranges is not None:
            self.ranges = ranges
        if buffers is not None:
            self.buffers = buffers

    @property
    def parameter_id(self):
        """Gets the parameter_id of this UDFArrayDetails.

        An optional client-generated identifier to distinguish between multiple range/buffer requests from the same array in the same call. This may be set for MultiArrayUDFs that use the `argument_json` style of passing arrays.

        :return: The parameter_id of this UDFArrayDetails.
        :rtype: str
        """
        return self._parameter_id

    @parameter_id.setter
    def parameter_id(self, parameter_id):
        """Sets the parameter_id of this UDFArrayDetails.

        An optional client-generated identifier to distinguish between multiple range/buffer requests from the same array in the same call. This may be set for MultiArrayUDFs that use the `argument_json` style of passing arrays.

        :param parameter_id: The parameter_id of this UDFArrayDetails.
        :type: str
        """

        self._parameter_id = parameter_id

    @property
    def uri(self):
        """Gets the uri of this UDFArrayDetails.

        array to set ranges and buffers on, must be in tiledb:// format

        :return: The uri of this UDFArrayDetails.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this UDFArrayDetails.

        array to set ranges and buffers on, must be in tiledb:// format

        :param uri: The uri of this UDFArrayDetails.
        :type: str
        """

        self._uri = uri

    @property
    def ranges(self):
        """Gets the ranges of this UDFArrayDetails.


        :return: The ranges of this UDFArrayDetails.
        :rtype: QueryRanges
        """
        return self._ranges

    @ranges.setter
    def ranges(self, ranges):
        """Sets the ranges of this UDFArrayDetails.


        :param ranges: The ranges of this UDFArrayDetails.
        :type: QueryRanges
        """

        self._ranges = ranges

    @property
    def buffers(self):
        """Gets the buffers of this UDFArrayDetails.

        List of buffers to fetch (attributes + dimensions)

        :return: The buffers of this UDFArrayDetails.
        :rtype: list[str]
        """
        return self._buffers

    @buffers.setter
    def buffers(self, buffers):
        """Sets the buffers of this UDFArrayDetails.

        List of buffers to fetch (attributes + dimensions)

        :param buffers: The buffers of this UDFArrayDetails.
        :type: list[str]
        """

        self._buffers = buffers

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
        if not isinstance(other, UDFArrayDetails):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UDFArrayDetails):
            return True

        return self.to_dict() != other.to_dict()
