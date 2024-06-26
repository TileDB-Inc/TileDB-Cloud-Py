# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from tiledb.cloud.rest_api.configuration import Configuration


class UDFInfo(object):
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
        "id": "str",
        "name": "str",
        "language": "UDFLanguage",
        "type": "UDFType",
        "readme": "str",
        "license_id": "str",
        "license_text": "str",
        "tags": "list[str]",
    }

    attribute_map = {
        "id": "id",
        "name": "name",
        "language": "language",
        "type": "type",
        "readme": "readme",
        "license_id": "license_id",
        "license_text": "license_text",
        "tags": "tags",
    }

    def __init__(
        self,
        id=None,
        name=None,
        language=None,
        type=None,
        readme=None,
        license_id=None,
        license_text=None,
        tags=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """UDFInfo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._language = None
        self._type = None
        self._readme = None
        self._license_id = None
        self._license_text = None
        self._tags = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if language is not None:
            self.language = language
        if type is not None:
            self.type = type
        if readme is not None:
            self.readme = readme
        if license_id is not None:
            self.license_id = license_id
        if license_text is not None:
            self.license_text = license_text
        if tags is not None:
            self.tags = tags

    @property
    def id(self):
        """Gets the id of this UDFInfo.  # noqa: E501

        Unique ID of UDF  # noqa: E501

        :return: The id of this UDFInfo.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UDFInfo.

        Unique ID of UDF  # noqa: E501

        :param id: The id of this UDFInfo.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this UDFInfo.  # noqa: E501

        name of UDF  # noqa: E501

        :return: The name of this UDFInfo.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UDFInfo.

        name of UDF  # noqa: E501

        :param name: The name of this UDFInfo.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def language(self):
        """Gets the language of this UDFInfo.  # noqa: E501


        :return: The language of this UDFInfo.  # noqa: E501
        :rtype: UDFLanguage
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this UDFInfo.


        :param language: The language of this UDFInfo.  # noqa: E501
        :type: UDFLanguage
        """

        self._language = language

    @property
    def type(self):
        """Gets the type of this UDFInfo.  # noqa: E501


        :return: The type of this UDFInfo.  # noqa: E501
        :rtype: UDFType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this UDFInfo.


        :param type: The type of this UDFInfo.  # noqa: E501
        :type: UDFType
        """

        self._type = type

    @property
    def readme(self):
        """Gets the readme of this UDFInfo.  # noqa: E501

        Markdown readme of UDFs  # noqa: E501

        :return: The readme of this UDFInfo.  # noqa: E501
        :rtype: str
        """
        return self._readme

    @readme.setter
    def readme(self, readme):
        """Sets the readme of this UDFInfo.

        Markdown readme of UDFs  # noqa: E501

        :param readme: The readme of this UDFInfo.  # noqa: E501
        :type: str
        """

        self._readme = readme

    @property
    def license_id(self):
        """Gets the license_id of this UDFInfo.  # noqa: E501

        License identifier from SPDX License List or Custom  # noqa: E501

        :return: The license_id of this UDFInfo.  # noqa: E501
        :rtype: str
        """
        return self._license_id

    @license_id.setter
    def license_id(self, license_id):
        """Sets the license_id of this UDFInfo.

        License identifier from SPDX License List or Custom  # noqa: E501

        :param license_id: The license_id of this UDFInfo.  # noqa: E501
        :type: str
        """

        self._license_id = license_id

    @property
    def license_text(self):
        """Gets the license_text of this UDFInfo.  # noqa: E501

        License text  # noqa: E501

        :return: The license_text of this UDFInfo.  # noqa: E501
        :rtype: str
        """
        return self._license_text

    @license_text.setter
    def license_text(self, license_text):
        """Sets the license_text of this UDFInfo.

        License text  # noqa: E501

        :param license_text: The license_text of this UDFInfo.  # noqa: E501
        :type: str
        """

        self._license_text = license_text

    @property
    def tags(self):
        """Gets the tags of this UDFInfo.  # noqa: E501

        optional tags for UDF  # noqa: E501

        :return: The tags of this UDFInfo.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this UDFInfo.

        optional tags for UDF  # noqa: E501

        :param tags: The tags of this UDFInfo.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

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
        if not isinstance(other, UDFInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UDFInfo):
            return True

        return self.to_dict() != other.to_dict()
