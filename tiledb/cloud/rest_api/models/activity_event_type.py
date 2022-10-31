# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.2.19
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class ActivityEventType(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    allowed enum values
    """
    READ_SCHEMA = "read_schema"
    MAX_BUFFER_SIZES = "max_buffer_sizes"
    NON_EMPTY_DOMAIN = "non_empty_domain"
    QUERY_READ = "query_read"
    QUERY_WRITE = "query_write"
    QUERY_DELETE = "query_delete"
    CREATE = "create"
    DELETE = "delete"
    REGISTER = "register"
    DEREGISTER = "deregister"
    UDF = "udf"
    ARRAY_METADATA_GET = "array_metadata_get"
    ARRAY_METADATA_UPDATE = "array_metadata_update"
    ESTIMATED_RESULT_SIZES = "estimated_result_sizes"

    allowable_values = [
        READ_SCHEMA,
        MAX_BUFFER_SIZES,
        NON_EMPTY_DOMAIN,
        QUERY_READ,
        QUERY_WRITE,
        QUERY_DELETE,
        CREATE,
        DELETE,
        REGISTER,
        DEREGISTER,
        UDF,
        ARRAY_METADATA_GET,
        ARRAY_METADATA_UPDATE,
        ESTIMATED_RESULT_SIZES,
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
        """ActivityEventType - a model defined in OpenAPI"""  # noqa: E501
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
        if not isinstance(other, ActivityEventType):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ActivityEventType):
            return True

        return self.to_dict() != other.to_dict()
