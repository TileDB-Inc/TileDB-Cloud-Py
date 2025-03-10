# coding: utf-8

"""
    Specification file for tiledb-server v4 API

    This spec is exposed to the public under /v4 route group  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Contact: info@tiledb.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud._common.api_v4.configuration import Configuration


class StorageSettingUpdateRequest(object):
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
        "name": "str",
        "is_default": "bool",
        "path": "str",
        "credentials_name": "str",
    }

    attribute_map = {
        "name": "name",
        "is_default": "is_default",
        "path": "path",
        "credentials_name": "credentials_name",
    }

    def __init__(
        self,
        name=None,
        is_default=None,
        path=None,
        credentials_name=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """StorageSettingUpdateRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._is_default = None
        self._path = None
        self._credentials_name = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if is_default is not None:
            self.is_default = is_default
        if path is not None:
            self.path = path
        if credentials_name is not None:
            self.credentials_name = credentials_name

    @property
    def name(self):
        """Gets the name of this StorageSettingUpdateRequest.  # noqa: E501

        storage location name  # noqa: E501

        :return: The name of this StorageSettingUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this StorageSettingUpdateRequest.

        storage location name  # noqa: E501

        :param name: The name of this StorageSettingUpdateRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def is_default(self):
        """Gets the is_default of this StorageSettingUpdateRequest.  # noqa: E501

        True if this is the workspace's or teamspace's default storage setting  # noqa: E501

        :return: The is_default of this StorageSettingUpdateRequest.  # noqa: E501
        :rtype: bool
        """
        return self._is_default

    @is_default.setter
    def is_default(self, is_default):
        """Sets the is_default of this StorageSettingUpdateRequest.

        True if this is the workspace's or teamspace's default storage setting  # noqa: E501

        :param is_default: The is_default of this StorageSettingUpdateRequest.  # noqa: E501
        :type: bool
        """

        self._is_default = is_default

    @property
    def path(self):
        """Gets the path of this StorageSettingUpdateRequest.  # noqa: E501

        The path to store an asset.  # noqa: E501

        :return: The path of this StorageSettingUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """Sets the path of this StorageSettingUpdateRequest.

        The path to store an asset.  # noqa: E501

        :param path: The path of this StorageSettingUpdateRequest.  # noqa: E501
        :type: str
        """

        self._path = path

    @property
    def credentials_name(self):
        """Gets the credentials_name of this StorageSettingUpdateRequest.  # noqa: E501

        The name of the credentials used to access this storage path  # noqa: E501

        :return: The credentials_name of this StorageSettingUpdateRequest.  # noqa: E501
        :rtype: str
        """
        return self._credentials_name

    @credentials_name.setter
    def credentials_name(self, credentials_name):
        """Sets the credentials_name of this StorageSettingUpdateRequest.

        The name of the credentials used to access this storage path  # noqa: E501

        :param credentials_name: The credentials_name of this StorageSettingUpdateRequest.  # noqa: E501
        :type: str
        """

        self._credentials_name = credentials_name

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
        if not isinstance(other, StorageSettingUpdateRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, StorageSettingUpdateRequest):
            return True

        return self.to_dict() != other.to_dict()
