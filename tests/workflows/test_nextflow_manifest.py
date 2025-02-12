import pytest
from jsonschema import ValidationError
from jsonschema import validate

from tiledb.cloud.workflows.nextflow.run import MANIFEST_SCHEMA

# Run tests with:
#   pytest -m workflows --run-workflows -svvv


@pytest.mark.workflows
def test_validate_manifest():
    manifest = {
        "workflow": {
            "name": "test",
            "version": "0.0.1",
            "teamspace": "tiledb-inc",
            "tiledb_uri": "tiledb://tiledb-inc/test:0.0.1",
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

    validate(manifest, MANIFEST_SCHEMA)

    # Remove a required field and expect a ValidationError.
    manifest.pop("workflow")
    with pytest.raises(ValidationError):
        validate(manifest, MANIFEST_SCHEMA)
