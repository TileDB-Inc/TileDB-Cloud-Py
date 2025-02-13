from threading import Lock

import jsonschema

MANIFEST_SCHEMA = {
    "type": "object",
    "properties": {
        "workflow": {
            "description": "Properties of the workflow template on TileDB.",
            "type": "object",
            "properties": {
                "uri": {
                    "description": "TileDB URI of the workflow.",
                    "type": "string",
                },
                "name": {
                    "description": "Name of the workflow.",
                    "type": "string",
                },
                "version": {
                    "description": "Version of the workflow.",
                    "type": "string",
                },
                "teamspace": {
                    "description": "Teamspace where the workflow is registered.",
                    "type": "string",
                },
            },
            "required": ["uri"],
            "additionalProperties": False,
        },
        "metadata": {
            "description": "Metadata for the run manifest.",
            "type": "object",
            "properties": {
                "id": {
                    "description": "Unique ID for the run manifest.",
                    "type": "string",
                },
                "outdir": {
                    "description": "Path to the workflow output directory.",
                    "type": "string",
                },
                "workdir": {
                    "description": "Path to the workflow working work directory.",
                    "type": "string",
                },
            },
            "required": [],
            "additionalProperties": False,
        },
        "options": {
            "description": "Workflow run options.",
            "type": "object",
            "properties": {
                "profile": {
                    "description": "Configuration profile used.",
                    "type": "string",
                },
                "options": {
                    "description": "Additional options passed to `nextflow run`.",
                    "type": "string",
                },
                "sample_sheet": {
                    "description": "An input sample sheet in CSV or TSV format.",
                    "type": "string",
                },
            },
            "required": [],
            "additionalProperties": False,
        },
        "params": {
            "description": "Workflow parameter values.",
            "type": "object",
            "properties": {},
            "additionalProperties": True,
        },
    },
    "required": ["workflow"],
    "additionalProperties": False,
}

validator = jsonschema.Draft7Validator(MANIFEST_SCHEMA)
lock = Lock()


def create_manifest(workflow_uri: str) -> dict:
    """
    Create a manifest for a workflow run.

    :param workflow_uri: URI of the workflow template on TileDB
    :return: run manifest
    """

    manifest = {
        "workflow": {
            "uri": workflow_uri,
        }
    }

    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: dict) -> None:
    """
    Validate a run manifest.

    :param manifest: run manifest
    """

    print("Validating manifest")
    with lock:
        print("Validating manifest with lock")
        validator.validate(manifest)
        print("Validated manifest")
