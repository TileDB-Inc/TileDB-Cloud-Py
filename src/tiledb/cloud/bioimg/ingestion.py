from typing import Any, Dict, Iterator, Mapping, Optional, Sequence, Tuple, Union

import tiledb
from tiledb.cloud import dag
from tiledb.cloud.bioimg.helpers import get_logger_wrapper
from tiledb.cloud.bioimg.helpers import serialize_filter
from tiledb.cloud.rest_api.models import RetryStrategy
from tiledb.cloud.utilities._common import run_dag

DEFAULT_RESOURCES = {"cpu": "8", "memory": "4Gi"}
DEFAULT_IMG_NAME = "3.9-imaging-dev"
DEFAULT_DAG_NAME = "bioimg-ingestion"
_SUPPORTED_EXTENSIONS = (".tiff", ".tif", ".svs")


def ingest(
    source: Union[Sequence[str], str],
    output: str,
    config: Mapping[str, Any],
    *args: Any,
    taskgraph_name: Optional[str] = None,
    num_batches: Optional[int] = None,
    threads: Optional[int] = 8,
    resources: Optional[Mapping[str, Any]] = None,
    compute: bool = True,
    namespace: Optional[str],
    verbose: bool = False,
    exclude_metadata: bool = False,
    output_ext: str = "",
    **kwargs,
) -> tiledb.cloud.dag.DAG:
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
    :param compute: When True the DAG returned will be computed inside the function
    otherwise DAG will only be returned.
    :param namespace: The namespace where the DAG will run
    :param verbose: verbose logging, defaults to False
    :output_ext: extension for the output images in tiledb
    """

    logger = get_logger_wrapper(verbose)
    max_workers = None if num_batches else 20  # Default picked heuristically.

    def build_io_uris_ingestion(
        source: Sequence[str],
        output_dir: str,
        output_ext: str,
        supported_exts: Tuple[str],
    ):
        """Match input uri/s with output destinations

        :param source: A sequence of paths or path to input
        :param output_dir: A path to the output directory
        """
        import os

        import tiledb

        vfs = tiledb.VFS()
        # Even though a tuple by definition when passed through submit becomes list
        supported_exts = tuple(supported_exts)

        def create_output_path(input_file, output_dir) -> str:
            filename = os.path.splitext(os.path.basename(input_file))[0]
            output_filename = filename + f".{output_ext}" if output_ext else filename
            return os.path.join(output_dir, output_filename)

        def iter_paths(source: Sequence[str]) -> Iterator[Tuple]:
            for uri in source:
                if vfs.is_dir(uri):
                    # Folder for exploration
                    contents = vfs.ls(uri)
                    yield from iter_paths(contents)
                elif uri.endswith(supported_exts):
                    yield uri, create_output_path(uri, output_dir)

        if len(source) == 0:
            raise ValueError("The source files cannot be empty")
        return tuple(iter_paths(source))

    def build_input_batches(
        source: Sequence[str],
        output: str,
        num_batches: int,
        out_ext: str,
        supported_exts: Tuple,
    ):
        """Groups input URIs into batches."""
        uri_pairs = build_io_uris_ingestion(source, output, out_ext, supported_exts)
        # If the user didn't specify a number of batches, run every import
        # as its own task.
        my_num_batches = num_batches or len(uri_pairs)
        # If they specified too many batches, don't create empty tasks.
        my_num_batches = min(len(uri_pairs), my_num_batches)
        return [uri_pairs[n::my_num_batches] for n in range(my_num_batches)]

    def ingest_tiff_udf(
        io_uris: Sequence[Tuple],
        config: Mapping[str, Any],
        verbose: bool = False,
        exclude_metadata: bool = False,
        *args: Any,
        **kwargs,
    ):
        """Internal udf that ingests server side batch of bioimaging files
        into tiledb arrays using tiledb-bioimg API

        :param io_uris: Pairs of tiff input - output tdb uris
        :param config: dict configuration to pass on tiledb.VFS
        """

        from tiledb import filter
        from tiledb.bioimg import Converters
        from tiledb.bioimg import from_bioimg

        compressor = kwargs.get("compressor", None)
        if compressor:
            compressor_args = dict(compressor)
            compressor_name = compressor_args.pop("_name")
            if compressor_name:
                compressor_args = {
                    k: None if not v else v for k, v in compressor_args.items()
                }
                kwargs["compressor"] = vars(filter).get(compressor_name)(
                    **compressor_args
                )
            else:
                raise ValueError

        write_context = tiledb.Ctx(config)
        vfs = tiledb.VFS()

        for input, output in io_uris:
            with vfs.open(input) as src:
                with tiledb.scope_ctx(ctx_or_config=write_context):
                    from_bioimg(
                        src,
                        output,
                        converter=Converters.OMETIFF,
                        exclude_metadata=exclude_metadata,
                        verbose=verbose,
                        **kwargs,
                    )

    if isinstance(source, str):
        # Handle only lists
        source = [source]
    logger.debug("Ingesting files: %s", source)

    # Build the task graph
    dag_name = taskgraph_name or DEFAULT_DAG_NAME

    logger.debug("Building graph")
    graph = dag.DAG(
        name=dag_name,
        mode=dag.Mode.BATCH,
        max_workers=max_workers,
        namespace=namespace,
        retry_strategy=RetryStrategy(
            limit=3,
            retry_policy="Always",
        ),
    )

    # The lister doesn't need many resources.
    input_list_node = graph.submit(
        build_input_batches,
        source,
        output,
        num_batches,
        output_ext,
        _SUPPORTED_EXTENSIONS,
        access_credentials_name=kwargs.get("access_credentials_name"),
        name=f"{dag_name} input collector",
        result_format="json",
    )

    # serialize udf arguments
    compressor = kwargs.pop("compressor", None)
    logger.debug("Compressor: %r", compressor)
    compressor_serial = serialize_filter(compressor) if compressor else None

    graph.submit(
        ingest_tiff_udf,
        input_list_node,
        config,
        verbose,
        threads,
        *args,
        name=f"{dag_name} ingestor ",
        expand_node_output=input_list_node,
        resources=DEFAULT_RESOURCES if resources is None else resources,
        image_name=DEFAULT_IMG_NAME,
        compressor=compressor_serial,
        **kwargs,
    )

    if compute:
        run_dag(graph, debug=verbose)
    return graph


def ingest_udf(*args: Any, **kwargs: Any) -> Dict[str, str]:
    """Ingestor wrapper function that can be used as a UDF."""
    grf = ingest(*args, **kwargs)
    return {"status": "started", "graph_id": str(grf.server_graph_uuid)}
