from urllib.parse import urlparse

import pytest

import tiledb
import tiledb.cloud
from tiledb.cloud.workflows.common import get_workflows_uri


def workflow_uri(workflow: str, version: str) -> str:
    """Generate a TileDB URI for a workflow, for test cleanup."""

    if workflow.startswith("https://"):
        workflow = urlparse(workflow).path.strip("/")

    uri = get_workflows_uri() + f"/templates/{workflow}-{version}"
    return uri


def delete_workgroup_asset(uri: str) -> None:
    """Recursively delete a TileDB workgroup asset."""

    # Delete the asset if it exists.
    if tiledb.object_type(uri) is not None:
        tiledb.cloud.asset.delete(uri, recursive=True)

    # Cleanup any remaining assets that were not deleted because they
    # were not in the group.
    assets = ["README.md", "workflow.tgz", "parameters.json", "input.json"]
    for asset in assets:
        asset_uri = f"{uri}/{asset}"
        if tiledb.object_type(asset_uri) is not None:
            tiledb.cloud.asset.delete(asset_uri)


@pytest.fixture
def test_fixture(workflow: str, version: str):
    """
    Test fixture to remove the asset before and after the test.

    This is useful for cleaning up the asset if a previous test failed.

    :param workflow: workflow name or URI
    :param version: workflow version
    :yield: None
    """

    # Setup: delete the asset if it already exists.
    uri = workflow_uri(workflow, version)
    delete_workgroup_asset(uri)

    yield None

    # Teardown: delete the asset.
    delete_workgroup_asset(uri)
