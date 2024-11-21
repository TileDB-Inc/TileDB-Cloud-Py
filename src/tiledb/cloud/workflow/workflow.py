import json
import os
import tarfile
import tempfile

import tiledb
import tiledb.cloud
from tiledb.cloud.utilities import get_logger
from tiledb.cloud.utilities import read_file

SUPPORTED_LANGUAGES = ["nextflow"]


def upload_file(
    *,
    tiledb_dir: str,
    file_path: str,
    filename: str = None,
    overwrite: bool = False,
    mime_type: str = None,
) -> str:
    # Set the filename, if not provided.
    if filename is None:
        filename = os.path.basename(file_path)

    # Create the URI for the TileDB file.
    tiledb_uri = tiledb_dir.rstrip("/") + "/" + filename
    tiledb_uri = tiledb_uri.replace("+", ".")

    # Validate the URI.
    try:
        object_type = tiledb.object_type(tiledb_uri)
    except tiledb.TileDBError:
        raise FileNotFoundError(
            f"The TileDB file is missing from storage backend at '{tiledb_uri}'."
        )

    if object_type == "group":
        raise FileExistsError(f"A TileDB group already exists at '{tiledb_uri}'.")

    if object_type == "array" and not overwrite:
        raise ValueError(f"The TileDB already exists at '{tiledb_uri}'.")

    # Create the array if it doesn't exist.
    if object_type is None:
        tiledb.Array.create(tiledb_uri, tiledb.ArraySchema.from_file(file_path))

    # Upload the file to TileDB.
    tiledb.Filestore.copy_from(tiledb_uri, file_path)

    # Fix the metadata created by copy_from.
    with tiledb.Array(tiledb_uri, "w") as a:
        a.meta["original_file_name"] = filename
        if mime_type:
            a.meta["mime_type"] = mime_type

    return tiledb_uri


def create(
    *,
    tiledb_uri: str,
    name: str,
    version: str,
    language: str,
    main: str,
    tarfile_path: str,
    parameters: dict = {},
    input: dict = {},
):
    if not isinstance(parameters, dict):
        raise ValueError(f"parameters must be a dict, not {type(parameters)}")
    if not isinstance(input, dict):
        raise ValueError(f"input must be a dict, not {type(input)}")

    # Validate user input.
    if tiledb.object_type(tiledb_uri) is not None:
        raise FileExistsError(f"'{tiledb_uri}' already exists.")

    language = language.lower()
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language '{language}'.",
            f"Supported languages: {SUPPORTED_LANGUAGES}",
        )

    if not os.path.exists(tarfile_path):
        raise FileNotFoundError(f"Workflow tarfile '{tarfile_path}' not found.")

    logger = get_logger()

    # Create the group.
    logger.info("Create group")
    tiledb.Group.create(tiledb_uri)

    # Update the name and description.
    logger.info("Update description")

    # Extract the README.md from the tarfile.
    readme_uri = None
    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(tarfile_path) as tar:
            readme_path = "workflow/README.md"
            if readme_path in tar.getnames():
                # Extract the README.md from the tarfile.
                tar.extract(readme_path, path=tmpdir)
                readme_path = os.path.join(tmpdir, readme_path)

                # Update the asset description and name.
                description = read_file(readme_path)
                # TODO: Remove when the TileDB description is longer.
                MAX_DESCRIPTION_LENGTH = 8000
                if len(description) > MAX_DESCRIPTION_LENGTH:
                    print(
                        f"Description is {len(description)} chars.",
                        f"Truncating to {MAX_DESCRIPTION_LENGTH} chars.",
                    )
                    description = description[:MAX_DESCRIPTION_LENGTH]

                name += f":{version}"
                tiledb.cloud.asset.update_info(
                    tiledb_uri,
                    name=name,
                    description=description,
                )

                # Upload README.md.
                logger.info("Upload README.md")
                readme_uri = upload_file(
                    tiledb_dir=tiledb_uri,
                    file_path=readme_path,
                    filename="README.md",
                    mime_type="text/markdown",
                )

    # Upload the tar file with the workflow.
    logger.info("Upload workflow.tgz")
    workflow_uri = upload_file(
        tiledb_dir=tiledb_uri,
        file_path=tarfile_path,
        filename="workflow.tgz",
    )

    # Upload the parameters as a JSON file.
    logger.info("Upload parameters.json")
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as fp:
        print(fp.name)
        json.dump(parameters, fp, indent=2)
        fp.flush()

        parameters_uri = upload_file(
            tiledb_dir=tiledb_uri,
            file_path=fp.name,
            filename="parameters.json",
        )

    # Upload the inputs as a JSON file.
    logger.info("Upload input.json")
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as fp:
        print(fp.name)
        json.dump(input, fp, indent=2)
        fp.flush()

        input_uri = upload_file(
            tiledb_dir=tiledb_uri,
            file_path=fp.name,
            filename="input.json",
        )

    # Add the group members and metadata.
    logger.info("Open group")
    with tiledb.Group(tiledb_uri, "w") as g:
        logger.info("Add group members")
        g.add(workflow_uri, "workflow.tgz")
        g.add(parameters_uri, "parameters.json")
        g.add(input_uri, "input.json")
        if readme_uri:
            g.add(readme_uri, "README.md")

        logger.info("Add metadata")
        g.meta["dataset_type"] = "workflow"
        g.meta["language"] = language
        g.meta["version"] = version
        g.meta["main"] = main
        logger.info("Close group")

    logger.info("Done")
