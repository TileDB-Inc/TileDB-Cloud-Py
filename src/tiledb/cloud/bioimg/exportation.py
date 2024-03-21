import logging
from typing import Any, Iterator, Mapping, Optional, Sequence, Tuple, Union

import tiledb
from tiledb.cloud import dag
from tiledb.cloud.bioimg.helpers import get_logger_wrapper
from tiledb.cloud.bioimg.helpers import validate_io_paths
from tiledb.cloud.dag.mode import Mode
from tiledb.cloud.rest_api.models import RetryStrategy
from tiledb.cloud.utilities._common import as_batch
from tiledb.cloud.utilities._common import run_dag

DEFAULT_RESOURCES = {"cpu": "8", "memory": "4Gi"}
DEFAULT_IMG_NAME = "3.9-imaging-dev"
DEFAULT_DAG_NAME = "bioimg-exportation"


def export(
    source: Union[Sequence[str], str],
    output: Union[Sequence[str], str],
    *args: Any,
    access_credentials_name: str,
    config: Optional[Mapping[str, Any]] = None,
    taskgraph_name: Optional[str] = None,
    num_batches: Optional[int] = None,
    resources: Optional[Mapping[str, Any]] = None,
    compute: bool = True,
    mode: Optional[Mode] = Mode.BATCH,
    namespace: Optional[str] = None,
    verbose: bool = False,
    output_ext: str = "tiff",
    **kwargs,
) -> tiledb.cloud.dag.DAG:
    """The function exports microscopy images from TileDB arrays

    :param source: uri / iterable of uris of input files
        If the uri points to a directory of files make sure it ends with a trailing '/'
    :param output: uri / iterable of uris of input files.
        If the uri points to a directory of files make sure it ends with a trailing '/'
    :param config: dict configuration to pass credentials of the destination
    :param taskgraph_name: Optional name for taskgraph, defaults to None
    :param num_batches: Number of graph nodes to spawn.
        Performs it sequentially if default, defaults to 1
    :param threads: Number of threads for node side multiprocessing, defaults to 8
    :param resources: configuration for node specs e.g. {"cpu": "8", "memory": "4Gi"},
        defaults to None
    :param compute: When True the DAG returned will be computed inside the function
    otherwise DAG will only be returned.
    :param mode: By default runs Mode.Batch
    :param run_on: By default runs on server if value is "client" runs client side.
    :param namespace: The namespace where the DAG will run
    :param verbose: verbose logging, defaults to False
    :param access_credentials_name: Access Credentials Name (ACN) registered
        in TileDB Cloud (ARN type)
    :param output_ext: extension for the output images in tiledb

    """
    if not access_credentials_name:
        raise ValueError(
            "Ingestion graph requires `access_credentials_name` to be set."
        )
    logger = get_logger_wrapper(verbose)
    logger.debug("Exporting files: %s", source)
    max_workers = None if num_batches else 20  # Default picked heuristically.

    def build_io_uris_exportation(
        source: Sequence[str],
        output: Sequence[str],
        output_ext: str,
        logger: logging.Logger,
    ):
        """Match input uri/s with output destinations
        :param source: A sequence of paths or path to input
        :param output_dir: A path to the output directory
        """
        import os

        import tiledb

        vfs = tiledb.VFS()

        def create_output_path(input_file: str, output: str) -> str:
            # Check if output is dir
            if not output.endswith("/"):
                # The output is considered a target file
                return output
            filename = os.path.splitext(os.path.basename(input_file))[0]
            output_filename = f"{filename}.{output_ext}" if output_ext else filename
            return os.path.join(output, output_filename)

        def iter_paths(source: Sequence[str], output: Sequence[str]) -> Iterator[Tuple]:
            if len(output) != 1:
                for s, o in zip(source, output):
                    if tiledb.object_type(s) == "group":
                        logger.debug("Pair %s and %s", s, o)
                        yield s, create_output_path(s, o)
                    else:
                        logger.debug("Input %s is not a tiledb asset", s)
                        continue
            else:
                logger.debug("Traverse source: %s", source)
                for s in source:
                    if tiledb.object_type(s) != "group":
                        # Folder for exploration
                        contents = vfs.ls(s)
                        # Explore folders only at depth 1
                        filtered_contents = [
                            c for c in contents if tiledb.object_type(c) == "group"
                        ]
                        yield from iter_paths(filtered_contents, output)
                    else:
                        logger.debug("Pair %s and %s", s, output[0])
                        yield s, create_output_path(s, output[0])

        logger.debug("Create pairs between %s and %s", source, output)
        return tuple(iter_paths(source, output))

    def build_input_batches(
        source: Sequence[str],
        output: Sequence[str],
        num_batches: int,
        out_ext: str,
        *,
        verbose: bool,
    ):
        logger = get_logger_wrapper(verbose)

        """Groups input URIs into batches."""
        uri_pairs = build_io_uris_exportation(source, output, out_ext, logger)
        # If the user didn't specify a number of batches, run every import
        # as its own task.
        logger.debug("Input batches: %s", uri_pairs)
        logger.debug("The io pairs for ingestion: %s:", uri_pairs)
        my_num_batches = num_batches or len(uri_pairs)
        # If they specified too many batches, don't create empty tasks.
        my_num_batches = min(len(uri_pairs), my_num_batches)
        logger.debug("Number of batches: %r", my_num_batches)
        split_batches = [uri_pairs[n::my_num_batches] for n in range(my_num_batches)]
        logger.debug("Split batches: %r", split_batches)
        return split_batches

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

    source = [source] if isinstance(source, str) else source
    output = [output] if isinstance(output, str) else output
    validate_io_paths(source, output, for_registration=False)

    # Build the task graph
    dag_name = taskgraph_name or DEFAULT_DAG_NAME

    logger.debug("Building graph")

    graph = dag.DAG(
        name=dag_name,
        mode=mode,
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
        *args,
        verbose=verbose,
        access_credentials_name=access_credentials_name,
        name=f"{dag_name} input collector",
        result_format="json",
    )

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
        access_credentials_name=access_credentials_name,
        **kwargs,
    )

    if compute:
        run_dag(graph, debug=verbose)
    return graph


# Wrapper function for batch VCF ingestion
export_batch = as_batch(export)
