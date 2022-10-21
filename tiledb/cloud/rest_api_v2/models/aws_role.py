# coding: utf-8

"""
    Tiledb Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 1.4.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api_v2.configuration import Configuration


class AWSRole(object):
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
        'role_arn': 'str',
        'external_id': 'str',
        'endpoint': 'str'
    }

    attribute_map = {
        'role_arn': 'role_arn',
        'external_id': 'external_id',
        'endpoint': 'endpoint'
    }

    def __init__(self, role_arn=None, external_id=None, endpoint=None, local_vars_configuration=None):  # noqa: E501
        """AWSRole - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._role_arn = None
        self._external_id = None
        self._endpoint = None
        self.discriminator = None

        if role_arn is not None:
            self.role_arn = role_arn
        if external_id is not None:
            self.external_id = external_id
        self.endpoint = endpoint

    @property
    def role_arn(self):
        """Gets the role_arn of this AWSRole.  # noqa: E501

        The role arn used to access  # noqa: E501

        :return: The role_arn of this AWSRole.  # noqa: E501
        :rtype: str
        """
        return self._role_arn

    @role_arn.setter
    def role_arn(self, role_arn):
        """Sets the role_arn of this AWSRole.

        The role arn used to access  # noqa: E501

        :param role_arn: The role_arn of this AWSRole.  # noqa: E501
        :type: str
        """

        self._role_arn = role_arn

    @property
    def external_id(self):
        """Gets the external_id of this AWSRole.  # noqa: E501

        The role external id used to access  # noqa: E501

        :return: The external_id of this AWSRole.  # noqa: E501
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        """Sets the external_id of this AWSRole.

        The role external id used to access  # noqa: E501

        :param external_id: The external_id of this AWSRole.  # noqa: E501
        :type: str
        """

        self._external_id = external_id

    @property
    def endpoint(self):
        """Gets the endpoint of this AWSRole.  # noqa: E501

        The endpoint used for this role  # noqa: E501

        :return: The endpoint of this AWSRole.  # noqa: E501
        :rtype: str
        """
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint):
        """Sets the endpoint of this AWSRole.

        The endpoint used for this role  # noqa: E501

        :param endpoint: The endpoint of this AWSRole.  # noqa: E501
        :type: str
        """

        self._endpoint = endpoint

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
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
        if not isinstance(other, AWSRole):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AWSRole):
            return True

        return self.to_dict() != other.to_dict()
