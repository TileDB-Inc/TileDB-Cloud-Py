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


class Organization(object):
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
        "role": "OrganizationRoles",
        "name": "str",
        "created_at": "datetime",
        "updated_at": "datetime",
        "logo": "str",
        "description": "str",
        "users": "list[OrganizationUser]",
        "allowed_actions": "list[NamespaceActions]",
        "num_of_arrays": "float",
        "enabled_features": "list[str]",
        "unpaid_subscription": "bool",
        "default_s3_path": "str",
        "default_s3_path_credentials_name": "str",
        "asset_locations": "AssetLocations",
        "stripe_connect": "bool",
        "assume_role_arn": "str",
    }

    attribute_map = {
        "id": "id",
        "role": "role",
        "name": "name",
        "created_at": "created_at",
        "updated_at": "updated_at",
        "logo": "logo",
        "description": "description",
        "users": "users",
        "allowed_actions": "allowed_actions",
        "num_of_arrays": "num_of_arrays",
        "enabled_features": "enabled_features",
        "unpaid_subscription": "unpaid_subscription",
        "default_s3_path": "default_s3_path",
        "default_s3_path_credentials_name": "default_s3_path_credentials_name",
        "asset_locations": "asset_locations",
        "stripe_connect": "stripe_connect",
        "assume_role_arn": "assume_role_arn",
    }

    def __init__(
        self,
        id=None,
        role=None,
        name=None,
        created_at=None,
        updated_at=None,
        logo=None,
        description=None,
        users=None,
        allowed_actions=None,
        num_of_arrays=None,
        enabled_features=None,
        unpaid_subscription=None,
        default_s3_path=None,
        default_s3_path_credentials_name=None,
        asset_locations=None,
        stripe_connect=None,
        assume_role_arn=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """Organization - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._role = None
        self._name = None
        self._created_at = None
        self._updated_at = None
        self._logo = None
        self._description = None
        self._users = None
        self._allowed_actions = None
        self._num_of_arrays = None
        self._enabled_features = None
        self._unpaid_subscription = None
        self._default_s3_path = None
        self._default_s3_path_credentials_name = None
        self._asset_locations = None
        self._stripe_connect = None
        self._assume_role_arn = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if role is not None:
            self.role = role
        self.name = name
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        self.logo = logo
        self.description = description
        if users is not None:
            self.users = users
        if allowed_actions is not None:
            self.allowed_actions = allowed_actions
        if num_of_arrays is not None:
            self.num_of_arrays = num_of_arrays
        if enabled_features is not None:
            self.enabled_features = enabled_features
        if unpaid_subscription is not None:
            self.unpaid_subscription = unpaid_subscription
        if default_s3_path is not None:
            self.default_s3_path = default_s3_path
        if default_s3_path_credentials_name is not None:
            self.default_s3_path_credentials_name = default_s3_path_credentials_name
        if asset_locations is not None:
            self.asset_locations = asset_locations
        if stripe_connect is not None:
            self.stripe_connect = stripe_connect
        if assume_role_arn is not None:
            self.assume_role_arn = assume_role_arn

    @property
    def id(self):
        """Gets the id of this Organization.  # noqa: E501

        unique ID of organization  # noqa: E501

        :return: The id of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Organization.

        unique ID of organization  # noqa: E501

        :param id: The id of this Organization.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def role(self):
        """Gets the role of this Organization.  # noqa: E501


        :return: The role of this Organization.  # noqa: E501
        :rtype: OrganizationRoles
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this Organization.


        :param role: The role of this Organization.  # noqa: E501
        :type: OrganizationRoles
        """

        self._role = role

    @property
    def name(self):
        """Gets the name of this Organization.  # noqa: E501

        organization name must be unique  # noqa: E501

        :return: The name of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Organization.

        organization name must be unique  # noqa: E501

        :param name: The name of this Organization.  # noqa: E501
        :type: str
        """
        if (
            self.local_vars_configuration.client_side_validation and name is None
        ):  # noqa: E501
            raise ValueError(
                "Invalid value for `name`, must not be `None`"
            )  # noqa: E501
        if (
            self.local_vars_configuration.client_side_validation
            and name is not None
            and len(name) > 63
        ):
            raise ValueError(
                "Invalid value for `name`, length must be less than or equal to `63`"
            )  # noqa: E501
        if (
            self.local_vars_configuration.client_side_validation
            and name is not None
            and len(name) < 1
        ):
            raise ValueError(
                "Invalid value for `name`, length must be greater than or equal to `1`"
            )  # noqa: E501
        if (
            self.local_vars_configuration.client_side_validation
            and name is not None
            and not re.search(r"^[\w.\-]+$", name)
        ):  # noqa: E501
            raise ValueError(
                r"Invalid value for `name`, must be a follow pattern or equal to `/^[\w.\-]+$/`"
            )  # noqa: E501

        self._name = name

    @property
    def created_at(self):
        """Gets the created_at of this Organization.  # noqa: E501

        Datetime organization was created in UTC  # noqa: E501

        :return: The created_at of this Organization.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Organization.

        Datetime organization was created in UTC  # noqa: E501

        :param created_at: The created_at of this Organization.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this Organization.  # noqa: E501

        Datetime organization was updated in UTC  # noqa: E501

        :return: The updated_at of this Organization.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this Organization.

        Datetime organization was updated in UTC  # noqa: E501

        :param updated_at: The updated_at of this Organization.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def logo(self):
        """Gets the logo of this Organization.  # noqa: E501

        Organization logo  # noqa: E501

        :return: The logo of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._logo

    @logo.setter
    def logo(self, logo):
        """Sets the logo of this Organization.

        Organization logo  # noqa: E501

        :param logo: The logo of this Organization.  # noqa: E501
        :type: str
        """

        self._logo = logo

    @property
    def description(self):
        """Gets the description of this Organization.  # noqa: E501

        Organization description  # noqa: E501

        :return: The description of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Organization.

        Organization description  # noqa: E501

        :param description: The description of this Organization.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def users(self):
        """Gets the users of this Organization.  # noqa: E501


        :return: The users of this Organization.  # noqa: E501
        :rtype: list[OrganizationUser]
        """
        return self._users

    @users.setter
    def users(self, users):
        """Sets the users of this Organization.


        :param users: The users of this Organization.  # noqa: E501
        :type: list[OrganizationUser]
        """

        self._users = users

    @property
    def allowed_actions(self):
        """Gets the allowed_actions of this Organization.  # noqa: E501

        list of actions user is allowed to do on this organization  # noqa: E501

        :return: The allowed_actions of this Organization.  # noqa: E501
        :rtype: list[NamespaceActions]
        """
        return self._allowed_actions

    @allowed_actions.setter
    def allowed_actions(self, allowed_actions):
        """Sets the allowed_actions of this Organization.

        list of actions user is allowed to do on this organization  # noqa: E501

        :param allowed_actions: The allowed_actions of this Organization.  # noqa: E501
        :type: list[NamespaceActions]
        """

        self._allowed_actions = allowed_actions

    @property
    def num_of_arrays(self):
        """Gets the num_of_arrays of this Organization.  # noqa: E501

        number of registered arrays for this organization  # noqa: E501

        :return: The num_of_arrays of this Organization.  # noqa: E501
        :rtype: float
        """
        return self._num_of_arrays

    @num_of_arrays.setter
    def num_of_arrays(self, num_of_arrays):
        """Sets the num_of_arrays of this Organization.

        number of registered arrays for this organization  # noqa: E501

        :param num_of_arrays: The num_of_arrays of this Organization.  # noqa: E501
        :type: float
        """

        self._num_of_arrays = num_of_arrays

    @property
    def enabled_features(self):
        """Gets the enabled_features of this Organization.  # noqa: E501

        List of extra/optional/beta features to enable for namespace  # noqa: E501

        :return: The enabled_features of this Organization.  # noqa: E501
        :rtype: list[str]
        """
        return self._enabled_features

    @enabled_features.setter
    def enabled_features(self, enabled_features):
        """Sets the enabled_features of this Organization.

        List of extra/optional/beta features to enable for namespace  # noqa: E501

        :param enabled_features: The enabled_features of this Organization.  # noqa: E501
        :type: list[str]
        """

        self._enabled_features = enabled_features

    @property
    def unpaid_subscription(self):
        """Gets the unpaid_subscription of this Organization.  # noqa: E501

        A notice that the user has an unpaid subscription  # noqa: E501

        :return: The unpaid_subscription of this Organization.  # noqa: E501
        :rtype: bool
        """
        return self._unpaid_subscription

    @unpaid_subscription.setter
    def unpaid_subscription(self, unpaid_subscription):
        """Sets the unpaid_subscription of this Organization.

        A notice that the user has an unpaid subscription  # noqa: E501

        :param unpaid_subscription: The unpaid_subscription of this Organization.  # noqa: E501
        :type: bool
        """

        self._unpaid_subscription = unpaid_subscription

    @property
    def default_s3_path(self):
        """Gets the default_s3_path of this Organization.  # noqa: E501

        The default location to store newly-created notebooks and other assets like UDFs. The name `default_s3_path` is a legacy holdover; it may refer to any supported storage location.   # noqa: E501

        :return: The default_s3_path of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._default_s3_path

    @default_s3_path.setter
    def default_s3_path(self, default_s3_path):
        """Sets the default_s3_path of this Organization.

        The default location to store newly-created notebooks and other assets like UDFs. The name `default_s3_path` is a legacy holdover; it may refer to any supported storage location.   # noqa: E501

        :param default_s3_path: The default_s3_path of this Organization.  # noqa: E501
        :type: str
        """

        self._default_s3_path = default_s3_path

    @property
    def default_s3_path_credentials_name(self):
        """Gets the default_s3_path_credentials_name of this Organization.  # noqa: E501

        The name of the credentials used to create and access files in the `default_s3_path`, if needed.   # noqa: E501

        :return: The default_s3_path_credentials_name of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._default_s3_path_credentials_name

    @default_s3_path_credentials_name.setter
    def default_s3_path_credentials_name(self, default_s3_path_credentials_name):
        """Sets the default_s3_path_credentials_name of this Organization.

        The name of the credentials used to create and access files in the `default_s3_path`, if needed.   # noqa: E501

        :param default_s3_path_credentials_name: The default_s3_path_credentials_name of this Organization.  # noqa: E501
        :type: str
        """

        self._default_s3_path_credentials_name = default_s3_path_credentials_name

    @property
    def asset_locations(self):
        """Gets the asset_locations of this Organization.  # noqa: E501


        :return: The asset_locations of this Organization.  # noqa: E501
        :rtype: AssetLocations
        """
        return self._asset_locations

    @asset_locations.setter
    def asset_locations(self, asset_locations):
        """Sets the asset_locations of this Organization.


        :param asset_locations: The asset_locations of this Organization.  # noqa: E501
        :type: AssetLocations
        """

        self._asset_locations = asset_locations

    @property
    def stripe_connect(self):
        """Gets the stripe_connect of this Organization.  # noqa: E501

        Denotes that the organization is able to apply pricing to arrays by means of Stripe Connect  # noqa: E501

        :return: The stripe_connect of this Organization.  # noqa: E501
        :rtype: bool
        """
        return self._stripe_connect

    @stripe_connect.setter
    def stripe_connect(self, stripe_connect):
        """Sets the stripe_connect of this Organization.

        Denotes that the organization is able to apply pricing to arrays by means of Stripe Connect  # noqa: E501

        :param stripe_connect: The stripe_connect of this Organization.  # noqa: E501
        :type: bool
        """

        self._stripe_connect = stripe_connect

    @property
    def assume_role_arn(self):
        """Gets the assume_role_arn of this Organization.  # noqa: E501

        A AWS Role that will be first assumed before assuming the organization's AWS Role. Visible to owners and admins.   # noqa: E501

        :return: The assume_role_arn of this Organization.  # noqa: E501
        :rtype: str
        """
        return self._assume_role_arn

    @assume_role_arn.setter
    def assume_role_arn(self, assume_role_arn):
        """Sets the assume_role_arn of this Organization.

        A AWS Role that will be first assumed before assuming the organization's AWS Role. Visible to owners and admins.   # noqa: E501

        :param assume_role_arn: The assume_role_arn of this Organization.  # noqa: E501
        :type: str
        """

        self._assume_role_arn = assume_role_arn

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
        if not isinstance(other, Organization):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Organization):
            return True

        return self.to_dict() != other.to_dict()
