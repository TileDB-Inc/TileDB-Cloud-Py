from typing import Dict, List, Optional, Sequence

from tiledb.cloud import dag
from tiledb.cloud.utilities import as_batch


def ingest_files_dag(
    file_dir_uri: str,
    index_uri: str,
    file_name: Optional[str] = None,
    acn: Optional[str] = None,
    config=None,
    namespace: Optional[str] = None,
    verbose: bool = False,
    trace_id: Optional[str] = None,
    # Index creation params
    create_index: bool = True,
    index_type: str = "IVF_FLAT",
    index_creation_kwargs: Dict = {},
    # DirectoryTextReader params
    glob: str = "**/[!.]*",
    exclude: Sequence[str] = (),
    suffixes: Optional[Sequence[str]] = None,
    text_splitter: str = "RecursiveCharacterTextSplitter",
    text_splitter_kwargs: Optional[Dict] = {
        "chunk_size": 500,
        "chunk_overlap": 50,
    },
    # SentenceTransformersEmbedding params
    model_name_or_path: str = "BAAI/bge-small-en-v1.5",
    # Index update params
    index_timestamp: int = None,
    workers: int = -1,
    worker_resources: Dict = None,
    worker_image: str = None,
    extra_worker_modules: Optional[List[str]] = None,
    driver_resources: Dict = {"cpu": "2", "memory": "8Gi"},
    driver_image: str = None,
    extra_driver_modules: Optional[List[str]] = None,
    max_tasks_per_stage: int = -1,
    embeddings_generation_mode: dag.Mode = dag.Mode.LOCAL,
    embeddings_generation_driver_mode: dag.Mode = dag.Mode.LOCAL,
    vector_indexing_mode: dag.Mode = dag.Mode.LOCAL,
    index_update_kwargs: Dict = {"files_per_partition": 100},
):
    """
    Ingest files into a vector search text index.

    :param file_dir_uri: directory of the files to be loaded. For individual files,
        also pass the `file_name` param.
    :param index_uri: URI of the vector index to load files to.
    :param file_name: Name of the file to be loaded.
    :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type),
        defaults to None.
    :param config: config dictionary, defaults to None.
    :param namespace: TileDB-Cloud namespace, defaults to None.
    :param verbose: verbose logging, defaults to False.
    :param trace_id: trace ID for logging, defaults to None.
    # Index creation params
    :param create_index: If true, creates a new vector search index.
    :param index_type: Vector search index type ("FLAT", "IVF_FLAT").
    :param index_creation_kwargs: Arguments to be passed to the index creation method
    # DirectoryTextReader params.
    :param glob: Glob pattern relative to the specified path by default set to pick up
        all non-hidden files.
    :param exclude: Patterns to exclude from results, use glob syntax.
    :param suffixes: Load only files with these suffixes. Suffixes must include the
        dot, e.g. ".txt".
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
    :param extra_worker_modules: If `embeddings_generation_mode=BATCH` this can be used
        to install extra pip package to the image.
    :param driver_resources: If `embeddings_generation_driver_mode=BATCH` this can be
        used to specify the driver resources.
    :param driver_image: If `embeddings_generation_driver_mode=BATCH` this can be used
        to specify the driver Docker image.
    :param extra_driver_modules: If `embeddings_generation_driver_mode=BATCH` this can
        be used to install extra pip package to the image.
    :param max_tasks_per_stage: Number of maximum udf tasks per computation stage.
    :param embeddings_generation_mode: TaskGraph execution mode for embeddings
        generation.
    :param embeddings_generation_driver_mode: TaskGraph execution mode for the ingestion
        driver.
    :param vector_indexing_mode: TaskGraph execution mode for the vector indexing.
    :param index_update_kwargs: Extra arguments to pass to the index update job.
    """

    def ingest_files_udf(
        file_dir_uri: str,
        index_uri: str,
        file_name: Optional[str] = None,
        acn: Optional[str] = None,
        config=None,
        namespace: Optional[str] = None,
        verbose: bool = False,
        trace_id: Optional[str] = None,
        # Index creation params
        create_index: bool = True,
        index_type: str = "IVF_FLAT",
        index_creation_kwargs: Dict = {},
        # DirectoryTextReader params
        glob: str = "**/[!.]*",
        exclude: Sequence[str] = (),
        suffixes: Optional[Sequence[str]] = None,
        text_splitter: str = "RecursiveCharacterTextSplitter",
        text_splitter_kwargs: Optional[Dict] = {
            "chunk_size": 500,
            "chunk_overlap": 50,
        },
        # SentenceTransformersEmbedding params
        model_name_or_path: str = "BAAI/bge-small-en-v1.5",
        # Index update params
        index_timestamp: int = None,
        workers: int = -1,
        worker_resources: Dict = None,
        worker_image: str = None,
        extra_worker_modules: Optional[List[str]] = None,
        driver_resources: Dict = {"cpu": "2", "memory": "8Gi"},
        driver_image: str = None,
        extra_driver_modules: Optional[List[str]] = None,
        max_tasks_per_stage: int = -1,
        embeddings_generation_mode: dag.Mode = dag.Mode.LOCAL,
        embeddings_generation_driver_mode: dag.Mode = dag.Mode.LOCAL,
        vector_indexing_mode: dag.Mode = dag.Mode.LOCAL,
        index_update_kwargs: Dict = {"files_per_partition": 100},
    ):
        """
        Ingest files into a vector search text index.

        :param file_dir_uri: directory of the files to be loaded. For individual files,
            also pass the `file_name` param.
        :param index_uri: URI of the vector index to load files to.
        :param file_name: Name of the file to be loaded.
        :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type),
            defaults to None.
        :param config: config dictionary, defaults to None.
        :param namespace: TileDB-Cloud namespace, defaults to None.
        :param verbose: verbose logging, defaults to False.
        :param trace_id: trace ID for logging, defaults to None.
        # Index creation params
        :param create_index: If true, creates a new vector search index.
        :param index_type: Vector search index type ("FLAT", "IVF_FLAT").
        :param index_creation_kwargs: Arguments to be passed to the index creation
            method.
        # DirectoryTextReader params.
        :param glob: Glob pattern relative to the specified path by default set to
            pick up all non-hidden files.
        :param exclude: Patterns to exclude from results, use glob syntax.
        :param suffixes: Load only files with these suffixes. Suffixes must include
            the dot, e.g. ".txt".
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
        import tiledb

        # Install extra packages not yet available in vectorsearch UDF image.
        # TODO(nikos) remove the pacakge installations after the image is updated
        def install_extra_worker_modules():
            import os
            import subprocess
            import sys

            sys.path.insert(0, "/home/udf/.local/bin")
            sys.path.insert(0, "/home/udf/.local/lib/python3.9/site-packages")
            os.environ["PATH"] = f"/home/udf/.local/bin:{os.environ['PATH']}"
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--force-reinstall",
                    "tiledb-vector-search==0.0.23",
                    "tiledb==0.25.0",
                    "tiledb-cloud==0.11.10",
                ]
            )
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "transformers==4.37.1",
                    "PyMuPDF",
                    "beautifulsoup4",
                ]
            )

        install_extra_worker_modules()
        import importlib

        importlib.reload(tiledb)

        from tiledb.vector_search.embeddings import SentenceTransformersEmbedding
        from tiledb.vector_search.object_api import object_index
        from tiledb.vector_search.object_readers import DirectoryTextReader

        reader = DirectoryTextReader(
            uri=file_dir_uri,
            glob=f"**/{file_name}" if file_name is not None else glob,
            exclude=exclude,
            suffixes=suffixes,
            text_splitter=text_splitter,
            text_splitter_kwargs=text_splitter_kwargs,
        )

        embedding = SentenceTransformersEmbedding(
            model_name_or_path=model_name_or_path,
        )
        if create_index:
            index = object_index.create(
                uri=index_uri,
                index_type=index_type,
                object_reader=reader,
                embedding=embedding,
                config=config,
                **index_creation_kwargs,
            )
        else:
            index = object_index.ObjectIndex(
                uri=index_uri, load_metadata_in_memory=False, memory_budget=1
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
            namespace=namespace,
            verbose=verbose,
            trace_id=trace_id,
            **index_update_kwargs,
        )

    graph = dag.DAG(
        name="file-vector-search-ingestion",
        mode=dag.Mode.BATCH,
        max_workers=1,
        namespace=namespace,
    )
    graph.submit(
        ingest_files_udf,
        file_dir_uri,
        index_uri,
        name="file-vector-search-ingestion",
        access_credentials_name=acn,
        resources=driver_resources,
        image_name="vectorsearch",
        acn=acn,
        config=config,
        namespace=namespace,
        verbose=verbose,
        trace_id=trace_id,
        create_index=create_index,
        index_type=index_type,
        index_creation_kwargs=index_creation_kwargs,
        file_name=file_name,
        glob=glob,
        exclude=exclude,
        suffixes=suffixes,
        text_splitter=text_splitter,
        text_splitter_kwargs=text_splitter_kwargs,
        model_name_or_path=model_name_or_path,
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
    )
    graph.compute()
    graph.wait()


ingest_files = as_batch(ingest_files_dag)
