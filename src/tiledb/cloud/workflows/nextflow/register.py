"""Functions for working with Nextflow workflows."""

import json
import os
import subprocess
import tarfile
from typing import Optional
from urllib.parse import urlparse

from tiledb.cloud.utilities import read_file

from ..common import cd_tmpdir
from ..common import create_workflow_tarfile
from ..common import get_workflows_uri
from ..workflow import create

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


def register(
    *,
    workflow: str,
    version: str,
    local_path: Optional[str] = None,
    main_script: str = MAIN_SCRIPT,
    teamspace: Optional[str] = None,
    scm_provider: Optional[str] = None,
    scm_user: Optional[str] = None,
    scm_token: Optional[str] = None,
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

    When registering a workflow from a private repository, the `provider`, `user`, and
    `token` must be provided. Currently, "github" and "gitlab" are supported providers.

    :param workflow: name or URI of the workflow to register
    :param version: workflow version (a git branch, tag, or version number)
    :param local_path: path to a local directory where the workflow is stored,
        defaults to None
    :param teamspace: TileDB teamspace where the workflow will be registered
    :param main_script: name of the script executed when running a workflow,
        defaults to "main.nf"
    :param scm_provider: SCM provider for nextflow, defaults to None
    :param scm_user: SCM user, defaults to None
    :param scm_token: SCM token, defaults to None
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

    # Create the TileDB URI for the workflow.
    tiledb_uri = get_workflows_uri(teamspace) + f"/templates/{name}-{version}"

    # Work in a temp directory
    with cd_tmpdir():
        # Configure the SCM platform, if provided.
        if scm_provider:
            scm_provider = scm_provider.lower()

            if scm_provider not in ["github", "gitlab"]:
                raise ValueError(f"Unsupported SCM provider '{scm_provider}'.")

            if scm_user is None or scm_token is None:
                raise ValueError(
                    "User and token must be provided for the SCM provider."
                )

            # Create the SCM configuration file in the temp directory.
            scm_config_str = "providers {\n"
            scm_config_str += f"    {scm_provider} {{\n"
            scm_config_str += f"        user = '{scm_user}'\n"
            scm_config_str += f"        password = '{scm_token}'\n"
            scm_config_str += "    }\n"
            scm_config_str += "}\n"

            scm_config_path = os.path.join(os.getcwd(), "scm.config")

            with open(scm_config_path, "w") as fp:
                fp.write(scm_config_str)

            os.environ["NXF_SCM_FILE"] = scm_config_path

        if local_path:
            tarfile_path = f"{os.getcwd()}/{WORKFLOW_TARFILE}"
            create_workflow_tarfile(tarfile_path, local_path)

            # Prepend the name with "local/" to indicate it was registered from a local
            # path and avoid an issue with a colon in the first part of a TileDB URI.
            name = "local/" + name
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
