# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.1.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class SQLParameters(object):
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
    openapi_types = {"name": "str", "query": "str", "output_uri": "str"}

    attribute_map = {"name": "name", "query": "query", "output_uri": "output_uri"}

    def __init__(
        self, name=None, query=None, output_uri=None, local_vars_configuration=None
    ):  # noqa: E501
        """SQLParameters - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._query = None
        self._output_uri = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if query is not None:
            self.query = query
        if output_uri is not None:
            self.output_uri = output_uri

    @property
    def name(self):
        """Gets the name of this SQLParameters.  # noqa: E501

        name of task, optional  # noqa: E501

        :return: The name of this SQLParameters.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SQLParameters.

        name of task, optional  # noqa: E501

        :param name: The name of this SQLParameters.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def query(self):
        """Gets the query of this SQLParameters.  # noqa: E501

        query to run  # noqa: E501

        :return: The query of this SQLParameters.  # noqa: E501
        :rtype: str
        """
        return self._query

    @query.setter
    def query(self, query):
        """Sets the query of this SQLParameters.

        query to run  # noqa: E501

        :param query: The query of this SQLParameters.  # noqa: E501
        :type: str
        """

        self._query = query

    @property
    def output_uri(self):
        """Gets the output_uri of this SQLParameters.  # noqa: E501

        Output array uri  # noqa: E501

        :return: The output_uri of this SQLParameters.  # noqa: E501
        :rtype: str
        """
        return self._output_uri

    @output_uri.setter
    def output_uri(self, output_uri):
        """Sets the output_uri of this SQLParameters.

        Output array uri  # noqa: E501

        :param output_uri: The output_uri of this SQLParameters.  # noqa: E501
        :type: str
        """

        self._output_uri = output_uri

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
        if not isinstance(other, SQLParameters):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SQLParameters):
            return True

        return self.to_dict() != other.to_dict()
