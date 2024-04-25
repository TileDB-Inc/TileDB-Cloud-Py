import os
import re
from math import ceil
from typing import Any, List, Mapping, Optional, Sequence, Union

import tiledb
import tiledb.cloud
from tiledb.cloud import dag
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud._common import utils
from tiledb.cloud.array import info
from tiledb.cloud.dag.mode import Mode
from tiledb.cloud.utilities import as_batch
from tiledb.cloud.utilities import get_logger_wrapper
from tiledb.cloud.vcf.ingestion import find_uris_udf

DEFAULT_RESOURCES = {"cpu": "1", "memory": "2Gi"}
DEFAULT_FILE_INGESTION_NAME = "file-ingestion"
DEFAULT_BATCH_SIZE = 100


def sanitize_filename(fname: str) -> str:
    """
    Sanitizes a filename by removing invalid characters.

    :param fname: A filename to sanitize
    :return str: The sanitized string
    """
    name, suffix = os.path.splitext(fname)
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[-_\s]+", "_", name).strip("-_")
    return name + suffix


def chunk_results_udf(
    udf_results: Sequence[Sequence[str]],
    batch_size: Optional[int] = DEFAULT_BATCH_SIZE,
    verbose: bool = False,
) -> List[List[str]]:
    """
    Flatten and break a list of udf results into batches of a specified size.

    :param udf_results: An iterable of iterables containing UDF results.
    :param batch_size: Resulting chunk size, defaults to 100.
    :return List[List[str]]: A list of chunks as lists.
    """
    logger = get_logger_wrapper(verbose)

    # Flatten the results into a list.
    flattened_results = [result for udf_result in udf_results for result in udf_result]

    # Reduce batch size if there are fewer sample URIs
    batch_size = min(batch_size, len(flattened_results))
    num_chunks = ceil(len(flattened_results) / batch_size)
    logger.info(f"Splitting results into {num_chunks} chunks...")

    return [
        flattened_results[n * batch_size : (n + 1) * batch_size]
        for n in range(num_chunks)
    ]


def add_arrays_to_group_udf(
    array_uris: Sequence[str],
    group_uri: str,
    *,
    config: Optional[dict] = None,
    verbose: bool = False,
) -> None:
    """
    Add a list of TileDB array uris in a TileDB group.

    :param array_uris: An iterable of TileDB URIs.
    :param group_uri: A TileDB Group URI.
    :param config: Config dictionary, defaults to None
    :param verbose: Verbose logging, defaults to False
    """
    logger = get_logger_wrapper(verbose)

    with tiledb.scope_ctx(config):
        try:
            if tiledb.object_type(group_uri) == "group":
                with tiledb.Group(group_uri, mode="w") as group:
                    logger.debug(
                        f"Adding to Group {group_uri} the following: {array_uris}"
                    )
                    for uri in array_uris:
                        if not isinstance(uri, str):
                            for array_uri in uri:
                                group.add(array_uri)
                        else:
                            group.add(uri)
            else:
                raise ValueError(
                    f"Group URI: '{group_uri}' does not match any existing group."
                )
        except Exception as exc:
            # tiledb.object_type raises an exception
            # if the namespace does not exist
            logger.error(f"Error checking if {group_uri} is a Group. Bad namespace?")
            raise exc


def ingest_files_udf(
    dataset_uri: str,
    file_uris: Sequence[str],
    *,
    acn: Optional[str] = None,
    namespace: Optional[str] = None,
    verbose: bool = False,
) -> List[str]:
    """
    Ingest files.

    :param dataset_uri: The dataset URI.
    :param file_uris: An iterable of file URIs.
    :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type),
        defaults to None
    :param namespace: TileDB-Cloud namespace, defaults to None.
    :param verbose: Verbose logging, defaults to False.
    :return List[str]: A list of the ingested files' resulting URIs.
    """
    logger = get_logger_wrapper(verbose)

    ingested = []
    for file_uri in file_uris:
        filename = sanitize_filename(os.path.basename(file_uri))
        array_uri = f"tiledb://{namespace}/{filename}"
        filestore_array_uri = f"{dataset_uri}/{filename}"
        namespace = namespace or tiledb.cloud.user_profile().default_namespace_charged
        logger.debug(
            f"""
            ---------------------------------------------
            - Input URI: {file_uri}
            - Sanitized Filename: {filename}
            - Array URI: {array_uri}
            - Destination URI: {filestore_array_uri}
            ---------------------------------------------"""
        )

        try:
            tiledb.cloud.file.create_file(
                namespace=namespace,
                name=filename,
                input_uri=file_uri,
                output_uri=filestore_array_uri,
                access_credentials_name=acn,
            )

            array_info = info(array_uri)
            ingested.append(array_info.tiledb_uri)
        except tiledb_cloud_error.TileDBCloudError as exc:
            error_msg = repr(exc)
            if "array already exists at location - Code: 8003" in error_msg:
                logger.warning(f"Array '{array_uri}' already exists.")
                continue
            elif f"array {array_uri} is not unique" in error_msg:
                logger.warning(
                    f"Array URI {array_uri} is not unique. "
                    f"Skipping {filename} ingestion"
                )
                continue
            else:
                raise exc

    return ingested


