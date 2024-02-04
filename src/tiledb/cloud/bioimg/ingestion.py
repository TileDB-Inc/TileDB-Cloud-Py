import logging
from typing import Any, Dict, Iterator, Mapping, Optional, Sequence, Tuple, Union

import tiledb
from tiledb.cloud import dag
from tiledb.cloud.bioimg.helpers import get_logger_wrapper
from tiledb.cloud.bioimg.helpers import serialize_filter
from tiledb.cloud.bioimg.helpers import validate_io_paths
from tiledb.cloud.dag.mode import Mode
from tiledb.cloud.rest_api.models import RetryStrategy
from tiledb.cloud.utilities._common import run_dag

DEFAULT_RESOURCES = {"cpu": "8", "memory": "4Gi"}
DEFAULT_IMG_NAME = "3.9-imaging-dev"
DEFAULT_DAG_NAME = "bioimg-ingestion"
_SUPPORTED_EXTENSIONS = (".tiff", ".tif", ".svs")
_SUPPORTED_CONVERTERS = ("tiff", "zarr", "osd")


def ingest(
    source: Union[Sequence[str], str],
    output: Union[Sequence[str], str],
    config: Mapping[str, Any],
    *args: Any,
    taskgraph_name: Optional[str] = None,
    num_batches: Optional[int] = None,
    threads: Optional[int] = 8,
    resources: Optional[Mapping[str, Any]] = None,
    compute: bool = True,
    mode: Optional[Mode] = Mode.BATCH,
    namespace: Optional[str],
    verbose: bool = False,
    exclude_metadata: bool = False,
    converter: Optional[str] = None,
    output_ext: str = "",
    traverse: bool = False,
    **kwargs,
) -> tiledb.cloud.dag.DAG:
    """The function ingests microscopy images into TileDB arrays

    :param source: uri / iterable of uris of input files.
        If the uri points to a directory of files make sure it ends with a trailing '/'
    :param output: uri / iterable of uris of input files.
        If the uri points to a directory of files make sure it ends with a trailing '/'
    :param config: dict configuration to pass on tiledb.VFS
    :param taskgraph_name: Optional name for taskgraph, defaults to None
    :param num_batches: Number of graph nodes to spawn.
        Performs it sequentially if default, defaults to 1
    :param threads: Number of threads for node side multiprocessing, defaults to 8
    :param resources: configuration for node specs e.g. {"cpu": "8", "memory": "4Gi"},
        defaults to None
    :param compute: When True the DAG returned will be computed inside the function
    otherwise DAG will only be returned.
    :param mode: By default runs Mode.Batch
    :param namespace: The namespace where the DAG will run
    :param verbose: verbose logging, defaults to False
    :param exclude_metadata: a boolean for excluding all the metadata from the
        ingested image
    :param converter: The converter to be used for the image ingestion,
        when None the default TIFF converter is used. Available converters
        are one of the ("tiff", "zarr", "osd").
    :param output_ext: extension for the output images in tiledb
    :param traverse: If true then traverse the src paths recursively
        to find images to convert in
        depths > 1. Default: (False) Check only in depth 1.
    """

    logger = get_logger_wrapper(verbose)
    max_workers = None if num_batches else 20  # Default picked heuristically.

    def build_io_uris_ingestion(
        source: Sequence[str],
        output: Sequence[str],
        output_ext: str,
        supported_exts: Tuple[str],
        traverse: bool,
        logger: logging.Logger,
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

        def create_output_path(input_file: str, output: str) -> str:
            # Check if output is dir
            if output.endswith("/"):
                filename = os.path.splitext(os.path.basename(input_file))[0]
                output_filename = (
                    filename + f".{output_ext}" if output_ext else filename
                )
                return os.path.join(output, output_filename)
            else:
                # The output is considered a target file
                return output

        def iter_paths(source: Sequence[str], output: Sequence[str]) -> Iterator[Tuple]:
            if len(output) != 1:
                for s, o in zip(source, output):
                    logger.debug(f"Pair {s} and {o}")
                    yield s, create_output_path(s, o)
            else:
                for s in source:
                    if s.endswith("/"):
                        # Folder for exploration
                        contents = vfs.ls(s)
                        # [1:] till the SC-40049 is resolved this will restrict
                        if traverse:
                            filtered_contents = [
                                c
                                for c in contents
                                if not (
                                    # vfs.is_dir and vfs.is_file checks in vfs
                                    # for empty folder objects SC-40049
                                    vfs.is_dir(c)
                                    and vfs.is_file(c)
                                    and vfs.file_size(c) == 0
                                )
                            ]
                        else:
                            # Explore folders only at depth 1
                            filtered_contents = [
                                c for c in contents if not vfs.is_dir(c)
                            ]
                        yield from iter_paths(filtered_contents, output)
                    elif s.endswith(supported_exts):
                        logger.debug(f"Pair {s} and {output[0]}")
                        yield s, create_output_path(s, output[0])

        logger.debug(f"Create pairs between {source} and {output}")
        return tuple(iter_paths(source, output))

    def build_input_batches(
        source: Sequence[str],
        output: str,
        num_batches: int,
        out_ext: str,
        supported_exts: Tuple,
        *,
        traverse: bool,
        verbose: bool,
    ):
        logger = get_logger_wrapper(verbose)

        """Groups input URIs into batches."""
        uri_pairs = build_io_uris_ingestion(
            source, output, out_ext, supported_exts, traverse, logger
        )
        logger.debug(f"Input batches:{uri_pairs}")
        # If the user didn't specify a number of batches, run every import
        # as its own task.
        my_num_batches = num_batches or len(uri_pairs)
        # If they specified too many batches, don't create empty tasks.
        my_num_batches = min(len(uri_pairs), my_num_batches)
        logger.debug(f"Number of batches:{my_num_batches}")
        split_batches = [uri_pairs[n::my_num_batches] for n in range(my_num_batches)]
        logger.debug(f"Split batches:{split_batches}")
        return [uri_pairs[n::my_num_batches] for n in range(my_num_batches)]

    def ingest_tiff_udf(
        io_uris: Sequence[Tuple],
        config: Mapping[str, Any],
        verbose: bool,
        exclude_metadata: bool,
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

        converter = kwargs.get("converter", None)
        user_converter = Converters.OMETIFF
        if not converter or converter == "tiff":
            user_converter = Converters.OMETIFF
        elif converter == "zarr":
            user_converter = Converters.OMEZARR
        elif converter == "osd":
            user_converter = Converters.OSD

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
                        converter=user_converter,
                        exclude_metadata=exclude_metadata,
                        verbose=verbose,
                        **kwargs,
                    )


    # Default None the TIFF converter is used
    # The Converters Enum is defined in the tiledb-bioimg package
    # and this is why we needed to pass them through the UDF
    # without using them directly.
    if converter and converter not in _SUPPORTED_CONVERTERS:
        raise ValueError(
            f"The selected converter is not supported please \
                choose on of {_SUPPORTED_CONVERTERS}"
        )
    source = [source] if isinstance(source, str) else source
    output = [output] if isinstance(output, str) else output
    validate_io_paths(source, output)

    logger.debug("Ingesting files: %s", source)

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
        _SUPPORTED_EXTENSIONS,
        *args,
        traverse=traverse,
        verbose=verbose,
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
        exclude_metadata,
        threads,
        *args,
        name=f"{dag_name} ingestor ",
        expand_node_output=input_list_node,
        resources=DEFAULT_RESOURCES if resources is None else resources,
        image_name=DEFAULT_IMG_NAME,
        compressor=compressor_serial,
        converter=converter,
        **kwargs,
    )
    if compute:
        run_dag(graph, debug=verbose)
    return graph


def ingest_udf(*args: Any, **kwargs: Any) -> Dict[str, str]:
    """Ingestor wrapper function that can be used as a UDF."""
    grf = ingest(*args, **kwargs)
    return {"status": "started", "graph_id": str(grf.server_graph_uuid)}
