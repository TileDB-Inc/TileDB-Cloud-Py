import os
from urllib.parse import urlparse

import pytest

import tiledb
import tiledb.cloud
from tiledb.cloud.workflows import register_nextflow
from tiledb.cloud.workflows.common import default_workflows_uri
from tiledb.cloud.workflows.nextflow import clone_workflow

# Run tests with:
#   pytest -m workflows --run-workflows


def check_workflow(
    uri,
    readme_present=True,
):
    with tiledb.Group(uri) as group:
        # Check for expected group members.
        assert "workflow.tgz" in group
        assert "parameters.json" in group
        assert "input.json" in group
        assert ("README.md" in group) == readme_present

        # Check the expected metadata.
        assert "dataset_type" in group.meta
        assert group.meta["dataset_type"] == "workflow"
        assert "language" in group.meta
        assert group.meta["language"] == "nextflow"
        assert "name" in group.meta
        assert "version" in group.meta
        assert "main" in group.meta

    # Check the group description.
    description = tiledb.cloud.asset.info(uri).description
    assert (description != "") == readme_present


def workflow_uri(workflow: str, version: str) -> str:
    """Generate a TileDB URI for a workflow, for test cleanup."""

    if workflow.startswith("https://"):
        workflow = urlparse(workflow).path.strip("/")

    uri = default_workflows_uri() + f"/{workflow}-{version}"
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


@pytest.mark.workflows
@pytest.mark.parametrize(
    "workflow,version",
    [
        ("nf-core/demo", "1.0.1"),
        ("https://github.com/TileDB-Inc/sarek", "tiledb"),
    ],
)
def test_register_workflow(test_fixture, workflow, version):
    # Register the workflow.
    uri = register_nextflow(workflow=workflow, version=version)

    # Check the registered workflow.
    check_workflow(uri)

    # Expect an exception when registering the same workflow again.
    with pytest.raises(FileExistsError):
        register_nextflow(workflow=workflow, version=version)


@pytest.mark.workflows
@pytest.mark.parametrize(
    "workflow,version",
    [("nf-core/demo", "1.0.1")],
)
def test_register_local(tmp_path, version, workflow):
    # Set the workflow name and local path.
    workflow_name = "local-demo"
    local_path = os.path.join(tmp_path, "workflow")

    # Cleanup from previous failed tests.
    delete_workgroup_asset(workflow_uri(workflow_name, version))

    # Clone the workflow to the local_path.
    clone_workflow(workflow, version, local_path)

    # Register the workflow from the local path.
    uri = register_nextflow(
        workflow=workflow_name,
        version=version,
        local_path=local_path,
    )

    # Check the registered workflow.
    check_workflow(uri)

    # Cleanup.
    delete_workgroup_asset(uri)


@pytest.mark.workflows
@pytest.mark.parametrize(
    "workflow,version",
    [("nf-core/demo", "1.0.1")],
)
def test_register_missing_files(tmp_path, version, workflow):
    # Set the workflow name and local path.
    workflow_name = "local-demo"
    local_path = os.path.join(tmp_path, "workflow")

    # Cleanup from previous failed tests.
    delete_workgroup_asset(workflow_uri(workflow_name, version))

    # Clone the workflow to the local_path.
    clone_workflow(workflow, version, local_path)

    # Remove files from the cloned workflow.
    os.remove(os.path.join(local_path, "README.md"))
    os.remove(os.path.join(local_path, "nextflow_schema.json"))
    os.remove(os.path.join(local_path, "assets", "schema_input.json"))

    # Register the workflow from the local path.
    uri = register_nextflow(
        workflow=workflow_name,
        version=version,
        local_path=local_path,
    )

    # Check the registered workflow.
    check_workflow(uri, readme_present=False)

    # Cleanup.
    delete_workgroup_asset(uri)


@pytest.mark.workflows
def test_register_workflow_errors():
    # Expect an exception when specifying a main script that does not exist.
    with pytest.raises(FileNotFoundError):
        register_nextflow(
            workflow="nf-core/demo",
            version="1.0.1",
            main_script="foo.nf",
        )

    # Expect an exception when registering with an invalid workflow
    with pytest.raises(ValueError):
        register_nextflow(
            workflow="https://github.com/TileDB-Inc/empty",
            version="1.0.1",
        )

    # Expect an exception when registering with an invalid version
    with pytest.raises(ValueError):
        register_nextflow(
            workflow="https://github.com/TileDB-Inc/sarek",
            version="-1",
        )

    # Expect an exception when specifying both a URI and a local path.
    with pytest.raises(ValueError):
        register_nextflow(
            workflow="https://github.com/TileDB-Inc/sarek",
            version="1.0.1",
            local_path="foo",
        )
