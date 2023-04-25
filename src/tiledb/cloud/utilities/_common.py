import configparser
import logging
import os
import pathlib
import sys
from typing import Any, Mapping, Optional

from tiledb.cloud import dag
from tiledb.cloud.tiledb_cloud_error import TileDBCloudError


def read_aws_config(
    path: str = "~/.aws/credentials",
    section: str = "default",
) -> Mapping[str, Any]:
    """
    Read config values from a file and return a dictionary.

    :param path: config file, defaults to "~/.aws/credentials"
    :param section: section to read in the config file, defaults to "default"
    :return: config dictionary
    """
    config = {}

    cp = configparser.ConfigParser()
    cp.read(os.path.expanduser(path))

    keys = [
        "aws_access_key_id",
        "aws_secret_access_key",
        "aws_session_token",
        "aws_role_arn",
        "aws_role_session_name",
        "aws_external_id",
    ]

    for key in keys:
        try:
            config["vfs.s3." + key] = cp[section][key]
        except KeyError:
            pass

    return config


def set_aws_context(config: Optional[Mapping[str, Any]] = None) -> None:
    """
    Set OS environment variables for commands that access S3 directly,
    like AWS CLI and bcftools.

    :param config: config dictionary, defaults to None
    """

    if not config:
        return

    # Set environment variables for non-TileDB commands (AWS CLI, bcftools, etc.)
    if "vfs.s3.aws_access_key_id" in config:
        os.environ["AWS_ACCESS_KEY_ID"] = config["vfs.s3.aws_access_key_id"]
    if "vfs.s3.aws_secret_access_key" in config:
        os.environ["AWS_SECRET_ACCESS_KEY"] = config["vfs.s3.aws_secret_access_key"]
    if "vfs.s3.aws_session_token" in config:
        os.environ["AWS_SESSION_TOKEN"] = config["vfs.s3.aws_session_token"]
    if "vfs.s3.aws_role_arn" in config:
        os.environ["AWS_ROLE_ARN"] = config["vfs.s3.aws_role_arn"]
    if "vfs.s3.aws_external_id" in config:
        os.environ["AWS_EXTERNAL_ID"] = config["vfs.s3.aws_external_id"]
    if "vfs.s3.aws_session_name" in config:
        os.environ["AWS_ROLE_SESSION_NAME"] = config["vfs.s3.aws_session_name"]


def get_logger(level: int = logging.INFO, name: str = __name__) -> logging.Logger:
    """
    Get a logger with a custom formatter and set the logging level.

    :param level: logging level, defaults to logging.INFO
    :param name: logger name, defaults to __name__
    :return: Logger object
    """

    sh = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(module)s] [%(funcName)s] [%(levelname)s] %(message)s"
    )
    sh.setFormatter(formatter)

    logger = logging.getLogger(name)
    # Only add one handler, in case get_logger is called multiple times
    if not logger.handlers:
        logger.addHandler(sh)
        logger.setLevel(level)

    return logger


def run_dag(
    graph: dag.DAG,
    *,
    wait: bool = True,
    retry: bool = True,
    debug: bool = False,
) -> None:
    """
    Run a graph and optionally wait for completion and retry on errors.

    :param graph: DAG object
    :param wait: wait for completion, defaults to True
    :param retry: retry on failure, defaults to True
    :param debug: print debug logs, defaults to False
    :raises TileDBCloudError
    """
    try:
        graph.compute()
    except TileDBCloudError as e:
        print(f"Fatal graph error:\n{e}")
        _print_logs(graph, debug=debug)
        raise

    if wait:
        try:
            graph.wait()
            retry = False
        except TileDBCloudError as e:
            print(f"Fatal graph error:\n{e}")
            _print_logs(graph, debug=debug)
            # Raise exception if retry is disabled or if the error will
            # not be resolved by retrying
            if not retry or "ModuleNotFoundError" in str(e):
                raise

    if wait and retry:
        print("Retrying...")
        graph.retry_all()
        try:
            graph.wait()
        except TileDBCloudError as e:
            print(f"Fatal graph error:\n{e}")
            _print_logs(graph, debug=debug)
            raise

    _print_logs(graph, debug=debug)


def _print_logs(
    graph: dag.DAG,
    *,
    debug: bool = False,
) -> None:
    """
    Print logs for a graph.

    :param graph: DAG object
    :param debug: print debug logs, defaults to False
    """
    try:
        server_logs = dag.server_logs(graph)
    except Exception:
        # TODO: get server logs from a batch UDF
        return

    for node in server_logs.nodes:
        if debug:
            print(f"name = {node.name}")
            print(f"status = {node.status}")
        for i, ex in enumerate(node.executions):
            logs = ex.logs.strip()
            if debug:
                print(f"  run #{i}")
                print(f"    status = {ex.status}")
                if ex.duration:
                    print(f"    time = {ex.duration / 1e9:.3f} sec")
                if logs:
                    print(logs)
            elif logs and node.status == "COMPLETED":
                print(logs)


def read_file(path: str) -> str:
    """
    Read a file and return the contents as a string.

    :param path: path to the file
    :return: file contents
    """

    return pathlib.Path(path).read_text().strip()


def max_memory_usage() -> int:
    """
    Return the maximum memory usage in bytes from the cgroup file
    `memory.memsw.max_usage_in_bytes`.

    :return: maximum memory usage in bytes or 0 if the cgroup file is not found
    """

    try:
        result = int(read_file("/sys/fs/cgroup/memory/memory.memsw.max_usage_in_bytes"))
    except Exception:
        result = 0

    return result
