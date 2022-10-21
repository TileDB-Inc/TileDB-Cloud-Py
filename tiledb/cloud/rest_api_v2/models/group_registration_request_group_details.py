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

from tiledb.cloud.rest_api.configuration import Configuration


class GroupRegistrationRequestGroupDetails(object):
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
        "parent": "str",
        "uri": "str",
        "logo": "str",
        "tags": "list[str]",
        "license_id": "str",
        "license_text": "str",
        "region": "str",
        "access_credentials_name": "str",
    }

    attribute_map = {
        "description": "description",
        "name": "name",
        "parent": "parent",
        "uri": "uri",
        "logo": "logo",
        "tags": "tags",
        "license_id": "license_id",
        "license_text": "license_text",
        "region": "region",
        "access_credentials_name": "access_credentials_name",
    }

    def __init__(
        self,
        description=None,
        name=None,
        parent=None,
        uri=None,
        logo=None,
        tags=None,
        license_id=None,
        license_text=None,
        region=None,
        access_credentials_name=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """GroupRegistrationRequestGroupDetails - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._description = None
        self._name = None
        self._parent = None
        self._uri = None
        self._logo = None
        self._tags = None
        self._license_id = None
        self._license_text = None
        self._region = None
        self._access_credentials_name = None
        self.discriminator = None

        if description is not None:
            self.description = description
        if name is not None:
            self.name = name
        if parent is not None:
            self.parent = parent
        if uri is not None:
            self.uri = uri
        if logo is not None:
            self.logo = logo
        if tags is not None:
            self.tags = tags
        if license_id is not None:
            self.license_id = license_id
        if license_text is not None:
            self.license_text = license_text
        if region is not None:
            self.region = region
        if access_credentials_name is not None:
            self.access_credentials_name = access_credentials_name

    @property
    def description(self):
        """Gets the description of this GroupRegistrationRequestGroupDetails.  # noqa: E501

        A human readable description of the contents of the group.  # noqa: E501

        :return: The description of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this GroupRegistrationRequestGroupDetails.

        A human readable description of the contents of the group.  # noqa: E501

        :param description: The description of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def name(self):
        """Gets the name of this GroupRegistrationRequestGroupDetails.  # noqa: E501

        The name of the group. If must be unique within the group.  # noqa: E501

        :return: The name of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GroupRegistrationRequestGroupDetails.

        The name of the group. If must be unique within the group.  # noqa: E501

        :param name: The name of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def parent(self):
        """Gets the parent of this GroupRegistrationRequestGroupDetails.  # noqa: E501

        The unique name or id of the parent of the group. If empty, then the new group will be a top level group.  # noqa: E501

        :return: The parent of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :rtype: str
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """Sets the parent of this GroupRegistrationRequestGroupDetails.

        The unique name or id of the parent of the group. If empty, then the new group will be a top level group.  # noqa: E501

        :param parent: The parent of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :type: str
        """

        self._parent = parent

    @property
    def uri(self):
        """Gets the uri of this GroupRegistrationRequestGroupDetails.  # noqa: E501

        uri of group.  # noqa: E501

        :return: The uri of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """Sets the uri of this GroupRegistrationRequestGroupDetails.

        uri of group.  # noqa: E501

        :param uri: The uri of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :type: str
        """

        self._uri = uri

    @property
    def logo(self):
        """Gets the logo of this GroupRegistrationRequestGroupDetails.  # noqa: E501

        logo (base64 encoded) for the group. Optional  # noqa: E501

        :return: The logo of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :rtype: str
        """
        return self._logo

    @logo.setter
    def logo(self, logo):
        """Sets the logo of this GroupRegistrationRequestGroupDetails.

        logo (base64 encoded) for the group. Optional  # noqa: E501

        :param logo: The logo of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :type: str
        """

        self._logo = logo

    @property
    def tags(self):
        """Gets the tags of this GroupRegistrationRequestGroupDetails.  # noqa: E501

        optional tags for groups.  # noqa: E501

        :return: The tags of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this GroupRegistrationRequestGroupDetails.

        optional tags for groups.  # noqa: E501

        :param tags: The tags of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def license_id(self):
        """Gets the license_id of this GroupRegistrationRequestGroupDetails.  # noqa: E501

        License identifier from SPDX License List or Custom.  # noqa: E501

        :return: The license_id of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :rtype: str
        """
        return self._license_id

    @license_id.setter
    def license_id(self, license_id):
        """Sets the license_id of this GroupRegistrationRequestGroupDetails.

        License identifier from SPDX License List or Custom.  # noqa: E501

        :param license_id: The license_id of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :type: str
        """

        self._license_id = license_id

    @property
    def license_text(self):
        """Gets the license_text of this GroupRegistrationRequestGroupDetails.  # noqa: E501

        License text  # noqa: E501

        :return: The license_text of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :rtype: str
        """
        return self._license_text

    @license_text.setter
    def license_text(self, license_text):
        """Sets the license_text of this GroupRegistrationRequestGroupDetails.

        License text  # noqa: E501

        :param license_text: The license_text of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :type: str
        """

        self._license_text = license_text

    @property
    def region(self):
        """Gets the region of this GroupRegistrationRequestGroupDetails.  # noqa: E501

        region of the group  # noqa: E501

        :return: The region of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this GroupRegistrationRequestGroupDetails.

        region of the group  # noqa: E501

        :param region: The region of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :type: str
        """

        self._region = region

    @property
    def access_credentials_name(self):
        """Gets the access_credentials_name of this GroupRegistrationRequestGroupDetails.  # noqa: E501

        the name of the access credentials to use. if unset, the default credentials will be used.  # noqa: E501

        :return: The access_credentials_name of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :rtype: str
        """
        return self._access_credentials_name

    @access_credentials_name.setter
    def access_credentials_name(self, access_credentials_name):
        """Sets the access_credentials_name of this GroupRegistrationRequestGroupDetails.

        the name of the access credentials to use. if unset, the default credentials will be used.  # noqa: E501

        :param access_credentials_name: The access_credentials_name of this GroupRegistrationRequestGroupDetails.  # noqa: E501
        :type: str
        """

        self._access_credentials_name = access_credentials_name

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
        if not isinstance(other, GroupRegistrationRequestGroupDetails):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GroupRegistrationRequestGroupDetails):
            return True

        return self.to_dict() != other.to_dict()
