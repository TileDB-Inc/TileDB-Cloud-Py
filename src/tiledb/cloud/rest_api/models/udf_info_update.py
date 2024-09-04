# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API  # noqa: E501

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint

import six

from tiledb.cloud.rest_api.configuration import Configuration


class UDFInfoUpdate(object):
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
        "language": "UDFLanguage",
        "version": "str",
        "image_name": "str",
        "type": "UDFType",
        "_exec": "str",
        "exec_raw": "str",
        "readme": "str",
        "license_id": "str",
        "license_text": "str",
        "tags": "list[str]",
    }

    attribute_map = {
        "name": "name",
        "language": "language",
        "version": "version",
        "image_name": "image_name",
        "type": "type",
        "_exec": "exec",
        "exec_raw": "exec_raw",
        "readme": "readme",
        "license_id": "license_id",
        "license_text": "license_text",
        "tags": "tags",
    }

    def __init__(
        self,
        name=None,
        language=None,
        version=None,
        image_name=None,
        type=None,
        _exec=None,
        exec_raw=None,
        readme=None,
        license_id=None,
        license_text=None,
        tags=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """UDFInfoUpdate - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._language = None
        self._version = None
        self._image_name = None
        self._type = None
        self.__exec = None
        self._exec_raw = None
        self._readme = None
        self._license_id = None
        self._license_text = None
        self._tags = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if language is not None:
            self.language = language
        if version is not None:
            self.version = version
        if image_name is not None:
            self.image_name = image_name
        if type is not None:
            self.type = type
        if _exec is not None:
            self._exec = _exec
        if exec_raw is not None:
            self.exec_raw = exec_raw
        if readme is not None:
            self.readme = readme
        if license_id is not None:
            self.license_id = license_id
        if license_text is not None:
            self.license_text = license_text
        if tags is not None:
            self.tags = tags

    @property
    def name(self):
        """Gets the name of this UDFInfoUpdate.  # noqa: E501

        name of UDF  # noqa: E501

        :return: The name of this UDFInfoUpdate.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UDFInfoUpdate.

        name of UDF  # noqa: E501

        :param name: The name of this UDFInfoUpdate.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def language(self):
        """Gets the language of this UDFInfoUpdate.  # noqa: E501


        :return: The language of this UDFInfoUpdate.  # noqa: E501
        :rtype: UDFLanguage
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this UDFInfoUpdate.


        :param language: The language of this UDFInfoUpdate.  # noqa: E501
        :type: UDFLanguage
        """

        self._language = language

    @property
    def version(self):
        """Gets the version of this UDFInfoUpdate.  # noqa: E501

        Type-specific version  # noqa: E501

        :return: The version of this UDFInfoUpdate.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this UDFInfoUpdate.

        Type-specific version  # noqa: E501

        :param version: The version of this UDFInfoUpdate.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def image_name(self):
        """Gets the image_name of this UDFInfoUpdate.  # noqa: E501

        Docker image name to use for UDF  # noqa: E501

        :return: The image_name of this UDFInfoUpdate.  # noqa: E501
        :rtype: str
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name):
        """Sets the image_name of this UDFInfoUpdate.

        Docker image name to use for UDF  # noqa: E501

        :param image_name: The image_name of this UDFInfoUpdate.  # noqa: E501
        :type: str
        """

        self._image_name = image_name

    @property
    def type(self):
        """Gets the type of this UDFInfoUpdate.  # noqa: E501


        :return: The type of this UDFInfoUpdate.  # noqa: E501
        :rtype: UDFType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this UDFInfoUpdate.


        :param type: The type of this UDFInfoUpdate.  # noqa: E501
        :type: UDFType
        """

        self._type = type

    @property
    def _exec(self):
        """Gets the _exec of this UDFInfoUpdate.  # noqa: E501

        Type-specific executable text  # noqa: E501

        :return: The _exec of this UDFInfoUpdate.  # noqa: E501
        :rtype: str
        """
        return self.__exec

    @_exec.setter
    def _exec(self, _exec):
        """Sets the _exec of this UDFInfoUpdate.

        Type-specific executable text  # noqa: E501

        :param _exec: The _exec of this UDFInfoUpdate.  # noqa: E501
        :type: str
        """

        self.__exec = _exec

    @property
    def exec_raw(self):
        """Gets the exec_raw of this UDFInfoUpdate.  # noqa: E501

        optional raw text to store of serialized function, used for showing in UI  # noqa: E501

        :return: The exec_raw of this UDFInfoUpdate.  # noqa: E501
        :rtype: str
        """
        return self._exec_raw

    @exec_raw.setter
    def exec_raw(self, exec_raw):
        """Sets the exec_raw of this UDFInfoUpdate.

        optional raw text to store of serialized function, used for showing in UI  # noqa: E501

        :param exec_raw: The exec_raw of this UDFInfoUpdate.  # noqa: E501
        :type: str
        """

        self._exec_raw = exec_raw

    @property
    def readme(self):
        """Gets the readme of this UDFInfoUpdate.  # noqa: E501

        Markdown readme of UDFs  # noqa: E501

        :return: The readme of this UDFInfoUpdate.  # noqa: E501
        :rtype: str
        """
        return self._readme

    @readme.setter
    def readme(self, readme):
        """Sets the readme of this UDFInfoUpdate.

        Markdown readme of UDFs  # noqa: E501

        :param readme: The readme of this UDFInfoUpdate.  # noqa: E501
        :type: str
        """

        self._readme = readme

    @property
    def license_id(self):
        """Gets the license_id of this UDFInfoUpdate.  # noqa: E501

        License identifier from SPDX License List or Custom  # noqa: E501

        :return: The license_id of this UDFInfoUpdate.  # noqa: E501
        :rtype: str
        """
        return self._license_id

    @license_id.setter
    def license_id(self, license_id):
        """Sets the license_id of this UDFInfoUpdate.

        License identifier from SPDX License List or Custom  # noqa: E501

        :param license_id: The license_id of this UDFInfoUpdate.  # noqa: E501
        :type: str
        """

        self._license_id = license_id

    @property
    def license_text(self):
        """Gets the license_text of this UDFInfoUpdate.  # noqa: E501

        License text  # noqa: E501

        :return: The license_text of this UDFInfoUpdate.  # noqa: E501
        :rtype: str
        """
        return self._license_text

    @license_text.setter
    def license_text(self, license_text):
        """Sets the license_text of this UDFInfoUpdate.

        License text  # noqa: E501

        :param license_text: The license_text of this UDFInfoUpdate.  # noqa: E501
        :type: str
        """

        self._license_text = license_text

    @property
    def tags(self):
        """Gets the tags of this UDFInfoUpdate.  # noqa: E501

        optional tags for UDF  # noqa: E501

        :return: The tags of this UDFInfoUpdate.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this UDFInfoUpdate.

        optional tags for UDF  # noqa: E501

        :param tags: The tags of this UDFInfoUpdate.  # noqa: E501
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
        if not isinstance(other, UDFInfoUpdate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UDFInfoUpdate):
            return True

        return self.to_dict() != other.to_dict()
