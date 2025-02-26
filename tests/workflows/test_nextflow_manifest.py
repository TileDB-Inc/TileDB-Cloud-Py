import pytest
from jsonschema import ValidationError

from tiledb.cloud.workflows.nextflow import create_manifest
from tiledb.cloud.workflows.nextflow import register
from tiledb.cloud.workflows.nextflow import save_manifest
from tiledb.cloud.workflows.nextflow import validate_manifest

from .common import test_fixture  # noqa: F401

# Run tests with:
#   pytest -m workflows --run-workflows -svvv


@pytest.mark.workflows
def test_validate_manifest():
    manifest = {
        "workflow": {
            "uri": "tiledb://tiledb-inc/test:0.0.1",
        },
        "metadata": {
            "name": "123",
            "outdir": "/tiledb/teamspace/workflows/output/123",
            "workdir": "/tiledb/teamspace/workflows/work/123",
        },
        "options": {},
        "params": {
            "foo": "bar",
        },
    }

    validate_manifest(manifest)

    # Remove a required field and expect a ValidationError.
    manifest.pop("workflow")
    with pytest.raises(ValidationError):
        validate_manifest(manifest)


@pytest.mark.workflows
@pytest.mark.parametrize(
    "workflow,version",
    [("https://github.com/TileDB-Inc/sarek", "tiledb")],
)
@pytest.mark.usefixtures("test_fixture")
def test_save_manifest(workflow, version):
    # Register the workflow.
    uri = register(workflow=workflow, version=version)

    # Create a manifest and validate it.
    manifest = create_manifest(uri)
    validate_manifest(manifest)

    # Save the manifest
    save_manifest(manifest)
