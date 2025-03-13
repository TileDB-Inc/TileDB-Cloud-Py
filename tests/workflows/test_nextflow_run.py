import os

import pytest

from tiledb.cloud.workflows.nextflow import create_manifest
from tiledb.cloud.workflows.nextflow import register
from tiledb.cloud.workflows.nextflow import resume
from tiledb.cloud.workflows.nextflow import run

from .common import delete_workgroup_asset
from .common import workflow_uri

# Run tests with:
#   pytest -m workflows --run-workflows -svvv


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
    manifest = create_manifest(uri)
    status, _ = run(manifest)
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
    manifest = create_manifest(uri)
    status, session_id = run(manifest)
    assert status == "ERR"

    # Resume the workflow.
    status, session_id = resume(session_id)
    assert status == "OK"

    # Cleanup.
    delete_workgroup_asset(uri)
