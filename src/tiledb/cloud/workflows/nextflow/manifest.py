import json
import uuid
from datetime import datetime
from datetime import timezone
from typing import Optional

import jsonschema
import pandas as pd

import tiledb
from tiledb.cloud.utilities import consolidate_and_vacuum

from ..common import get_manifests_uri

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


def create_manifest_array(uri: str) -> None:
    """
    Create a TileDB array to store run manifests.

    :param uri: URI of the manifest array
    """

    d0 = tiledb.Dim(name="name", dtype="ascii")
    domain = tiledb.Domain(d0)

    attrs = [
        tiledb.Attr(name="timestamp", dtype="ascii"),
        tiledb.Attr(name="manifest", dtype="ascii"),
    ]

    # Do not allow duplicate manifest names.
    schema = tiledb.ArraySchema(
        domain=domain,
        sparse=True,
        attrs=attrs,
        allows_duplicates=False,
    )

    tiledb.Array.create(uri, schema)

    # Update the asset name.
    tiledb.cloud.asset.update_info(uri, name="nextflow/manifest")


def save_manifest(
    manifest: dict,
    *,
    teamspace: Optional[str] = None,
    consolidate: bool = True,
) -> None:
    """
    Save a run manifest to a manifest array. The manifest name must be unique.

    :param manifest: run manifest
    :param teamspace: TileDB teamspace, defaults to None
    :param consolidate: consolidate the manifest array, defaults to True
    """

    manifests_uri = get_manifests_uri(teamspace)

    # Create the manifest array if it does not exist.
    if tiledb.object_type(manifests_uri) is None:
        create_manifest_array(manifests_uri)

    # Verify the manifest name is unique.
    manifest_name = manifest["metadata"]["name"]
    with tiledb.open(manifests_uri) as A:
        df = A.df[manifest_name]
        if len(df):
            raise ValueError(f"Manifest name '{manifest_name}' already exists.")

    # Write the manifest to the manifest array.
    with tiledb.open(manifests_uri, mode="w") as A:
        A[manifest_name] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "manifest": json.dumps(manifest),
        }

    # Consolidate the manifest array.
    if consolidate:
        consolidate_and_vacuum(manifests_uri)


def get_manifests(teamspace: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    Return the manifests array as a dataframe.

    :param teamspace: TileDB teamspace containing the manifests array, defaults to None
    :return: manifests array as a dataframe, or None if the array does not exist
    """

    try:
        with tiledb.open(get_manifests_uri(teamspace)) as A:
            df = A.df[:]

        df.sort_values(by="timestamp", ascending=False, inplace=True)

        def get_workflow_name(x):
            manifest = json.loads(x)
            return f"{manifest['workflow']['name']}:{manifest['workflow']['version']}"

        # Append the name column
        df["workflow"] = df["manifest"].apply(get_workflow_name)

    except Exception:
        return None

    return df


def consolidate_manifests(teamspace: Optional[str] = None) -> None:
    """
    Consolidate the manifests array.

    :param teamspace: TileDB teamspace containing the manifest array, defaults to None
    """

    manifests_uri = get_manifests_uri(teamspace)
    consolidate_and_vacuum(manifests_uri)
