"""Functions for working with TileDB workflows."""

import json
import os
import tarfile
import tempfile

import tiledb
import tiledb.cloud
from tiledb.cloud.utilities import read_file

from .common import upload_file

SUPPORTED_LANGUAGES = ["nextflow"]


def create(
    *,
    tiledb_uri: str,
    language: str,
    name: str,
    version: str,
    main: str,
    tarfile_path: str,
    parameter_schema_dict: dict = {},
    input_schema_dict: dict = {},
) -> None:
    """
    Create a TileDB workflow template asset, which includes the members:

        - README.md: A description of the workflow template.
        - workflow.tgz: The workflow template contents in a tarfile.
        - parameters.json: The workflow parameter schema as a JSON file.
        - input.json: The workflow input schema as a JSON file.

    and metadata:

        - dataset_type: "workflow"
        - language: The workflow language.
        - name: The name of the workflow.
        - version: The workflow version.
        - main: The name of the main file in the workflow.

    :param tiledb_uri: URI where the workflow will be registered and stored
    :param language: workflow language
    :param name: name of the workflow
    :param version: version of the workflow
    :param main: name of the main file in the workflow
    :param tarfile_path: path to the tarfile containing the workflow
    :param parameter_schema_dict: workflow parameter spec, defaults to {}
    :param input_schema_dict: input spec, defaults to {}
    :return: None
    """

    # Validate user input.
    if tiledb.object_type(tiledb_uri) is not None:
        raise FileExistsError(f"'{tiledb_uri}' already exists.")

    language = language.lower()
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language '{language}'. ",
            f"Supported languages: {SUPPORTED_LANGUAGES}",
        )

    if not os.path.exists(tarfile_path):
        raise FileNotFoundError(f"Workflow tarfile '{tarfile_path}' not found.")

    # Create the group.
    tiledb.Group.create(tiledb_uri)

    # Extract the README.md from the tarfile.
    readme_uri = None
    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(tarfile_path) as tar:
            readme_path = "workflow/README.md"
            if readme_path in tar.getnames():
                # Extract the README.md from the tarfile.
                tar.extract(readme_path, path=tmpdir)
                readme_path = os.path.join(tmpdir, readme_path)

                description = read_file(readme_path)

                # Truncate the description, if needed.
                MAX_DESCRIPTION_LENGTH = 8000
                if len(description) > MAX_DESCRIPTION_LENGTH:
                    description = description[:MAX_DESCRIPTION_LENGTH]
                    post_script = " ...\n\n[TRUNCATED]"
                    description = description[: -len(post_script)] + post_script

                # Update the asset name and description
                tiledb.cloud.asset.update_info(
                    tiledb_uri,
                    name=f"{name}:{version}",
                    description=description,
                )

                # Upload README.md.
                readme_uri = upload_file(
                    tiledb_dir=tiledb_uri,
                    file_path=readme_path,
                    filename="README.md",
                    mime_type="text/markdown",
                )

    # Update the asset name if the readme was not found.
    if readme_uri is None:
        tiledb.cloud.asset.update_info(
            tiledb_uri,
            name=f"{name}:{version}",
        )

    # Upload the tar file with the workflow.
    workflow_uri = upload_file(
        tiledb_dir=tiledb_uri,
        file_path=tarfile_path,
        filename="workflow.tgz",
    )

    # Upload the parameters as a JSON file.
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w") as fp:
        json.dump(parameter_schema_dict, fp, indent=2)
        fp.flush()

        parameters_uri = upload_file(
            tiledb_dir=tiledb_uri,
            file_path=fp.name,
            filename="parameters.json",
        )

    # Upload the inputs as a JSON file.
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w") as fp:
        json.dump(input_schema_dict, fp, indent=2)
        fp.flush()

        input_uri = upload_file(
            tiledb_dir=tiledb_uri,
            file_path=fp.name,
            filename="input.json",
        )

    # Add the group members and metadata.
    with tiledb.Group(tiledb_uri, "w") as g:
        g.add(workflow_uri, "workflow.tgz")
        g.add(parameters_uri, "parameters.json")
        g.add(input_uri, "input.json")
        if readme_uri:
            g.add(readme_uri, "README.md")

        g.meta["dataset_type"] = "workflow"
        g.meta["language"] = language
        g.meta["version"] = version
        g.meta["main"] = main
        g.meta["name"] = name
