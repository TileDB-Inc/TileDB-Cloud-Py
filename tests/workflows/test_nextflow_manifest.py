import pytest
from jsonschema import ValidationError

from tiledb.cloud.workflows.nextflow import create_manifest
from tiledb.cloud.workflows.nextflow import validate_manifest

# Run tests with:
#   pytest -m workflows --run-workflows -svvv


@pytest.mark.workflows
def test_validate_manifest():
    manifest = {
        "workflow": {
            "name": "test",
            "version": "0.0.1",
            "teamspace": "tiledb-inc",
            "uri": "tiledb://tiledb-inc/test:0.0.1",
        },
        "metadata": {
            "id": "123",
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

    # Check the create_manifest function.
    uri = "tiledb://tiledb-inc/test:0.0.1"
    manifest = create_manifest(uri)
    validate_manifest(manifest)
