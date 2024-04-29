from typing import Dict, List, Mapping, Optional, Sequence

from tiledb.cloud import dag
from tiledb.cloud.utilities import as_batch


def ingest_files(
    search_uri: str,
    index_uri: str,
    acn: Optional[str] = None,
    config=None,
    environment_variables: Optional[Mapping[str, str]] = None,
    namespace: Optional[str] = None,
    verbose: bool = False,
    trace_id: Optional[str] = None,
    # Index creation params
    index_type: str = "IVF_FLAT",
    index_creation_kwargs: Optional[Dict] = None,
    # DirectoryTextReader params
    include: str = "*",
    exclude: Optional[Sequence[str]] = ("[.]*", "*/[.]*"),
    suffixes: Optional[Sequence[str]] = None,
    max_files: Optional[int] = None,
    text_splitter: str = "RecursiveCharacterTextSplitter",
    text_splitter_kwargs: Optional[Dict] = None,
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
    embeddings_generation_driver_mode: dag.Mode = dag.Mode.LOCAL,
    vector_indexing_mode: dag.Mode = dag.Mode.BATCH,
    index_update_kwargs: Optional[Dict] = None,
):
    """
    Ingest files into a vector search text index.

    :param search_uri: Uri to load files from. This can be a directory URI or a FileStore
       file URI.
    :param index_uri: URI of the vector index to load files to.
    :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type),
        defaults to None.
    :param config: config dictionary, defaults to None.
    :param environment_variables: Environment variables to use during ingestion.
    :param namespace: TileDB-Cloud namespace, defaults to None.
    :param verbose: verbose logging, defaults to False.
    :param trace_id: trace ID for logging, defaults to None.
    # Vector Index params
    :param index_type: Vector search index type ("FLAT", "IVF_FLAT").
    :param index_creation_kwargs: Arguments to be passed to the index creation
        method.
    # DirectoryTextReader params.
    :param include: File pattern to iclude relative to `search_uri`. By default
        set to include all files.
    :param exclude: File patterns to exclude relative to `search_uri`. By default
        set to ignore all hidden files.
    :param suffixes: Provide to keep only files with these suffixes
        Useful when wanting to keep files with different suffixes
        Suffixes must include the dot, e.g. ".txt"
    :param max_files: Maximum number of files to include.
    :param text_splitter_kwargs: Arguments for the splitter class.
    # SentenceTransformersEmbedding params.
    :param model_name_or_path: Huggingface SentenceTransformer model name or path
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
    """
    import logging

    import tiledb
    from tiledb.cloud import dag
    from tiledb.cloud.utilities import get_logger
    from tiledb.cloud.utilities import run_dag

    DEFAULT_IMG_NAME = "vectorsearch"

    def get_logger_wrapper(
        verbose: bool = False,
    ) -> logging.Logger:
        """
        Get a logger instance and log version information.

        :param verbose: verbose logging, defaults to False
        :return: logger instance
        """

        level = logging.DEBUG if verbose else logging.INFO
        logger = get_logger(level)

        logger.debug(
            "tiledb.cloud=%s, tiledb=%s, libtiledb=%s",
            tiledb.cloud.version.version,
            tiledb.version(),
            tiledb.libtiledb.version(),
        )

        return logger

    # --------------------------------------------------------------------
    # UDFs
    # --------------------------------------------------------------------

    def create_dataset_udf(
        search_uri: str,
        index_uri: str,
        config=None,
        environment_variables: Optional[Mapping[str, str]] = None,
        verbose: bool = False,
        # Index creation params
        index_type: str = "IVF_FLAT",
        index_creation_kwargs: Optional[Dict] = None,
        # DirectoryTextReader params
        include: str = "*",
        exclude: Optional[Sequence[str]] = ("[.]*", "*/[.]*"),
        suffixes: Optional[Sequence[str]] = None,
        max_files: Optional[int] = None,
        text_splitter: str = "RecursiveCharacterTextSplitter",
        text_splitter_kwargs: Optional[Dict] = None,
        # Embedding params
        embedding_class: str = "LangChainEmbedding",
        embedding_kwargs: Optional[Dict] = None,
    ) -> str:
        """
        Create a TileDB vector search dataset.
        """
        import tiledb.vector_search as vs
        import tiledb.vector_search.embeddings as embeddings_module
        from tiledb.vector_search.object_api import object_index
        from tiledb.vector_search.object_readers import DirectoryTextReader

        logger = get_logger_wrapper(verbose)
        logger.debug("tiledb-vector-search=%s", vs.__version__)

        # Check if the dataset already exists
        with tiledb.scope_ctx(config):
            if environment_variables is None:
                environment_variables = {}
            if index_creation_kwargs is None:
                index_creation_kwargs = {}
            if embedding_kwargs is None:
                embedding_kwargs = {
                    "dimensions": 1536,
                    "embedding_class": "OpenAIEmbeddings",
                    "embedding_kwargs": {
                        "model": "text-embedding-ada-002",
                    },
                }
            if text_splitter_kwargs is None:
                text_splitter_kwargs = {
                    "chunk_size": 500,
                    "chunk_overlap": 50,
                }

            reader = DirectoryTextReader(
                search_uri=search_uri,
                include=include,
                exclude=exclude,
                suffixes=suffixes,
                max_files=max_files,
                text_splitter=text_splitter,
                text_splitter_kwargs=text_splitter_kwargs,
            )

            embedding_class_ = getattr(embeddings_module, embedding_class)
            embedding = embedding_class_(**embedding_kwargs)

            if tiledb.object_type(index_uri) == "group":
                logger.info("Existing dataset: %r. Updating reader.", index_uri)
                index = object_index.ObjectIndex(
                    uri=index_uri,
                    environment_variables=environment_variables,
                    # We don't want to perform any queries here. We open the index without
                    # loading the embedding model, metadata and vector data.
                    load_embedding=False,
                    load_metadata_in_memory=False,
                    # `memory_budget=1` avoids loading the array data in main memory.
                    memory_budget=1,
                )
                index.update_object_reader(reader)
                return index_uri
            else:
                logger.info("Creating dataset: %r", index_uri)
                object_index.create(
                    uri=index_uri,
                    index_type=index_type,
                    object_reader=reader,
                    embedding=embedding,
                    config=config,
                    environment_variables=environment_variables,
                    **index_creation_kwargs,
                )
                return index_uri

    def ingest_files_udf(
        index_uri: str,
        acn: Optional[str] = None,
        config=None,
        environment_variables: Optional[Mapping[str, str]] = None,
        openai_key: Optional[str] = None,
        namespace: Optional[str] = None,
        verbose: bool = False,
        trace_id: Optional[str] = None,
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
        embeddings_generation_mode: dag.Mode = dag.Mode.LOCAL,
        embeddings_generation_driver_mode: dag.Mode = dag.Mode.LOCAL,
        vector_indexing_mode: dag.Mode = dag.Mode.LOCAL,
        index_update_kwargs: Optional[Dict] = None,
    ):
        """
        Ingest files into a vector search text index.
        """
        from tiledb.vector_search.object_api import object_index

        if environment_variables is None:
            environment_variables = {}
        if openai_key is not None:
            environment_variables["OPENAI_API_KEY"] = openai_key
        if index_update_kwargs is None:
            index_update_kwargs = {"files_per_partition": 100}

        index = object_index.ObjectIndex(
            uri=index_uri,
            environment_variables=environment_variables,
            # We don't want to perform any queries here. We open the index without
            # loading the embedding model, metadata and vector data.
            load_embedding=False,
            load_metadata_in_memory=False,
            # `memory_budget=1` avoids loading the array data in main memory.
            memory_budget=1,
        )
        index.update_index(
            index_timestamp=index_timestamp,
            workers=workers,
            worker_resources=worker_resources,
            worker_image=worker_image,
            extra_worker_modules=extra_worker_modules,
            driver_resources=driver_resources,
            driver_image=driver_image,
            extra_driver_modules=extra_driver_modules,
            worker_access_credentials_name=acn,
            max_tasks_per_stage=max_tasks_per_stage,
            embeddings_generation_mode=embeddings_generation_mode,
            embeddings_generation_driver_mode=embeddings_generation_driver_mode,
            vector_indexing_mode=vector_indexing_mode,
            config=config,
            environment_variables=environment_variables,
            namespace=namespace,
            verbose=verbose,
            trace_id=trace_id,
            **index_update_kwargs,
        )

    # --------------------------------------------------------------------
    # DAG
    # --------------------------------------------------------------------

    graph = dag.DAG(
        name="vector-search-file-indexing",
        namespace=namespace,
        mode=dag.Mode.BATCH,
    )
    if worker_resources is None:
        worker_resources = {"cpu": "2", "memory": "8Gi"}

    create_index_node = graph.submit(
        create_dataset_udf,
        search_uri=search_uri,
        index_uri=index_uri,
        config=config,
        environment_variables=environment_variables,
        verbose=verbose,
        index_type=index_type,
        index_creation_kwargs=index_creation_kwargs,
        include=include,
        exclude=exclude,
        suffixes=suffixes,
        max_files=max_files,
        text_splitter=text_splitter,
        text_splitter_kwargs=text_splitter_kwargs,
        embedding_class=embedding_class,
        embedding_kwargs=embedding_kwargs,
        name="Create Vector Search index",
        access_credentials_name=acn,
        resources={"cpu": "1", "memory": "2Gi"},
        image_name=DEFAULT_IMG_NAME,
    )

    ingest_files_node = graph.submit(
        ingest_files_udf,
        index_uri=index_uri,
        acn=acn,
        config=config,
        environment_variables=environment_variables,
        openai_key=openai_key,
        namespace=namespace,
        verbose=verbose,
        trace_id=trace_id,
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
        name="Ingest Files to Vector Search index",
        access_credentials_name=acn,
        resources=worker_resources,
        image_name=DEFAULT_IMG_NAME,
    )

    ingest_files_node.depends_on(create_index_node)
    run_dag(graph, debug=verbose)


ingest = as_batch(ingest_files)
