import os
from math import ceil
from typing import Any, List, Mapping, Optional, Sequence, Union

import tiledb
from tiledb.cloud import dag
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
    file_uris: Sequence[str],
    destination: str,
    *,
    acn: Optional[str] = None,
    namespace: Optional[str] = None,
    group_uri: Optional[str] = None,
    verbose: bool = False,
) -> None:
    """
    Ingest files.

    :param file_uris: An iterable of file URIs.
    :param destination: URI to ingest the files into.
    :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type),
        defaults to None
    :param namespace: TileDB-Cloud namespace, defaults to None.
    :param group_uri: TileDB Group URI to add ingested file into,
        defaults to None.
    :param verbose: Verbose logging, defaults to False.
    """
    logger = get_logger_wrapper(verbose)
    # Trim potential trailing / in the destination URI
    destination = destination.rstrip("/")

    for file_uri in file_uris:
        filename = sanitize_filename(os.path.basename(file_uri))
        filestore_array_uri = f"{destination}/{filename}"
        namespace = namespace or tiledb.cloud.user_profile().default_namespace_charged
        logger.debug(
            f"""
            ---------------------------------------------
            - Filename: {filename}
            - Namespace: {namespace}
            - Destination URI: {filestore_array_uri}
            ---------------------------------------------"""
        )

        if not tiledb.array_exists(filestore_array_uri):
            tiledb.cloud.file.create_file(
                namespace=namespace,
                name=filename,
                input_uri=file_uri,
                output_uri=filestore_array_uri,
                access_credentials_name=acn,
            )
        else:
            logger.warning(f"Array '{filestore_array_uri}' already exists.")

        if group_uri:
            with tiledb.Group(group_uri, mode="w") as group:
                logger.debug(f"Adding to Group {group_uri}")
                group.add(f"tiledb://{namespace}/{filename}")


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
) -> tiledb.cloud.dag.DAG:
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
    :return tiledb.cloud.dag.DAG: The resulting ingestion graph
    """
    # Preparation and argument cleanup
    config = config or dict()
    namespace = namespace or tiledb.cloud.user_profile().default_namespace_charged
    resources = resources or DEFAULT_RESOURCES
    dataset_uri = dataset_uri.rstrip("/")
    logger = get_logger_wrapper(verbose)
    if isinstance(source, str):
        source = [source]

    with tiledb.scope_ctx(config):
        try:
            is_group = tiledb.object_type(dataset_uri) == "group"
        except Exception as exc:
            # tiledb.object_type raises an exception
            # if the namespace does not exist
            logger.error(f"Error checking if {dataset_uri} is a Group. Bad namespace?")
            raise exc

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
        access_credentials_name=acn,
    )

    # Step 3: Ingest the files
    graph.submit(
        ingest_files_udf,
        file_uris=chunks,
        destination=destination,
        namespace=namespace,
        group_uri=dataset_uri if is_group else None,
        verbose=verbose,
        # Expand list of results into multiple node operations
        expand_node_output=chunks,
        name="Ingest file URIs",
        resources=resources,
        access_credentials_name=acn,
    )

    return graph


ingest = as_batch(ingest_files)
