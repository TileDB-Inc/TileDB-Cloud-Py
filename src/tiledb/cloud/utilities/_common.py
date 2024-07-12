import configparser
import functools
import inspect
import logging
import os
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from fnmatch import fnmatch
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

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


def get_logger_wrapper(
    verbose: bool = False,
    level: Optional[int] = None,
) -> logging.Logger:
    """
    Get a logger instance and log version information.

    Nominal use-case is a simple two-level approach: verbose or not.

    Using ``level`` provides access to the ``logging`` package's levels.

    :param verbose: verbose logging, defaults to False
    :param level: if provided, supersedes ``verbose`` and applies the
      requested level.
    :return: logger instance
    """

    if level is None:
        level = logging.DEBUG if verbose else logging.INFO
    logger = get_logger(level)

    logger.debug(
        "tiledb.cloud=%s, tiledb=%s, libtiledb=%s",
        tiledb.cloud.__version__,
        tiledb.version(),
        tiledb.libtiledb.version(),
    )

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
    *,
    output_uri: Optional[str] = None,
    read_size: int = 16 << 20,
    config: Optional[Mapping[str, Any]] = None,
) -> Tuple[int, str, str]:
    """
    Process a stream of data from VFS with a subprocess. Optionally write the
    subprocess stdout to the output_uri.

    If the file is large and the subprocess only reads a small amount of data,
    then reduce `read_size` to improve performance.

    :param uri: file URI
    :param cmd: command to run in the subprocess
    :param output_uri: output file URI, defaults to None
    :param read_size: number of bytes to read per iteration, defaults to 16 MiB
    :param config: config dictionary, defaults to None
    :return: (return code, stdout, stderr) from the subprocess
    """

    vfs = tiledb.VFS(config=config)

    # If output_uri is defined, open the URI with VFS, otherwise open /dev/null.
    # We need to open something to add to the following context manager.
    output_fp = vfs.open(output_uri, "wb") if output_uri else open("/dev/null", "wb")

    # Including output_fp in the context manager is needed when writing to s3
    with vfs.open(uri) as input_fp, output_fp:
        with subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as process:

            def vfs_to_stdin() -> None:
                """Read from VFS and write to the subprocess stdin."""

                while True:
                    data = input_fp.read(read_size)
                    if not data:
                        break

                    try:
                        process.stdin.write(data)
                    except BrokenPipeError:
                        # The subprocess has exited, stop reading.
                        # This is an expected situation.
                        break
                try:
                    process.stdin.close()
                except BrokenPipeError:
                    # Ignore broken pipe when closing stdin
                    pass

            def output_to_str(stream: subprocess.PIPE) -> str:
                """Return the stream contents as a string."""

                return "".join(line.decode() for line in stream).strip()

            def output_to_vfs(stream: subprocess.PIPE) -> str:
                """Write the stream contents to the output URI."""

                while True:
                    data = stream.read(read_size)
                    if not data:
                        break

                    output_fp.write(data)

                return ""

            # Create separate threads for writing and reading to drain the
            # subprocess output pipes. This prevents a deadlock if the
            # subprocess fills its output buffers.
            with ThreadPoolExecutor(max_workers=3) as executor:
                input_future = executor.submit(vfs_to_stdin)
                if output_uri:
                    stdout_future = executor.submit(output_to_vfs, process.stdout)
                else:
                    stdout_future = executor.submit(output_to_str, process.stdout)
                stderr_future = executor.submit(output_to_str, process.stderr)

            # Wait for all threads to complete
            wait([input_future, stdout_future, stderr_future])

            # Get the return code from the subprocess
            rc = process.wait()

            # Retrieve results
            stdout = stdout_future.result()
            stderr = stderr_future.result()

            return rc, stdout, stderr


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

    optional kwargs:
    - name: name of the node in the DAG, defaults to func.__name__
    - namespace: TileDB Cloud namespace, defaults to the user's default namespace
    - acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type)
    - resources: resources to allocate for the UDF, defaults to None

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
        - image_name: Docker image_name to use for UDFs, defaults to None
        """

        name = kwargs.get("name", func.__name__)
        namespace = kwargs.get("namespace", None)
        acn = kwargs.get("acn", kwargs.pop("access_credentials_name", None))
        kwargs["acn"] = acn  # for backwards compatibility
        resources = kwargs.pop("resources", None)
        image_name = kwargs.pop("image_name", None)

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
            image_name=image_name,
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


def find(
    uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    include: Optional[Union[str, Callable]] = None,
    exclude: Optional[Union[str, Callable]] = None,
    max_count: Optional[int] = None,
) -> Iterator[str]:
    """Searches a path for files matching the include/exclude pattern using VFS.

    :param uri: Input path to search
    :param config: Optional dict configuration to pass on tiledb.VFS
    :param include: Optional include pattern string
    :param exclude: Optional exclude pattern string
    :param max_count: Optional stop point when searching for files
    """
    with tiledb.scope_ctx(config):
        vfs = tiledb.VFS(config=config, ctx=tiledb.Ctx(config))
        listing = vfs.ls(uri)
        current_count = 0

        def list_files(listing):
            for f in listing:
                # Avoid infinite recursion
                if f == uri:
                    continue

                if vfs.is_dir(f):
                    yield from list_files(
                        vfs.ls(f),
                    )
                else:
                    # Skip files that do not match the include pattern or match
                    # the exclude pattern.
                    if callable(include):
                        if not include(f):
                            continue
                    else:
                        if include and not fnmatch(f, include):
                            continue

                    if callable(exclude):
                        if exclude(f):
                            continue
                    else:
                        if exclude and fnmatch(f, exclude):
                            continue
                    yield f

        for f in list_files(listing):
            yield f

            current_count += 1
            if max_count and current_count == max_count:
                return


T = TypeVar("T")


def chunk(items: Sequence[T], chunk_size: int) -> Iterator[Sequence[T]]:
    """Chunks a sequence of objects and returns an iterator where
    each return sequence is of length chunk_size.

    :param items: Sequence to split into batches
    :param chunk_size: Size of chunks of the sequence to return
    """
    # Iterator for providing batches of chunks
    length = len(items)
    for ndx in range(0, length, chunk_size):
        yield items[ndx : min(ndx + chunk_size, length)]


def serialize_filter(filter) -> dict:
    """Serialize TileDB filter.

    :param filter: TileDB filter to serialize
    :return: dict, TileDB filter attributes
    """
    if isinstance(filter, tiledb.Filter):
        filter_dict = filter._attrs_()
        filter_dict["_type"] = type(filter).__name__
        return filter_dict
    else:
        raise TypeError
