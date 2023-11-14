from typing import Any, Dict, Mapping, Optional, Sequence, Tuple, Union

import tiledb
from tiledb.cloud._common.utils import logger
from tiledb.cloud.bioimg.helpers import batch
from tiledb.cloud.bioimg.helpers import get_uris
from tiledb.cloud.bioimg.helpers import scale_calc

DEFAULT_RESOURCES = {"cpu": "8", "memory": "4Gi"}
DEFAULT_IMG_NAME = "3.9-imaging-dev"
DEFAULT_DAG_NAME = "bioimg-exportation"


def export(
    source: Union[Sequence[str], str],
    output: str,
    config: Mapping[str, Any],
    *args: Any,
    taskgraph_name: Optional[str] = None,
    num_batches: Optional[int] = None,
    resources: Optional[Mapping[str, Any]] = None,
    compute: bool = True,
    namespace: Optional[str] = None,
    **kwargs,
) -> tiledb.cloud.dag.DAG:
    """The function exports microscopy images from TileDB arrays

    :param source: uri / iterable of uris of input files
    :param output: output dir for the exported tiledb arrays
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

    def export_tiff_udf(
        io_uris: Sequence[Tuple],
        config: Mapping[str, Any],
        *args: Any,
        **kwargs,
    ):
        """Internal udf that exports server side batch of tiledb arrays
        2Tiff biomedical images using tiledb-bioimg API

        :param io_uris: Pairs of tiff input - output tdb uris
        :param config: dict configuration to pass on tiledb.VFS
        """

        from tiledb.bioimg.converters.ome_tiff import OMETiffConverter

        conf = tiledb.Config(params=config)
        for input, output in io_uris:
            OMETiffConverter.from_tiledb(input, output, config=conf, **kwargs)

    if isinstance(source, str):
        # Handle only lists
        source = [source]

    # Get the list of all BioImg samples input/out
    samples = get_uris(source, output, config, "tiff")
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

    for i, work in enumerate(batch(samples, batch_size)):
        logger.info(f"Adding batch {i}")
        graph.submit(
            export_tiff_udf,
            work,
            config,
            *args,
            name=f"{task_prefix} - {i}",
            mode=tiledb.cloud.dag.Mode.BATCH,
            resources=DEFAULT_RESOURCES if resources is None else resources,
            image_name=DEFAULT_IMG_NAME,
            **kwargs,
        )

    if compute:
        graph.compute()
    return graph


def export_udf(*args: Any, **kwargs: Any) -> Dict[str, str]:
    """Exporter wrapper function that can be used as a UDF."""
    grf = export(*args, **kwargs)
    return {"status": "started", "graph_id": str(grf.server_graph_uuid)}
