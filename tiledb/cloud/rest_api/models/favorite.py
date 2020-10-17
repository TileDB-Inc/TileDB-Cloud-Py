# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.0.13
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class Favorite(object):
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
        "id": "str",
        "object_type": "FavoriteType",
        "namespace": "str",
        "name": "str",
    }

    attribute_map = {
        "id": "id",
        "object_type": "object_type",
        "namespace": "namespace",
        "name": "name",
    }

    def __init__(
        self, id=None, object_type=None, namespace=None, name=None
    ):  # noqa: E501
        """Favorite - a model defined in OpenAPI"""  # noqa: E501

        self._id = None
        self._object_type = None
        self._namespace = None
        self._name = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if object_type is not None:
            self.object_type = object_type
        if namespace is not None:
            self.namespace = namespace
        if name is not None:
            self.name = name

    @property
    def id(self):
        """Gets the id of this Favorite.  # noqa: E501

        unique uuid of the favorite   # noqa: E501

        :return: The id of this Favorite.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Favorite.

        unique uuid of the favorite   # noqa: E501

        :param id: The id of this Favorite.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def object_type(self):
        """Gets the object_type of this Favorite.  # noqa: E501


        :return: The object_type of this Favorite.  # noqa: E501
        :rtype: FavoriteType
        """
        return self._object_type

    @object_type.setter
    def object_type(self, object_type):
        """Sets the object_type of this Favorite.


        :param object_type: The object_type of this Favorite.  # noqa: E501
        :type: FavoriteType
        """

        self._object_type = object_type

    @property
    def namespace(self):
        """Gets the namespace of this Favorite.  # noqa: E501

        The namespace the favorite is in. It won't be persisted in DB  # noqa: E501

        :return: The namespace of this Favorite.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this Favorite.

        The namespace the favorite is in. It won't be persisted in DB  # noqa: E501

        :param namespace: The namespace of this Favorite.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def name(self):
        """Gets the name of this Favorite.  # noqa: E501

        Name of the object. It wont be persisted in DB  # noqa: E501

        :return: The name of this Favorite.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Favorite.

        Name of the object. It wont be persisted in DB  # noqa: E501

        :param name: The name of this Favorite.  # noqa: E501
        :type: str
        """

        self._name = name

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
        if not isinstance(other, Favorite):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
