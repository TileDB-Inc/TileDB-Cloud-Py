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


class NonEmptyDomain(object):
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
    openapi_types = {"non_empty_domain": "DomainArray", "is_empty": "bool"}

    attribute_map = {"non_empty_domain": "nonEmptyDomain", "is_empty": "isEmpty"}

    def __init__(
        self, non_empty_domain=None, is_empty=None, local_vars_configuration=None
    ):
        """NonEmptyDomain - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._non_empty_domain = None
        self._is_empty = None
        self.discriminator = None

        self.non_empty_domain = non_empty_domain
        self.is_empty = is_empty

    @property
    def non_empty_domain(self):
        """Gets the non_empty_domain of this NonEmptyDomain.


        :return: The non_empty_domain of this NonEmptyDomain.
        :rtype: DomainArray
        """
        return self._non_empty_domain

    @non_empty_domain.setter
    def non_empty_domain(self, non_empty_domain):
        """Sets the non_empty_domain of this NonEmptyDomain.


        :param non_empty_domain: The non_empty_domain of this NonEmptyDomain.
        :type: DomainArray
        """
        if (
            self.local_vars_configuration.client_side_validation
            and non_empty_domain is None
        ):
            raise ValueError("Invalid value for `non_empty_domain`, must not be `None`")

        self._non_empty_domain = non_empty_domain

    @property
    def is_empty(self):
        """Gets the is_empty of this NonEmptyDomain.

        Is non-empty domain really empty?

        :return: The is_empty of this NonEmptyDomain.
        :rtype: bool
        """
        return self._is_empty

    @is_empty.setter
    def is_empty(self, is_empty):
        """Sets the is_empty of this NonEmptyDomain.

        Is non-empty domain really empty?

        :param is_empty: The is_empty of this NonEmptyDomain.
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and is_empty is None:
            raise ValueError("Invalid value for `is_empty`, must not be `None`")

        self._is_empty = is_empty

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
        if not isinstance(other, NonEmptyDomain):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NonEmptyDomain):
            return True

        return self.to_dict() != other.to_dict()
