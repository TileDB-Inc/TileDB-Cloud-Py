"""Functions for working with Nextflow workflows."""

import io
import json
import os
import subprocess
import tarfile
from typing import Optional
from urllib.parse import urlparse

import numpy as np

import tiledb
from tiledb.cloud.utilities import read_file

from .common import cd_tmpdir
from .common import create_workflow_tarfile
from .common import default_workflows_uri
from .common import download_group_files
from .workflow import create

# Name of the workflow tar file stored in the TileDB workflow asset.
WORKFLOW_TARFILE = "workflow.tgz"

# Path to the Nextflow parameter schema, if present.
PARAMETER_SCHEMA = "workflow/nextflow_schema.json"

# Path to the Nextflow input schema, if present.
INPUT_SCHEMA = "workflow/assets/schema_input.json"

# Name of the script executed when launching the Nextflow workflow.
MAIN_SCRIPT = "main.nf"


def get_description(
    readme_path: str,
    workflow: str,
    version: str,
) -> str:
    """
    Modify the README.md file for use as a TileDB asset description.
     - Include full URLs in image links.
     - Add a link to the original workflow.

    :param readme_path: path to the README.md file
    :param workflow: workflow name
    :param version: workflow version
    :return: modified description
    """

    # Convert a nf-core workflow to a URL for use in links.
    if not workflow.startswith("https://github.com/"):
        workflow = f"https://github.com/{workflow}"

    # Read the description into a string.
    description = read_file(readme_path)

    # Replace relative image paths with full URLs.
    description = description.replace(
        "docs/images",
        f"{workflow}/raw/{version}/docs/images",
    )

    name = workflow.replace("https://github.com/", "") + f":{version}"
    url = f"{workflow}/tree/{version}"

    description = (
        f"### *A snapshot of [{name}]({url}) for execution on TileDB.*\n\n"
        + description
    )

    return description


