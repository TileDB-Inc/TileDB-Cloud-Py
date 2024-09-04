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


class NotebookCopy(object):
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
    openapi_types = {"output_uri": "str", "name": "str", "namespace": "str"}

    attribute_map = {
        "output_uri": "output_uri",
        "name": "name",
        "namespace": "namespace",
    }

    def __init__(
        self, output_uri=None, name=None, namespace=None, local_vars_configuration=None
    ):
        """NotebookCopy - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._output_uri = None
        self._name = None
        self._namespace = None
        self.discriminator = None

        if output_uri is not None:
            self.output_uri = output_uri
        if name is not None:
            self.name = name
        if namespace is not None:
            self.namespace = namespace

    @property
    def output_uri(self):
        """Gets the output_uri of this NotebookCopy.

        output location of the TileDB File

        :return: The output_uri of this NotebookCopy.
        :rtype: str
        """
        return self._output_uri

    @output_uri.setter
    def output_uri(self, output_uri):
        """Sets the output_uri of this NotebookCopy.

        output location of the TileDB File

        :param output_uri: The output_uri of this NotebookCopy.
        :type: str
        """

        self._output_uri = output_uri

    @property
    def name(self):
        """Gets the name of this NotebookCopy.

        name to set for registered notebook

        :return: The name of this NotebookCopy.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this NotebookCopy.

        name to set for registered notebook

        :param name: The name of this NotebookCopy.
        :type: str
        """

        self._name = name

    @property
    def namespace(self):
        """Gets the namespace of this NotebookCopy.

        namespace to copy to

        :return: The namespace of this NotebookCopy.
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this NotebookCopy.

        namespace to copy to

        :param namespace: The namespace of this NotebookCopy.
        :type: str
        """

        self._namespace = namespace

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
        if not isinstance(other, NotebookCopy):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NotebookCopy):
            return True

        return self.to_dict() != other.to_dict()
