import enum
import logging
import subprocess
import sys
from collections import defaultdict
from math import ceil
from typing import Any, Mapping, Optional, Sequence, Union

import numpy as np

import tiledb
from tiledb.cloud import dag
from tiledb.cloud.utilities import Profiler
from tiledb.cloud.utilities import create_log_array
from tiledb.cloud.utilities import get_logger
from tiledb.cloud.utilities import read_file
from tiledb.cloud.utilities import run_dag
from tiledb.cloud.utilities import set_aws_context
from tiledb.cloud.utilities import write_log_event

# Testing hooks
local_ingest = False

# Array names
LOG_ARRAY = "log"
MANIFEST_ARRAY = "manifest"

# Default attributes to materialize
DEFAULT_ATTRIBUTES = ["fmt_GT"]

# Default values for ingestion parameters
MANIFEST_BATCH_SIZE = 100
MANIFEST_WORKERS = 20
VCF_BATCH_SIZE = 10
VCF_WORKERS = 40
VCF_THREADS = 8
VCF_HEADER_MB = 25  # memory per sample per thread

# Consolidation task resources
CONSOLIDATE_CPUS = 4
CONSOLIDATE_MEMORY_MB = 4096


class Contigs(enum.Enum):
    """
    The contigs to ingest.

    ALL = all contigs
    CHROMOSOMES = all human chromosomes
    OTHER = all contigs other than the human chromosomes
    ALL_DISABLE_MERGE = all contigs with merging disabled, for non-human datasets
    """

    ALL = enum.auto()
    CHROMOSOMES = enum.auto()
    OTHER = enum.auto()
    ALL_DISABLE_MERGE = enum.auto()


