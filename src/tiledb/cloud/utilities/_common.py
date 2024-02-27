import configparser
import functools
import inspect
import logging
import os
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, Mapping, Optional, Sequence, Tuple, TypeVar

import tiledb
from tiledb.cloud import dag
from tiledb.cloud.tiledb_cloud_error import TileDBCloudError

# Default value if not set in config["vfs.s3.aws_region"]
AWS_DEFAULT_REGION = "us-east-1"


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

    # Always set AWS_DEFAULT_REGION because it is required by the AWS CLI
    os.environ["AWS_DEFAULT_REGION"] = config.get("vfs.s3.region", AWS_DEFAULT_REGION)


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
    except Exception:
        # Ignore errors in case logs are not available.
        pass


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


def process_stream(
    uri: str,
    cmd: Sequence[str],
    read_size: int = 16 << 20,
) -> Tuple[str, str]:
    """
    Process a stream of data from VFS with a subprocess.

    If the file is large and the subprocess only reads a small amount of data,
    then reduce `read_size` to improve performance.

    :param uri: file URI
    :param cmd: command to run in the subprocess
    :param read_size: number of bytes to read per iteration, defaults to 16 MiB
    :return: stdout and stderr from the subprocess
    """

    with tiledb.VFS().open(uri) as fp:
        with subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as process:

            def writer():
                """Read from VFS and write to the subprocess stdin."""

                data = fp.read(read_size)
                while data:
                    try:
                        process.stdin.write(data)
                    except BrokenPipeError:
                        # The subprocess has exited, stop reading.
                        # This is an expected situation.
                        break
                    data = fp.read(read_size)
                try:
                    process.stdin.close()
                except BrokenPipeError:
                    # Ignore broken pipe when closing stdin
                    pass

            def reader(stream):
                """Return the stream contents as a string."""

                return "".join(line.decode() for line in stream).strip()

            # Create separate threads for writing and reading to drain the
            # subprocess output pipes. This prevents a deadlock if the
            # subprocess fills its output buffers.
            with ThreadPoolExecutor(max_workers=3) as executor:
                executor.submit(writer)
                stdout_future = executor.submit(reader, process.stdout)
                stderr_future = executor.submit(reader, process.stderr)

            # Retrieve results
            stdout = stdout_future.result()
            stderr = stderr_future.result()

            return stdout, stderr


def _filter_kwargs(function: Callable, kwargs: Mapping[str, Any]) -> Mapping[str, Any]:
    """
    Filter kwargs to only include valid arguments for the function.

    :param function: function to validate kwargs for
    :param kwargs: kwargs to filter
    :return: filtered kwargs
    """
    valid_args = inspect.signature(function).parameters
    filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_args}
    return filtered_kwargs


_CT = TypeVar("_CT", bound=Callable)


def as_batch(func: _CT) -> _CT:
    """
    Decorator to run a function as a batch UDF on TileDB Cloud.

    :param func: function to run
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, object]:
        """
        Run the function as a batch UDF on TileDB Cloud.

        kwargs optionally includes:
        - name: name of the node in the DAG, defaults to func.__name__
        - namespace: TileDB Cloud namespace, defaults to the user's default namespace
        - acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type)
        - access_credentials_name: alias for acn, for backwards compatibility
        - resources: resources to allocate for the UDF, defaults to None
        """

        name = kwargs.get("name", func.__name__)
        namespace = kwargs.get("namespace", None)
        acn = kwargs.get("acn", kwargs.pop("access_credentials_name", None))
        kwargs["acn"] = acn  # for backwards compatibility
        resources = kwargs.pop("resources", None)

        # Create a new DAG
        graph = dag.DAG(
            name=f"batch->{name}",
            namespace=namespace,
            mode=dag.Mode.BATCH,
        )

        # Submit the function as a batch UDF
        graph.submit(
            func,
            *args,
            name=name,
            access_credentials_name=acn,
            resources=resources,
            **_filter_kwargs(func, kwargs),
        )

        # Run the DAG asynchronously
        graph.compute()

        print(
            "TileDB Cloud task submitted - https://cloud.tiledb.com/activity/taskgraphs/{}/{}".format(
                graph.namespace,
                graph.server_graph_uuid,
            )
        )
        return {"status": "started", "graph_id": str(graph.server_graph_uuid)}

    return wrapper
