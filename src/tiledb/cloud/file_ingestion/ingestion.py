import os
from math import ceil
from typing import Any, List, Mapping, Optional, Sequence, Union

import tiledb
from tiledb.cloud import dag
from tiledb.cloud import tiledb_cloud_error
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
    return fname.replace(",", "").replace(" ", "_")


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


def ingest_files_udf(
    dataset_uri: str,
    file_uris: Sequence[str],
    destination: str,
    *,
    acn: Optional[str] = None,
    config: Optional[dict] = None,
    namespace: Optional[str] = None,
    verbose: bool = False,
) -> None:
    """
    Ingest files.

    :param dataset_uri: The dataset URI.
    :param file_uris: An iterable of file URIs.
    :param destination: URI to ingest the files into.
    :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type),
        defaults to None
    :param config: Config dictionary, defaults to None.
    :param namespace: TileDB-Cloud namespace, defaults to None.
    :param verbose: Verbose logging, defaults to False.
    """
    logger = get_logger_wrapper(verbose)
    # Trim potential trailing / in the destination URI
    destination = destination.rstrip("/")

    with tiledb.scope_ctx(config):
        try:
            if dataset_uri:
                is_group = tiledb.object_type(dataset_uri) == "group"
            else:
                is_group = False
        except Exception as exc:
            # tiledb.object_type raises an exception
            # if the namespace does not exist
            logger.error(f"Error checking if {dataset_uri} is a Group. Bad namespace?")
            raise exc

        add_to_group = []
        for file_uri in file_uris:
            filename = sanitize_filename(os.path.basename(file_uri))
            array_uri = f"tiledb://{namespace}/{filename}"
            filestore_array_uri = f"{destination}/{filename}"
            namespace = (
                namespace or tiledb.cloud.user_profile().default_namespace_charged
            )
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

                add_to_group.append(array_uri)
            except tiledb_cloud_error.TileDBCloudError as exc:
                if "array already exists at location - Code: 8003" in repr(exc):
                    logger.warning(f"Array '{array_uri}' already exists.")
                    continue
                else:
                    raise exc

        if is_group:
            with tiledb.Group(dataset_uri, mode="w") as group:
                logger.debug(
                    f"Adding to Group {dataset_uri} the following: {add_to_group}"
                )
                for uri in add_to_group:
                    group.add(uri)


def ingest_files(
    dataset_uri: str,
    source: Union[Sequence[str], str],
    destination: str,
    *,
    acn: Optional[str] = None,
    config: Optional[dict] = None,
    namespace: Optional[str] = None,
    include: Optional[str] = None,
    exclude: Optional[str] = None,
    taskgraph_name: Optional[str] = DEFAULT_FILE_INGESTION_NAME,
    batch_size: Optional[int] = DEFAULT_BATCH_SIZE,
    max_files: Optional[int] = None,
    resources: Optional[Mapping[str, Any]] = None,
    verbose: bool = False,
) -> str:
    """
    Ingest files into a dataset.

    :param dataset_uri: The dataset URI
    :param source: URI or an iterable of URIs of input files.
    :param destination: URI to ingest the files into.
    :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type),
        defaults to None
    :param config: Config dictionary, defaults to None
    :param namespace: TileDB-Cloud namespace, defaults to None
    :param include: UNIX shell style pattern to filter files in the search,
        defaults to None
    :param exclude: UNIX shell style pattern to filter files out of the search,
        defaults to None
    :param taskgraph_name: Optional name for taskgraph, defaults to "file-ingestion"
    :param batch_size: Batch size for file ingestion, defaults to 100
    :param max_files: maximum number of File URIs to read/find,
        defaults to None (no limit)
    :param resources: Configuration for node specs,
        defaults to {"cpu": "1", "memory": "2Gi"}
    :param verbose: Verbose logging, defaults to False
    :return str: The resulting TaskGraph's server UUID as string.
    """
    # Preparation and argument cleanup
    namespace = namespace or tiledb.cloud.user_profile().default_namespace_charged
    resources = resources or DEFAULT_RESOURCES
    dataset_uri = dataset_uri.rstrip("/")
    logger = get_logger_wrapper(verbose)
    if isinstance(source, str):
        source = [source]

    logger.debug("Build the file finding graph...")
    graph = dag.DAG(
        name=f"{taskgraph_name}-ingestor",
        namespace=namespace,
        mode=Mode.BATCH,
    )

    # Step 1: Find the files
    results = []
    for idx, source_uri in enumerate(source):
        results.append(
            graph.submit(
                find_uris_udf,
                dataset_uri=dataset_uri,
                search_uri=source_uri,
                config=config,
                include=include,
                exclude=exclude,
                max_files=max_files,
                verbose=verbose,
                name=f"Find file URIs ({idx})",
                resources=resources,
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
        resources=resources,
        access_credentials_name=acn,
    )

    # Step 3: Ingest the files
    graph.submit(
        ingest_files_udf,
        file_uris=chunks,
        destination=destination,
        namespace=namespace,
        dataset_uri=dataset_uri,
        config=config,
        verbose=verbose,
        # Expand list of results into multiple node operations
        expand_node_output=chunks,
        name="Ingest file URIs",
        resources=resources,
        access_credentials_name=acn,
    )

    # Start the ingestion process
    graph.compute()
    return str(graph.server_graph_uuid)


ingest = as_batch(ingest_files)
