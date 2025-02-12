"""Functions for working with Nextflow workflows."""

import io
import json
import os
import re
import subprocess
import tarfile
import uuid
from typing import Optional

import jsonschema

import tiledb
import tiledb.cloud

from ..common import cd_tmpdir
from ..common import default_outdir
from ..common import default_workdir
from ..common import download_group_files
from ..common import workflow_history_uri
from .history import update_history

MANIFEST_SCHEMA = {
    "type": "object",
    "properties": {
        "workflow": {
            "description": "Properties of the workflow template on TileDB.",
            "type": "object",
            "properties": {
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
                "tiledb_uri": {
                    "description": "TileDB URI of the workflow.",
                    "type": "string",
                },
            },
            "required": ["name", "version", "teamspace", "tiledb_uri"],
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
            "required": ["id", "outdir", "workdir"],
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
    "required": ["workflow", "metadata"],
    "additionalProperties": False,
}


def extract_tar_bytes(tar_bytes: bytes, path: str = ".") -> None:
    """
    Extract a tarfile stored in memory to a directory.

    :param tar_bytes: tarfile stored in memory as bytes
    :param path: directory to extract the tarfile, defaults to "."
    """

    with io.BytesIO(tar_bytes) as buffer:
        with tarfile.open(fileobj=buffer, mode="r:gz") as tar:
            tar.extractall(path)


def get_run_command(
    *,
    workflow_uri: str,
    manifest: dict = {},
    namespace: Optional[str] = None,
    run_uuid: Optional[str] = None,
) -> tuple[list[str], str]:
    """
    Prepare to run the Nextflow workflow and return the command to run.

    :param workflow_uri: workflow URI
    :param manifest: run manifest used to launch the workflow, defaults to {}
    :param namespace: TileDB namespace where the workflow will run, defaults to None
    :param run_uuid: unique identifier for the run, defaults to None, which generates
        a new UUID
    :return: run_command, workdir
    """

    if run_uuid is None:
        run_uuid = str(uuid.uuid4())

    # Read from the workflow metadata.
    with tiledb.Group(workflow_uri) as g:
        workflow_name = g.meta["name"].replace("/", "-")
        main = workflow_name + "/" + g.meta["main"]

    # Download the workflow tarfile.
    download_group_files(workflow_uri, "workflow.tgz")

    # Extract the workflow to a directory with the workflow name
    # since the directory name is visible in the Nextflow logs.
    with tarfile.open("workflow.tgz") as tar:
        tar.extractall()
    if os.path.exists(workflow_name):
        raise ValueError(f"Workflow directory '{workflow_name}' already exists.")
    os.rename("workflow", workflow_name)

    # Get the parameters used on the command line.
    profile = manifest.get("options", {}).get("profile", None)
    options = manifest.get("options", {}).get("options", None)

    # Set unique workdir and outdir for the run.
    workdir = default_workdir(namespace) + "/" + run_uuid
    outdir = default_outdir(namespace) + "/" + run_uuid

    # Set the workflow parameters.
    params = manifest.get("options", {})

    # If provided, save the sample sheet to a file and override the input parameter.
    sample_sheet = manifest.get("options", {}).get("sample_sheet", None)
    if sample_sheet:
        sample_sheet_file = "sample_sheet.csv"
        with open(sample_sheet_file, "w") as fp:
            fp.write(sample_sheet)
        params["input"] = sample_sheet_file

    # Dump the parameters to a file.
    if params:
        nf_json = json.dumps(params, indent=4)
        with open("nf-params.json", "w") as fp:
            fp.write(nf_json)

    # Build the Nextflow command as an array.
    cmd = [
        "nextflow",
        "run",
        main,
        "-c",
        "tiledb.config",
    ]

    if params:
        cmd += ["-params-file", "nf-params.json"]
    if workdir:
        cmd += ["-work-dir", workdir]
    if profile:
        cmd += ["-profile", profile]
    if outdir:
        cmd += ["--outdir", outdir]
    if options:
        cmd += options.split()

    return cmd, workdir


def setup_nextflow(
    namespace: str,
    acn: str,
    *,
    plugin_id: str = "nf-tiledb@0.1.0",
    config_file: str = "tiledb.config",
) -> None:
    """
    Setup the Nextflow environment to run a workflow on TileDB.

    - Create a tiledb.config file in the current directory.
    - Copy the Nextflow TileDB plugin to the required location, if needed.
    - Set Nextflow environment variables.

    :param namespace: TileDB namespace where the workflow will run
    :param acn: TileDB access credentials name
    :param plugin_id: TileDB plugin ID, defaults to "nf-tiledb@0.1.0"
    :param config_file: name of the config file, defaults to "tiledb.config"
    """

    # Validate user input.
    if namespace and acn is None:
        raise ValueError("Access credentials name required with namespace.")

    if acn and namespace is None:
        raise ValueError("Namespace required with access credentials name.")

    # Get the namespace and access credentials name, if not provided.
    if namespace is None:
        namespace = tiledb.cloud.client.default_charged_namespace()
        org = tiledb.cloud.client.organization(namespace)
        acn = org.default_s3_path_credentials_name

    try:
        config = tiledb.cloud.Ctx().config()
    except Exception:
        raise "Login to TileDB before running a workflow."

    # Get the token from the config or current session.
    token = config.get("rest.token", None)
    if not token:
        user_api = tiledb.cloud.client.Client().build(tiledb.cloud.rest_api.UserApi)
        token = user_api.get_session(remember_me=True).token

    host = config["rest.server_address"]

    tiledb_config_str = f"""process {{
  executor = 'tiledb'
}}
plugins {{
    id '{plugin_id}'
}}
tiledb {{
  namespace = '{namespace}'
  accessCredentialsName = '{acn}'
  login {{
    host = '{host}'
    token = '{token}'
  }}
}}
"""

    with open(config_file, "w") as fp:
        fp.write(tiledb_config_str)

    # TODO: copy the plugin to $HOME/.nextflow/plugins and unzip with `jar xf`.

    # Set the Nextflow environment variables.
    os.environ["NXF_DISABLE_CHECK_LATEST"] = "true"
    os.environ["NXF_ANSI_LOG"] = "true"


def run(
    workflow_uri: str,
    *,
    manifest: dict = {},
    namespace: Optional[str] = None,
    acn: Optional[str] = None,
    run_uuid: Optional[str] = None,
    tmpdir: Optional[str] = None,
    run_wrapper: Optional[callable] = None,
    keep: bool = False,
) -> tuple[str, str]:
    """
    Run a workflow asset on TileDB.

    :param workflow_uri: TileDB URI of the workflow asset
    :param manifest: run manifest used to launch the workflow, defaults to {}
    :param namespace: TileDB namespace where the workflow will run, defaults to None,
        the default charged namespace
    :param acn: TileDB access credentials name, defaults to None
    :param run_uuid: unique identifier for the run, defaults to None, which generates
        a new UUID
    :param tmpdir: temporary run directory, defaults to None
    :param run_wrapper: function to run the command, defaults to None
    :param keep: keep the temporary run directory, defaults to False
    :return: status, session ID
    """

    # Validate user input.
    if tiledb.object_type(workflow_uri) != "group":
        raise FileNotFoundError(f"'{workflow_uri}' not found.")

    jsonschema.validate(manifest, MANIFEST_SCHEMA)

    # Run the workflow in a temporary directory.
    with cd_tmpdir(keep=keep, tmpdir=tmpdir):
        if keep:
            print(f"Running in {os.getcwd()}")

        # Setup the nextflow environment.
        setup_nextflow(namespace, acn)

        # Setup the command to run the workflow.
        cmd, workdir = get_run_command(
            workflow_uri=workflow_uri,
            manifest=manifest,
            namespace=namespace,
            run_uuid=run_uuid,
        )

        # Run the workflow.
        if run_wrapper:
            run_wrapper(cmd)
        else:
            subprocess.run(cmd)

        # Update the history.
        status, session_id = update_history(workflow_uri)

        # Remove the workdir if the workflow was successful.
        if status == "OK":
            vfs = tiledb.VFS()
            vfs.remove_dir(workdir)

    return status, session_id


def resume(
    session_id: str,
    *,
    namespace: Optional[str] = None,
    acn: Optional[str] = None,
    keep: bool = False,
    tmpdir: Optional[str] = None,
    run_wrapper: Optional[callable] = None,
) -> tuple[str, str]:
    """
    Resume a workflow run from the history array.

    :param session_id: session ID from the history array
    :param namespace: TileDB namespace containing the history array, defaults to None
    :param acn: TileDB access credentials name, defaults to None
    :param keep: keep the temporary run directory, defaults to False
    :param tmpdir: temporary run directory, defaults to None
    :param run_wrapper: function to run the command, defaults to None
    :return: status, session ID
    """

    with cd_tmpdir(keep=keep, tmpdir=tmpdir):
        if keep:
            print(f"Running in {os.getcwd()}")

        # Setup the nextflow environment.
        setup_nextflow(namespace, acn)

        # Read the history from the array.
        history_uri = workflow_history_uri(namespace)

        with tiledb.open(history_uri) as A:
            data = A[session_id]

        # Raise an exception if the session ID is not found.
        if len(data["workflow_uri"]) == 0:
            raise ValueError(f"session_id '{session_id}' not found in '{history_uri}'.")

        # Download the workflow files.
        workflow_uri = data["workflow_uri"][0]

        download_group_files(workflow_uri, "workflow.tgz")

        with tiledb.Group(workflow_uri) as g:
            workflow_name = g.meta["name"].replace("/", "-")

        # Extract the workflow to a directory with the workflow name
        # since the directory name is visible in the Nextflow logs.
        with tarfile.open("workflow.tgz") as tar:
            tar.extractall()
        if os.path.exists(workflow_name):
            raise ValueError(f"Workflow directory '{workflow_name}' already exists.")
        os.rename("workflow", workflow_name)

        # Extract nextflow_tgz in the current directory.
        tar_bytes = data["nextflow_tgz"][0]
        extract_tar_bytes(tar_bytes)

        # Run the command from the history, with `-resume` added.
        cmd = data["command"][0].decode()

        if " -resume" not in cmd:
            cmd += " -resume"

        # Run the workflow.
        if run_wrapper:
            run_wrapper(cmd)
        else:
            subprocess.run(cmd, shell=True)

        # Update the history.
        status, session_id = update_history(workflow_uri)

        # Remove the workdir if the workflow was successful.
        if status == "OK":
            match = re.search(r"-work-dir (\S+)", cmd)
            if match:
                workdir = match.group(1).strip("'")
                vfs = tiledb.VFS()
                vfs.remove_dir(workdir)

    return status, session_id
