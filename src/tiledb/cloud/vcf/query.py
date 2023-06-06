#!/usr/bin/env python

import logging
from math import ceil
from typing import Any, Callable, List, Mapping, Optional, Sequence, Tuple, Union

import pyarrow as pa

import tiledb.cloud
from tiledb.cloud.utilities import Profiler
from tiledb.cloud.utilities import get_logger
from tiledb.cloud.utilities import max_memory_usage
from tiledb.cloud.utilities import run_dag
from tiledb.cloud.utilities import set_aws_context

DEFAULT_ATTRS = [
    "sample_name",
    "contig",
    "pos_start",
    "alleles",
    "fmt_GT",
]

MAX_WORKERS = 40
MAX_SAMPLE_BATCH_SIZE = 500
MIN_SAMPLE_BATCH_SIZE = 20


def setup(
    config: Optional[Mapping[str, Any]] = None,
    verbose: bool = False,
) -> logging.Logger:
    """
    Set the default TileDB context, OS environment variables for AWS,
    and return a logger instance.

    :param config: config dictionary, defaults to None
    :return: logger instance
    """

    try:
        tiledb.default_ctx(config)
    except tiledb.TileDBError:
        # Ignore error if the default context was already set
        pass

    set_aws_context(config)

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


def vcf_query_udf(
    dataset_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    attrs: Optional[Union[Sequence[str], str]] = None,
    regions: Optional[Union[Sequence[str], str]] = None,
    bed_file: Optional[str] = None,
    samples: Optional[Union[Sequence[str], str]] = None,
    region_partition: Optional[Tuple[int, int]] = None,
    sample_partition: Optional[Tuple[int, int]] = None,
    memory_budget_mb: int = 1024,
    af_filter: Optional[str] = None,
    transform_result: Optional[Callable[[pa.Table], pa.Table]] = None,
    log_uri: Optional[str] = None,
    log_id: str = "query",
    verbose: bool = False,
) -> pa.table:
    """
    Run a query on a TileDB-VCF dataset.

    :param dataset_uri: dataset URI
    :param config: config dictionary, defaults to None
    :param attrs: attribute names to read, defaults to None
    :param regions: genomics regions to read, defaults to None
    :param bed_file: URI of a BED file containing genomics regions to read,
        defaults to None
    :param samples: sample names to read, defaults to None
    :param region_partition: region partition tuple (0-based indexed, num_partitions),
        defaults to None
    :param sample_partition: sample partition tuple (0-based indexed, num_partitions),
        defaults to None
    :param memory_budget_mb: VCF memory budget in MiB, defaults to 1024
    :param af_filter: allele frequency filter, defaults to None
    :param transform_result: function to apply to the result table;
        by default, does not transform the result
    :param log_uri: log array URI for profiling, defaults to None
    :param log_id: profiler event ID, defaults to "query"
    :param verbose: verbose logging, defaults to False
    :return: Arrow table containing the query results
    """
    import tiledbvcf

    # Adjust inputs
    if config is None:
        config = {}
    else:
        config = config.copy()

    if isinstance(attrs, str):
        attrs = [attrs]
    if isinstance(regions, str):
        regions = [regions]
    if isinstance(samples, str):
        samples = [samples]

    logger = setup(config, verbose)
    logger.debug("tiledbvcf=%s", tiledbvcf.version)

    config["rest.use_refactored_array_open"] = True

    # TODO: evaluate TileDB config options
    # Avoid issue loading tile offsets for a large number of fragments
    # config["sm.mem.reader.sparse_unordered_with_dups.ratio_array_data"] = 0.4
    # config["sm.mem.reader.sparse_unordered_with_dups.ratio_coords"] = 0.4
    # Alternative to above
    # config["sm.partial_tile_offsets_loading"] = True

    # Define TileDB-VCF config
    cfg = tiledbvcf.ReadConfig(
        region_partition=region_partition,
        sample_partition=sample_partition,
        memory_budget_mb=memory_budget_mb,
        tiledb_config=config,
    )

    if verbose:
        tiledbvcf.config_logging("debug")

    with Profiler(array_uri=log_uri, id=log_id) as prof:
        # Open TileDB-VCF Dataset
        ds = tiledbvcf.Dataset(dataset_uri, cfg=cfg)

        # Issue read query
        tables = [
            ds.read_arrow(
                attrs=attrs,
                regions=regions,
                bed_file=bed_file,
                samples=samples,
                set_af_filter=af_filter or "",
            )
        ]

        # Loop over any incomplete queries
        while not ds.read_completed():
            tables.append(ds.continue_read_arrow())

        # Combine any incomplete queries into a single arrow table
        table = pa.concat_tables(tables)

        prof.write("result", table.num_rows, table.nbytes)

    # Apply function to the result table
    if transform_result is not None:
        with Profiler(array_uri=log_uri, id=log_id + "-tr") as prof:
            table = transform_result(table)
            prof.write("result", table.num_rows, table.nbytes)

    memory_usage_gb = max_memory_usage() / (1 << 30)
    logger.debug("Max memory usage: %0.3f GiB", memory_usage_gb)
    logger.debug("Incomplete queries: %d", len(tables) - 1)
    logger.debug("Records read: %d", table.num_rows)
    logger.debug("Arrow table size: %0.3f MiB", table.nbytes / (1 << 20))

    return table


