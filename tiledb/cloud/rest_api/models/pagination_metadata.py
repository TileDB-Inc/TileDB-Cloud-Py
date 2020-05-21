# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class PaginationMetadata(object):
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
        "page": "float",
        "per_page": "float",
        "total_pages": "float",
        "total_items": "float",
    }

    attribute_map = {
        "page": "page",
        "per_page": "per_page",
        "total_pages": "total_pages",
        "total_items": "total_items",
    }

    def __init__(
        self, page=None, per_page=None, total_pages=None, total_items=None
    ):  # noqa: E501
        """PaginationMetadata - a model defined in OpenAPI"""  # noqa: E501

        self._page = None
        self._per_page = None
        self._total_pages = None
        self._total_items = None
        self.discriminator = None

        if page is not None:
            self.page = page
        if per_page is not None:
            self.per_page = per_page
        if total_pages is not None:
            self.total_pages = total_pages
        if total_items is not None:
            self.total_items = total_items

    @property
    def page(self):
        """Gets the page of this PaginationMetadata.  # noqa: E501

        pagination offset  # noqa: E501

        :return: The page of this PaginationMetadata.  # noqa: E501
        :rtype: float
        """
        return self._page

    @page.setter
    def page(self, page):
        """Sets the page of this PaginationMetadata.

        pagination offset  # noqa: E501

        :param page: The page of this PaginationMetadata.  # noqa: E501
        :type: float
        """

        self._page = page

    @property
    def per_page(self):
        """Gets the per_page of this PaginationMetadata.  # noqa: E501

        pagination limit  # noqa: E501

        :return: The per_page of this PaginationMetadata.  # noqa: E501
        :rtype: float
        """
        return self._per_page

    @per_page.setter
    def per_page(self, per_page):
        """Sets the per_page of this PaginationMetadata.

        pagination limit  # noqa: E501

        :param per_page: The per_page of this PaginationMetadata.  # noqa: E501
        :type: float
        """

        self._per_page = per_page

    @property
    def total_pages(self):
        """Gets the total_pages of this PaginationMetadata.  # noqa: E501

        number of total pages with current limit  # noqa: E501

        :return: The total_pages of this PaginationMetadata.  # noqa: E501
        :rtype: float
        """
        return self._total_pages

    @total_pages.setter
    def total_pages(self, total_pages):
        """Sets the total_pages of this PaginationMetadata.

        number of total pages with current limit  # noqa: E501

        :param total_pages: The total_pages of this PaginationMetadata.  # noqa: E501
        :type: float
        """

        self._total_pages = total_pages

    @property
    def total_items(self):
        """Gets the total_items of this PaginationMetadata.  # noqa: E501

        number of total available items  # noqa: E501

        :return: The total_items of this PaginationMetadata.  # noqa: E501
        :rtype: float
        """
        return self._total_items

    @total_items.setter
    def total_items(self, total_items):
        """Sets the total_items of this PaginationMetadata.

        number of total available items  # noqa: E501

        :param total_items: The total_items of this PaginationMetadata.  # noqa: E501
        :type: float
        """

        self._total_items = total_items

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
        if not isinstance(other, PaginationMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
