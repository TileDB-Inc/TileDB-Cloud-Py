from math import ceil
from typing import Any, List, Mapping, Optional, Sequence, Union

import tiledb
from tiledb.cloud import dag
from tiledb.cloud.dag.mode import Mode
from tiledb.cloud.utilities import as_batch
from tiledb.cloud.utilities import get_logger_wrapper
from tiledb.cloud.vcf.ingestion import find_uris_udf

DEFAULT_RESOURCES = {"cpu": "2", "memory": "8Gi"}
DEFAULT_FILE_INGESTION_NAME = "file-ingestion"
DEFAULT_BATCH_SIZE = 100


def chunk_results_udf(
    udf_results: Sequence[Sequence[str]], batch_size: Optional[int] = DEFAULT_BATCH_SIZE
) -> List[List[str]]:
    """
    Flatten and break a list of udf results into batches of a specified size.

    :param udf_results: An iterable of iterables containing UDF results.
    :param batch_size: Resulting chunk size, defaults to 100.
    :return List[List[str]]: A list of chunks as lists.
    """
    # Reduce batch size if there are fewer sample URIs
    batch_size = min(batch_size, len(udf_results))
    num_chunks = ceil(len(udf_results) / batch_size)

    flattened_results = [result for udf_result in udf_results for result in udf_result]
    return [
        flattened_results[n * batch_size : (n + 1) * batch_size]
        for n in range(num_chunks)
    ]


def ingest_files_udf(
    dataset_uri: str,
    file_uris: Sequence[str],
    *,
    namespace: Optional[str] = None,
    verbose: bool = False,
) -> None:
    """
    Ingest files.

    :param dataset_uri: The dataset URI.
    :param file_uris: An iterable of file URIs.
    :param namespace: TileDB-Cloud namespace, defaults to None.
    :param verbose: Verbose logging, defaults to False.
    """
    logger = get_logger_wrapper(verbose)

    for file_uri in file_uris:
        filename = file_uri.replace(",", "").replace(" ", "_")
        filestore_array_uri = f"{dataset_uri}/{filename}"
        filestore_array_s3_uri = f"s3{filestore_array_uri.split('s3')[1]}"
        namespace = (
            namespace or filestore_array_uri.split("tiledb://")[1].split("/s3")[0]
        )
        logger.debug(
            f"""
            ---------------------------------------------\n
            - Filename: {filename}\n
            - Namespace: {namespace}\n
            - Array URI: {filestore_array_uri}\n
            - S3 Array URI: {filestore_array_s3_uri}\n
            ---------------------------------------------
            """
        )

        if not tiledb.array_exists(filestore_array_uri):
            tiledb.cloud.file.create_file(
                namespace=namespace,
                name=filename,
                input_uri=file_uri,
                output_uri=filestore_array_s3_uri,
            )


def ingest_files(
    dataset_uri: str,
    *,
    acn: Optional[str] = None,
    config: Optional[dict] = None,
    namespace: Optional[str] = None,
    source: Union[Sequence[str], str],
    include: Optional[str] = None,
    exclude: Optional[str] = None,
    taskgraph_name: Optional[str] = DEFAULT_FILE_INGESTION_NAME,
    batch_size: Optional[int] = DEFAULT_BATCH_SIZE,
    resources: Optional[Mapping[str, Any]] = None,
    verbose: bool = False,
) -> tiledb.cloud.dag.DAG:
    """
    Ingest files into a dataset.

    :param dataset_uri: The dataset URI
    :param source: URI or an iterable of URIs of input files.
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
    :param resources: Configuration for node specs,
        defaults to {"cpu": "2", "memory": "8Gi"}
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

    # logger.debug("Building the graph...")
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
        name="Break Found Files in Chunks",
        verbose=verbose,
        access_credentials_name=acn,
    )

    # Step 3: Ingest the files
    graph.submit(
        # load_files_method, need to discuss
        chunks=chunks,
        dataset_uri=dataset_uri,
        # Expand list of results into multiple node operations
        expand_node_output=chunks,
        config=config,
        verbose=verbose,
        id="file-ingest",
        name="Ingest file URIs",
        resources=resources,
        access_credentials_name=acn,
    )

    return graph


ingest = as_batch(ingest_files)
