import uuid
from typing import Optional

import jsonschema

import tiledb

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
            },
            "required": ["uri"],
            "additionalProperties": False,
        },
        "metadata": {
            "description": "Metadata for the run manifest.",
            "type": "object",
            "properties": {
                "name": {
                    "description": "Unique name for the run manifest.",
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


def create_manifest(
    workflow_uri: str,
    *,
    name: Optional[str] = None,
    options: Optional[dict] = None,
    params: Optional[dict] = None,
) -> dict:
    """
    Create a manifest for a workflow run.

    :param workflow_uri: URI of the workflow template on TileDB
    :param name: unique name for the manifest, defaults to None which
        creates a name based on the workflow name and version.
    :param options: run options, defaults to None
    :param params: run parameters, defaults to None
    :return: the manifest
    """

    if tiledb.object_type(workflow_uri) != "group":
        raise FileNotFoundError(f"'{workflow_uri}' not found.")

    with tiledb.Group(workflow_uri) as group:
        workflow_name = group.meta.get("name")
        workflow_version = group.meta.get("version")

    if name is None:
        name = f"{workflow_name}:{workflow_version}_{uuid.uuid4().hex[:8]}"

    manifest = {
        "workflow": {
            "uri": workflow_uri,
            "name": workflow_name,
            "version": workflow_version,
        },
        "metadata": {"name": name},
        "options": options.copy() if options is not None else {},
        "params": params.copy() if params is not None else {},
    }

    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: dict) -> None:
    """
    Validate a run manifest.

    :param manifest: run manifest
    """

    jsonschema.validate(manifest, MANIFEST_SCHEMA)
