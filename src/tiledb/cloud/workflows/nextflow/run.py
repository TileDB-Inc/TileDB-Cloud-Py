"""Functions for working with Nextflow workflows."""

import io
import json
import os
import subprocess
import tarfile
from typing import Optional

import numpy as np

import tiledb
import tiledb.cloud
from tiledb.cloud.utilities import read_file

from ..common import cd_tmpdir
from ..common import default_workdir
from ..common import download_group_files
from ..common import workflow_history_uri


def create_history(history_uri: str) -> None:
    """
    Create a TileDB array to store the workflow run history, needed for resume.

    :param history_uri: URI for the history array
    """

    d0 = tiledb.Dim(name="session_id", dtype="ascii")
    domain = tiledb.Domain(d0)

    attrs = [
        tiledb.Attr(name="timestamp", dtype="ascii"),
        tiledb.Attr(name="duration", dtype="ascii"),
        tiledb.Attr(name="run_name", dtype="ascii"),
        tiledb.Attr(name="status", dtype="ascii"),
        tiledb.Attr(name="revision_id", dtype="ascii"),
        tiledb.Attr(name="command", dtype="ascii"),
        tiledb.Attr(name="workflow_uri", dtype="ascii"),
        tiledb.Attr(name="nextflow_log", dtype=np.dtype("U")),
        tiledb.Attr(name="nextflow_tgz", dtype="blob"),
    ]

    # Do not allow duplicate session IDs, always read the latest session ID.
    schema = tiledb.ArraySchema(
        domain=domain,
        sparse=True,
        attrs=attrs,
        allows_duplicates=False,
    )

    tiledb.Array.create(history_uri, schema)


def update_history(
    workflow_uri: str,
    namespace: Optional[str] = None,
) -> tuple[str, str]:
    """
    Update the history array with the latest workflow run information.

    :param workflow_uri: URI of the workflow asset
    :param namespace: TileDB namespace containing the history array, defaults to None
    :return: status, session ID
    """

    history_uri = workflow_history_uri(namespace, check=False)

    # Create the history array if it does not exist.
    if tiledb.object_type(history_uri) is None:
        create_history(history_uri)

    # Read the history with `nextflow log`
    try:
        res = subprocess.run(
            ["nextflow", "log"], capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print(e.stderr)
        return None, None

    # Convert the log output to a dictionary.
    lines = res.stdout.strip().split("\n")
    keys = lines[0].split("\t")
    values = lines[-1].split("\t")
    data = {
        k.strip().replace(" ", "_").lower(): v.strip() for k, v in zip(keys, values)
    }

    # Add the workflow URI to the data.
    data["workflow_uri"] = workflow_uri

    # Read the nextflow log file.
    data["nextflow_log"] = read_file(".nextflow.log")

    # Create the tar bytes for .nextflow/cache and .nextflow/history.
    data["nextflow_tgz"] = create_tar_bytes([".nextflow/cache", ".nextflow/history"])

    # Write the history to the array
    with tiledb.open(history_uri, "w") as A:
        session_id = data.pop("session_id")
        A[session_id] = data

    return data["status"], session_id


def create_tar_bytes(paths: list[str]) -> bytes:
    """
    Create a tarfile in memory from a list of paths.

    :param paths: list of paths to include in the tarfile
    :return: tarfile stored in memory as bytes
    """

    with io.BytesIO() as buffer:
        with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
            for path in paths:
                tar.add(path)

        tar_bytes = buffer.getvalue()

    return tar_bytes


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
    run_params: dict = {},
    workflow_params: dict = {},
    namespace: Optional[str] = None,
) -> tuple[str, str, list[str]]:
    """
    Prepare to run the Nextflow workflow and return the command to run.

    :param workflow_uri: workflow URI
    :param run_params: run parameters, defaults to {}
    :param workflow_params: workflow parameters, defaults to {}
    :param namespace: TileDB namespace where the workflow will run, defaults to None
    :return: run ID, run directory, run command
    """

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
    workdir = run_params.get("workdir", default_workdir(namespace))
    profile = run_params.get("profile", None)
    options = run_params.get("options", None)
    outdir = workflow_params.pop("outdir", None)

    # If provided, save the sample sheet to a file and override the input parameter.
    sample_sheet = run_params.get("sample_sheet", None)
    if sample_sheet:
        sample_sheet_file = "sample_sheet.csv"
        with open(sample_sheet_file, "w") as fp:
            fp.write(sample_sheet)
        workflow_params["input"] = sample_sheet_file

    # Dump the parameters to a file.
    if workflow_params:
        nf_json = json.dumps(workflow_params, indent=4)
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

    if workflow_params:
        cmd += ["-params-file", "nf-params.json"]
    if workdir:
        cmd += ["-work-dir", workdir]
    if profile:
        cmd += ["-profile", profile]
    if outdir:
        cmd += ["--outdir", outdir]
    if options:
        cmd += options.split()

    return cmd


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

    # TODO: copy the plugin to $HOME/.nextflow/plugins

    # Set the Nextflow environment variables.
    os.environ["NXF_DISABLE_CHECK_LATEST"] = "true"
    os.environ["NXF_ANSI_LOG"] = "true"


def run(
    workflow_uri: str,
    *,
    run_params: dict = {},
    workflow_params: dict = {},
    namespace: Optional[str] = None,
    acn: Optional[str] = None,
    keep: bool = False,
    tmpdir: Optional[str] = None,
    run_wrapper: Optional[callable] = None,
) -> tuple[str, str]:
    """
    Run a workflow asset on TileDB.

    The run_params dict contains options for the `nextflow run` command:
      - "workdir" : directory where intermediate results are stored
      - "profile" : the workflow configuration profile
      - "options" : additional `nextflow run` command options
      - "sample_sheet" : a string containing CSV data to be written to a file and
            passed to the `--input` parameter

    The workflow_params dict contains values for parameters specified by the workflow.

    :param workflow_uri: TileDB URI of the workflow asset
    :param run_params: parameters not specific to the workflow, defaults to {}
    :param workflow_params: workflow specific parameters, defaults to {}
    :param namespace: TileDB namespace where the workflow will run, defaults to None,
        the default charged namespace
    :param acn: TileDB access credentials name, defaults to None
    :param keep: keep the temporary run directory, defaults to False
    :param tmpdir: temporary run directory, defaults to None
    :param run_wrapper: function to run the command, defaults to None
    :return: status, session ID
    """

    # Validate user input.
    if tiledb.object_type(workflow_uri) != "group":
        raise FileNotFoundError(f"'{workflow_uri}' not found.")

    # Run the workflow in a temporary directory.
    with cd_tmpdir(keep=keep, tmpdir=tmpdir):
        if keep:
            print(f"Running in {os.getcwd()}")

        # Setup the nextflow environment.
        setup_nextflow(namespace, acn)

        # Setup the command to run the workflow.
        cmd = get_run_command(
            workflow_uri=workflow_uri,
            run_params=run_params,
            workflow_params=workflow_params,
            namespace=namespace,
        )

        # Run the workflow.
        if run_wrapper:
            run_wrapper(cmd)
        else:
            subprocess.run(cmd)

        # Update the history.
        try:
            status, session_id = update_history(workflow_uri)
        except Exception as e:
            print(f"Error updating history: {e}")
            return None, None

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
        try:
            status, session_id = update_history(workflow_uri)
        except Exception as e:
            print(f"Error updating history: {e}")
            return None, None

    return status, session_id
