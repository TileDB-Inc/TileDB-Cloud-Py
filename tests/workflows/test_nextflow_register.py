import os

import pytest

import tiledb
import tiledb.cloud
from tiledb.cloud.workflows.nextflow import register
from tiledb.cloud.workflows.nextflow.register import clone_workflow

from .common import delete_workgroup_asset
from .common import test_fixture  # noqa: F401
from .common import workflow_uri

# Run tests with:
#   pytest -m workflows --run-workflows -svvv


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


@pytest.mark.workflows
@pytest.mark.parametrize(
    "workflow,version",
    [
        ("nf-core/demo", "1.0.1"),
        ("https://github.com/TileDB-Inc/sarek", "tiledb"),
    ],
)
@pytest.mark.usefixtures("test_fixture")
def test_register_workflow(workflow, version):
    # Register the workflow.
    uri = register(workflow=workflow, version=version)

    # Check the registered workflow.
    check_workflow(uri)

    # Expect an exception when registering the same workflow again.
    with pytest.raises(FileExistsError):
        register(workflow=workflow, version=version)


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
    uri = register(
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
    uri = register(
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
        register(
            workflow="nf-core/demo",
            version="1.0.1",
            main_script="foo.nf",
        )

    # Expect an exception when registering with an invalid workflow
    with pytest.raises(ValueError):
        register(
            workflow="https://github.com/TileDB-Inc/empty",
            version="1.0.1",
        )

    # Expect an exception when registering with an invalid version
    with pytest.raises(ValueError):
        register(
            workflow="https://github.com/TileDB-Inc/sarek",
            version="-1",
        )

    # Expect an exception when specifying both a URI and a local path.
    with pytest.raises(ValueError):
        register(
            workflow="https://github.com/TileDB-Inc/sarek",
            version="1.0.1",
            local_path="foo",
        )


@pytest.mark.skip(reason="Requires a private repository URL and token.")
@pytest.mark.workflows
@pytest.mark.parametrize(
    "workflow,version",
    [
        ("__private_repo_url__", "__branch__"),
    ],
)
@pytest.mark.usefixtures("test_fixture")
def test_register_workflow_scm(workflow, version):
    # Register the workflow.
    uri = register(
        workflow=workflow,
        version=version,
        provider="github",
        user="...",
        token="...",
    )

    # Check the registered workflow.
    check_workflow(uri)
