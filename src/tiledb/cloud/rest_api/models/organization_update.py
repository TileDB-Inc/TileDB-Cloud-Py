# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint
import re

from tiledb.cloud.rest_api.configuration import Configuration


class OrganizationUpdate:
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
        "logo": "str",
        "description": "str",
        "default_s3_path": "str",
        "default_s3_path_credentials_name": "str",
        "asset_locations": "AssetLocations",
    }

    attribute_map = {
        "name": "name",
        "logo": "logo",
        "description": "description",
        "default_s3_path": "default_s3_path",
        "default_s3_path_credentials_name": "default_s3_path_credentials_name",
        "asset_locations": "asset_locations",
    }

    def __init__(
        self,
        name=None,
        logo=None,
        description=None,
        default_s3_path=None,
        default_s3_path_credentials_name=None,
        asset_locations=None,
        local_vars_configuration=None,
    ):
        """OrganizationUpdate - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._logo = None
        self._description = None
        self._default_s3_path = None
        self._default_s3_path_credentials_name = None
        self._asset_locations = None
        self.discriminator = None

        self.name = name
        self.logo = logo
        self.description = description
        self.default_s3_path = default_s3_path
        self.default_s3_path_credentials_name = default_s3_path_credentials_name
        if asset_locations is not None:
            self.asset_locations = asset_locations

    @property
    def name(self):
        """Gets the name of this OrganizationUpdate.

        organization name must be unique

        :return: The name of this OrganizationUpdate.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this OrganizationUpdate.

        organization name must be unique

        :param name: The name of this OrganizationUpdate.
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation
            and name is not None
            and len(name) > 63
        ):
            raise ValueError(
                "Invalid value for `name`, length must be less than or equal to `63`"
            )
        if (
            self.local_vars_configuration.client_side_validation
            and name is not None
            and len(name) < 1
        ):
            raise ValueError(
                "Invalid value for `name`, length must be greater than or equal to `1`"
            )
        if (
            self.local_vars_configuration.client_side_validation
            and name is not None
            and not re.search(r"^[\w.\-]+$", name)
        ):
            raise ValueError(
                r"Invalid value for `name`, must be a follow pattern or equal to `/^[\w.\-]+$/`"
            )

        self._name = name

    @property
    def logo(self):
        """Gets the logo of this OrganizationUpdate.

        Organization logo

        :return: The logo of this OrganizationUpdate.
        :rtype: str
        """
        return self._logo

    @logo.setter
    def logo(self, logo):
        """Sets the logo of this OrganizationUpdate.

        Organization logo

        :param logo: The logo of this OrganizationUpdate.
        :type: str
        """

        self._logo = logo

    @property
    def description(self):
        """Gets the description of this OrganizationUpdate.

        Organization description

        :return: The description of this OrganizationUpdate.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this OrganizationUpdate.

        Organization description

        :param description: The description of this OrganizationUpdate.
        :type: str
        """

        self._description = description

    @property
    def default_s3_path(self):
        """Gets the default_s3_path of this OrganizationUpdate.

        The default location to store newly-created notebooks and other assets like UDFs. The name `default_s3_path` is a legacy holdover; it may refer to any supported storage location.

        :return: The default_s3_path of this OrganizationUpdate.
        :rtype: str
        """
        return self._default_s3_path

    @default_s3_path.setter
    def default_s3_path(self, default_s3_path):
        """Sets the default_s3_path of this OrganizationUpdate.

        The default location to store newly-created notebooks and other assets like UDFs. The name `default_s3_path` is a legacy holdover; it may refer to any supported storage location.

        :param default_s3_path: The default_s3_path of this OrganizationUpdate.
        :type: str
        """

        self._default_s3_path = default_s3_path

    @property
    def default_s3_path_credentials_name(self):
        """Gets the default_s3_path_credentials_name of this OrganizationUpdate.

        The name of the credentials used to create and access files in the `default_s3_path`, if needed.

        :return: The default_s3_path_credentials_name of this OrganizationUpdate.
        :rtype: str
        """
        return self._default_s3_path_credentials_name

    @default_s3_path_credentials_name.setter
    def default_s3_path_credentials_name(self, default_s3_path_credentials_name):
        """Sets the default_s3_path_credentials_name of this OrganizationUpdate.

        The name of the credentials used to create and access files in the `default_s3_path`, if needed.

        :param default_s3_path_credentials_name: The default_s3_path_credentials_name of this OrganizationUpdate.
        :type: str
        """

        self._default_s3_path_credentials_name = default_s3_path_credentials_name

    @property
    def asset_locations(self):
        """Gets the asset_locations of this OrganizationUpdate.


        :return: The asset_locations of this OrganizationUpdate.
        :rtype: AssetLocations
        """
        return self._asset_locations

    @asset_locations.setter
    def asset_locations(self, asset_locations):
        """Sets the asset_locations of this OrganizationUpdate.


        :param asset_locations: The asset_locations of this OrganizationUpdate.
        :type: AssetLocations
        """

        self._asset_locations = asset_locations

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
        if not isinstance(other, OrganizationUpdate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrganizationUpdate):
            return True

        return self.to_dict() != other.to_dict()
