# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


import pprint

import six

from tiledb.cloud._common.api_v2.configuration import Configuration


class Datatype(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    allowed enum values
    """
    INT32 = "INT32"
    INT64 = "INT64"
    FLOAT32 = "FLOAT32"
    FLOAT64 = "FLOAT64"
    CHAR = "CHAR"
    INT8 = "INT8"
    UINT8 = "UINT8"
    INT16 = "INT16"
    UINT16 = "UINT16"
    UINT32 = "UINT32"
    UINT64 = "UINT64"
    STRING_ASCII = "STRING_ASCII"
    STRING_UTF8 = "STRING_UTF8"
    STRING_UTF16 = "STRING_UTF16"
    STRING_UTF32 = "STRING_UTF32"
    STRING_UCS2 = "STRING_UCS2"
    STRING_UCS4 = "STRING_UCS4"
    ANY = "ANY"
    DATETIME_YEAR = "DATETIME_YEAR"
    DATETIME_MONTH = "DATETIME_MONTH"
    DATETIME_WEEK = "DATETIME_WEEK"
    DATETIME_DAY = "DATETIME_DAY"
    DATETIME_HR = "DATETIME_HR"
    DATETIME_MIN = "DATETIME_MIN"
    DATETIME_SEC = "DATETIME_SEC"
    DATETIME_MS = "DATETIME_MS"
    DATETIME_US = "DATETIME_US"
    DATETIME_NS = "DATETIME_NS"
    DATETIME_PS = "DATETIME_PS"
    DATETIME_FS = "DATETIME_FS"
    DATETIME_AS = "DATETIME_AS"
    TIME_HR = "TIME_HR"
    TIME_MIN = "TIME_MIN"
    TIME_SEC = "TIME_SEC"
    TIME_MS = "TIME_MS"
    TIME_US = "TIME_US"
    TIME_NS = "TIME_NS"
    TIME_PS = "TIME_PS"
    TIME_FS = "TIME_FS"
    TIME_AS = "TIME_AS"
    BLOB = "BLOB"
    BOOL = "BOOL"

    allowable_values = [
        INT32,
        INT64,
        FLOAT32,
        FLOAT64,
        CHAR,
        INT8,
        UINT8,
        INT16,
        UINT16,
        UINT32,
        UINT64,
        STRING_ASCII,
        STRING_UTF8,
        STRING_UTF16,
        STRING_UTF32,
        STRING_UCS2,
        STRING_UCS4,
        ANY,
        DATETIME_YEAR,
        DATETIME_MONTH,
        DATETIME_WEEK,
        DATETIME_DAY,
        DATETIME_HR,
        DATETIME_MIN,
        DATETIME_SEC,
        DATETIME_MS,
        DATETIME_US,
        DATETIME_NS,
        DATETIME_PS,
        DATETIME_FS,
        DATETIME_AS,
        TIME_HR,
        TIME_MIN,
        TIME_SEC,
        TIME_MS,
        TIME_US,
        TIME_NS,
        TIME_PS,
        TIME_FS,
        TIME_AS,
        BLOB,
        BOOL,
    ]  # noqa: E501

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {}

    attribute_map = {}

    def __init__(self, local_vars_configuration=None):  # noqa: E501
        """Datatype - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration
        self.discriminator = None

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
        if not isinstance(other, Datatype):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Datatype):
            return True

        return self.to_dict() != other.to_dict()
