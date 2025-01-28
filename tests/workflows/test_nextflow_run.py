import os
from urllib.parse import urlparse

import pytest

import tiledb
from tiledb.cloud.workflows.common import default_workflows_uri
from tiledb.cloud.workflows.nextflow import register
from tiledb.cloud.workflows.nextflow import resume
from tiledb.cloud.workflows.nextflow import run

PASS_WORKFLOW = '''
process pass_test {
    container 'quay.io/nextflow/bash'

    output:
        stdout
    script:
    """
    echo "PASS - This is a passing workflow."
    """
}

workflow {
    pass_test | view
}
'''


RESUME_WORKFLOW = '''
process resume_test {
    container 'quay.io/nextflow/bash'

    output:
        stdout
    script:
    """
    if [ ${workflow.resume} == true ]; then
        echo "PASS - This is a resumed workflow."
    else
        echo "FAIL - This is not a resumed workflow."
        exit 1
    fi
    """
}

workflow {
    resume_test | view
}
'''


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


@pytest.mark.workflows
def test_run_workflow(tmp_path):
    workflow_name = "pass"
    version = "0.0.0"

    # Cleanup from previous failed tests.
    delete_workgroup_asset(workflow_uri(workflow_name, version))

    # Create the local workflow.
    local_path = os.path.join(tmp_path, "workflow")
    os.mkdir(local_path)
    with open(os.path.join(local_path, "main.nf"), "w") as fp:
        fp.write(PASS_WORKFLOW)

    # Register the workflow from the local path.
    uri = register(
        workflow=workflow_name,
        version=version,
        local_path=local_path,
    )

    # Run the workflow.
    status, _ = run(uri, keep=True)
    assert status == "OK"

    # Cleanup.
    delete_workgroup_asset(uri)


@pytest.mark.workflows
def test_resume_workflow(tmp_path):
    workflow_name = "resume"
    version = "0.0.0"

    # Cleanup from previous failed tests.
    delete_workgroup_asset(workflow_uri(workflow_name, version))

    # Create the local workflow.
    local_path = os.path.join(tmp_path, "workflow")
    os.mkdir(local_path)
    with open(os.path.join(local_path, "main.nf"), "w") as fp:
        fp.write(RESUME_WORKFLOW)

    # Register the workflow from the local path.
    uri = register(
        workflow=workflow_name,
        version=version,
        local_path=local_path,
    )

    # Run the workflow.
    status, session_id = run(uri)
    assert status == "ERR"

    # Resume the workflow.
    status, session_id = resume(session_id)
    assert status == "OK"

    # Cleanup.
    delete_workgroup_asset(uri)


# TODO: test exceptions
