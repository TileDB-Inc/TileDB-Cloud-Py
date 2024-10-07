"""Test of invites."""

import unittest.mock

from tiledb.cloud import invites


@unittest.mock.patch("tiledb.cloud.invites.client")
def test_invite_to_organization(client):
    """Function is properly wired to low-level generated API."""
    # This call used to raise a ValueError.
    invites.invite_to_organization(
        "test_org", recipients=["user1@example.com"], role="read_only"
    )
