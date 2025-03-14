"""Tests of low-level client construction."""

import json

import pytest

import tiledb.cloud.client
from tiledb.cloud._common.api_v4.api import assets_api


class NoResponseError(Exception):
    """Raise when an intercepted request has no response."""


@pytest.fixture(scope="function")
def workspace_header_check(monkeypatch):
    """Intercept server requests and checks the headers."""

    def fake_and_check_request(self, method, url, *args, **kwargs):
        assert kwargs["headers"]["X-TILEDB-WORKSPACE-ID"] == "workspace"
        raise NoResponseError("Intercepted request has no response")

    monkeypatch.setattr("urllib3.PoolManager.urlopen", fake_and_check_request)


def test_workspace_header(monkeypatch, workspace_header_check):
    """Check v4 HTTP request for workspace header."""
    # Simulate login to a workspace using username/password.
    monkeypatch.setattr(tiledb.cloud.client.config, "workspace_id", "workspace")
    monkeypatch.setattr(tiledb.cloud.client.config._config, "username", "testuser")
    monkeypatch.setattr(tiledb.cloud.client.config._config, "password", "password")
    monkeypatch.setattr(tiledb.cloud.client.config._config, "api_key", {})
    monkeypatch.setattr(tiledb.cloud.client.config, "logged_in", True)

    client = tiledb.cloud.client.Client()
    # We could use any v4 endpoint, asset listing is a choice.
    api_instance = client.build(assets_api.AssetsApi)

    # The workspace_header_check fixture asserts that the HTTP request
    # the X-TILEDB-WORKSPACE-ID header. No valid response is prepared,
    # we catch the fixture's normal exception instead. If the expected
    # header wasn't found, an AssertionError would be raised.
    with pytest.raises(NoResponseError):
        api_instance.list_assets("teamspace")


def test_login_workspace(monkeypatch, tmp_path):
    """Accept and store workspace when logging in."""
    # Use monkeypatch to simulate logging out.
    monkeypatch.setattr(
        tiledb.cloud.client.config,
        "default_config_file",
        tmp_path.joinpath("cloud.json"),
    )
    monkeypatch.setattr(
        tiledb.cloud.client.config,
        "_config",
        tiledb.cloud.config.configuration.Configuration(),
    )
    monkeypatch.setattr(
        tiledb.cloud.client.config,
        "workspace_id",
        None,
    )
    monkeypatch.setattr(tiledb.cloud.client.config, "logged_in", False)

    tiledb.cloud.login(
        username="testuser", password="password", workspace="workspace", no_session=True
    )
    assert tiledb.cloud.client.config.config.username == "testuser"
    assert tiledb.cloud.client.config.config.password == "password"
    assert tiledb.cloud.client.config.workspace_id == "workspace"
    assert tiledb.cloud.client.config.logged_in
    assert tmp_path.joinpath("cloud.json").exists()
    assert json.load(tmp_path.joinpath("cloud.json").open())["workspace"] == "workspace"


def test_login_error(monkeypatch, tmp_path):
    """Token and workspace are incompatible."""
    # Use monkeypatch to simulate logging out.
    monkeypatch.setattr(
        tiledb.cloud.client.config,
        "default_config_file",
        tmp_path.joinpath("cloud.json"),
    )
    monkeypatch.setattr(
        tiledb.cloud.client.config,
        "_config",
        tiledb.cloud.config.configuration.Configuration(),
    )
    monkeypatch.setattr(
        tiledb.cloud.client.config,
        "workspace_id",
        None,
    )
    monkeypatch.setattr(tiledb.cloud.client.config, "logged_in", False)

    with pytest.raises(tiledb.cloud.client.LoginError):
        tiledb.cloud.login(
            username="testuser", token="token", workspace="workspace", no_session=True
        )

    # Assert that login state hasn't changed.
    assert tiledb.cloud.client.config.config.username is None
    assert tiledb.cloud.client.config.config.password is None
    assert tiledb.cloud.client.config.config.api_key == {}
    assert tiledb.cloud.client.config.workspace_id is None
    assert not tiledb.cloud.client.config.logged_in
    assert not tmp_path.joinpath("cloud.json").exists()