def concat_tables_udf(
    tables: List[pa.Table],
    *,
    config: Optional[Mapping[str, Any]] = None,
    log_uri: Optional[str] = None,
    verbose: bool = False,
) -> pa.table:
    """
    Concatenate a list of Arrow tables.

    :param tables: Arrow tables
    :param config: config dictionary, defaults to None
    :param log_uri: log URI for profiling, defaults to None
    :param verbose: verbose logging, defaults to False
    :return: concatenated Arrow table
    """

    logger = setup(config, verbose)

    with Profiler(array_uri=log_uri) as prof:
        table = pa.concat_tables(x for x in tables if x is not None and x.num_rows > 0)
        prof.write("result", table.num_rows, table.nbytes)

    memory_usage_gb = max_memory_usage() / (1 << 30)
    logger.debug("Max memory usage: %0.3f GiB", memory_usage_gb)
    logger.debug("Records read: %d", table.num_rows)
    logger.debug("Arrow table size: %0.3f MiB", table.nbytes / (1 << 20))

    return table


# --------------------------------------------------------------------
# DAGs
# --------------------------------------------------------------------


def build_read_dag(
    dataset_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    attrs: Optional[Union[Sequence[str], str]] = None,
    regions: Optional[Union[Sequence[str], str]] = None,
    bed_file: Optional[str] = None,
    num_region_partitions: int = 1,
    max_workers: int = MAX_WORKERS,
    samples: Optional[Union[Sequence[str], str]] = None,
    memory_budget_mb: int = 1024,
    af_filter: Optional[str] = None,
    transform_result: Optional[Callable[[pa.Table], pa.Table]] = None,
    log_uri: Optional[str] = None,
    namespace: Optional[str] = None,
    resource_class: Optional[str] = None,
    verbose: bool = False,
) -> Tuple[tiledb.cloud.dag.DAG, tiledb.cloud.dag.Node]:
    """
    Build the DAG for a distributed read on a TileDB-VCF dataset.

    :param dataset_uri: dataset URI
    :param config: config dictionary, defaults to None
    :param attrs: attribute names to read, defaults to None
    :param regions: genomics regions to read, defaults to None
    :param bed_file: URI of a BED file containing genomics regions to read,
        defaults to None
    :param num_region_partitions: number of region partitions, defaults to 1
    :param samples: sample names to read, defaults to None
    :param memory_budget_mb: VCF memory budget in MiB, defaults to 1024
    :param af_filter: allele frequency filter, defaults to None
    :param transform_result: function to apply to each partition;
        by default, does not transform the result
    :param log_uri: log array URI for profiling, defaults to None
    :param namespace: TileDB-Cloud namespace, defaults to None
    :param resource_class: TileDB-Cloud resource class for UDFs, defaults to None
    :param verbose: verbose logging, defaults to False
    :return: DAG and result Node
    """

    logger = setup(config, verbose)

    # Return an empty table if no samples or regions are specified.
    # This avoids reading the entire array by accident.
    if samples is None or (regions is None and bed_file is None):
        return pa.table({})

    attrs = attrs or DEFAULT_ATTRS

    # Set number of sample partitions
    num_samples = len(samples)
    sample_batch_size = ceil(num_samples * num_region_partitions / max_workers)
    sample_batch_size = min(sample_batch_size, MAX_SAMPLE_BATCH_SIZE)  # max batch size
    sample_batch_size = max(sample_batch_size, MIN_SAMPLE_BATCH_SIZE)  # min batch size
    num_sample_partitions = ceil(num_samples / sample_batch_size)

    logger.debug("num_samples=%d", num_samples)
    logger.debug("sample_batch_size=%d", sample_batch_size)
    logger.debug("num_sample_partitions=%d", num_sample_partitions)
    logger.debug("num_region_partitions=%d", num_region_partitions)

    dag = tiledb.cloud.dag.DAG(
        namespace=namespace,
        name="VCF-Distributed-Query",
        max_workers=max_workers,
    )

    tables = []
    for region in range(num_region_partitions):
        for sample in range(num_sample_partitions):
            tables.append(
                dag.submit(
                    vcf_query_udf,
                    dataset_uri,
                    config=config,
                    attrs=attrs,
                    regions=regions,
                    region_partition=(region, num_region_partitions),
                    samples=samples,
                    sample_partition=(sample, num_sample_partitions),
                    memory_budget_mb=memory_budget_mb,
                    af_filter=af_filter,
                    transform_result=transform_result,
                    log_uri=log_uri,
                    log_id=f"query-reg{region}-sam{sample}",
                    name=f"VCF Query - Region {region+1}/{num_region_partitions},"
                    f" Sample {sample+1}/{num_sample_partitions}",
                    resource_class=resource_class,
                    result_format=tiledb.cloud.UDFResultType.ARROW,
                )
            )

    if len(tables) > 1:
        table = dag.submit_local(
            concat_tables_udf,
            tables,
            config=config,
            log_uri=log_uri,
            name="Combine Results",
        )
    else:
        table = tables[0]

    logger.debug("tasks=%d", len(tables))

    return dag, table