def clone_workflow(workflow: str, version: str, dest_path: str) -> None:
    """
    Clone a nextflow workflow to a local directory.

    :param workflow: workflow name or URI
    :param version: version of the workflow: a git branch, tag, or version number
    :param dest_path: path to the local directory where the workflow will be cloned
    """

    cmd = [
        "nextflow",
        "clone",
        "-r",
        version,
        workflow,
        dest_path,
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Error cloning workflow: {e.stderr}")


def convert_nextflow(
    workflow: str,
    version: str,
) -> str:
    """
    Create a TileDB workflow asset from a Nextflow workflow.

    :param workflow: name of the project as specified by the `nextflow clone` command
    :param version: version of the workflow: a git branch, tag, or version number
    :return: path to the tarfile containing the workflow
    """

    tarfile_path = f"{os.getcwd()}/{WORKFLOW_TARFILE}"

    with cd_tmpdir():
        workflow_clone_path = "workflow"

        # Clone the workflow into a local directory.
        clone_workflow(workflow, version, workflow_clone_path)

        # Modify the README.md for use as a TileDB asset description.
        readme_path = f"{workflow_clone_path}/README.md"
        if os.path.exists(readme_path):
            description = get_description(readme_path, workflow, version)
            with open(readme_path, "w") as f:
                f.write(description)

        # Create the workflow tarfile.
        create_workflow_tarfile(tarfile_path, workflow_clone_path)

    return tarfile_path


def register_nextflow(
    *,
    workflow: str,
    version: str,
    local_path: Optional[str] = None,
    main_script: str = MAIN_SCRIPT,
    namespace: Optional[str] = None,
) -> str:
    """
    Register a Nextflow workflow as a TileDB asset.

    If `local_path` is not provided, the workflow is cloned using:
        ```
        nextflow clone -r <version> <workflow> ...
        ```
    and registered with the name `workflow`:`version`.

    If `local_path` is provided, the workflow is registered from a local directory
    with the name `workflow`:`version`.

    :param workflow: name or URI of the workflow to register
    :param version: workflow version (a git branch, tag, or version number)
    :param local_path: path to a local directory where the workflow is stored,
        defaults to None
    :param namespace: TileDB namespace where the workflow will be registered
    :param main_script: name of the script executed when running a workflow,
        defaults to "main.nf"
    :return: URI of the registered workflow
    """

    # Validate user input.
    if workflow.startswith("https://") and local_path:
        raise ValueError("Cannot provide both a URI and a local path for the workflow.")

    # Extract the name of the workflow.
    if workflow.startswith("https://"):
        name = urlparse(workflow).path.strip("/")
    else:
        name = workflow

    # Create the URI for the workflow.
    tiledb_uri = default_workflows_uri(namespace) + f"/{name}-{version}"

    # Work in a temp directory
    with cd_tmpdir():
        if local_path:
            tarfile_path = f"{os.getcwd()}/{WORKFLOW_TARFILE}"
            create_workflow_tarfile(tarfile_path, local_path)
        else:
            tarfile_path = convert_nextflow(workflow=workflow, version=version)

        with tarfile.open(tarfile_path) as tar:
            # Check for the main script in the tarfile.
            main_script_path = "workflow/" + main_script
            if main_script_path not in tar.getnames():
                raise FileNotFoundError(
                    f"Main script '{main_script}' not found in workflow"
                )

            # Read the parameter schema and input schema from the tarfile.
            if PARAMETER_SCHEMA in tar.getnames():
                member = tar.getmember(PARAMETER_SCHEMA)
                with tar.extractfile(member) as f:
                    parameter_schema_dict = json.loads(f.read().decode())
            else:
                parameter_schema_dict = {}

            if INPUT_SCHEMA in tar.getnames():
                member = tar.getmember(INPUT_SCHEMA)
                with tar.extractfile(member) as f:
                    input_schema_dict = json.loads(f.read().decode())
            else:
                input_schema_dict = {}

        # Create the workflow.
        create(
            tiledb_uri=tiledb_uri,
            name=name,
            version=version,
            language="nextflow",
            main=main_script,
            tarfile_path=tarfile_path,
            parameter_schema_dict=parameter_schema_dict,
            input_schema_dict=input_schema_dict,
        )

    return tiledb_uri


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

    history_uri = default_workflows_uri(namespace) + "/.nextflow_history"

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
    workflow_uri: str,
    run_params: dict = {},
    workflow_params: dict = {},
) -> tuple[str, str, list[str]]:
    """
    Prepare to run the Nextflow workflow and return the command to run.

    :param workflow_uri: workflow URI
    :param run_params: run parameters, defaults to {}
    :param workflow_params: workflow parameters, defaults to {}
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
    workdir = run_params.get("workdir", None)
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

    :param namespace: TileDB namespace
    :param acn: TileDB access credentials name
    :param plugin_id: TileDB plugin ID, defaults to "nf-tiledb@0.1.0"
    :param config_file: name of the config file, defaults to "tiledb.config"
    """

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

    # Disable check for latest version.
    os.environ["NXF_DISABLE_CHECK_LATEST"] = "true"


def run_nextflow(
    workflow_uri: str,
    *,
    run_params: dict = {},
    workflow_params: dict = {},
    namespace: Optional[str] = None,
    acn: Optional[str] = None,
    keep: bool = False,
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
    :param namespace: TileDB namespace, defaults to None, the default charged namespace
    :param acn: TileDB access credentials name, defaults to None
    :param keep: keep the temporary run directory, defaults to False
    :return: status, session ID
    """

    # Validate user input.
    if tiledb.object_type(workflow_uri) != "group":
        raise FileNotFoundError(f"'{workflow_uri}' not found.")

    if namespace and acn is None:
        raise ValueError("Access credentials name required with namespace.")

    if acn and namespace is None:
        raise ValueError("Namespace required with access credentials name.")

    # Get the namespace and access credentials name, if not provided.
    if namespace is None:
        namespace = tiledb.cloud.client.default_charged_namespace()
        org = tiledb.cloud.client.organization(namespace)
        acn = org.default_s3_path_credentials_name

    # Run the workflow in a temporary directory.
    with cd_tmpdir(keep=keep) as tmpdir:
        if keep:
            print(f"Running in {tmpdir}")

        # Setup the nextflow environment.
        setup_nextflow(namespace, acn)

        # Setup the command to run the workflow.
        cmd = get_run_command(
            workflow_uri=workflow_uri,
            run_params=run_params,
            workflow_params=workflow_params,
        )

        # Run the workflow.
        subprocess.run(cmd)

        # Update the history.
        try:
            status, session_id = update_history(workflow_uri)
        except Exception as e:
            print(f"Error updating history: {e}")
            return None, None

        return status, session_id
