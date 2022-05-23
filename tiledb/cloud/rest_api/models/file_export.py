# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec

import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class FileExport(object):
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
    openapi_types = {"output_uri": "str"}

    attribute_map = {"output_uri": "output_uri"}

    def __init__(self, output_uri=None, local_vars_configuration=None):  # noqa: E501
        """FileExport - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._output_uri = None
        self.discriminator = None

        if output_uri is not None:
            self.output_uri = output_uri

    @property
    def output_uri(self):
        """Gets the output_uri of this FileExport.  # noqa: E501

        output location of the TileDB File  # noqa: E501

        :return: The output_uri of this FileExport.  # noqa: E501
        :rtype: str
        """
        return self._output_uri

    @output_uri.setter
    def output_uri(self, output_uri):
        """Sets the output_uri of this FileExport.

        output location of the TileDB File  # noqa: E501

        :param output_uri: The output_uri of this FileExport.  # noqa: E501
        :type output_uri: str
        """

        self._output_uri = output_uri

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(lambda x: convert(x), value))
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(lambda item: (item[0], convert(item[1])), value.items())
                )
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, FileExport):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FileExport):
            return True

        return self.to_dict() != other.to_dict()
