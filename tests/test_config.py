"""Tests of configuration and login."""

import tiledb.cloud
import tiledb.cloud.config


def test_login_bare_host(monkeypatch, tmp_path):
    """Accept a bare host, store it with https scheme."""
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
    monkeypatch.setattr(tiledb.cloud.client.config, "logged_in", False)
    monkeypatch.setattr(tiledb.cloud.client, "client", tiledb.cloud.client.Client())
    tiledb.cloud.login(token="foo", host="bar")
    assert tiledb.cloud.config.config.host == "https://bar"


def test_login_bare_host_bis():
    """Check on the first."""
    assert tiledb.cloud.config.config.host != "https://bar"
