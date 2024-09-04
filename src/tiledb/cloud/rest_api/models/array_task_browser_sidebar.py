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


class ArrayTaskBrowserSidebar(object):
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
        "organizations": "list[str]",
        "result_count_for_all": "int",
        "result_count_by_namespace": "object",
    }

    attribute_map = {
        "organizations": "organizations",
        "result_count_for_all": "result_count_for_all",
        "result_count_by_namespace": "result_count_by_namespace",
    }

    def __init__(
        self,
        organizations=None,
        result_count_for_all=None,
        result_count_by_namespace=None,
        local_vars_configuration=None,
    ):
        """ArrayTaskBrowserSidebar - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._organizations = None
        self._result_count_for_all = None
        self._result_count_by_namespace = None
        self.discriminator = None

        if organizations is not None:
            self.organizations = organizations
        if result_count_for_all is not None:
            self.result_count_for_all = result_count_for_all
        if result_count_by_namespace is not None:
            self.result_count_by_namespace = result_count_by_namespace

    @property
    def organizations(self):
        """Gets the organizations of this ArrayTaskBrowserSidebar.

        list of all unique organizations the user is part of that have array tasks

        :return: The organizations of this ArrayTaskBrowserSidebar.
        :rtype: list[str]
        """
        return self._organizations

    @organizations.setter
    def organizations(self, organizations):
        """Sets the organizations of this ArrayTaskBrowserSidebar.

        list of all unique organizations the user is part of that have array tasks

        :param organizations: The organizations of this ArrayTaskBrowserSidebar.
        :type: list[str]
        """

        self._organizations = organizations

    @property
    def result_count_for_all(self):
        """Gets the result_count_for_all of this ArrayTaskBrowserSidebar.

        A count of \"all\"

        :return: The result_count_for_all of this ArrayTaskBrowserSidebar.
        :rtype: int
        """
        return self._result_count_for_all

    @result_count_for_all.setter
    def result_count_for_all(self, result_count_for_all):
        """Sets the result_count_for_all of this ArrayTaskBrowserSidebar.

        A count of \"all\"

        :param result_count_for_all: The result_count_for_all of this ArrayTaskBrowserSidebar.
        :type: int
        """

        self._result_count_for_all = result_count_for_all

    @property
    def result_count_by_namespace(self):
        """Gets the result_count_by_namespace of this ArrayTaskBrowserSidebar.

        A map that includes the result count by namespace

        :return: The result_count_by_namespace of this ArrayTaskBrowserSidebar.
        :rtype: object
        """
        return self._result_count_by_namespace

    @result_count_by_namespace.setter
    def result_count_by_namespace(self, result_count_by_namespace):
        """Sets the result_count_by_namespace of this ArrayTaskBrowserSidebar.

        A map that includes the result count by namespace

        :param result_count_by_namespace: The result_count_by_namespace of this ArrayTaskBrowserSidebar.
        :type: object
        """

        self._result_count_by_namespace = result_count_by_namespace

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
        if not isinstance(other, ArrayTaskBrowserSidebar):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ArrayTaskBrowserSidebar):
            return True

        return self.to_dict() != other.to_dict()
