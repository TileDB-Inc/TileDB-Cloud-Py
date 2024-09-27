"""Tests of configuration and login."""

import tiledb.cloud
import tiledb.cloud.config


def test_login_bare_host():
    """Accept a bare host, store it with https scheme."""
    tiledb.cloud.login(token="foo", host="bar")
    assert tiledb.cloud.config.config.host == "https://bar"
