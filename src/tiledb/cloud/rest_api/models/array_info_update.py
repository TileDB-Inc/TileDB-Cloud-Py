# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint

from tiledb.cloud.rest_api.configuration import Configuration


class ArrayInfoUpdate(object):
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
        "description": "str",
        "name": "str",
        "uri": "str",
        "file_type": "FileType",
        "file_properties": "dict(str, str)",
        "access_credentials_name": "str",
        "logo": "str",
        "tags": "list[str]",
        "license_id": "str",
        "license_text": "str",
        "read_only": "bool",
    }

    attribute_map = {
        "description": "description",
        "name": "name",
        "uri": "uri",
        "file_type": "file_type",
        "file_properties": "file_properties",
        "access_credentials_name": "access_credentials_name",
        "logo": "logo",
        "tags": "tags",
        "license_id": "license_id",
        "license_text": "license_text",
        "read_only": "read_only",
    }

    def __init__(
        self,
        description=None,
        name=None,
        uri=None,
        file_type=None,
        file_properties=None,
        access_credentials_name=None,
        logo=None,
        tags=None,
        license_id=None,
        license_text=None,
        read_only=None,
        local_vars_configuration=None,
    ):
        """ArrayInfoUpdate - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._description = None
        self._name = None
        self._uri = None
        self._file_type = None
        self._file_properties = None
        self._access_credentials_name = None
        self._logo = None
        self._tags = None
        self._license_id = None
        self._license_text = None
        self._read_only = None
        self.discriminator = None

        self.description = description
        if name is not None:
            self.name = name
        if uri is not None:
            self.uri = uri
        if file_type is not None:
            self.file_type = file_type
        if file_properties is not None:
            self.file_properties = file_properties
        if access_credentials_name is not None:
            self.access_credentials_name = access_credentials_name
        if logo is not None:
            self.logo = logo
        if tags is not None:
            self.tags = tags
        if license_id is not None:
            self.license_id = license_id
        if license_text is not None:
            self.license_text = license_text
        if read_only is not None:
            self.read_only = read_only

    @property
    def description(self):
        """Gets the description of this ArrayInfoUpdate.

        description of array

        :return: The description of this ArrayInfoUpdate.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ArrayInfoUpdate.

        description of array

        :param description: The description of this ArrayInfoUpdate.
        :type: str
        """

        self._description = description

    @property
    def name(self):
        """Gets the name of this ArrayInfoUpdate.

        description of array

        :return: The name of this ArrayInfoUpdate.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ArrayInfoUpdate.

        description of array

        :param name: The name of this ArrayInfoUpdate.
        :type: str
        """

        self._name = name

    @property
    def uri(self):
        """Gets the uri of this ArrayInfoUpdate.

        uri of array

        :return: The uri of this ArrayInfoUpdate.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this ArrayInfoUpdate.

        uri of array

        :param uri: The uri of this ArrayInfoUpdate.
        :type: str
        """

        self._uri = uri

    @property
    def file_type(self):
        """Gets the file_type of this ArrayInfoUpdate.


        :return: The file_type of this ArrayInfoUpdate.
        :rtype: FileType
        """
        return self._file_type

    @file_type.setter
    def file_type(self, file_type):
        """Sets the file_type of this ArrayInfoUpdate.


        :param file_type: The file_type of this ArrayInfoUpdate.
        :type: FileType
        """

        self._file_type = file_type

    @property
    def file_properties(self):
        """Gets the file_properties of this ArrayInfoUpdate.

        map of file properties created for this array

        :return: The file_properties of this ArrayInfoUpdate.
        :rtype: dict(str, str)
        """
        return self._file_properties

    @file_properties.setter
    def file_properties(self, file_properties):
        """Sets the file_properties of this ArrayInfoUpdate.

        map of file properties created for this array

        :param file_properties: The file_properties of this ArrayInfoUpdate.
        :type: dict(str, str)
        """

        self._file_properties = file_properties

    @property
    def access_credentials_name(self):
        """Gets the access_credentials_name of this ArrayInfoUpdate.

        the name of the access credentials to use. if unset, the default credentials will be used

        :return: The access_credentials_name of this ArrayInfoUpdate.
        :rtype: str
        """
        return self._access_credentials_name

    @access_credentials_name.setter
    def access_credentials_name(self, access_credentials_name):
        """Sets the access_credentials_name of this ArrayInfoUpdate.

        the name of the access credentials to use. if unset, the default credentials will be used

        :param access_credentials_name: The access_credentials_name of this ArrayInfoUpdate.
        :type: str
        """

        self._access_credentials_name = access_credentials_name

    @property
    def logo(self):
        """Gets the logo of this ArrayInfoUpdate.

        logo (base64 encoded) for the array. Optional

        :return: The logo of this ArrayInfoUpdate.
        :rtype: str
        """
        return self._logo

    @logo.setter
    def logo(self, logo):
        """Sets the logo of this ArrayInfoUpdate.

        logo (base64 encoded) for the array. Optional

        :param logo: The logo of this ArrayInfoUpdate.
        :type: str
        """

        self._logo = logo

    @property
    def tags(self):
        """Gets the tags of this ArrayInfoUpdate.

        optional tags for array

        :return: The tags of this ArrayInfoUpdate.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this ArrayInfoUpdate.

        optional tags for array

        :param tags: The tags of this ArrayInfoUpdate.
        :type: list[str]
        """

        self._tags = tags

    @property
    def license_id(self):
        """Gets the license_id of this ArrayInfoUpdate.

        License identifier from SPDX License List or Custom

        :return: The license_id of this ArrayInfoUpdate.
        :rtype: str
        """
        return self._license_id

    @license_id.setter
    def license_id(self, license_id):
        """Sets the license_id of this ArrayInfoUpdate.

        License identifier from SPDX License List or Custom

        :param license_id: The license_id of this ArrayInfoUpdate.
        :type: str
        """

        self._license_id = license_id

    @property
    def license_text(self):
        """Gets the license_text of this ArrayInfoUpdate.

        License text

        :return: The license_text of this ArrayInfoUpdate.
        :rtype: str
        """
        return self._license_text

    @license_text.setter
    def license_text(self, license_text):
        """Sets the license_text of this ArrayInfoUpdate.

        License text

        :param license_text: The license_text of this ArrayInfoUpdate.
        :type: str
        """

        self._license_text = license_text

    @property
    def read_only(self):
        """Gets the read_only of this ArrayInfoUpdate.

        Suggests if the array is in read_only mode

        :return: The read_only of this ArrayInfoUpdate.
        :rtype: bool
        """
        return self._read_only

    @read_only.setter
    def read_only(self, read_only):
        """Sets the read_only of this ArrayInfoUpdate.

        Suggests if the array is in read_only mode

        :param read_only: The read_only of this ArrayInfoUpdate.
        :type: bool
        """

        self._read_only = read_only

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in self.openapi_types.items():
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
        if not isinstance(other, ArrayInfoUpdate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ArrayInfoUpdate):
            return True

        return self.to_dict() != other.to_dict()
