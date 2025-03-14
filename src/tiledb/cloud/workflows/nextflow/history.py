"""Functions for working with Nextflow workflows."""

import io
import subprocess
import tarfile
from typing import Dict, Optional, Union

import numpy as np
import pandas as pd

import tiledb
import tiledb.cloud
from tiledb.cloud.utilities import consolidate_and_vacuum
from tiledb.cloud.utilities import read_file

from ..common import get_history_uri


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
        tiledb.Attr(name="workflow_name", dtype="ascii"),
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

    # Update the asset name.
    tiledb.cloud.asset.update_info(history_uri, name="nextflow/history")


def update_history(
    workflow_uri: str,
    *,
    teamspace: Optional[str] = None,
    consolidate: bool = True,
) -> tuple[str, str]:
    """
    Update the history array with the latest workflow run information.

    :param workflow_uri: URI of the workflow asset
    :param teamspace: TileDB teamspace containing the history array, defaults to None
    :param consolidate: consolidate the history array, defaults to True
    :return: status, session ID
    """

    history_uri = get_history_uri(teamspace, check=False)

    try:
        object_type = tiledb.object_type(history_uri)
    except Exception:
        # Handle tiledb:// URIs that do not exist.
        object_type = None

    # Create the history array if it does not exist.
    if object_type is None:
        create_history(history_uri)

    # Read the history with `nextflow log`
    try:
        res = subprocess.run(
            ["nextflow", "log"], capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError:
        return None, None

    # Convert the log output to a dictionary.
    lines = res.stdout.strip().split("\n")
    keys = lines[0].split("\t")
    values = lines[-1].split("\t")
    data: Dict[str, Union[str, bytes]] = {
        k.strip().replace(" ", "_").lower(): v.strip() for k, v in zip(keys, values)
    }

    # Add the workflow URI to the data.
    data["workflow_uri"] = workflow_uri

    # Add the workflow name to the data.
    with tiledb.Group(workflow_uri) as g:
        workflow_name = g.meta["name"] + ":" + g.meta["version"]
    data["workflow_name"] = workflow_name

    # Read the nextflow log file.
    data["nextflow_log"] = read_file(".nextflow.log")

    # Create the tar bytes for .nextflow/cache and .nextflow/history.
    data["nextflow_tgz"] = create_tar_bytes([".nextflow/cache", ".nextflow/history"])

    # Write the history to the array
    with tiledb.open(history_uri, "w") as A:
        session_id = data.pop("session_id")
        A[session_id] = data

    # Consolidate the history array.
    if consolidate:
        consolidate_and_vacuum(history_uri)

    return data["status"], session_id


def get_history(teamspace: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    Return the history array as a dataframe.

    :param teamspace: TileDB teamspace containing the history array, defaults to None
    :return: history array as a dataframe, or None if the array does not exist
    """

    try:
        with tiledb.open(get_history_uri(teamspace)) as A:
            df = A.query(
                attrs=[
                    "timestamp",
                    "duration",
                    "run_name",
                    "status",
                    "command",
                    "workflow_name",
                ]
            ).df[:]

        df.sort_values(by="timestamp", ascending=False, inplace=True)

    except Exception:
        return None

    return df


def get_log(
    session_id: str,
    *,
    teamspace: Optional[str] = None,
) -> str:
    """
    Return the Nextflow log for a session ID.

    :param session_id: session ID from the history array
    :param teamspace: TileDB teamspace containing the history array, defaults to None
    :return: nextflow log as a string
    """

    with tiledb.open(get_history_uri(teamspace)) as A:
        data = A[session_id]

    return data["nextflow_log"][0]


def consolidate_history(teamspace: Optional[str] = None) -> None:
    """
    Consolidate the history array.

    :param teamspace: TileDB teamspace containing the history array, defaults to None
    """

    history_uri = get_history_uri(teamspace)
    consolidate_and_vacuum(history_uri)
