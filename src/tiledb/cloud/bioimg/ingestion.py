import os
import posixpath
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union

import tiledb
from tiledb.cloud import dag
from tiledb.cloud._common.utils import logger

DEFAULT_RESOURCES = {"cpu": "8", "memory": "4Gi"}
DEFAULT_IMG_NAME = "3.9-imaging-dev"


def ingest(
    source: Union[Sequence[str], str],
    output: str,
    config: Mapping[str, Any],
    *args: Any,
    taskgraph_name: Optional[str] = None,
    num_batches: Optional[int] = None,
    threads: Optional[int] = 8,
    resources: Optional[Mapping[str, Any]] = None,
    namespace: Optional[str],
    **kwargs,
) -> dag.DAG:
    """The function ingests microscopy images into TileDB arrays

    :param source: uri / iterable of uris of input files
    :param output: output dir for the ingested tiledb arrays
    :param config: dict configuration to pass on tiledb.VFS
    :param taskgraph_name: Optional name for taskgraph, defaults to None
    :param num_batches: Number of graph nodes to spawn.
        Performs it sequentially if default, defaults to 1
    :param threads: Number of threads for node side multiprocessing, defaults to 8
    :param resources: configuration for node specs e.g. {"cpu": "8", "memory": "4Gi"},
        defaults to None
    :param namespace: The namespace where the DAG will run
    """
    source_list = [source] if isinstance(source, str) else list(source)
    max_workers = None if num_batches else 20  # Default picked heuristically.

    def build_io_uris() -> List[Tuple[str, str]]:
        """Match input uri/s with output destinations

        :param source: A sequence of paths or path to input
        :param output_dir: A path to the output directory
        """
        vfs = tiledb.VFS()
        my_source_list = source_list
        if len(my_source_list) == 1 and vfs.is_dir(my_source_list[0]):
            # Folder like input
            my_source_list = vfs.ls(my_source_list[0])
        return [
            (uri, os.path.join(output, posixpath.basename(uri)))
            for uri in my_source_list
        ]

    def build_input_batches():
        """Groups input URIs into batches."""
        uri_pairs = build_io_uris()
        # If the user didn't specify a number of batches, run every import
        # as its own task.
        my_num_batches = num_batches or len(uri_pairs)
        # If they specified too many batches, don't create empty tasks.
        my_num_batches = min(len(uri_pairs), my_num_batches)
        return [uri_pairs[n::my_num_batches] for n in range(my_num_batches)]

    def ingest_tiff_udf(
        io_uris: Sequence[Tuple[str, str]],
        config: Mapping[str, Any],
        workers: int,
        *args: Any,
        **kwargs,
    ):
        """Internal udf that ingests server side batch of bioimaging files
        into tiledb arrays using tiledb-bioimg API

        :param io_uris: Pairs of tiff input - output tdb uris
        :param config: dict configuration to pass on tiledb.VFS
        :param workers: Number of threads that will spawn for parallelizing ingestion
        """

        from tiledb.bioimg.converters.ome_tiff import OMETiffConverter

        write_context = tiledb.Ctx(config)
        vfs = tiledb.VFS()
        for input, output in io_uris:
            with vfs.open(input) as src:
                with tiledb.scope_ctx(write_context):
                    OMETiffConverter.to_tiledb(
                        src, output, *args, max_workers=workers, chunked=True, **kwargs
                    )

    # Calculate number batches - default fair split

    # Build the task graph
    dag_name = taskgraph_name or "batch-ingest-bioimg"

    logger.info("Building graph")
    graph = dag.DAG(
        name=dag_name,
        mode=dag.Mode.BATCH,
        max_workers=max_workers,
        namespace=namespace,
    )
    # The lister doesn't need many resources.
    input_list_node = graph.submit(
        build_input_batches,
        access_credentials_name=kwargs.get("access_credentials_name"),
        name=f"{dag_name} input collector",
        result_format="json",
    )
    graph.submit(
        ingest_tiff_udf,
        input_list_node,
        config,
        threads,
        *args,
        name=f"{dag_name} ingestor",
        expand_node_output=input_list_node,
        resources=DEFAULT_RESOURCES if resources is None else resources,
        image_name=DEFAULT_IMG_NAME,
        **kwargs,
    )
    graph.compute()
    return graph


def ingest_udf(*args: Any, **kwargs: Any) -> Dict[str, str]:
    """Ingestor wrapper function that can be used as a UDF."""
    grf = ingest(*args, **kwargs)
    return {"status": "started", "graph_id": str(grf.server_graph_uuid)}
