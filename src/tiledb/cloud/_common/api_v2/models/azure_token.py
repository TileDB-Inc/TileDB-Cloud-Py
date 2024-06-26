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

from tiledb.cloud._common.api_v2.configuration import Configuration


class AzureToken(object):
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
    openapi_types = {"account_name": "str", "sas_token": "str"}

    attribute_map = {"account_name": "account_name", "sas_token": "sas_token"}

    def __init__(
        self, account_name=None, sas_token=None, local_vars_configuration=None
    ):  # noqa: E501
        """AzureToken - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._account_name = None
        self._sas_token = None
        self.discriminator = None

        if account_name is not None:
            self.account_name = account_name
        if sas_token is not None:
            self.sas_token = sas_token

    @property
    def account_name(self):
        """Gets the account_name of this AzureToken.  # noqa: E501

        The account name of the configuration  # noqa: E501

        :return: The account_name of this AzureToken.  # noqa: E501
        :rtype: str
        """
        return self._account_name

    @account_name.setter
    def account_name(self, account_name):
        """Sets the account_name of this AzureToken.

        The account name of the configuration  # noqa: E501

        :param account_name: The account_name of this AzureToken.  # noqa: E501
        :type: str
        """

        self._account_name = account_name

    @property
    def sas_token(self):
        """Gets the sas_token of this AzureToken.  # noqa: E501

        The token to use for this account  # noqa: E501

        :return: The sas_token of this AzureToken.  # noqa: E501
        :rtype: str
        """
        return self._sas_token

    @sas_token.setter
    def sas_token(self, sas_token):
        """Sets the sas_token of this AzureToken.

        The token to use for this account  # noqa: E501

        :param sas_token: The sas_token of this AzureToken.  # noqa: E501
        :type: str
        """

        self._sas_token = sas_token

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
        if not isinstance(other, AzureToken):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AzureToken):
            return True

        return self.to_dict() != other.to_dict()