def ingest_files(
    dataset_uri: str,
    *,
    search_uri: Optional[Union[Sequence[str], str]] = None,
    pattern: Optional[str] = None,
    ignore: Optional[str] = None,
    max_files: Optional[int] = None,
    batch_size: Optional[int] = DEFAULT_BATCH_SIZE,
    acn: Optional[str] = None,
    config: Optional[dict] = None,
    namespace: Optional[str] = None,
    group_uri: Optional[str] = None,
    taskgraph_name: Optional[str] = DEFAULT_FILE_INGESTION_NAME,
    ingest_resources: Optional[Mapping[str, Any]] = DEFAULT_RESOURCES,
    verbose: bool = False,
) -> str:
    """
    Ingest files into a dataset.

    :param dataset_uri: The dataset URI
    :param search_uri: URI or an iterable of URIs of input files. Defaults to None.
    :param pattern: UNIX shell style pattern to filter files in the search,
        defaults to None
    :param ignore: UNIX shell style pattern to filter files out of the search,
        defaults to None
    :param max_files: maximum number of File URIs to read/find,
        defaults to None (no limit)
    :param batch_size: Batch size for file ingestion, defaults to 100.
    :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type),
        defaults to None
    :param config: Config dictionary, defaults to None
    :param namespace: TileDB-Cloud namespace, defaults to None
    :param group_uri: A TileDB Group URI, defaults to None.
    :param taskgraph_name: Optional name for taskgraph, defaults to "file-ingestion".
    :param ingest_resources: Configuration for node specs,
        defaults to {"cpu": "1", "memory": "2Gi"}
    :param verbose: Verbose logging, defaults to False
    :return str: The resulting TaskGraph's server UUID as string.
    """
    # Argument Validation
    if not search_uri:
        raise ValueError("search_uri must be provided")

    # Preparation and argument cleanup
    logger = get_logger_wrapper(verbose)

    dataset_uri = dataset_uri.rstrip("/")
    if group_uri:
        try:
            namespace, group_name = utils.split_uri(group_uri)
            # Set the destination path to match the path of the group.
            dataset_uri = f"{dataset_uri}/{group_name}"
        except Exception as exc:
            error_msg = f"Group URI: '{group_uri}' is not correctly formatted"
            logger.error(error_msg)
            raise ValueError(error_msg) from exc

    namespace = namespace or tiledb.cloud.user_profile().default_namespace_charged
    if isinstance(search_uri, str):
        search_uri = [search_uri]

    logger.debug(
        f"""
        ----------------------------------------------
        Build the file ingestion graph with arguments:
        ----------------------------------------------
        - Dataset URI: {dataset_uri}
        - Search:
            - URI: {search_uri}
            - Patterns:
                - Include: {pattern}
                - Exclude: {ignore}
            - Max Files: {max_files}
            - Batch Size: {batch_size}
        - Namespace: {namespace}
        - Group URI: {group_uri}
        - Taskgraph Name: {taskgraph_name}
        - Resources: {ingest_resources}
        ----------------------------------------------
        """
    )

    # Graph Setup
    graph = dag.DAG(
        name=f"{taskgraph_name}-ingestor",
        namespace=namespace,
        mode=Mode.BATCH,
    )

    # Step 1: Find the files
    results = []
    for idx, source_uri in enumerate(search_uri):
        results.append(
            graph.submit(
                find_uris_udf,
                dataset_uri=dataset_uri,
                search_uri=source_uri,
                config=config,
                include=pattern,
                exclude=ignore,
                max_files=max_files,
                verbose=verbose,
                name=f"Find file URIs ({idx})",
                resources=ingest_resources,
                access_credentials_name=acn,
            )
        )

    # Step 2: Break found files into chunks for ingestion.
    chunks = graph.submit(
        chunk_results_udf,
        udf_results=results,
        batch_size=batch_size,
        verbose=verbose,
        name="Break Found Files in Chunks",
        resources=ingest_resources,
        access_credentials_name=acn,
    )

    # Step 3: Ingest the files
    ingested = graph.submit(
        ingest_files_udf,
        file_uris=chunks,
        namespace=namespace,
        dataset_uri=dataset_uri,
        verbose=verbose,
        # Expand list of results into multiple node operations
        expand_node_output=chunks,
        name="Ingest file URIs",
        resources=ingest_resources,
        access_credentials_name=acn,
    )

    # Step 4 (Optional): Add the files into a group.
    if group_uri:
        graph.submit(
            add_arrays_to_group_udf,
            array_uris=ingested,
            group_uri=group_uri,
            config=config,
            verbose=verbose,
        ).depends_on(ingested)

    # Start the ingestion process
    graph.compute()
    return str(graph.server_graph_uuid)


ingest = as_batch(ingest_files)
