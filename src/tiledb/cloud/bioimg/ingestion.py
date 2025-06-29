import logging
import warnings
from enum import Enum
from typing import Any, Callable, Iterator, Mapping, Optional, Sequence, Tuple, Union

import tiledb
from tiledb.cloud import dag
from tiledb.cloud.bioimg.helpers import serialize_filter
from tiledb.cloud.bioimg.helpers import validate_io_paths
from tiledb.cloud.dag.mode import Mode
from tiledb.cloud.rest_api.models import RetryStrategy
from tiledb.cloud.utilities import get_logger_wrapper
from tiledb.cloud.utilities._common import as_batch
from tiledb.cloud.utilities._common import run_dag

DEFAULT_RESOURCES = {"cpu": "8", "memory": "4Gi"}
DEFAULT_IMG_NAME = "3.9-imaging-dev"
DEFAULT_DAG_NAME = "bioimg-ingestion"
_SUPPORTED_EXTENSIONS = (".tiff", ".tif", ".svs", ".ndpi", ".png")
_SUPPORTED_CONVERTERS = ("tiff", "zarr", "osd", "png")


class ReaderType(Enum):
    PRODUCTION = "production"
    EXPERIMENTAL = "experimental"


def ingest(
    source: Union[Sequence[str], str],
    output: Union[Sequence[str], str],
    config: Mapping[str, Any],
    *args: Any,
    acn: str = "",
    taskgraph_name: Optional[str] = None,
    num_batches: Optional[int] = None,
    threads: Optional[int] = 0,
    resources: Optional[Mapping[str, Any]] = None,
    ingest_resources: Optional[Mapping[str, Any]] = None,
    compute: bool = True,
    register: bool = True,
    mode: Optional[Mode] = Mode.BATCH,
    namespace: Optional[str],
    verbose: bool = False,
    exclude_metadata: Optional[Union[bool, Callable[[str], str]]] = None,
    converter: Optional[str] = None,
    output_ext: str = "",
    tile_scale: int = 128,
    timeout: Optional[int] = 86400,
    **kwargs,
) -> tiledb.cloud.dag.DAG:
    """The function ingests microscopy images into TileDB arrays

    :param source: uri / iterable of uris of input files.
        If the uri points to a directory of files make sure it ends with a trailing '/'
    :param output: uri / iterable of uris of output files.
        If the uri points to a directory of files make sure it ends with a trailing '/'
    :param config: dict configuration to pass on tiledb.VFS for the source's resolution
    :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type)
    :param taskgraph_name: Optional name for taskgraph, defaults to None
    :param num_batches: Number of graph nodes to spawn.
        Performs it sequentially if default, defaults to 1
    :param threads: Number of threads for node side multiprocessing, defaults to 0
    :param resources: configuration for node specs e.g. {"cpu": "8", "memory": "4Gi"},
        defaults to None
    :param ingest_resources: configuration for node specs e.g.
        {"cpu": "8", "memory": "4Gi"}. This parameter is intended to be used with the
        as_batch() wrapper and with the TileDB UI ingest endpoint. It defaults to None
        and will be superseded by the resources parameter described above.
    :param compute: When True the DAG returned will be computed inside the function
    otherwise DAG will only be returned.
    :param register: When True the ingested images are also being registered under the
        namespace in which were ingested. Should be False when tiledb uris are given as
        destination paths, registration node is merged with the ingestion stage.
    :param mode: By default runs Mode.Batch
    :param namespace: The namespace where the DAG will run
    :param verbose: verbose logging, defaults to False
    :param exclude_metadata: An optional argument that specifies how to transform
        the original metadata. It can be one of the following:
        *   A callable (function, method, etc.) that takes an OME-XML string and returns
            it as a string, while removing some of the original metadata and excluding
            them from being ingested.
        *   A boolean value:
            *   ``True``: Indicates a specific built-in transformation should be applied
            *   ``False``: Indicates no transformation should be applied
        *   ``None``: Indicates no transformation should be applied (same as ``False``).
    :param converter: The converter to be used for the image ingestion,
        when None the default TIFF converter is used. Available converters
        are one of the ("tiff", "zarr", "osd").
    :param output_ext: extension for the output images in tiledb
    :param tile_scale: The scaling factor applied to each tile during I/O.
        Larger scale factors will result in less I/O operations.
    :param access_credentials_name: [TBDeprecated] Access Credentials Name (ACN)
        registered in TileDB Cloud (ARN type) if ``acn`` is not set.
    :param dest_config: dict configuration to pass on tiledb.VFS for the destination's
        resolution
    :param reader: The selected reader backend implementation either "experimental"
        or "production". Default["production"]
    :param timeout: Duration (sec) ingestion DAG allowed to execute before timeout.
        The default is 86400 seconds (24 hours).
    """

    logger = get_logger_wrapper(verbose)
    max_workers = None if num_batches else 20  # Default picked heuristically.

    # Demand for mutual exclusion of the two arguments and existence.
    access_credentials_name = kwargs.pop("access_credentials_name", None)
    if bool(acn) == bool(access_credentials_name):
        raise ValueError(
            "Ingestion graph requires either 'acn' or 'access_credentials_name'"
            " (deprecated), cannot decipher correct credential when both specified."
        )
    # Backwards compatibility: Assign when only access_credentials_name is set
    if not acn:
        acn = access_credentials_name
        warnings.warn(
            DeprecationWarning(
                "The 'access_credentials_name' parameter is about to be"
                "deprecated and will be removed in future versions."
                "Please use the 'acn' parameter instead."
            )
        )

    def build_io_uris_ingestion(
        source: Sequence[str],
        output: Sequence[str],
        output_ext: str,
        supported_exts: Tuple[str],
        logger: logging.Logger,
        config: Optional[Mapping[str, Any]] = None,
    ):
        """Match input uri/s with output destinations
        :param source: A sequence of paths or path to input
        :param output_dir: A path to the output directory
        """
        import os

        import tiledb

        ctx = tiledb.Ctx(config)
        vfs = tiledb.VFS(ctx=ctx)
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
                    logger.debug("Pair %s and %s", s, o)
                    yield s, create_output_path(s, o)
            else:
                logger.debug("Traverse source: %s", source)
                for s in source:
                    if s.endswith("/"):
                        # Folder for exploration
                        contents = vfs.ls(s)
                        # Explore folders only at depth 1
                        filtered_contents = [c for c in contents if not vfs.is_dir(c)]
                        yield from iter_paths(filtered_contents, output)
                    elif s.endswith(supported_exts):
                        logger.debug("Pair %s and %s", s, output[0])
                        yield s, create_output_path(s, output[0])

        logger.debug("Create pairs between %s and %s", source, output)
        return tuple(iter_paths(source, output))

    def build_input_batches(
        source: Sequence[str],
        output: Sequence[str],
        num_batches: int,
        out_ext: str,
        supported_exts: Tuple,
        *,
        verbose: bool,
        config: Optional[Mapping[str, Any]] = None,
    ):
        logger = get_logger_wrapper(verbose)

        """Groups input URIs into batches."""
        uri_pairs = build_io_uris_ingestion(
            source, output, out_ext, supported_exts, logger, config=config
        )
        logger.debug(f"Input batches:{uri_pairs}")
        # If the user didn't specify a number of batches, run every import
        # as its own task.
        logger.debug(f"The io pairs for ingestion: {uri_pairs}")
        my_num_batches = num_batches or len(uri_pairs)
        # If they specified too many batches, don't create empty tasks.
        my_num_batches = min(len(uri_pairs), my_num_batches)
        logger.debug(f"Number of batches:{my_num_batches}")
        split_batches = [uri_pairs[n::my_num_batches] for n in range(my_num_batches)]
        logger.debug(f"Split batches:{split_batches}")
        return split_batches

    def ingest_tiff_udf(
        io_uris: Sequence[Tuple],
        config: Mapping[str, Any],
        verbose: bool,
        exclude_metadata: bool,
        tile_scale: int,
        converter: str = "tiff",
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

        user_converter = {
            "zarr": Converters.OMEZARR,
            "osd": Converters.OSD,
            "png": Converters.PNG,
        }.get(converter, Converters.OMETIFF)

        experimental_reader = kwargs.pop("experimental_reader", False)

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

        for input, output in io_uris:
            from_bioimg(
                input,
                output,
                converter=user_converter,
                exclude_metadata=exclude_metadata,
                verbose=verbose,
                tile_scale=tile_scale,
                source_config=config,
                dest_config=kwargs.pop("dest_config", None),
                experimental_reader=experimental_reader,
                **kwargs,
            )

        return io_uris

    def register_dataset_udf(
        io_uris: Sequence[Tuple],
        *,
        acn: str,
        namespace: Optional[str] = None,
        config: Optional[Mapping[str, Any]] = None,
        verbose: bool = False,
        **kwargs,
    ) -> None:
        """
        Register the dataset on TileDB Cloud.
        The ingested assets are being registered with the register name matching
        the ingested filename of the data

        :param io_uris: Tuple of source and dest paths from ingestion UDF
        :param namespace: TileDB Cloud namespace, defaults to the user's
            default namespace
        :param config: config dictionary, defaults to None
        :param verbose: verbose logging, defaults to False
        """
        import os

        logger = get_logger_wrapper(verbose)

        namespace = namespace or tiledb.cloud.user_profile().default_namespace_charged
        # Default registration based on the output filename
        register_map = {}
        tiledb_uris = {}
        for _, output_path in io_uris:
            register_name = os.path.splitext(os.path.basename(output_path))[0]
            register_map[output_path] = register_name
            tiledb_uris[output_path] = f"tiledb://{namespace}/{register_name}"

        with tiledb.scope_ctx(config):
            for dataset_uri, tiledb_uri in tiledb_uris.items():
                found = False
                try:
                    object_type = tiledb.object_type(tiledb_uri)
                    logger.debug("Object type of %s : %s", tiledb_uri, object_type)
                    if object_type == "group":
                        found = True
                    elif object_type is not None:
                        raise ValueError(
                            f"Another object is already registered at '{tiledb_uri}'."
                        )

                except Exception:
                    # tiledb.object_type raises an exception
                    # if the namespace does not exist
                    logger.error(
                        "Error checking if %r is registered. Bad namespace?", tiledb_uri
                    )
                    raise

                if found:
                    logger.info("Dataset already registered at %r.", tiledb_uri)
                else:
                    logger.info(
                        "Registering dataset %s at %s with name %s",
                        dataset_uri,
                        tiledb_uri,
                        register_map[dataset_uri],
                    )
                    tiledb.cloud.groups.register(
                        dataset_uri,
                        name=register_map[dataset_uri],
                        namespace=namespace,
                        credentials_name=acn,
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
    validate_io_paths(source, output, for_registration=register)

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
        deadline=timeout,
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
        verbose=verbose,
        config=config,
        access_credentials_name=acn,
        name=f"{dag_name} input collector",
        result_format="json",
    )

    # serialize udf arguments
    compressor = kwargs.pop("compressor", None)

    # Get either the new experimental or default reader
    reader = kwargs.pop("reader", ReaderType.PRODUCTION.value)
    experimental_reader = reader == ReaderType.EXPERIMENTAL.value

    logger.debug("Compressor: %r", compressor)
    compressor_serial = serialize_filter(compressor) if compressor else None

    ingest_list_node = graph.submit(
        ingest_tiff_udf,
        input_list_node,
        config,
        verbose,
        exclude_metadata,
        tile_scale,
        converter,
        *args,
        name=f"{dag_name} ingestor ",
        expand_node_output=input_list_node,
        resources=resources or ingest_resources or DEFAULT_RESOURCES,
        image_name=DEFAULT_IMG_NAME,
        max_workers=threads,
        compressor=compressor_serial,
        experimental_reader=experimental_reader,
        access_credentials_name=acn,
        **kwargs,
    )

    if register:
        graph.submit(
            register_dataset_udf,
            ingest_list_node,
            config=config,
            verbose=verbose,
            acn=acn,
            namespace=namespace,
            name=f"{dag_name} registrator ",
            expand_node_output=ingest_list_node,
            access_credentials_name=acn,
            **kwargs,
        )
    if compute:
        run_dag(graph, debug=verbose)
    else:
        return graph


# Wrapper function for batch VCF ingestion
ingest_batch = as_batch(ingest)
