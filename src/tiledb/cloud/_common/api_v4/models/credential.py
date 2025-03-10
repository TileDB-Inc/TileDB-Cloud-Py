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


class Credential(object):
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
        "aws": "AWSCredential",
        "azure": "AzureCredential",
        "gcp": "GCPInteroperabilityCredential",
    }

    attribute_map = {"aws": "aws", "azure": "azure", "gcp": "gcp"}

    def __init__(
        self, aws=None, azure=None, gcp=None, local_vars_configuration=None
    ):  # noqa: E501
        """Credential - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._aws = None
        self._azure = None
        self._gcp = None
        self.discriminator = None

        if aws is not None:
            self.aws = aws
        if azure is not None:
            self.azure = azure
        if gcp is not None:
            self.gcp = gcp

    @property
    def aws(self):
        """Gets the aws of this Credential.  # noqa: E501


        :return: The aws of this Credential.  # noqa: E501
        :rtype: AWSCredential
        """
        return self._aws

    @aws.setter
    def aws(self, aws):
        """Sets the aws of this Credential.


        :param aws: The aws of this Credential.  # noqa: E501
        :type: AWSCredential
        """

        self._aws = aws

    @property
    def azure(self):
        """Gets the azure of this Credential.  # noqa: E501


        :return: The azure of this Credential.  # noqa: E501
        :rtype: AzureCredential
        """
        return self._azure

    @azure.setter
    def azure(self, azure):
        """Sets the azure of this Credential.


        :param azure: The azure of this Credential.  # noqa: E501
        :type: AzureCredential
        """

        self._azure = azure

    @property
    def gcp(self):
        """Gets the gcp of this Credential.  # noqa: E501


        :return: The gcp of this Credential.  # noqa: E501
        :rtype: GCPInteroperabilityCredential
        """
        return self._gcp

    @gcp.setter
    def gcp(self, gcp):
        """Sets the gcp of this Credential.


        :param gcp: The gcp of this Credential.  # noqa: E501
        :type: GCPInteroperabilityCredential
        """

        self._gcp = gcp

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
        if not isinstance(other, Credential):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Credential):
            return True

        return self.to_dict() != other.to_dict()
