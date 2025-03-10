"""Python client tests for v4."""

import uuid

import pytest

import tiledb.cloud._common.api_v4


def test_configure_client():
    """Can configure a client."""
    configuration = tiledb.cloud._common.api_v4.Configuration(
        host="http://localhost:8181/v4"
    )
    with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
        api_instance = tiledb.cloud._common.api_v4.UsersApi(api_client)
        assert hasattr(api_instance, "create_user")


def test_user_create_request():
    """Can create a user creation request."""
    TAG = str(uuid.uuid4())[:8]
    DISPLAY_NAME = "Test User"
    EMAIL = f"testuser-{TAG}@example.com"
    USERNAME = f"testuser-{TAG}"
    PASSWORD = "password"
    request = tiledb.cloud._common.api_v4.models.user_create_request.UserCreateRequest(
        display_name=DISPLAY_NAME,
        email=EMAIL,
        username=USERNAME,
        password=PASSWORD,
    )
    assert request.display_name == DISPLAY_NAME
    assert request.email == EMAIL
    assert request.username == USERNAME
    assert request.password == PASSWORD


@pytest.mark.server
def test_create_user():
    """Can create a user."""
    TAG = str(uuid.uuid4())[:8]
    DISPLAY_NAME = "Test User"
    EMAIL = f"testuser-{TAG}@example.com"
    USERNAME = f"testuser-{TAG}"
    PASSWORD = "password"

    configuration = tiledb.cloud._common.api_v4.Configuration(
        host="http://localhost:8181/v4"
    )
    with tiledb.cloud._common.api_v4.ApiClient(configuration) as api_client:
        api_instance = tiledb.cloud._common.api_v4.UsersApi(api_client)
        request = (
            tiledb.cloud._common.api_v4.models.user_create_request.UserCreateRequest(
                display_name=DISPLAY_NAME,
                email=EMAIL,
                username=USERNAME,
                password=PASSWORD,
            )
        )
        create_response = api_instance.create_user(request)
        assert create_response.data.display_name == DISPLAY_NAME
        assert create_response.data.email == EMAIL
        assert create_response.data.username == USERNAME
        assert not hasattr(create_response.data, "password")
