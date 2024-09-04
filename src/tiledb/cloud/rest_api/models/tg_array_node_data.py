# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint

from tiledb.cloud.rest_api.configuration import Configuration


class TGArrayNodeData:
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
    openapi_types = {"uri": "object", "ranges": "TGQueryRanges", "buffers": "object"}

    attribute_map = {"uri": "uri", "ranges": "ranges", "buffers": "buffers"}

    def __init__(
        self, uri=None, ranges=None, buffers=None, local_vars_configuration=None
    ):
        """TGArrayNodeData - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._uri = None
        self._ranges = None
        self._buffers = None
        self.discriminator = None

        if uri is not None:
            self.uri = uri
        if ranges is not None:
            self.ranges = ranges
        if buffers is not None:
            self.buffers = buffers

    @property
    def uri(self):
        """Gets the uri of this TGArrayNodeData.

        An argument provided to a node. This is one of a direct value (i.e., a raw JSON value) or a `TGSentinel`. For example this Python value:      {\"a\": [1, \"pipe\", range(30), None], \"b\": b\"bytes\"}  is encoded thusly (with included comments):      {  // A dictionary with string keys is JSON-encodable.       \"a\": [  // As is a list.         1,         \"pipe\",         {  // A `range` is replaced with its pickle.           \"__tdbudf__\": \"immediate\",           \"format\": \"python_pickle\",           \"base64_data\": \"gASVIAAAAAAAAACMCGJ1aWx0aW5zlIwFcmFuZ2WUk5RLAEseSwGHlFKULg==\"         },         null       ],       \"b\": {  // Raw binary data is encoded into base64.         \"__tdbudf__\": \"immediate\"         \"format\": \"bytes\",         \"base64_data\": \"Ynl0ZXM=\"       }     }

        :return: The uri of this TGArrayNodeData.
        :rtype: object
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this TGArrayNodeData.

        An argument provided to a node. This is one of a direct value (i.e., a raw JSON value) or a `TGSentinel`. For example this Python value:      {\"a\": [1, \"pipe\", range(30), None], \"b\": b\"bytes\"}  is encoded thusly (with included comments):      {  // A dictionary with string keys is JSON-encodable.       \"a\": [  // As is a list.         1,         \"pipe\",         {  // A `range` is replaced with its pickle.           \"__tdbudf__\": \"immediate\",           \"format\": \"python_pickle\",           \"base64_data\": \"gASVIAAAAAAAAACMCGJ1aWx0aW5zlIwFcmFuZ2WUk5RLAEseSwGHlFKULg==\"         },         null       ],       \"b\": {  // Raw binary data is encoded into base64.         \"__tdbudf__\": \"immediate\"         \"format\": \"bytes\",         \"base64_data\": \"Ynl0ZXM=\"       }     }

        :param uri: The uri of this TGArrayNodeData.
        :type: object
        """

        self._uri = uri

    @property
    def ranges(self):
        """Gets the ranges of this TGArrayNodeData.


        :return: The ranges of this TGArrayNodeData.
        :rtype: TGQueryRanges
        """
        return self._ranges

    @ranges.setter
    def ranges(self, ranges):
        """Sets the ranges of this TGArrayNodeData.


        :param ranges: The ranges of this TGArrayNodeData.
        :type: TGQueryRanges
        """

        self._ranges = ranges

    @property
    def buffers(self):
        """Gets the buffers of this TGArrayNodeData.

        An argument provided to a node. This is one of a direct value (i.e., a raw JSON value) or a `TGSentinel`. For example this Python value:      {\"a\": [1, \"pipe\", range(30), None], \"b\": b\"bytes\"}  is encoded thusly (with included comments):      {  // A dictionary with string keys is JSON-encodable.       \"a\": [  // As is a list.         1,         \"pipe\",         {  // A `range` is replaced with its pickle.           \"__tdbudf__\": \"immediate\",           \"format\": \"python_pickle\",           \"base64_data\": \"gASVIAAAAAAAAACMCGJ1aWx0aW5zlIwFcmFuZ2WUk5RLAEseSwGHlFKULg==\"         },         null       ],       \"b\": {  // Raw binary data is encoded into base64.         \"__tdbudf__\": \"immediate\"         \"format\": \"bytes\",         \"base64_data\": \"Ynl0ZXM=\"       }     }

        :return: The buffers of this TGArrayNodeData.
        :rtype: object
        """
        return self._buffers

    @buffers.setter
    def buffers(self, buffers):
        """Sets the buffers of this TGArrayNodeData.

        An argument provided to a node. This is one of a direct value (i.e., a raw JSON value) or a `TGSentinel`. For example this Python value:      {\"a\": [1, \"pipe\", range(30), None], \"b\": b\"bytes\"}  is encoded thusly (with included comments):      {  // A dictionary with string keys is JSON-encodable.       \"a\": [  // As is a list.         1,         \"pipe\",         {  // A `range` is replaced with its pickle.           \"__tdbudf__\": \"immediate\",           \"format\": \"python_pickle\",           \"base64_data\": \"gASVIAAAAAAAAACMCGJ1aWx0aW5zlIwFcmFuZ2WUk5RLAEseSwGHlFKULg==\"         },         null       ],       \"b\": {  // Raw binary data is encoded into base64.         \"__tdbudf__\": \"immediate\"         \"format\": \"bytes\",         \"base64_data\": \"Ynl0ZXM=\"       }     }

        :param buffers: The buffers of this TGArrayNodeData.
        :type: object
        """

        self._buffers = buffers

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in self.openapi_types.items():
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
        if not isinstance(other, TGArrayNodeData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TGArrayNodeData):
            return True

        return self.to_dict() != other.to_dict()
