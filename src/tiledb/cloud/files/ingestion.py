import os
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

import tiledb
import tiledb.cloud
from tiledb.cloud import dag
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud._common import utils
from tiledb.cloud.array import info
from tiledb.cloud.dag.mode import Mode
from tiledb.cloud.files import udfs as file_udfs
from tiledb.cloud.files import utils as file_utils
from tiledb.cloud.files.indexing import IndexTypes
from tiledb.cloud.files.indexing import ingest_files as index_files
from tiledb.cloud.utilities import as_batch
from tiledb.cloud.utilities import get_logger_wrapper
from tiledb.cloud.utilities import run_dag

DEFAULT_FILE_INGESTION_NAME = "file-ingestion"


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
                        "Adding to Group %s the following: %s" % (group_uri, array_uris)
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
            logger.error(
                "Error checking if '%s' is a Group. Bad namespace?" % group_uri
            )
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
        filename = file_utils.sanitize_filename(os.path.basename(file_uri))
        array_uri = f"tiledb://{namespace}/{filename}"
        filestore_array_uri = f"{dataset_uri}/{filename}"
        namespace = namespace or tiledb.cloud.user_profile().default_namespace_charged
        logger.debug(
            """
            ---------------------------------------------
            - Input URI: %s
            - Sanitized Filename: %s
            - Array URI: %s
            - Destination URI: %s
            ---------------------------------------------"""
            % (file_uri, filename, array_uri, filestore_array_uri)
        )

        try:
            file_utils.create_file(
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
                logger.warning("Array '%s' already exists." % array_uri)
                continue
            elif f"array {array_uri} is not unique" in error_msg:
                logger.warning(
                    "Array URI %s is not unique. Skipping %s ingestion"
                    % (array_uri, filename)
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
    batch_size: Optional[int] = file_udfs.DEFAULT_BATCH_SIZE,
    acn: Optional[str] = None,
    config: Optional[dict] = None,
    namespace: Optional[str] = None,
    group_uri: Optional[str] = None,
    taskgraph_name: Optional[str] = DEFAULT_FILE_INGESTION_NAME,
    ingest_resources: Optional[Mapping[str, Any]] = dag.MIN_BATCH_RESOURCES,
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
    :return str: The resulting TaskGraph's server UUID.
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
            error_msg = "Group URI: '%s' is not correctly formatted" % group_uri
            logger.error(error_msg)
            raise ValueError(error_msg) from exc

    namespace = namespace or tiledb.cloud.user_profile().default_namespace_charged
    if isinstance(search_uri, str):
        search_uri = [search_uri]

    logger.debug(
        """
        ----------------------------------------------
        Build the file ingestion graph with arguments:
        ----------------------------------------------
        - Dataset URI: %s
        - Search:
            - URI: %s
            - Patterns:
                - Include: %s
                - Exclude: %s
            - Max Files: %s
            - Batch Size: %s
        - Namespace: %s
        - Group URI: %s
        - Taskgraph Name: %s
        - Resources: %s
        ----------------------------------------------
        """
        % (
            dataset_uri,
            search_uri,
            pattern,
            ignore,
            max_files,
            batch_size,
            namespace,
            group_uri,
            taskgraph_name,
            ingest_resources,
        )
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
                file_udfs.find_uris_udf,
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
        file_udfs.chunk_udf,
        items=results,
        batch_size=batch_size,
        flatten_items=True,
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
    ## graph is waited by default using `run_dag`
    run_dag(graph, debug=verbose)
    return str(graph.server_graph_uuid)


ingest = as_batch(ingest_files)


# ====================================
#         Ingest and Index
# ====================================
def ingest_and_index(
    dataset_uri: str,
    search_uri: str,
    index_uri: str,
    *,
    # Configuration params
    acn: Optional[str] = None,
    config: Optional[dict] = None,
    namespace: Optional[str] = None,
    # Common params
    environment_variables: Optional[Mapping[str, str]] = None,
    pattern: Optional[str] = None,
    ignore: Optional[str] = None,
    max_files: Optional[int] = None,
    trace_id: Optional[str] = None,
    wait: bool = False,
    verbose: bool = False,
    # Ingest params
    group_uri: Optional[str] = None,
    batch_size: Optional[int] = file_udfs.DEFAULT_BATCH_SIZE,
    taskgraph_name: Optional[str] = None,
    ingest_resources: Optional[Mapping[str, Any]] = dag.MIN_BATCH_RESOURCES,
    # Index creation params
    index_type: IndexTypes = IndexTypes.IVF_FLAT,
    index_creation_kwargs: Optional[Dict] = None,
    index_dag_resources: Optional[Mapping[str, Any]] = dag.MIN_BATCH_RESOURCES,
    # DirectoryTextReader params
    text_splitter: str = "RecursiveCharacterTextSplitter",
    text_splitter_kwargs: Optional[Dict] = None,
    suffixes: Optional[Sequence[str]] = None,
    # Embedding params
    embedding_class: str = "LangChainEmbedding",
    embedding_kwargs: Optional[Dict] = None,
    openai_key: Optional[str] = None,
    # Index update params
    index_timestamp: Optional[int] = None,
    workers: int = -1,
    worker_resources: Optional[Dict] = None,
    worker_image: Optional[str] = None,
    extra_worker_modules: Optional[List[str]] = None,
    driver_resources: Optional[Dict] = None,
    driver_image: Optional[str] = None,
    extra_driver_modules: Optional[List[str]] = None,
    max_tasks_per_stage: int = -1,
    embeddings_generation_mode: dag.Mode = dag.Mode.BATCH,
    embeddings_generation_driver_mode: dag.Mode = dag.Mode.BATCH,
    vector_indexing_mode: dag.Mode = dag.Mode.BATCH,
    index_update_kwargs: Optional[Dict] = None,
    ## Vector Search BATCH Embedding Resources
    threads: str = "16",
    index_resources: Optional[Dict] = None,
    consolidate_partition_resources: Optional[Dict] = None,
    copy_centroids_resources: Optional[Dict] = None,
    random_sample_resources: Optional[Dict] = None,
    kmeans_resources: Optional[Dict] = None,
    compute_new_centroids_resources: Optional[Dict] = None,
    assign_points_and_partial_new_centroids_resources: Optional[Dict] = None,
    write_centroids_resources: Optional[Dict] = None,
    partial_index_resources: Optional[Dict] = None,
) -> str:
    """
     Ingest files into a dataset and index them afterwards.

     :param dataset_uri: The dataset URI
     :param search_uri: URI or an iterable of URIs of input files.
     :param index_uri: URI of the vector index to load files to.
     # Configuration params
     :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type),
         defaults to None
     :param config: Config dictionary, defaults to None
     :param namespace: TileDB-Cloud namespace, defaults to None
     # Common params
     :param environment_variables: Environment variables to use during ingestion.
     :param pattern: UNIX shell style pattern to filter files in the search,
         defaults to None
     :param ignore: UNIX shell style pattern to filter files out of the search,
         defaults to None
     :param max_files: maximum number of File URIs to read/find,
         defaults to None (no limit)
     :param trace_id: trace ID for logging, defaults to None.
     :param wait: wait for completion, defaults to False (non-blocking)
     :param verbose: Verbose logging, defaults to False
     # Ingest params
     :param group_uri: A TileDB Group URI, defaults to None.
     :param batch_size: Batch size for file ingestion, defaults to 100.
     :param taskgraph_name: Optional name for taskgraph, defaults to None.
     :param ingest_resources: Configuration for node specs,
         defaults to {"cpu": "1", "memory": "2Gi"}
     # Index creation params
     :param index_type: Vector search index type ("FLAT", "IVF_FLAT").
     :param index_creation_kwargs: Arguments to be passed to the index creation
         method.
     :param index_dag_resources: Index creation Node Specs configuration.
     # DirectoryTextReader params.
     :param text_splitter: Text splitter class,
         defaults to "RecursiveCharacterTextSplitter"
     :param text_splitter_kwargs: Arguments for the splitter class.
     :param suffixes: Provide to keep only files with these suffixes
         Useful when wanting to keep files with different suffixes
         Suffixes must include the dot, e.g. ".txt"
     # Embedding params
     :param embedding_class: Embedding class, defaults to "LangChainEmbedding"
     :param embedding_kwargs: Arguments of the embedding class, defaults to None
     :param openai_key: OpenAI key, defaults to None
    # Index update params.
     :param index_timestamp: Timestamp to add index updates at.
     :param workers: If `embeddings_generation_mode=BATCH` this is the number of
         distributed workers to be used.
     :param worker_resources: If `embeddings_generation_mode=BATCH` this can be used
         to specify the worker resources.
     :param worker_image: If `embeddings_generation_mode=BATCH` this can be used
         to specify the worker Docker image.
     :param extra_worker_modules: If `embeddings_generation_mode=BATCH` this can be
         used to install extra pip package to the image.
     :param driver_resources: If `embeddings_generation_driver_mode=BATCH` this can
         be used to specify the driver resources.
     :param driver_image: If `embeddings_generation_driver_mode=BATCH` this can be
         used to specify the driver Docker image.
     :param extra_driver_modules: If `embeddings_generation_driver_mode=BATCH` this
         can be used to install extra pip package to the image.
     :param max_tasks_per_stage: Number of maximum udf tasks per computation stage.
     :param embeddings_generation_mode: TaskGraph execution mode for embeddings
         generation.
     :param embeddings_generation_driver_mode: TaskGraph execution mode for the
         ingestion driver.
     :param vector_indexing_mode: TaskGraph execution mode for the vector indexing.
     :param index_update_kwargs: Extra arguments to pass to the index update job.
         These can be any of the documented tiledb.vector_search.ingest method with the
         exception of BATCH Embedding Resources (see next params):
         https://tiledb-inc.github.io/TileDB-Vector-Search/documentation/reference/ingestion.html#tiledb.vector_search.ingestion.ingest
         Also `files_per_partition: int` can be included (defaults to -1)
     ## Vector Search BATCH Embedding Resources
     ## These are only applicable if indexing update is executed in BATCH mode.
     :param threads: Threads to be used in the Nodes, defaults to 16.
     :param ingest_resources: Resources to request when performing vector ingestion.
     :param consolidate_partition_resources: Resources to request when performing
         consolidation of a partition.
     :param copy_centroids_resources: Resources to request when performing copy
         of centroids from input array to output array.
     :param random_sample_resources: Resources to request when performing random
         sample selection.
     :param kmeans_resources: Resources to request when performing kmeans task.
     :param compute_new_centroids_resources: Resources to request when performing
         centroid computation.
     :param assign_points_and_partial_new_centroids_resources: Resources to request
         when performing the computation of partial centroids.
     :param write_centroids_resources: Resources to request when performing the
         write of centroids.
     :param partial_index_resources: Resources to request when performing the
         computation of partial indexing.

     :return str: The resulting TaskGraph's server UUID.
    """
    # Graph Setup
    taskgraph_name = taskgraph_name or "files-ingest-and-index"
    graph = dag.DAG(
        name=taskgraph_name,
        namespace=namespace,
        mode=Mode.BATCH,
    )

    # Step 1: File ingestion graph
    ingestion = graph.submit(
        ingest_files,
        dataset_uri,
        search_uri=search_uri,
        pattern=pattern,
        ignore=ignore,
        max_files=max_files,
        batch_size=batch_size,
        acn=acn,
        config=config,
        namespace=namespace,
        group_uri=group_uri,
        taskgraph_name=f"initiated from: ({taskgraph_name})",
        ingest_resources=ingest_resources,
        verbose=verbose,
    )

    # Step 2: File indexing graph
    indexing = graph.submit(
        index_files,
        # Search in the ingested files' uri
        search_uri=dataset_uri,
        index_uri=index_uri,
        acn=acn,
        config=config,
        environment_variables=environment_variables,
        namespace=namespace,
        verbose=verbose,
        trace_id=trace_id,
        index_type=index_type,
        index_creation_kwargs=index_creation_kwargs,
        index_dag_resources=index_dag_resources,
        include=pattern,
        exclude=ignore,
        suffixes=suffixes,
        max_files=max_files,
        text_splitter=text_splitter,
        text_splitter_kwargs=text_splitter_kwargs,
        embedding_class=embedding_class,
        embedding_kwargs=embedding_kwargs,
        openai_key=openai_key,
        index_timestamp=index_timestamp,
        workers=workers,
        worker_resources=worker_resources,
        worker_image=worker_image,
        extra_worker_modules=extra_worker_modules,
        driver_resources=driver_resources,
        driver_image=driver_image,
        extra_driver_modules=extra_driver_modules,
        max_tasks_per_stage=max_tasks_per_stage,
        embeddings_generation_mode=embeddings_generation_mode,
        embeddings_generation_driver_mode=embeddings_generation_driver_mode,
        vector_indexing_mode=vector_indexing_mode,
        index_update_kwargs=index_update_kwargs,
        threads=threads,
        ingest_resources=index_resources,
        consolidate_partition_resources=consolidate_partition_resources,
        copy_centroids_resources=copy_centroids_resources,
        random_sample_resources=random_sample_resources,
        kmeans_resources=kmeans_resources,
        compute_new_centroids_resources=compute_new_centroids_resources,
        assign_points_and_partial_new_centroids_resources=assign_points_and_partial_new_centroids_resources,
        write_centroids_resources=write_centroids_resources,
        partial_index_resources=partial_index_resources,
    )
    indexing.depends_on(ingestion)

    # Start the ingestion and indexing process
    run_dag(graph, wait=wait, debug=verbose)
    return str(graph.server_graph_uuid)


ingest_and_index = as_batch(ingest_and_index)
