import json
import os
import subprocess
import tempfile
from contextlib import contextmanager

import requests

from tiledb.cloud.utilities import read_file

CONTAINERS_JSON = "tiledb-containers.json"
WORKFLOW_TARFILE = "workflow.tgz"


def run_cmd(cmd, capture_output=False, check=True, verbose=False):
    if verbose:
        print(f"Running: {cmd}\n")

    result = subprocess.run(
        cmd,
        capture_output=capture_output,
        check=check,
        text=True,
    )

    return result.stdout, result.stderr


def url_exists(url):
    response = requests.head(url)
    return response.status_code == 200


@contextmanager
def cd_tmpdir():
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"cd to {tmpdir}")
        os.chdir(tmpdir)
        try:
            yield tmpdir
        finally:
            print(f"cd to {cwd}")
            os.chdir(cwd)


def get_description(readme_path, workflow, version):
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


def get_docker_images(workflow_path) -> str:
    # TODO: Add manual parsing of the workflow files to get the Docker images
    # if the Nextflow command fails.
    cmd = [
        "nextflow",
        "inspect",
        "-i",
        ".",
        "-profile",
        "test,docker",
        "--outdir",
        ".",
    ]
    result = subprocess.run(
        cmd,
        check=True,
        cwd=workflow_path,
        capture_output=True,
        text=True,
    )

    images = set()
    for process in json.loads(result.stdout)["processes"]:
        images.add(process["container"])

    return sorted(list(images))


def get_parameters(workflow_path) -> dict:
    # Read the Nextflow schema

    pass


def convert_nextflow(
    workflow: str,
    version: str,
) -> str:
    """
    Create a TileDB workflow asset from a Nextflow workflow.

    :param workflow: A github URL for the Nextflow workflow. If the URL does not
        start with 'https://github.com/', it will be prepended.
    :param version: The version of the workflow to use.
    :return: The path to the tarfile containing the workflow.
    """

    if not workflow.startswith("https://github.com/"):
        workflow = f"https://github.com/{workflow}"

    if not url_exists(workflow):
        raise ValueError(f"Workflow URL '{workflow}' not found.")

    cwd = os.getcwd()

    with cd_tmpdir():
        workflow_clone_path = "workflow"

        cmd = [
            "git",
            "clone",
            "--branch",
            version,
            "--single-branch",
            workflow,
            workflow_clone_path,
        ]
        run_cmd(cmd)

        # Add a list of Docker images to the workflow.
        # with open(f"{workflow_clone_path}/{CONTAINERS_JSON}", "w") as fp:
        #    json.dump(get_docker_images(workflow_clone_path), fp)

        # Modify the README.md to include full URLs to images and a link to
        # the original workflow.
        readme_path = f"{workflow_clone_path}/README.md"
        if os.path.exists(readme_path):
            description = get_description(readme_path, workflow, version)
            with open(readme_path, "w") as f:
                f.write(description)

        # Create the workflow tarfile in the directory where the command was run.
        cmd = [
            "tar",
            "--exclude=.git",
            "--exclude=*.pdf",
            "--exclude=*.svg",
            "--exclude=*.png",
            "-czf",
            f"{cwd}/{WORKFLOW_TARFILE}",
            workflow_clone_path,
        ]
        run_cmd(cmd)

    return f"{cwd}/{WORKFLOW_TARFILE}"
