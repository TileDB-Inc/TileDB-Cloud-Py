from typing import Any, Dict, Mapping, Optional, Sequence, Tuple, Union

import tiledb
from tiledb.cloud._common.utils import logger
from tiledb.cloud.bioimg.helpers import batch
from tiledb.cloud.bioimg.helpers import get_uris
from tiledb.cloud.bioimg.helpers import scale_calc
from tiledb.cloud.bioimg.helpers import serialize_filter

DEFAULT_RESOURCES = {"cpu": "8", "memory": "4Gi"}
DEFAULT_IMG_NAME = "3.9-imaging-dev"
DEFAULT_DAG_NAME = "bioimg-ingestion"


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
    """

    def ingest_tiff_udf(
        io_uris: Sequence[Tuple],
        config: Mapping[str, Any],
        *args: Any,
        **kwargs,
    ):
        """Internal udf that ingests server side batch of bioimaging files
        into tiledb arrays using tiledb-bioimg API

        :param io_uris: Pairs of tiff input - output tdb uris
        :param config: dict configuration to pass on tiledb.VFS
        """

        from tiledb import filter
        from tiledb.bioimg.converters.ome_tiff import OMETiffConverter

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

        conf = tiledb.Config(params=config)
        vfs = tiledb.VFS(config=conf)

        with tiledb.scope_ctx(ctx_or_config=conf):
            for input, output in io_uris:
                with vfs.open(input) as src:
                    OMETiffConverter.to_tiledb(src, output, **kwargs)

    if isinstance(source, str):
        # Handle only lists
        source = [source]

    # Get the list of all BioImg samples input/out
    samples = get_uris(source, output, config, "tdb")
    batch_size, max_workers = scale_calc(samples, num_batches)

    # Build the task graph
    dag_name = taskgraph_name or DEFAULT_DAG_NAME
    task_prefix = f"{dag_name} - Task"

    logger.info("Building graph")
    graph = tiledb.cloud.dag.DAG(
        name=dag_name,
        mode=tiledb.cloud.dag.Mode.BATCH,
        max_workers=max_workers,
        namespace=namespace,
    )

    # serialize udf arguments
    compressor = kwargs.pop("compressor", None)
    compressor_serial = serialize_filter(compressor) if compressor else None

    for i, work in enumerate(batch(samples, batch_size)):
        logger.info(f"Adding batch {i}")
        graph.submit(
            ingest_tiff_udf,
            work,
            config,
            threads,
            *args,
            name=f"{task_prefix} - {i}/{num_batches}",
            mode=tiledb.cloud.dag.Mode.BATCH,
            resources=DEFAULT_RESOURCES if resources is None else resources,
            image_name=DEFAULT_IMG_NAME,
            compressor=compressor_serial,
            **kwargs,
        )

    if compute:
        graph.compute()
    return graph


def ingest_udf(*args: Any, **kwargs: Any) -> Dict[str, str]:
    """Ingestor wrapper function that can be used as a UDF."""
    grf = ingest(*args, **kwargs)
    return {"status": "started", "graph_id": str(grf.server_graph_uuid)}
