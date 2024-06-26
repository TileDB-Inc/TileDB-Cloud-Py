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


class TGInputNodeData(object):
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
    openapi_types = {"default_value": "object", "datatype": "str"}

    attribute_map = {"default_value": "default_value", "datatype": "datatype"}

    def __init__(
        self, default_value=None, datatype=None, local_vars_configuration=None
    ):  # noqa: E501
        """TGInputNodeData - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._default_value = None
        self._datatype = None
        self.discriminator = None

        if default_value is not None:
            self.default_value = default_value
        self.datatype = datatype

    @property
    def default_value(self):
        """Gets the default_value of this TGInputNodeData.  # noqa: E501

        An argument provided to a node. This is one of a direct value (i.e., a raw JSON value) or a `TGSentinel`. For example this Python value:      {\"a\": [1, \"pipe\", range(30), None], \"b\": b\"bytes\"}  is encoded thusly (with included comments):      {  // A dictionary with string keys is JSON-encodable.       \"a\": [  // As is a list.         1,         \"pipe\",         {  // A `range` is replaced with its pickle.           \"__tdbudf__\": \"immediate\",           \"format\": \"python_pickle\",           \"base64_data\": \"gASVIAAAAAAAAACMCGJ1aWx0aW5zlIwFcmFuZ2WUk5RLAEseSwGHlFKULg==\"         },         null       ],       \"b\": {  // Raw binary data is encoded into base64.         \"__tdbudf__\": \"immediate\"         \"format\": \"bytes\",         \"base64_data\": \"Ynl0ZXM=\"       }     }   # noqa: E501

        :return: The default_value of this TGInputNodeData.  # noqa: E501
        :rtype: object
        """
        return self._default_value

    @default_value.setter
    def default_value(self, default_value):
        """Sets the default_value of this TGInputNodeData.

        An argument provided to a node. This is one of a direct value (i.e., a raw JSON value) or a `TGSentinel`. For example this Python value:      {\"a\": [1, \"pipe\", range(30), None], \"b\": b\"bytes\"}  is encoded thusly (with included comments):      {  // A dictionary with string keys is JSON-encodable.       \"a\": [  // As is a list.         1,         \"pipe\",         {  // A `range` is replaced with its pickle.           \"__tdbudf__\": \"immediate\",           \"format\": \"python_pickle\",           \"base64_data\": \"gASVIAAAAAAAAACMCGJ1aWx0aW5zlIwFcmFuZ2WUk5RLAEseSwGHlFKULg==\"         },         null       ],       \"b\": {  // Raw binary data is encoded into base64.         \"__tdbudf__\": \"immediate\"         \"format\": \"bytes\",         \"base64_data\": \"Ynl0ZXM=\"       }     }   # noqa: E501

        :param default_value: The default_value of this TGInputNodeData.  # noqa: E501
        :type: object
        """

        self._default_value = default_value

    @property
    def datatype(self):
        """Gets the datatype of this TGInputNodeData.  # noqa: E501

        An annotation of what datatype this node is supposed to be. Conventionally, this is a Python-format type annotation, but it’s purely for documentation purposes and not validated.   # noqa: E501

        :return: The datatype of this TGInputNodeData.  # noqa: E501
        :rtype: str
        """
        return self._datatype

    @datatype.setter
    def datatype(self, datatype):
        """Sets the datatype of this TGInputNodeData.

        An annotation of what datatype this node is supposed to be. Conventionally, this is a Python-format type annotation, but it’s purely for documentation purposes and not validated.   # noqa: E501

        :param datatype: The datatype of this TGInputNodeData.  # noqa: E501
        :type: str
        """

        self._datatype = datatype

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
        if not isinstance(other, TGInputNodeData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TGInputNodeData):
            return True

        return self.to_dict() != other.to_dict()
