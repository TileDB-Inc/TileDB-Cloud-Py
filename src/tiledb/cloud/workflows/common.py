"""Common functions used in other workflow functions."""

import os
import tarfile
import tempfile
from contextlib import contextmanager
from typing import Any, Mapping, Optional, Sequence, Union

import tiledb


@contextmanager
def cd_tmpdir(*, keep: bool = False, tmpdir: Optional[str] = None):
    """
    A context manager that creates a tmpdir and changes the current working
    directory to it. When the context is exited, the current working directory
    is restored to the original location.

    If `keep` is True, the temporary directory is not deleted when the context exits.

    If `tmpdir` is provided, the context manager uses the existing directory. The
    provided `tmpdir` is never deleted, regardless of the value of `keep`.

    :param keep: keep the temporary directory after the context exits, defaults to False
    :param tmpdir: existing temporary directory to use, defaults to None
    """

    if tmpdir and not os.path.exists(tmpdir):
        raise FileNotFoundError(f"Temporary directory does not exist: '{tmpdir}'.")

    # Save the current working directory.
    cwd = os.getcwd()

    if keep or tmpdir:
        tmpdir = tmpdir or tempfile.mkdtemp()
        os.chdir(tmpdir)
        try:
            yield tmpdir
        finally:
            os.chdir(cwd)
    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                yield tmpdir
            finally:
                os.chdir(cwd)


def get_workflows_uri(
    teamspace: Optional[str] = None,
    *,
    s3_uri: bool = False,
) -> str:
    """
    Return the URI for storing workflow related data.
     - If the teamspace is not provided, the default workspace is used.
     - If `s3_uri` is True, an S3 URI is returned. Otherwise, a TileDB URI is returned.

    ## Example

    ```python
        workflows_storage_uri("teamspace")
        # Returns: "tiledb://teamspace/s3://workspace/teamspace/__workflows"

        workflows_storage_uri("teamspace", s3_uri=True)
        # Returns: "s3://workspace/teamspace/__workflows"
    ```

    :param teamspace: TileDB teamspace used for storage, defaults to None
    :param s3_uri: if True, returns an S3 URI instead of a TileDB URI, defaults to False
    :return: root path for storing workflow related data
    """

    if teamspace is None:
        # TODO: adjust the default location as needed for 3.0.
        # Another option would be the default charged teamspace.
        # teamspace = tiledb.cloud.client.default_charged_namespace()
        # s3_path = tiledb.cloud.client.organization(teamspace).default_s3_path
        profile = tiledb.cloud.client.user_profile()
        s3_path = profile.default_s3_path
        teamspace = profile.username
    else:
        # TODO: adjust this logic as needed for 3.0.
        try:
            org = tiledb.cloud.client.organization(teamspace)
            s3_path = org.default_s3_path
        except Exception:
            # Handle the case where the teamspace is the user's username.
            profile = tiledb.cloud.client.user_profile()
            if teamspace == profile.username:
                s3_path = profile.default_s3_path
            else:
                raise

    uri = s3_path.rstrip("/") + "/__workflows"

    if s3_uri:
        return uri

    return f"tiledb://{teamspace}/{uri}"


def get_history_uri(
    teamspace: Optional[str] = None,
    *,
    check: bool = True,
) -> str:
    """
    Return the default TileDB URI for storing the workflow history. If `check` is
    True, raise an error if the URI does not exist.

    :param teamspace: TileDB teamspace used for storage, defaults to None
    :param check: check if the URI exists, defaults to True
    :return: TileDB URI for the workflow history
    """

    uri = get_workflows_uri(teamspace) + "/nextflow/history"

    if check and not tiledb.object_type(uri):
        raise FileNotFoundError(f"Workflow history not found at '{uri}'.")

    return uri


def get_manifests_uri(
    teamspace: Optional[str] = None,
    *,
    check: bool = False,
) -> str:
    """
    Return the default TileDB URI for storing run manifests. If `check` is
    True, raise an error if the URI does not exist.

    :param teamspace: TileDB teamspace used for storage, defaults to None
    :param check: check if the URI exists, defaults to True
    :return: TileDB URI for the workflow manifests
    """

    uri = get_workflows_uri(teamspace) + "/nextflow/manifests"

    if check and not tiledb.object_type(uri):
        raise FileNotFoundError(f"Manifest array not found at '{uri}'.")

    return uri


def download_group_files(
    group_uri: str,
    members: Union[Sequence[str], str],
    dest_path: str = None,
    config: Optional[Mapping[str, Any]] = None,
) -> None:
    """
    Download a list of files from a TileDB group to a local directory.

    :param group_uri: URI of the TileDB group
    :param members: list of members to download
    :param dest_path: download destination path, defaults to the current directory
    :param config: TileDB config, defaults to None
    """

    if not isinstance(members, list):
        members = [members]

    dest_path = dest_path or os.getcwd()

    with tiledb.Group(group_uri, config=config) as group:
        for member in members:
            dest = os.path.join(dest_path, member)
            tiledb.Filestore.copy_to(group[member].uri, dest)


def upload_file(
    *,
    tiledb_dir: str,
    file_path: str,
    filename: str = None,
    overwrite: bool = False,
    mime_type: str = None,
) -> str:
    """
    Upload a file to TileDB.

    :param tiledb_dir: URI in `tiledb://.../s3://...` format for the location
        to store the file
    :param file_path: local path to the file
    :param filename: filename on TileDB, defaults to None which uses the
        file_path basename
    :param overwrite: overwrite the file if it already exists, defaults to False
    :param mime_type: mime type of the file, defaults to None, which automatically
        detects the type
    :return: TileDB URI of the file
    """

    # Set the filename, if not provided.
    if filename is None:
        filename = os.path.basename(file_path)

    # Create the URI for the TileDB file.
    tiledb_uri = tiledb_dir.rstrip("/") + "/" + filename
    tiledb_uri = tiledb_uri.replace("+", ".")

    # Validate the URI, checking for existing assets.
    try:
        object_type = tiledb.object_type(tiledb_uri)
    except tiledb.TileDBError:
        # Catch edge case errors.
        raise FileNotFoundError(
            f"The TileDB file is missing from storage backend at '{tiledb_uri}'."
        )

    if object_type == "group":
        raise FileExistsError(f"A TileDB group already exists at '{tiledb_uri}'.")

    if object_type == "array" and not overwrite:
        raise ValueError(f"A TileDB array already exists at '{tiledb_uri}'.")

    # Create the array.
    tiledb.Array.create(tiledb_uri, tiledb.ArraySchema.from_file(file_path))

    # Upload the file to TileDB.
    tiledb.Filestore.copy_from(tiledb_uri, file_path)

    # Fix the metadata created by copy_from.
    with tiledb.Array(tiledb_uri, "w") as a:
        a.meta["original_file_name"] = filename
        if mime_type:
            a.meta["mime_type"] = mime_type

    return tiledb_uri


def create_workflow_tarfile(
    tarfile_path: str,
    workflow_path: str,
) -> None:
    """
    Create a tarfile containing the workflow.

    :param tarfile_path: destination path for the tarfile
    :param src_path: path to the workflow directory
    """

    with tarfile.open(tarfile_path, "w:gz") as tar:
        # Set the name of the workflow directory to "workflow" in the tarfile.
        tar.add(workflow_path, arcname="workflow")
