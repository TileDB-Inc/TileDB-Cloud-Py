import jsonschema

MANIFEST_SCHEMA = {
    "type": "object",
    "properties": {
        "uri": {
            "description": "TileDB URI of the workflow.",
            "type": "string",
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
    "required": ["uri"],
    "additionalProperties": False,
}


def create_manifest(workflow_uri: str) -> dict:
    """
    Create a manifest for a workflow run.

    :param workflow_uri: URI of the workflow template on TileDB
    :return: run manifest
    """

    manifest = {
        "uri": workflow_uri,
        "metadata": {},
        "options": {},
        "params": {},
    }

    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: dict) -> None:
    """
    Validate a run manifest.

    :param manifest: run manifest
    """

    jsonschema.validate(manifest, MANIFEST_SCHEMA)
