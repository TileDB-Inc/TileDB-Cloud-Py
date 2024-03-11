from typing import Sequence

from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud._common import utils
from tiledb.cloud.rest_api.models.invitation_array_share_email import (
    InvitationArrayShareEmail,
)
from tiledb.cloud.rest_api.models.invitation_group_share_email import (
    InvitationGroupShareEmail,
)
from tiledb.cloud.rest_api.models.invitation_organization_join_email import (
    InvitationOrganizationJoinEmail,
)


def accept_invitation(invitation_id: str) -> None:
    """
    Accept an invitation.

    :param invitation_id: the ID of invitation about to be accepted.
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
    :param str type: invitation type, "ARRAY_SHARE", "JOIN_ORGANIZATION"
    :param str status: Filter to only return "PENDING", "ACCEPTED"
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
    organization: str, *, recipients: Sequence[str], role: str
) -> None:
    """
    Sends email to multiple recipients with joining information
    regarding an organization.

    :param organization: name or UUID of organization.
    :param recipients: list of recipient emails/usernames.
    :param role: role assigned to the recipient.
    :return: None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    email_invite = InvitationOrganizationJoinEmail(role, recipients)
    try:
        return invitation_api.join_organization(organization, email_invite)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def cancel_invite_to_organization(organization: str, *, invitation_id: str) -> None:
    """
    Cancels join organization invitation.

    :param organization: name or UUID of organization.
    :param invitation_id: the ID of invitation about to be canceled.
    :return: None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    try:
        return invitation_api.cancel_join_organization(invitation_id, organization)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def invite_to_array(
    uri: str, *, recipients: Sequence[str], actions: Sequence[str]
) -> None:
    """
    Share array by email invite.

    :param uri: URI of array in the form 'tiledb://<namespace>/<array>'
    :param recipients: list of recipient emails/usernames.
    :param actions: list of ArrayActions allowed to the recipient.
    :return: None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    namespace, uri = utils.split_uri(uri)
    email_invite = InvitationArrayShareEmail(actions, recipients)
    try:
        return invitation_api.share_array_by_invite(namespace, uri, email_invite)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def cancel_invite_to_array(uri: str, *, invitation_id: str) -> None:
    """
    Cancels array sharing invitation.

    :param uri: URI of array in the form 'tiledb://<namespace>/<array>'
    :param invitation_id: the ID of invitation about to be canceled.
    :return: None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    namespace, uri = utils.split_uri(uri)
    try:
        return invitation_api.cancel_share_array_by_invite(
            namespace, invitation_id, uri
        )
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def invite_to_group(
    uri: str,
    *,
    recipients: Sequence[str],
    array_actions: Sequence[str],
    group_actions: Sequence[str],
) -> None:
    """
    Sends email to multiple recipients with sharing information regarding a group.

    :param uri: URI of group in the form 'tiledb://<namespace>/<group>'
    :param recipients: list of recipient emails/usernames.
    :param array_actions: list of ArrayActions allowed to the recipient.
    :param group_actions: list of GroupActions allowed to the recipient.
    :return: None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    namespace, uri = utils.split_uri(uri)
    email_invite = InvitationGroupShareEmail(array_actions, group_actions, recipients)
    try:
        return invitation_api.share_group_by_invite(namespace, uri, email_invite)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def cancel_invite_to_group(uri: str, *, invitation_id: str) -> None:
    """
    Cancels group sharing invitation.

    :param uri: URI of group in the form 'tiledb://<namespace>/<group>'
    :param invitation_id: the ID of invitation about to be canceled.
    :return: None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    namespace, uri = utils.split_uri(uri)
    try:
        return invitation_api.cancel_share_group_by_invite(
            namespace, invitation_id, uri
        )
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)
