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


class AccessCredential(object):
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
        'name': 'str',
        'provider': 'CloudProvider',
        'provider_default': 'bool',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'credential': 'AccessCredentialCredential',
        'role': 'AccessCredentialRole'
    }

    attribute_map = {
        'name': 'name',
        'provider': 'provider',
        'provider_default': 'provider_default',
        'created_at': 'created_at',
        'updated_at': 'updated_at',
        'credential': 'credential',
        'role': 'role'
    }

    def __init__(self, name=None, provider=None, provider_default=None, created_at=None, updated_at=None, credential=None, role=None, local_vars_configuration=None):  # noqa: E501
        """AccessCredential - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._provider = None
        self._provider_default = None
        self._created_at = None
        self._updated_at = None
        self._credential = None
        self._role = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if provider is not None:
            self.provider = provider
        self.provider_default = provider_default
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if credential is not None:
            self.credential = credential
        if role is not None:
            self.role = role

    @property
    def name(self):
        """Gets the name of this AccessCredential.  # noqa: E501

        A user-specified name for the key  # noqa: E501

        :return: The name of this AccessCredential.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AccessCredential.

        A user-specified name for the key  # noqa: E501

        :param name: The name of this AccessCredential.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def provider(self):
        """Gets the provider of this AccessCredential.  # noqa: E501


        :return: The provider of this AccessCredential.  # noqa: E501
        :rtype: CloudProvider
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """Sets the provider of this AccessCredential.


        :param provider: The provider of this AccessCredential.  # noqa: E501
        :type: CloudProvider
        """

        self._provider = provider

    @property
    def provider_default(self):
        """Gets the provider_default of this AccessCredential.  # noqa: E501

        True if this is the namespace's default credential to be used when connecting to the given cloud provider. There can be at most one default for each unique provider.  # noqa: E501

        :return: The provider_default of this AccessCredential.  # noqa: E501
        :rtype: bool
        """
        return self._provider_default

    @provider_default.setter
    def provider_default(self, provider_default):
        """Sets the provider_default of this AccessCredential.

        True if this is the namespace's default credential to be used when connecting to the given cloud provider. There can be at most one default for each unique provider.  # noqa: E501

        :param provider_default: The provider_default of this AccessCredential.  # noqa: E501
        :type: bool
        """

        self._provider_default = provider_default

    @property
    def created_at(self):
        """Gets the created_at of this AccessCredential.  # noqa: E501

        Time when the credential was created (rfc3339)  # noqa: E501

        :return: The created_at of this AccessCredential.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this AccessCredential.

        Time when the credential was created (rfc3339)  # noqa: E501

        :param created_at: The created_at of this AccessCredential.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this AccessCredential.  # noqa: E501

        Time when the credential was last updated (rfc3339)  # noqa: E501

        :return: The updated_at of this AccessCredential.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this AccessCredential.

        Time when the credential was last updated (rfc3339)  # noqa: E501

        :param updated_at: The updated_at of this AccessCredential.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def credential(self):
        """Gets the credential of this AccessCredential.  # noqa: E501


        :return: The credential of this AccessCredential.  # noqa: E501
        :rtype: AccessCredentialCredential
        """
        return self._credential

    @credential.setter
    def credential(self, credential):
        """Sets the credential of this AccessCredential.


        :param credential: The credential of this AccessCredential.  # noqa: E501
        :type: AccessCredentialCredential
        """

        self._credential = credential

    @property
    def role(self):
        """Gets the role of this AccessCredential.  # noqa: E501


        :return: The role of this AccessCredential.  # noqa: E501
        :rtype: AccessCredentialRole
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this AccessCredential.


        :param role: The role of this AccessCredential.  # noqa: E501
        :type: AccessCredentialRole
        """

        self._role = role

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
        if not isinstance(other, AccessCredential):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AccessCredential):
            return True

        return self.to_dict() != other.to_dict()