def setup(
    config: Optional[Mapping[str, Any]] = None,
    verbose: bool = False,
) -> logging.Logger:
    """
    Set the default TileDB context, OS environment variables for AWS,
    and return a logger instance.

    :param config: config dictionary, defaults to None
    :param verbose: verbose logging, defaults to False
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


def create_manifest(dataset_uri: str) -> None:
    """
    Create a manifest array in the dataset.

    :param dataset_uri: dataset URI
    """

    manifest_uri = f"{dataset_uri}/{MANIFEST_ARRAY}"

    int_fl = tiledb.FilterList(
        [
            tiledb.DoubleDeltaFilter(),
            tiledb.BitWidthReductionFilter(),
            tiledb.ZstdFilter(level=22),
        ]
    )
    ascii_fl = tiledb.FilterList([tiledb.ZstdFilter(level=22)])

    d0 = tiledb.Dim(name="sample_name", dtype="ascii", filters=ascii_fl)
    dom = tiledb.Domain(d0)

    attrs = [
        tiledb.Attr(name="status", dtype="ascii", filters=ascii_fl),
        tiledb.Attr(name="vcf_uri", dtype="ascii", filters=ascii_fl),
        tiledb.Attr(name="vcf_bytes", dtype=np.uint64, filters=int_fl),
        tiledb.Attr(name="index_uri", dtype="ascii", filters=ascii_fl),
        tiledb.Attr(name="index_bytes", dtype=np.uint64, filters=int_fl),
        tiledb.Attr(name="records", dtype=np.uint64, filters=int_fl),
    ]

    schema = tiledb.ArraySchema(
        domain=dom,
        sparse=True,
        attrs=attrs,
        offsets_filters=int_fl,
        allows_duplicates=True,
    )

    schema.check()

    tiledb.Array.create(manifest_uri, schema)

    group = tiledb.Group(dataset_uri, "w")
    group.add(manifest_uri, name=MANIFEST_ARRAY)
    group.close()


# --------------------------------------------------------------------
# UDFs
# --------------------------------------------------------------------


def create_dataset_udf(
    dataset_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    extra_attrs: Optional[Union[Sequence[str], str]] = None,
    vcf_attrs: Optional[str] = None,
    verbose: bool = False,
) -> str:
    """
    Create a TileDB-VCF dataset.

    :param dataset_uri: dataset URI
    :param config: config dictionary, defaults to None
    :param extra_attrs: INFO/FORMAT fields to materialize, defaults to None
    :param vcf_attrs: VCF with all INFO/FORMAT fields to materialize, defaults to None
    :param verbose: verbose logging, defaults to False
    :return: dataset URI
    """
    import tiledbvcf

    logger = setup(config, verbose)
    logger.debug("tiledbvcf=%s", tiledbvcf.version)

    # Check if the dataset already exists
    if tiledb.object_type(dataset_uri) != "group":
        logger.info("Creating dataset: %r", dataset_uri)

        # vcf_attrs overrides extra_attrs
        if vcf_attrs:
            extra_attrs = None
        elif isinstance(extra_attrs, str):
            extra_attrs = [extra_attrs]

        ds = tiledbvcf.Dataset(
            dataset_uri, mode="w", cfg=tiledbvcf.ReadConfig(tiledb_config=config)
        )
        ds.create_dataset(
            enable_allele_count=True,
            enable_variant_stats=True,
            extra_attrs=extra_attrs,
            vcf_attrs=vcf_attrs,
        )

        # Create log array and add it to the dataset group
        log_uri = f"{dataset_uri}/{LOG_ARRAY}"
        create_log_array(log_uri)
        with tiledb.Group(dataset_uri, "w") as group:
            group.add(log_uri, name=LOG_ARRAY)

        write_log_event(log_uri, "create_dataset_udf", "create", data=dataset_uri)

        create_manifest(dataset_uri)
    else:
        logger.info("Using existing dataset: %r", dataset_uri)

    return dataset_uri


def read_uris_udf(
    dataset_uri: str,
    list_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    max_files: Optional[int] = None,
    verbose: bool = False,
) -> Sequence[str]:
    """
    Read a list of URIs from a URI.

    :param dataset_uri: dataset URI
    :param list_uri: URI of the list of URIs
    :param config: config dictionary, defaults to None
    :param max_files: maximum number of URIs returned, defaults to None
    :param verbose: verbose logging, defaults to False
    :return: list of URIs
    """

    logger = setup(config, verbose)

    with Profiler(group_uri=dataset_uri, group_member=LOG_ARRAY):
        result = []
        vfs = tiledb.VFS()
        for line in vfs.open(list_uri):
            result.append(line.decode().strip())
            if max_files and len(result) == max_files:
                break

        logger.info("Found %d VCF files.", len(result))

    return result


def find_uris_udf(
    dataset_uri: str,
    search_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    pattern: Optional[str] = None,
    ignore: Optional[str] = None,
    max_files: Optional[int] = None,
    verbose: bool = False,
) -> Sequence[str]:
    """
    Find URIs matching a pattern in a directory or S3 bucket using this command:

        find <search_uri> -name <pattern> | grep -Ev <ignore> -m <max_files>

    with an efficient implementation for S3.

    :param dataset_uri: dataset URI
    :param search_uri: URI to search for VCF files
    :param config: config dictionary, defaults to None
    :param pattern: pattern used in the search, defaults to None
    :param ignore: exclude pattern applied to the search results, defaults to None
    :param max_files: maximum number of URIs returned, defaults to None
    :param verbose: verbose logging, defaults to False
    :return: list of URIs
    """

    logger = setup(config, verbose)

    with Profiler(group_uri=dataset_uri, group_member=LOG_ARRAY) as prof:
        use_s3 = search_uri.startswith("s3://")
        # Run command to find URIs matching the pattern
        if use_s3:
            cmd = [
                "aws",
                "s3",
                "sync",
                "--dryrun",
                "--exclude",
                "*",
                "--include",
                pattern,
                search_uri,
                ".",
            ]
        else:
            cmd = ["find", search_uri, "-name", pattern]

        logger.debug(cmd)
        p1 = subprocess.Popen(
            cmd,
            text=True,
            stdout=subprocess.PIPE,
        )

        # Optionally ignore URIs and limit the number returned
        if ignore:
            cmd = ["grep", "-Ev", ignore]
        else:
            cmd = ["grep", "."]
        if max_files:
            cmd.extend(["-m", str(max_files)])

        logger.debug(cmd)
        p2 = subprocess.Popen(
            cmd,
            text=True,
            stdin=p1.stdout,
            stdout=subprocess.PIPE,
            stderr=sys.stdout,
        )

        # Wait for p2 to finish, then kill p1
        res_stdout = p2.communicate()[0]
        p1.kill()

        # Build list of URIs from command output.
        # Example line from s3:
        # (dryrun) download: s3://1000genomes-dragen-v3.7.6/foo to foo
        result = []
        if res_stdout:
            for line in res_stdout.splitlines():
                line = line.split()[2] if use_s3 else line
                result.append(line)

        logger.info("Found %d VCF files.", len(result))
        prof.write("count", len(result))

    return result


def filter_uris_udf(
    dataset_uri: str,
    sample_uris: Sequence[str],
    *,
    config: Optional[Mapping[str, Any]] = None,
    verbose: bool = False,
) -> Sequence[str]:
    """
    Return URIs from `sample_uris` that are not in the manifest.

    :param dataset_uri: dataset URI
    :param sample_uris: sample URIs
    :param config: config dictionary, defaults to None
    :param verbose: verbose logging, defaults to False
    :return: filtered sample URIs
    """

    logger = setup(config, verbose)

    with Profiler(group_uri=dataset_uri, group_member=LOG_ARRAY) as prof:
        # Read all sample URIs in the manifest
        group = tiledb.Group(dataset_uri)
        manifest_uri = group[MANIFEST_ARRAY].uri
        with tiledb.open(manifest_uri) as A:
            manifest_df = A.df[:]

        # Find URIs that are not in the manifest
        sample_uris_set = set(sample_uris)
        manifest_uris = set(manifest_df.vcf_uri)
        result = sorted(list(sample_uris_set.difference(manifest_uris)))

        logger.info("%d URIs in the manifest.", len(manifest_uris))
        logger.info("%d new URIs.", len(result))
        prof.write("count", len(result))

    return result


def filter_samples_udf(
    dataset_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    verbose: bool = False,
) -> Sequence[str]:
    """
    Return URIs for samples not already in the dataset.

    :param dataset_uri: dataset URI
    :param config: config dictionary, defaults to None
    :param verbose: verbose logging, defaults to False
    :return: sample URIs
    """
    import tiledbvcf

    logger = setup(config, verbose)
    logger.debug("tiledbvcf=%s", tiledbvcf.version)

    with Profiler(group_uri=dataset_uri, group_member=LOG_ARRAY) as prof:
        # Read existing samples in VCF dataset
        ds = tiledbvcf.Dataset(
            dataset_uri,
            cfg=tiledbvcf.ReadConfig(tiledb_config=config),
        )
        existing_samples = set(ds.samples())

        # Read all samples in the manifest with status == "ok"
        group = tiledb.Group(dataset_uri)
        manifest_uri = group[MANIFEST_ARRAY].uri

        with tiledb.open(manifest_uri) as A:
            manifest_df = A.query(cond="status == 'ok'").df[:]

        # Sort manifest by sample_name
        manifest_df = manifest_df.sort_values(by=["sample_name"])

        # Find samples that have not already been ingested
        manifest_samples = set(manifest_df.sample_name)
        new_samples = manifest_samples.difference(existing_samples)
        manifest_df = manifest_df[manifest_df.sample_name.isin(new_samples)]
        result = manifest_df.vcf_uri.to_list()

        logger.info("%d samples in the manifest.", len(manifest_samples))
        logger.info("%d samples already ingested.", len(existing_samples))
        logger.info("%d new samples to ingest.", len(result))
        prof.write("count", len(result))

    return result


def ingest_manifest_udf(
    dataset_uri: str,
    sample_uris: Sequence[str],
    *,
    config: Optional[Mapping[str, Any]] = None,
    id: str = "manifest",
    verbose: bool = False,
) -> None:
    """
    Ingest sample URIs into the manifest array.

    :param dataset_uri: dataset URI
    :param sample_uris: sample URIs
    :param config: config dictionary, defaults to None
    :param id: profiler event id, defaults to "manifest"
    :param verbose: verbose logging, defaults to False
    """

    setup(config, verbose)

    with Profiler(group_uri=dataset_uri, group_member=LOG_ARRAY, id=id):
        group = tiledb.Group(dataset_uri)
        manifest_uri = group[MANIFEST_ARRAY].uri

        vfs = tiledb.VFS()

        def file_size(uri: str) -> int:
            try:
                return vfs.file_size(uri)
            except Exception:
                return 0

        def find_index(vcf: str) -> str:
            for ext in ["tbi", "csi"]:
                index = f"{vcf}.{ext}"
                if vfs.is_file(index):
                    return index
            return ""

        def get_sample_name(vcf: str) -> str:
            # TODO: use this when bcftools works with S3
            if False:
                sample = subprocess.run(
                    ["bcftools", "query", "-l", vcf],
                    capture_output=True,
                    text=True,
                ).stdout.strip()

            else:
                aws_process = subprocess.Popen(
                    ["aws", "s3", "cp", "--quiet", vcf_uri, "-"],
                    stdout=subprocess.PIPE,
                    stderr=sys.stdout,
                )

                bcftools_process = subprocess.Popen(
                    ["bcftools", "query", "-l"],
                    stdin=aws_process.stdout,
                    stdout=subprocess.PIPE,
                    stderr=sys.stdout,
                    text=True,
                )

                sample = bcftools_process.communicate()[0].strip()
                aws_process.kill()

            return sample

        def get_records(vcf: str) -> int:
            # TODO: remove when bcftools index -n works with S3
            return 0

            cmd = ["bcftools", "index", "-n", vcf]
            res = subprocess.run(cmd, capture_output=True, text=True)
            # If there is an error, this means there was a problem reading the
            # index file or the index file is an old format that does not
            # contain the required metadata. In either case, return 0 to
            # indicate a problem with the index that needs to be addressed
            # before ingesting the sample.
            if res.stderr:
                print(res.stderr)
                return 0
            records = int(res.stdout)

            return records

        with tiledb.open(manifest_uri, "w") as A:
            keys = []
            values = defaultdict(list)

            for vcf_uri in sample_uris:
                status = "ok"

                # Handle sample name errors
                sample_name = get_sample_name(vcf_uri)
                if not sample_name:
                    status = "missing sample name"
                elif len(sample_name.split()) > 1:
                    status = "multiple samples"
                elif sample_name in keys:
                    status = "duplicate sample name"

                # Handle index errors
                index_uri = find_index(vcf_uri)
                if not index_uri:
                    status = "" if status == "ok" else status + ","
                    status += "missing index"

                records = get_records(vcf_uri)

                # TODO: remove False when bcftools index -n works with S3
                if False and records == 0:
                    status = "old index format"

                keys.append(sample_name)
                values["status"].append(status)
                values["vcf_uri"].append(vcf_uri)
                values["vcf_bytes"].append(str(file_size(vcf_uri)))
                values["index_uri"].append(index_uri)
                values["index_bytes"].append(str(file_size(index_uri)))
                values["records"].append(str(records))

            # Write to TileDB array
            A[keys] = dict(values)


def ingest_samples_udf(
    dataset_uri: str,
    sample_uris: Sequence[str],
    *,
    config: Optional[Mapping[str, Any]] = None,
    threads: int,
    memory_mb: int,
    sample_batch_size: int,
    contig_mode: str = "all",
    contigs_to_keep_separate: Optional[Sequence[str]] = None,
    contig_fragment_merging: bool = True,
    resume: bool = False,
    id: str = "samples",
    verbose: bool = False,
    trace_id: Optional[str] = None,
) -> None:
    """
    Ingest samples into the dataset.

    :param dataset_uri: dataset URI
    :param sample_uris: sample URIs
    :param threads: number of threads to use for ingestion
    :param memory_mb: memory to use for ingestion in MiB
    :param sample_batch_size: sample batch size to use for ingestion
    :param config: config dictionary, defaults to None
    :param contig_mode: ingestion mode, defaults to "all"
    :param contigs_to_keep_separate: list of contigs to keep separate, defaults to None
    :param contig_fragment_merging: enable contig fragment merging, defaults to True
    :param resume: enable resume ingestion mode, defaults to False
    :param id: profiler event id, defaults to "samples"
    :param verbose: verbose logging, defaults to False
    :param trace_id: trace ID for logging, defaults to None
    """
    import tiledbvcf

    logger = setup(config, verbose)
    logger.debug("tiledbvcf=%s", tiledbvcf.version)

    trace = trace_id == id

    with Profiler(
        group_uri=dataset_uri, group_member=LOG_ARRAY, id=id, trace=trace
    ) as prof:
        prof.write("uris", ",".join(sample_uris))

        level = "debug" if verbose else "info"
        tiledbvcf.config_logging(level, "ingest.log")
        ds = tiledbvcf.Dataset(
            uri=dataset_uri, mode="w", cfg=tiledbvcf.ReadConfig(tiledb_config=config)
        )
        ds.ingest_samples(
            sample_uris=sample_uris,
            sample_batch_size=sample_batch_size,
            threads=threads,
            total_memory_budget_mb=memory_mb,
            contig_mode=contig_mode,
            contigs_to_keep_separate=contigs_to_keep_separate,
            contig_fragment_merging=contig_fragment_merging,
            resume=resume,
        )

        prof.write("log", read_file("ingest.log"))


def consolidate_dataset_udf(
    dataset_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    exclude: Optional[Union[Sequence[str], str]] = MANIFEST_ARRAY,
    include: Optional[Union[Sequence[str], str]] = None,
    id: str = "consolidate",
    verbose: bool = False,
) -> None:
    """
    Consolidate arrays in the dataset.

    :param dataset_uri: dataset URI
    :param config: config dictionary, defaults to None
    :param exclude: group members to exclude, defaults to MANIFEST_ARRAY
    :param include: group members to include, defaults to None
    :param id: profiler event id, defaults to "consolidate"
    :param verbose: verbose logging, defaults to False
    """

    if exclude and include:
        raise ValueError("use exclude or include, not both")

    if isinstance(exclude, str):
        exclude = [exclude]
    if isinstance(include, str):
        include = [include]

    setup(config, verbose)

    with Profiler(group_uri=dataset_uri, group_member=LOG_ARRAY, id=id):
        group = tiledb.Group(dataset_uri)

        for member in group:
            uri = member.uri
            name = member.name

            # Skip excluded and non-included arrays
            if (exclude and name in exclude) or (include and name not in include):
                continue

            # NOTE: REST currently only supports fragment_meta, commits, metadata
            modes = ["commits", "fragment_meta", "array_meta"]

            # Consolidate fragments for selected arrays
            if name in [LOG_ARRAY, MANIFEST_ARRAY, "vcf_headers"]:
                modes += ["fragments"]

            for mode in modes:
                config = tiledb.Config({"sm.consolidation.mode": mode})
                try:
                    tiledb.consolidate(uri, config=config)
                except Exception as e:
                    print(e)

            for mode in modes:
                config = tiledb.Config({"sm.vacuum.mode": mode})
                try:
                    tiledb.vacuum(uri, config=config)
                except Exception as e:
                    print(e)


# --------------------------------------------------------------------
# DAGs
# --------------------------------------------------------------------


def ingest_manifest_dag(
    dataset_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    namespace: Optional[str] = None,
    search_uri: Optional[str] = None,
    pattern: Optional[str] = None,
    ignore: Optional[str] = None,
    sample_list_uri: Optional[str] = None,
    max_files: Optional[int] = None,
    batch_size: int = MANIFEST_BATCH_SIZE,
    workers: int = MANIFEST_WORKERS,
    extra_attrs: Optional[Union[Sequence[str], str]] = None,
    vcf_attrs: Optional[str] = None,
    verbose: bool = False,
) -> None:
    """
    Create a DAG to load the manifest array.

    :param dataset_uri: dataset URI
    :param config: config dictionary, defaults to None
    :param namespace: TileDB-Cloud namespace, defaults to None
    :param search_uri: URI to search for VCF files, defaults to None
    :param pattern: pattern to match when searching for VCF files, defaults to None
    :param ignore: pattern to ignore when searching for VCF files, defaults to None
    :param sample_list_uri: URI with a list of VCF URIs, defaults to None
    :param max_files: maximum number of URIs to ingest, defaults to None
    :param batch_size: manifest batch size, defaults to MANIFEST_BATCH_SIZE
    :param workers: maximum number of parallel workers, defaults to MANIFEST_WORKERS
    :param extra_attrs: INFO/FORMAT fields to materialize, defaults to None
    :param vcf_attrs: VCF with all INFO/FORMAT fields to materialize, defaults to None
    :param verbose: verbose logging, defaults to False
    """

    logger = get_logger()

    graph = dag.DAG(
        name="vcf-filter-uris",
        namespace=namespace,
        mode=dag.Mode.REALTIME,
    )
    submit = graph.submit_local if local_ingest else graph.submit

    dataset_uri = submit(
        create_dataset_udf,
        dataset_uri,
        config=config,
        extra_attrs=extra_attrs,
        vcf_attrs=vcf_attrs,
        verbose=verbose,
        name="Create VCF dataset ",
    )

    if sample_list_uri:
        sample_uris = submit(
            read_uris_udf,
            dataset_uri,
            sample_list_uri,
            config=config,
            max_files=max_files,
            verbose=verbose,
            name="Read VCF URIs ",
        )

    if search_uri:
        sample_uris = submit(
            find_uris_udf,
            dataset_uri,
            search_uri,
            config=config,
            pattern=pattern,
            ignore=ignore,
            max_files=max_files,
            verbose=verbose,
            name="Find VCF URIs ",
        )

    sample_uris = submit(
        filter_uris_udf,
        dataset_uri,
        sample_uris,
        config=config,
        verbose=verbose,
        name="Filter VCF URIs ",
    )

    run_dag(graph)

    sample_uris = sample_uris.result()

    if not sample_uris:
        logger.info("All samples in the manifest have been ingested.")
        return

    logger.info("Found %d new URIs.", len(sample_uris))

    graph = dag.DAG(
        name="vcf-ingest-manifest",
        namespace=namespace,
        mode=dag.Mode.REALTIME,
        max_workers=workers,
    )
    submit = graph.submit_local if local_ingest else graph.submit

    # Adjust batch size to ensure at least 20 samples per worker
    batch_size = min(batch_size, len(sample_uris) // workers)
    batch_size = max(batch_size, 20)

    num_partitions = ceil(len(sample_uris) / batch_size)
    num_consolidates = ceil(num_partitions / workers)

    # This loop creates a DAG with the following structure:
    # - Submit N ingest tasks in parallel, where N is `workers` or less if there
    #   are fewer batches
    # - Submit a consolidate task that runs when the previous N ingest tasks complete
    # - Repeat until all batches are ingested
    consolidate = None
    for i in range(num_partitions):
        if i % workers == 0:
            prev_consolidate = consolidate
            consolidate = submit(
                consolidate_dataset_udf,
                dataset_uri,
                config=config,
                exclude=None,
                include=[MANIFEST_ARRAY, LOG_ARRAY],
                id=f"manifest-consol-{i//workers}",
                verbose=verbose,
                name=f"Consolidate VCF Manifest {i//workers + 1}/{num_consolidates} ",
            )

        ingest = submit(
            ingest_manifest_udf,
            dataset_uri,
            sample_uris[i * batch_size : (i + 1) * batch_size],
            config=config,
            verbose=verbose,
            id=f"manifest-ingest-{i}",
            name=f"Ingest VCF Manifest {i+1}/{num_partitions} ",
        )
        if prev_consolidate:
            ingest.depends_on(prev_consolidate)

        if consolidate:
            consolidate.depends_on(ingest)

    logger.info("Populating the manifest.")
    run_dag(graph)


def ingest_samples_dag(
    dataset_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    namespace: Optional[str] = None,
    contigs: Optional[Union[Sequence[str], Contigs]] = Contigs.ALL,
    threads: int = VCF_THREADS,
    batch_size: int = VCF_BATCH_SIZE,
    workers: int = VCF_WORKERS,
    resume: bool = False,
    ingest_resources: Optional[Mapping[str, str]] = None,
    verbose: bool = False,
    trace_id: Optional[str] = None,
) -> dag.DAG:
    """
    Create a DAG to ingest samples into the dataset.

    :param dataset_uri: dataset URI
    :param config: config dictionary, defaults to None
    :param namespace: TileDB-Cloud namespace, defaults to None
    :param contigs: contig mode
        (Contigs.ALL | Contigs.CHROMOSOMES | Contigs.OTHER | Contigs.ALL_DISABLE_MERGE)
        or list of contigs to ingest, defaults to Contigs.ALL
    :param threads: number of threads to use per ingestion task, defaults to VCF_THREADS
    :param batch_size: sample batch size, defaults to VCF_BATCH_SIZE
    :param workers: maximum number of parallel workers, defaults to VCF_WORKERS
    :param resume: enable resume ingestion mode, defaults to False
    :param ingest_resources: manual override for ingest UDF resources, defaults to None
    :param verbose: verbose logging, defaults to False
    :param trace_id: trace ID for logging, defaults to None
    :return: sample ingestion DAG for visualization
    """

    logger = setup(config, verbose)

    graph = dag.DAG(
        name="vcf-filter-samples",
        namespace=namespace,
        mode=dag.Mode.REALTIME,
    )
    submit = graph.submit_local if local_ingest else graph.submit

    # Get list of sample uris that have not been ingested yet
    # TODO: handle second pass resume
    sample_uris = submit(
        filter_samples_udf,
        dataset_uri,
        config=config,
        verbose=verbose,
        name="Filter VCF samples",
    )

    run_dag(graph)

    sample_uris = sample_uris.result()

    if not sample_uris:
        logger.info("No new samples to ingest.")
        return

    logger.info("Ingesting %d samples.", len(sample_uris))

    contig_fragment_merging = True
    if type(contigs) == list:
        contig_mode = "separate"
        contigs_to_keep_separate = contigs
    else:
        contig_mode = "all"
        contigs_to_keep_separate = None
        if contigs == Contigs.CHROMOSOMES:
            contig_mode = "separate"
        elif contigs == Contigs.OTHER:
            contig_mode = "merged"
        elif contigs == Contigs.ALL_DISABLE_MERGE:
            contig_fragment_merging = False

    graph = dag.DAG(
        name="vcf-ingest-samples",
        namespace=namespace,
        mode=dag.Mode.REALTIME if local_ingest else dag.Mode.BATCH,
        max_workers=workers,
    )

    submit = graph.submit_local if local_ingest else graph.submit

    # Reduce batch size if there are fewer sample URIs
    batch_size = min(batch_size, len(sample_uris))

    num_partitions = ceil(len(sample_uris) / batch_size)
    num_consolidates = ceil(num_partitions / workers)

    # Calculate resources for ingest nodes
    # TODO: update vcf_memory_mb calculation to account for htslib header memory
    node_memory_mb = 2048 * threads
    vcf_memory_mb = 1024 * threads

    if ingest_resources is None:
        ingest_resources = {"cpu": f"{threads}", "memory": f"{node_memory_mb}Mi"}

    consolidate_resources = {
        "cpu": f"{CONSOLIDATE_CPUS}",
        "memory": f"{CONSOLIDATE_MEMORY_MB}Mi",
    }

    logger.debug("partitions=%d, consolidates=%d", num_partitions, num_consolidates)
    logger.debug("ingest_resources=%s", ingest_resources)
    logger.debug("consolidate_resources=%s", consolidate_resources)

    # This loop creates a DAG with the following structure:
    # - Submit N ingest tasks in parallel, where N is `workers` or less
    #   if there are fewer batches
    # - Submit a consolidate task that runs when the previous N ingest tasks complete
    # - Repeat until all batches are ingested
    consolidate = None
    for i in range(num_partitions):
        if i % workers == 0:
            prev_consolidate = consolidate
            consolidate = submit(
                consolidate_dataset_udf,
                dataset_uri,
                config=config,
                id=f"vcf-consol-{i//workers}",
                verbose=verbose,
                resources=consolidate_resources,
                name=f"Consolidate VCF {i//workers + 1}/{num_consolidates} ",
            )

        ingest = submit(
            ingest_samples_udf,
            dataset_uri,
            sample_uris[i * batch_size : (i + 1) * batch_size],
            config=config,
            threads=threads,
            memory_mb=vcf_memory_mb,
            sample_batch_size=batch_size,
            contig_mode=contig_mode,
            contigs_to_keep_separate=contigs_to_keep_separate,
            contig_fragment_merging=contig_fragment_merging,
            resume=resume,
            id=f"vcf-ingest-{i}",
            verbose=verbose,
            trace_id=trace_id,
            resources=ingest_resources,
            name=f"Ingest VCF {i+1}/{num_partitions} ",
        )

        if prev_consolidate:
            ingest.depends_on(prev_consolidate)

        if consolidate:
            consolidate.depends_on(ingest)

    run_dag(graph, wait=local_ingest)

    if not local_ingest:
        logger.info(
            "Batch ingestion submitted -"
            " https://cloud.tiledb.com/activity/taskgraphs/%s/%s",
            graph.namespace,
            graph.server_graph_uuid,
        )

    return graph


# --------------------------------------------------------------------
# User functions
# --------------------------------------------------------------------


def ingest(
    dataset_uri: str,
    *,
    config=None,
    namespace: Optional[str] = None,
    search_uri: Optional[str] = None,
    pattern: Optional[str] = None,
    ignore: Optional[str] = None,
    sample_list_uri: Optional[str] = None,
    max_files: Optional[int] = None,
    contigs: Optional[Union[Sequence[str], Contigs]] = Contigs.ALL,
    resume: bool = False,
    extra_attrs: Optional[Union[Sequence[str], str]] = DEFAULT_ATTRIBUTES,
    vcf_attrs: Optional[str] = None,
    manifest_batch_size: int = MANIFEST_BATCH_SIZE,
    manifest_workers: int = MANIFEST_WORKERS,
    vcf_batch_size: int = VCF_BATCH_SIZE,
    vcf_workers: int = VCF_WORKERS,
    vcf_threads: int = VCF_THREADS,
    ingest_resources: Optional[Mapping[str, str]] = None,
    verbose: bool = False,
    trace_id: Optional[str] = None,
) -> dag.DAG:
    """
    Ingest samples into a dataset.

    :param dataset_uri: dataset URI
    :param config: config dictionary, defaults to None
    :param namespace: TileDB-Cloud namespace, defaults to None
    :param search_uri: URI to search for VCF files, defaults to None
    :param pattern: pattern to match when searching for VCF files, defaults to None
    :param ignore: pattern to ignore when searching for VCF files, defaults to None
    :param sample_list_uri: URI with a list of VCF URIs, defaults to None
    :param max_files: maximum number of VCF URIs to read/find,
        defaults to None (no limit)
    :param contigs: contig mode
        (Contigs.ALL | Contigs.CHROMOSOMES | Contigs.OTHER | Contigs.ALL_DISABLE_MERGE)
        or list of contigs to ingest, defaults to Contigs.ALL
    :param resume: enable resume ingestion mode, defaults to False
    :param extra_attrs: INFO/FORMAT fields to materialize,
        defaults to `repr(DEFAULT_ATTRIBUTES)`
    :param vcf_attrs: VCF with all INFO/FORMAT fields to materialize,
        defaults to None
    :param manifest_batch_size: batch size for manifest ingestion,
        defaults to MANIFEST_BATCH_SIZE
    :param manifest_workers: number of workers for manifest ingestion,
        defaults to MANIFEST_WORKERS
    :param vcf_batch_size: batch size for VCF ingestion, defaults to VCF_BATCH_SIZE
    :param vcf_workers: number of workers for VCF ingestion, defaults to VCF_WORKERS
    :param vcf_threads: number of threads for VCF ingestion, defaults to VCF_THREADS
    :param ingest_resources: manual override for ingest UDF resources, defaults to None
    :param verbose: verbose logging, defaults to False
    :param trace_id: trace ID for logging, defaults to None
    :return: sample ingestion DAG for visualization
    """

    # Validate user input
    if not search_uri and not sample_list_uri:
        raise ValueError("Either `search_uri` or `sample_list_uri` must be provided.")

    if search_uri and sample_list_uri:
        raise ValueError("Cannot specify both `search_uri` and `sample_list_uri`.")

    if sample_list_uri and (pattern or ignore):
        raise ValueError("Cannot specify `pattern` or `ignore` with `sample_list_uri`.")

    logger = setup(config, verbose)
    logger.info("Ingesting VCF samples into %r", dataset_uri)

    # Add VCF URIs to the manifest
    ingest_manifest_dag(
        dataset_uri,
        config=config,
        namespace=namespace,
        search_uri=search_uri,
        pattern=pattern,
        ignore=ignore,
        sample_list_uri=sample_list_uri,
        max_files=max_files,
        batch_size=manifest_batch_size,
        workers=manifest_workers,
        extra_attrs=extra_attrs,
        vcf_attrs=vcf_attrs,
        verbose=verbose,
    )

    # Ingest VCFs using URIs in the manifest
    return ingest_samples_dag(
        dataset_uri,
        config=config,
        namespace=namespace,
        batch_size=vcf_batch_size,
        workers=vcf_workers,
        threads=vcf_threads,
        contigs=contigs,
        resume=resume,
        ingest_resources=ingest_resources,
        verbose=verbose,
        trace_id=trace_id,
    )
