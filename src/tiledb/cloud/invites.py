from typing import List

from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud._common import utils
from tiledb.cloud.rest_api.models.invitation_organization_join_email import (
    InvitationOrganizationJoinEmail,
)
from tiledb.cloud.rest_api.models.organization_roles import OrganizationRoles


def accept_invitation(invitation_id: str) -> None:
    """
    Accept an invitation.

    :param str invitation_id: the ID of invitation about to be accepted.
    :return: None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    try:
        return invitation_api.accept_invitation(invitation=invitation_id)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def fetch_invitations(**filters):
    """
    Fetches a paginated list of invitations.

    :param str organization: name or ID of organization to filter
    :param str array: name/uri of array that is url-encoded to filter
    :param str group: name or ID of group to filter
    :param int start: start time for tasks to filter by
    :param int end: end time for tasks to filter by
    :param int page: pagination offset
    :param int per_page: pagination limit
    :param str type: invitation type, \"ARRAY_SHARE\", \"JOIN_ORGANIZATION\"
    :param str status: Filter to only return \"PENDING\", \"ACCEPTED\"
    :param str orderby: sort by which field valid values include
                        timestamp, array_name, organization_name
    :return dict: Invitations and pagination metadata.
    """
    invitation_api = client.build(rest_api.InvitationApi)
    try:
        return invitation_api.fetch_invitations(**filters)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def invite_to_organization(
    organization: str, *, recipients: List[str], role: OrganizationRoles
) -> None:
    """
    Sends email to multiple recipients with joining information
    regarding an organization.

    :param str organization: name or UUID of organization.
    :param List[str] recipients: list of recipient emails
    :param OrganizationRoles role: role assigned to the recipient.
    :return: None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    email_invite = InvitationOrganizationJoinEmail(
        organization_role=role, invitee_email=recipients
    )
    try:
        return invitation_api.join_organization(organization, email_invite)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def cancel_invite_to_organization(*, invitation_id: str, organization: str) -> None:
    """
    Cancels join organization invitation.

    :param str invitation_id: the ID of invitation about to be canceled.
    :param str organization: name or UUID of organization.
    :return: None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    try:
        return invitation_api.cancel_join_organization(invitation_id, organization)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def invite_to_array(
    array: str, *, recipients: List[str], role: OrganizationRoles
) -> None:
    """
    Share array by email invite.

    :param str array: name/uri of array that is url-encoded
    :param List[str] recipients: list of recipient emails
    :param OrganizationRoles role: role assigned to the recipient.
    :return: None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    namespace, array = utils.split_uri(array)
    email_invite = InvitationOrganizationJoinEmail(
        organization_role=role, invitee_email=recipients
    )
    try:
        return invitation_api.share_array_by_invite(namespace, array, email_invite)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def cancel_share_array_invitation(*, invitation_id: str, array: str) -> None:
    """
    Cancels array sharing invitation.

    :param str invitation_id: the ID of invitation about to be canceled.
    :param str array: name/uri of array that is url-encoded
    :return: None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    namespace, array = utils.split_uri(array)
    try:
        return invitation_api.cancel_share_array_by_invite(
            namespace, invitation_id, array
        )
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def invite_to_group(
    group: str, *, recipients: List[str], role: OrganizationRoles
) -> None:
    """
    Sends email to multiple recipients with sharing information regarding a group.

    :param str group: uri of group that is url-encoded
    :param List[str] recipients: list of recipient emails
    :param OrganizationRoles role: role assigned to the recipient.
    :return: None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    namespace, group = utils.split_uri(group)
    email_invite = InvitationOrganizationJoinEmail(
        organization_role=role, invitee_email=recipients
    )
    try:
        return invitation_api.share_group_by_invite(namespace, group, email_invite)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def cancel_share_group_invitation(*, invitation_id: str, group: str) -> None:
    """
    Cancels group sharing invitation.

    :param str invitation_id: the ID of invitation about to be canceled.
    :param str group: name/uri of group that is url-encoded
    :return: None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    namespace, group = utils.split_uri(group)
    try:
        return invitation_api.cancel_share_group_by_invite(
            namespace, invitation_id, group
        )
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)
