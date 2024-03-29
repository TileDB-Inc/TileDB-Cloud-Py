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


class GroupMetadataUpdateRequest(object):
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
    openapi_types = {"config": "TileDBConfig", "metadata": "Metadata"}

    attribute_map = {"config": "config", "metadata": "metadata"}

    def __init__(
        self, config=None, metadata=None, local_vars_configuration=None
    ):  # noqa: E501
        """GroupMetadataUpdateRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._config = None
        self._metadata = None
        self.discriminator = None

        if config is not None:
            self.config = config
        self.metadata = metadata

    @property
    def config(self):
        """Gets the config of this GroupMetadataUpdateRequest.  # noqa: E501


        :return: The config of this GroupMetadataUpdateRequest.  # noqa: E501
        :rtype: TileDBConfig
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this GroupMetadataUpdateRequest.


        :param config: The config of this GroupMetadataUpdateRequest.  # noqa: E501
        :type: TileDBConfig
        """

        self._config = config

    @property
    def metadata(self):
        """Gets the metadata of this GroupMetadataUpdateRequest.  # noqa: E501


        :return: The metadata of this GroupMetadataUpdateRequest.  # noqa: E501
        :rtype: Metadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this GroupMetadataUpdateRequest.


        :param metadata: The metadata of this GroupMetadataUpdateRequest.  # noqa: E501
        :type: Metadata
        """
        if (
            self.local_vars_configuration.client_side_validation and metadata is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `metadata`, must not be `None`"
            )  # noqa: E501

        self._metadata = metadata

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
        if not isinstance(other, GroupMetadataUpdateRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GroupMetadataUpdateRequest):
            return True

        return self.to_dict() != other.to_dict()
