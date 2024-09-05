# coding: utf-8

"""
    TileDB Storage Platform API

    TileDB Storage Platform REST API

    The version of the OpenAPI document: 2.17.51
    Generated by: https://openapi-generator.tech
"""


import pprint

from tiledb.cloud.rest_api.configuration import Configuration


class Invitation:
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
        "invitation_type": "InvitationType",
        "owner_namespace_uuid": "str",
        "inviter_uuid": "str",
        "user_namespace_uuid": "str",
        "organization_user_uuid": "str",
        "organization_name": "str",
        "organization_role": "OrganizationRoles",
        "organization_uuid": "str",
        "array_uuid": "str",
        "group_uuid": "str",
        "array_name": "str",
        "email": "str",
        "actions": "str",
        "group_actions": "str",
        "status": "InvitationStatus",
        "created_at": "datetime",
        "expires_at": "datetime",
        "accepted_at": "datetime",
        "namespace_invited": "str",
    }

    attribute_map = {
        "id": "id",
        "invitation_type": "invitation_type",
        "owner_namespace_uuid": "owner_namespace_uuid",
        "inviter_uuid": "inviter_uuid",
        "user_namespace_uuid": "user_namespace_uuid",
        "organization_user_uuid": "organization_user_uuid",
        "organization_name": "organization_name",
        "organization_role": "organization_role",
        "organization_uuid": "organization_uuid",
        "array_uuid": "array_uuid",
        "group_uuid": "group_uuid",
        "array_name": "array_name",
        "email": "email",
        "actions": "actions",
        "group_actions": "group_actions",
        "status": "status",
        "created_at": "created_at",
        "expires_at": "expires_at",
        "accepted_at": "accepted_at",
        "namespace_invited": "namespace_invited",
    }

    def __init__(
        self,
        id=None,
        invitation_type=None,
        owner_namespace_uuid=None,
        inviter_uuid=None,
        user_namespace_uuid=None,
        organization_user_uuid=None,
        organization_name=None,
        organization_role=None,
        organization_uuid=None,
        array_uuid=None,
        group_uuid=None,
        array_name=None,
        email=None,
        actions=None,
        group_actions=None,
        status=None,
        created_at=None,
        expires_at=None,
        accepted_at=None,
        namespace_invited=None,
        local_vars_configuration=None,
    ):
        """Invitation - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._invitation_type = None
        self._owner_namespace_uuid = None
        self._inviter_uuid = None
        self._user_namespace_uuid = None
        self._organization_user_uuid = None
        self._organization_name = None
        self._organization_role = None
        self._organization_uuid = None
        self._array_uuid = None
        self._group_uuid = None
        self._array_name = None
        self._email = None
        self._actions = None
        self._group_actions = None
        self._status = None
        self._created_at = None
        self._expires_at = None
        self._accepted_at = None
        self._namespace_invited = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if invitation_type is not None:
            self.invitation_type = invitation_type
        if owner_namespace_uuid is not None:
            self.owner_namespace_uuid = owner_namespace_uuid
        if inviter_uuid is not None:
            self.inviter_uuid = inviter_uuid
        if user_namespace_uuid is not None:
            self.user_namespace_uuid = user_namespace_uuid
        if organization_user_uuid is not None:
            self.organization_user_uuid = organization_user_uuid
        if organization_name is not None:
            self.organization_name = organization_name
        if organization_role is not None:
            self.organization_role = organization_role
        if organization_uuid is not None:
            self.organization_uuid = organization_uuid
        if array_uuid is not None:
            self.array_uuid = array_uuid
        if group_uuid is not None:
            self.group_uuid = group_uuid
        if array_name is not None:
            self.array_name = array_name
        if email is not None:
            self.email = email
        if actions is not None:
            self.actions = actions
        if group_actions is not None:
            self.group_actions = group_actions
        if status is not None:
            self.status = status
        if created_at is not None:
            self.created_at = created_at
        if expires_at is not None:
            self.expires_at = expires_at
        if accepted_at is not None:
            self.accepted_at = accepted_at
        if namespace_invited is not None:
            self.namespace_invited = namespace_invited

    @property
    def id(self):
        """Gets the id of this Invitation.

        Unique ID of invitation added to magic link

        :return: The id of this Invitation.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Invitation.

        Unique ID of invitation added to magic link

        :param id: The id of this Invitation.
        :type: str
        """

        self._id = id

    @property
    def invitation_type(self):
        """Gets the invitation_type of this Invitation.


        :return: The invitation_type of this Invitation.
        :rtype: InvitationType
        """
        return self._invitation_type

    @invitation_type.setter
    def invitation_type(self, invitation_type):
        """Sets the invitation_type of this Invitation.


        :param invitation_type: The invitation_type of this Invitation.
        :type: InvitationType
        """

        self._invitation_type = invitation_type

    @property
    def owner_namespace_uuid(self):
        """Gets the owner_namespace_uuid of this Invitation.

        Namespace of the owner of the invitation (user or organization)

        :return: The owner_namespace_uuid of this Invitation.
        :rtype: str
        """
        return self._owner_namespace_uuid

    @owner_namespace_uuid.setter
    def owner_namespace_uuid(self, owner_namespace_uuid):
        """Sets the owner_namespace_uuid of this Invitation.

        Namespace of the owner of the invitation (user or organization)

        :param owner_namespace_uuid: The owner_namespace_uuid of this Invitation.
        :type: str
        """

        self._owner_namespace_uuid = owner_namespace_uuid

    @property
    def inviter_uuid(self):
        """Gets the inviter_uuid of this Invitation.

        Unique ID of the user that sent the invitation

        :return: The inviter_uuid of this Invitation.
        :rtype: str
        """
        return self._inviter_uuid

    @inviter_uuid.setter
    def inviter_uuid(self, inviter_uuid):
        """Sets the inviter_uuid of this Invitation.

        Unique ID of the user that sent the invitation

        :param inviter_uuid: The inviter_uuid of this Invitation.
        :type: str
        """

        self._inviter_uuid = inviter_uuid

    @property
    def user_namespace_uuid(self):
        """Gets the user_namespace_uuid of this Invitation.

        Unique ID of the user accepted the invitation

        :return: The user_namespace_uuid of this Invitation.
        :rtype: str
        """
        return self._user_namespace_uuid

    @user_namespace_uuid.setter
    def user_namespace_uuid(self, user_namespace_uuid):
        """Sets the user_namespace_uuid of this Invitation.

        Unique ID of the user accepted the invitation

        :param user_namespace_uuid: The user_namespace_uuid of this Invitation.
        :type: str
        """

        self._user_namespace_uuid = user_namespace_uuid

    @property
    def organization_user_uuid(self):
        """Gets the organization_user_uuid of this Invitation.

        Unique ID of the organization user accepted the invitation

        :return: The organization_user_uuid of this Invitation.
        :rtype: str
        """
        return self._organization_user_uuid

    @organization_user_uuid.setter
    def organization_user_uuid(self, organization_user_uuid):
        """Sets the organization_user_uuid of this Invitation.

        Unique ID of the organization user accepted the invitation

        :param organization_user_uuid: The organization_user_uuid of this Invitation.
        :type: str
        """

        self._organization_user_uuid = organization_user_uuid

    @property
    def organization_name(self):
        """Gets the organization_name of this Invitation.

        Name of the organization, does not persist in database

        :return: The organization_name of this Invitation.
        :rtype: str
        """
        return self._organization_name

    @organization_name.setter
    def organization_name(self, organization_name):
        """Sets the organization_name of this Invitation.

        Name of the organization, does not persist in database

        :param organization_name: The organization_name of this Invitation.
        :type: str
        """

        self._organization_name = organization_name

    @property
    def organization_role(self):
        """Gets the organization_role of this Invitation.


        :return: The organization_role of this Invitation.
        :rtype: OrganizationRoles
        """
        return self._organization_role

    @organization_role.setter
    def organization_role(self, organization_role):
        """Sets the organization_role of this Invitation.


        :param organization_role: The organization_role of this Invitation.
        :type: OrganizationRoles
        """

        self._organization_role = organization_role

    @property
    def organization_uuid(self):
        """Gets the organization_uuid of this Invitation.

        Unique ID of the organization whose user(s) accepted the invitation

        :return: The organization_uuid of this Invitation.
        :rtype: str
        """
        return self._organization_uuid

    @organization_uuid.setter
    def organization_uuid(self, organization_uuid):
        """Sets the organization_uuid of this Invitation.

        Unique ID of the organization whose user(s) accepted the invitation

        :param organization_uuid: The organization_uuid of this Invitation.
        :type: str
        """

        self._organization_uuid = organization_uuid

    @property
    def array_uuid(self):
        """Gets the array_uuid of this Invitation.

        Unique ID of the array

        :return: The array_uuid of this Invitation.
        :rtype: str
        """
        return self._array_uuid

    @array_uuid.setter
    def array_uuid(self, array_uuid):
        """Sets the array_uuid of this Invitation.

        Unique ID of the array

        :param array_uuid: The array_uuid of this Invitation.
        :type: str
        """

        self._array_uuid = array_uuid

    @property
    def group_uuid(self):
        """Gets the group_uuid of this Invitation.

        Unique ID of the group

        :return: The group_uuid of this Invitation.
        :rtype: str
        """
        return self._group_uuid

    @group_uuid.setter
    def group_uuid(self, group_uuid):
        """Sets the group_uuid of this Invitation.

        Unique ID of the group

        :param group_uuid: The group_uuid of this Invitation.
        :type: str
        """

        self._group_uuid = group_uuid

    @property
    def array_name(self):
        """Gets the array_name of this Invitation.

        Name of the array, does not persist in database

        :return: The array_name of this Invitation.
        :rtype: str
        """
        return self._array_name

    @array_name.setter
    def array_name(self, array_name):
        """Sets the array_name of this Invitation.

        Name of the array, does not persist in database

        :param array_name: The array_name of this Invitation.
        :type: str
        """

        self._array_name = array_name

    @property
    def email(self):
        """Gets the email of this Invitation.

        Email of the individual we send the invitation to

        :return: The email of this Invitation.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this Invitation.

        Email of the individual we send the invitation to

        :param email: The email of this Invitation.
        :type: str
        """

        self._email = email

    @property
    def actions(self):
        """Gets the actions of this Invitation.

        A comma separated list of ArrayActions or NamespaceActions

        :return: The actions of this Invitation.
        :rtype: str
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """Sets the actions of this Invitation.

        A comma separated list of ArrayActions or NamespaceActions

        :param actions: The actions of this Invitation.
        :type: str
        """

        self._actions = actions

    @property
    def group_actions(self):
        """Gets the group_actions of this Invitation.

        A comma separated list of GroupActions

        :return: The group_actions of this Invitation.
        :rtype: str
        """
        return self._group_actions

    @group_actions.setter
    def group_actions(self, group_actions):
        """Sets the group_actions of this Invitation.

        A comma separated list of GroupActions

        :param group_actions: The group_actions of this Invitation.
        :type: str
        """

        self._group_actions = group_actions

    @property
    def status(self):
        """Gets the status of this Invitation.


        :return: The status of this Invitation.
        :rtype: InvitationStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Invitation.


        :param status: The status of this Invitation.
        :type: InvitationStatus
        """

        self._status = status

    @property
    def created_at(self):
        """Gets the created_at of this Invitation.

        Datetime the invitation was created in UTC

        :return: The created_at of this Invitation.
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Invitation.

        Datetime the invitation was created in UTC

        :param created_at: The created_at of this Invitation.
        :type: datetime
        """

        self._created_at = created_at

    @property
    def expires_at(self):
        """Gets the expires_at of this Invitation.

        Datetime the invitation is expected to expire in UTC

        :return: The expires_at of this Invitation.
        :rtype: datetime
        """
        return self._expires_at

    @expires_at.setter
    def expires_at(self, expires_at):
        """Sets the expires_at of this Invitation.

        Datetime the invitation is expected to expire in UTC

        :param expires_at: The expires_at of this Invitation.
        :type: datetime
        """

        self._expires_at = expires_at

    @property
    def accepted_at(self):
        """Gets the accepted_at of this Invitation.

        Datetime the invitation was accepted in UTC

        :return: The accepted_at of this Invitation.
        :rtype: datetime
        """
        return self._accepted_at

    @accepted_at.setter
    def accepted_at(self, accepted_at):
        """Sets the accepted_at of this Invitation.

        Datetime the invitation was accepted in UTC

        :param accepted_at: The accepted_at of this Invitation.
        :type: datetime
        """

        self._accepted_at = accepted_at

    @property
    def namespace_invited(self):
        """Gets the namespace_invited of this Invitation.

        The namespace invited (user or organization, if it exists in the DB)

        :return: The namespace_invited of this Invitation.
        :rtype: str
        """
        return self._namespace_invited

    @namespace_invited.setter
    def namespace_invited(self, namespace_invited):
        """Sets the namespace_invited of this Invitation.

        The namespace invited (user or organization, if it exists in the DB)

        :param namespace_invited: The namespace_invited of this Invitation.
        :type: str
        """

        self._namespace_invited = namespace_invited

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
        if not isinstance(other, Invitation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Invitation):
            return True

        return self.to_dict() != other.to_dict()
