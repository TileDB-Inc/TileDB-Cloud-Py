"""Functions for working with Nextflow workflows."""

from typing import Optional

import pandas as pd

import tiledb
import tiledb.cloud
from tiledb.cloud.utilities import consolidate_and_vacuum

from ..common import workflow_history_uri


def list_history(namespace: Optional[str] = None) -> pd.DataFrame:
    """
    Return the history array as a dataframe.

    :param namespace: TileDB namespace containing the history array, defaults to None
    :return: history array as a dataframe
    """

    with tiledb.open(workflow_history_uri(namespace)) as A:
        df = A.query(
            attrs=["timestamp", "duration", "run_name", "status", "command"]
        ).df[:]

    df.sort_values(by="timestamp", ascending=True, inplace=True)

    df = df[["timestamp", "duration", "run_name", "status", "session_id", "command"]]

    return df


def get_log(
    session_id: str,
    *,
    namespace: Optional[str] = None,
) -> str:
    """
    Return the Nextflow log for a session ID.

    :param session_id: session ID from the history array
    :param namespace: TileDB namespace containing the history array, defaults to None
    :return: nextflow log as a string
    """

    with tiledb.open(workflow_history_uri(namespace)) as A:
        data = A[session_id]

    return data["nextflow_log"][0]


def consolidate_history(namespace: Optional[str] = None) -> None:
    """
    Consolidate the history array.

    :param namespace: TileDB namespace containing the history array, defaults to None
    """

    history_uri = workflow_history_uri(namespace)
    consolidate_and_vacuum(history_uri)


def delete_history(namespace: Optional[str] = None) -> None:
    """
    Delete the history array.

    :param namespace: TileDB namespace containing the history array, defaults to None
    """

    history_uri = workflow_history_uri(namespace)
    tiledb.cloud.asset.delete(history_uri)