def read(
    dataset_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    attrs: Optional[Union[Sequence[str], str]] = None,
    regions: Optional[Union[Sequence[str], str]] = None,
    bed_file: Optional[str] = None,
    num_region_partitions: int = 1,
    max_workers: int = MAX_WORKERS,
    samples: Optional[Union[Sequence[str], str]] = None,
    memory_budget_mb: int = 1024,
    af_filter: Optional[str] = None,
    transform_result: Optional[Callable[[pa.Table], pa.Table]] = None,
    log_uri: Optional[str] = None,
    namespace: Optional[str] = None,
    resource_class: Optional[str] = None,
    verbose: bool = False,
) -> pa.Table:
    """
    Run a distributed read on a TileDB-VCF dataset.

    :param dataset_uri: dataset URI
    :param config: config dictionary, defaults to None
    :param attrs: attribute names to read, defaults to None
    :param regions: genomics regions to read, defaults to None
    :param bed_file: URI of a BED file containing genomics regions to read,
        defaults to None
    :param num_region_partitions: number of region partitions, defaults to 1
    :param samples: sample names to read, defaults to None
    :param memory_budget_mb: VCF memory budget in MiB, defaults to 1024
    :param af_filter: allele frequency filter, defaults to None
    :param transform_result: function to apply to each partition;
        by default, does not transform the result
    :param log_uri: log array URI for profiling, defaults to None
    :param namespace: TileDB-Cloud namespace, defaults to None
    :param resource_class: TileDB-Cloud resource class for UDFs, defaults to None
    :param verbose: verbose logging, defaults to False
    :return: Arrow table containing the query results
    """

    dag, table = build_read_dag(
        dataset_uri,
        config=config,
        attrs=attrs,
        regions=regions,
        bed_file=bed_file,
        num_region_partitions=num_region_partitions,
        max_workers=max_workers,
        samples=samples,
        memory_budget_mb=memory_budget_mb,
        af_filter=af_filter,
        transform_result=transform_result,
        log_uri=log_uri,
        namespace=namespace,
        resource_class=resource_class,
        verbose=verbose,
    )

    run_dag(dag, debug=verbose)

    return table.result()
