from typing import Any, Dict, Iterator, Mapping, Optional, Sequence, Tuple, Union

import tiledb
from tiledb.cloud import dag
from tiledb.cloud.bioimg.helpers import get_logger_wrapper
from tiledb.cloud.utilities._common import run_dag

DEFAULT_RESOURCES = {"cpu": "8", "memory": "4Gi"}
DEFAULT_IMG_NAME = "3.9-imaging-dev"
DEFAULT_DAG_NAME = "bioimg-exportation"
_RUNNING_PROFILES = ("client", "server")


def export(
    source: Union[Sequence[str], str],
    output: str,
    *args: Any,
    config: Optional[Mapping[str, Any]] = None,
    taskgraph_name: Optional[str] = None,
    num_batches: Optional[int] = None,
    resources: Optional[Mapping[str, Any]] = None,
    compute: bool = True,
    run_on: Optional[str] = None,
    namespace: Optional[str] = None,
    verbose: bool = False,
    output_ext: str = "tiff",
    **kwargs,
) -> tiledb.cloud.dag.DAG:
    """The function exports microscopy images from TileDB arrays

    :param source: uri / iterable of uris of input files
    :param output: output dir for the exported tiledb arrays
    :param config: dict configuration to pass credentials of the destination
    :param taskgraph_name: Optional name for taskgraph, defaults to None
    :param num_batches: Number of graph nodes to spawn.
        Performs it sequentially if default, defaults to 1
    :param threads: Number of threads for node side multiprocessing, defaults to 8
    :param resources: configuration for node specs e.g. {"cpu": "8", "memory": "4Gi"},
        defaults to None
    :param compute: When True the DAG returned will be computed inside the function
    otherwise DAG will only be returned.
    :param run_on: By default runs on server if value is "client" runs client side.
    :param namespace: The namespace where the DAG will run
    :param verbose: verbose logging, defaults to False
    :output_ext: extension for the output images in tiledb

    """

    logger = get_logger_wrapper(verbose)
    logger.debug("Exporting files: %s", source)
    max_workers = None if num_batches else 20  # Default picked heuristically.

    def build_io_uris_exportation(
        source: Sequence[str], output_dir: str, output_ext: str
    ):
        """Match input uri/s with output destinations

        :param source: A sequence of paths or path to input
        :param output_dir: A path to the output directory
        """
        import os

        import tiledb

        vfs = tiledb.VFS()

        def create_output_path(input_file, output_dir) -> str:
            filename = os.path.splitext(os.path.basename(input_file))[0]
            output_filename = filename + f".{output_ext}" if output_ext else filename
            return os.path.join(output_dir, output_filename)

        def iter_paths(source: Sequence) -> Iterator[Tuple]:
            for uri in source:
                if vfs.is_dir(uri) and tiledb.object_type(uri) != "group":
                    # Folder for exploration
                    contents = vfs.ls(uri)
                    yield from iter_paths(contents)
                elif tiledb.object_type(uri) == "group":
                    # For exportation we require the source path to be a tiledb group
                    yield uri, create_output_path(uri, output_dir)

        if len(source) == 0:
            raise ValueError("The source files cannot be empty")
        return tuple(iter_paths(source))

    def build_input_batches(
        source: Sequence[str], output: str, num_batches: int, out_ext: str
    ):
        """Groups input URIs into batches."""
        uri_pairs = build_io_uris_exportation(source, output, out_ext)
        # If the user didn't specify a number of batches, run every import
        # as its own task.
        my_num_batches = num_batches or len(uri_pairs)
        # If they specified too many batches, don't create empty tasks.
        my_num_batches = min(len(uri_pairs), my_num_batches)
        return [uri_pairs[n::my_num_batches] for n in range(my_num_batches)]

    def export_tiff_udf(
        io_uris: Sequence[Tuple],
        config: Mapping[str, Any],
        verbose: bool = False,
        *args: Any,
        **kwargs,
    ):
        """Internal udf that exports server side batch of tiledb arrays
        2Tiff biomedical images using tiledb-bioimg API

        :param io_uris: Pairs of tiff input - output tdb uris
        :param config: dict configuration to pass on tiledb.VFS
        """
        from tiledb.bioimg import Converters
        from tiledb.bioimg import to_bioimg
        from tiledb.ctx import default_ctx

        # if writer config not given assume same as source
        src_cfg = default_ctx().config()
        dest_cfg = config or src_cfg

        for input, output in io_uris:
            to_bioimg(
                input,
                output,
                converter=Converters.OMETIFF,
                config=src_cfg,
                output_config=dest_cfg,
                verbose=verbose,
                **kwargs,
            )

    if isinstance(source, str):
        # Handle only lists
        source = [source]
    logger.debug("Exporting files: %s", source)

    # Build the task graph
    dag_name = taskgraph_name or DEFAULT_DAG_NAME

    logger.debug("Building graph")

    run_mode = run_on or "server"
    if run_mode not in _RUNNING_PROFILES:
        raise ValueError("Invalid value for argument 'run_on'")

    graph = dag.DAG(
        name=dag_name,
        mode=dag.Mode.REALTIME if run_mode == "client" else dag.Mode.BATCH,
        max_workers=max_workers,
        namespace=namespace,
    )

    # The lister doesn't need many resources.
    input_list_node = graph.submit(
        build_input_batches,
        source,
        output,
        num_batches,
        output_ext,
        access_credentials_name=kwargs.get("access_credentials_name"),
        name=f"{dag_name} input collector",
        result_format="json",
    )

    logger.debug("Batched Input-Output pairs: %s", input_list_node)

    graph.submit(
        export_tiff_udf,
        input_list_node,
        config,
        verbose,
        *args,
        name=f"{dag_name} exporter",
        expand_node_output=input_list_node,
        resources=DEFAULT_RESOURCES if resources is None else resources,
        image_name=DEFAULT_IMG_NAME,
        **kwargs,
    )

    if compute:
        run_dag(graph, debug=verbose)
    return graph


def export_udf(*args: Any, **kwargs: Any) -> Dict[str, str]:
    """Exporter wrapper function that can be used as a UDF."""
    grf = export(*args, **kwargs)
    return {"status": "started", "graph_id": str(grf.server_graph_uuid)}
