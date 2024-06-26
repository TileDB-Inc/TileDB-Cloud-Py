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


class QueryJson(object):
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
    openapi_types = {"query_ranges": "QueryRanges", "fields": "list[str]"}

    attribute_map = {"query_ranges": "query_ranges", "fields": "fields"}

    def __init__(
        self, query_ranges=None, fields=None, local_vars_configuration=None
    ):  # noqa: E501
        """QueryJson - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._query_ranges = None
        self._fields = None
        self.discriminator = None

        if query_ranges is not None:
            self.query_ranges = query_ranges
        if fields is not None:
            self.fields = fields

    @property
    def query_ranges(self):
        """Gets the query_ranges of this QueryJson.  # noqa: E501


        :return: The query_ranges of this QueryJson.  # noqa: E501
        :rtype: QueryRanges
        """
        return self._query_ranges

    @query_ranges.setter
    def query_ranges(self, query_ranges):
        """Sets the query_ranges of this QueryJson.


        :param query_ranges: The query_ranges of this QueryJson.  # noqa: E501
        :type: QueryRanges
        """

        self._query_ranges = query_ranges

    @property
    def fields(self):
        """Gets the fields of this QueryJson.  # noqa: E501

        List of fields to return data from, empty means return data for all fields  # noqa: E501

        :return: The fields of this QueryJson.  # noqa: E501
        :rtype: list[str]
        """
        return self._fields

    @fields.setter
    def fields(self, fields):
        """Sets the fields of this QueryJson.

        List of fields to return data from, empty means return data for all fields  # noqa: E501

        :param fields: The fields of this QueryJson.  # noqa: E501
        :type: list[str]
        """

        self._fields = fields

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
        if not isinstance(other, QueryJson):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, QueryJson):
            return True

        return self.to_dict() != other.to_dict()
