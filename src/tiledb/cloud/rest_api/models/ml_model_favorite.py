# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint

from tiledb.cloud.rest_api.configuration import Configuration


class MLModelFavorite(object):
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
    openapi_types = {"mlmodel_uuid": "str", "namespace": "str", "name": "str"}

    attribute_map = {
        "mlmodel_uuid": "mlmodel_uuid",
        "namespace": "namespace",
        "name": "name",
    }

    def __init__(
        self,
        mlmodel_uuid=None,
        namespace=None,
        name=None,
        local_vars_configuration=None,
    ):
        """MLModelFavorite - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._mlmodel_uuid = None
        self._namespace = None
        self._name = None
        self.discriminator = None

        if mlmodel_uuid is not None:
            self.mlmodel_uuid = mlmodel_uuid
        if namespace is not None:
            self.namespace = namespace
        if name is not None:
            self.name = name

    @property
    def mlmodel_uuid(self):
        """Gets the mlmodel_uuid of this MLModelFavorite.

        unique UUID of the MLModel

        :return: The mlmodel_uuid of this MLModelFavorite.
        :rtype: str
        """
        return self._mlmodel_uuid

    @mlmodel_uuid.setter
    def mlmodel_uuid(self, mlmodel_uuid):
        """Sets the mlmodel_uuid of this MLModelFavorite.

        unique UUID of the MLModel

        :param mlmodel_uuid: The mlmodel_uuid of this MLModelFavorite.
        :type: str
        """

        self._mlmodel_uuid = mlmodel_uuid

    @property
    def namespace(self):
        """Gets the namespace of this MLModelFavorite.

        the namespace of the MLModel

        :return: The namespace of this MLModelFavorite.
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this MLModelFavorite.

        the namespace of the MLModel

        :param namespace: The namespace of this MLModelFavorite.
        :type: str
        """

        self._namespace = namespace

    @property
    def name(self):
        """Gets the name of this MLModelFavorite.

        the name of the MLModel

        :return: The name of this MLModelFavorite.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MLModelFavorite.

        the name of the MLModel

        :param name: The name of this MLModelFavorite.
        :type: str
        """

        self._name = name

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
        if not isinstance(other, MLModelFavorite):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MLModelFavorite):
            return True

        return self.to_dict() != other.to_dict()
