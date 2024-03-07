from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud.rest_api.models.invitation_organization_join_email import (
    InvitationOrganizationJoinEmail,
)


def accept_invitation(invitation_id: str) -> None:
    """
    Accept an invitation.

    Args:
        invitation_id (str): the ID of invitation about to be accepted.

    Raises:
        TileDBCloudError

    Returns:
        None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    try:
        return invitation_api.accept_invitation(invitation=invitation_id)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def fetch_invitations(**filters):
    """
    Fetches a paginated list of invitations.

    Args (filters):
        organization (str): name or ID of organization to filter
        array (str): name/uri of array that is url-encoded to filter
        group (str): name or ID of group to filter
        start (int): start time for tasks to filter by
        end (int): end time for tasks to filter by
        page (int): pagination offset
        per_page (int): pagination limit
        type (str): invitation type, \"ARRAY_SHARE\", \"JOIN_ORGANIZATION\"
        status (str): Filter to only return \"PENDING\", \"ACCEPTED\"
        orderby (str): sort by which field valid values include
                       timestamp, array_name, organization_name

    Raises:
        TileDBCloudError

    Returns:
        dict: Invitations and pagination metadata.
    """
    invitation_api = client.build(rest_api.InvitationApi)
    try:
        return invitation_api.fetch_invitations(**filters)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def invite_to_organization(
    organization: str, email_invite: InvitationOrganizationJoinEmail
) -> None:
    """
    Sends email to multiple recipients with joining information
    regarding an organization.

    Args:
        organization (str): name or UUID of organization.
        email_invite (InvitationOrganizationJoinEmail): list of email recipients

    Raises:
        TileDBCloudError

    Returns:
        None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    try:
        return invitation_api.join_organization(organization, email_invite)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def cancel_invite_to_organization(invitation_id: str, organization: str) -> None:
    """
    Cancels join organization invitation.

    Args:
        invitation_id (str): the ID of invitation about to be canceled.
        organization (str): name or UUID of organization.

    Raises:
        TileDBCloudError

    Returns:
        None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    try:
        return invitation_api.cancel_join_organization(invitation_id, organization)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def invite_to_array(
    namespace: str, array: str, email_invite: InvitationOrganizationJoinEmail
) -> None:
    """
    Share array by email invite.

    Args:
        namespace (str): namespace array is in (an organization name or user's username)
        array (str): name/uri of array that is url-encoded
        email_invite (InvitationOrganizationJoinEmail): list of email recipients

    Raises:
        TileDBCloudError

    Returns:
        None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    try:
        return invitation_api.share_array_by_invite(namespace, array, email_invite)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def cancel_share_array_invitation(
    invitation_id: str, namespace: str, array: str
) -> None:
    """
    Cancels array sharing invitation.

    Args:
        invitation_id (str): the ID of invitation about to be canceled.
        namespace (str): namespace array is in (an organization name or user's username)
        array (str): name/uri of array that is url-encoded

    Raises:
        TileDBCloudError

    Returns:
        None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    try:
        return invitation_api.cancel_share_array_by_invite(
            namespace, invitation_id, array
        )
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def invite_to_group(
    namespace: str, group: str, email_invite: InvitationOrganizationJoinEmail
) -> None:
    """
    Sends email to multiple recipients with sharing information regarding a group.

    Args:
        namespace (str): namespace array is in (an organization name or user's username)
        group (str): name/uri of group that is url-encoded
        email_invite (InvitationOrganizationJoinEmail): list of email recipients

    Raises:
        TileDBCloudError

    Returns:
        None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    try:
        return invitation_api.share_group_by_invite(namespace, group, email_invite)
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)


def cancel_share_group_invitation(
    invitation_id: str, namespace: str, group: str
) -> None:
    """
    Cancels group sharing invitation.

    Args:
        invitation_id (str): the ID of invitation about to be canceled.
        namespace (str): namespace array is in (an organization name or user's username)
        group (str): name/uri of group that is url-encoded

    Raises:
        TileDBCloudError

    Returns:
        None
    """
    invitation_api = client.build(rest_api.InvitationApi)
    try:
        return invitation_api.cancel_share_group_by_invite(
            namespace, invitation_id, group
        )
    except rest_api.ApiException as exc:
        raise tiledb_cloud_error.check_exc(exc)
