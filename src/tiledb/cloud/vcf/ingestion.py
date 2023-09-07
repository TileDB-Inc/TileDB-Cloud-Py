import enum
import logging
import subprocess
import sys
from collections import defaultdict
from fnmatch import fnmatch
from functools import partial
from math import ceil
from multiprocessing.pool import ThreadPool
from os.path import basename
from typing import Any, Mapping, Optional, Sequence, Tuple, Union

import numpy as np

import tiledb
from tiledb.cloud import dag
from tiledb.cloud.rest_api.models import RetryStrategy
from tiledb.cloud.utilities import Profiler
from tiledb.cloud.utilities import create_log_array
from tiledb.cloud.utilities import get_logger
from tiledb.cloud.utilities import read_file
from tiledb.cloud.utilities import run_dag
from tiledb.cloud.utilities import set_aws_context
from tiledb.cloud.utilities import write_log_event
from tiledb.cloud.vcf.utils import create_index_file
from tiledb.cloud.vcf.utils import find_index
from tiledb.cloud.vcf.utils import get_record_count
from tiledb.cloud.vcf.utils import get_sample_name

# Testing hooks
local_ingest = False

# Array names
LOG_ARRAY = "log"
MANIFEST_ARRAY = "manifest"

# Default attributes to materialize
DEFAULT_ATTRIBUTES = ["fmt_GT"]

# Default values for ingestion parameters
MANIFEST_BATCH_SIZE = 200
MANIFEST_WORKERS = 40
VCF_BATCH_SIZE = 10
VCF_WORKERS = 40
VCF_THREADS = 8
VCF_HEADER_MB = 50  # memory per sample per thread
TARGET_FRAGMENT_BYTES = 1 << 30  # 1 GiB
CONSOLIDATION_BUFFER_SIZE = 1 << 30  # 1 GiB
CONSOLIDATION_THREADS = 8

# Consolidation task resources
CONSOLIDATE_RESOURCES = {
    "cpu": "4",
    "memory": "16Gi",
}

# Consolidation fragment task resources
CONSOLIDATE_FRAGMENT_RESOURCES = {
    "cpu": "8",
    "memory": "32Gi",
}

# Load manifest task resources
MANIFEST_RESOURCES = {
    "cpu": "1",
    "memory": "1Gi",
}


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


def get_logger_wrapper(
    verbose: bool = False,
) -> logging.Logger:
    """
    Get a logger instance and log version information.

    :param verbose: verbose logging, defaults to False
    :return: logger instance
    """

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
    anchor_gap: Optional[int] = None,
    compression_level: Optional[int] = None,
    verbose: bool = False,
) -> str:
    """
    Create a TileDB-VCF dataset.

    :param dataset_uri: dataset URI
    :param config: config dictionary, defaults to None
    :param extra_attrs: INFO/FORMAT fields to materialize, defaults to None
    :param vcf_attrs: VCF with all INFO/FORMAT fields to materialize, defaults to None
    :param anchor_gap: anchor gap for VCF dataset, defaults to None
    :param compression_level: zstd compression level for the VCF dataset,
        defaults to None (uses the default level in TileDB-VCF)
    :param verbose: verbose logging, defaults to False
    :return: dataset URI
    """
    import tiledbvcf

    logger = get_logger_wrapper(verbose)
    logger.debug("tiledbvcf=%s", tiledbvcf.version)

    # Check if the dataset already exists
    with tiledb.scope_ctx(config):
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
                anchor_gap=anchor_gap,
                compression_level=compression_level,
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


def register_dataset_udf(
    dataset_uri: str,
    *,
    register_name: str,
    namespace: Optional[str] = None,
    config: Optional[Mapping[str, Any]] = None,
    verbose: bool = False,
) -> None:
    """
    Register the dataset on TileDB Cloud.

    :param dataset_uri: dataset URI
    :param register_name: name to register the dataset with on TileDB Cloud
    :param namespace: TileDB Cloud namespace, defaults to the user's default namespace
    :param config: config dictionary, defaults to None
    :param verbose: verbose logging, defaults to False
    """

    logger = get_logger_wrapper(verbose)

    namespace = namespace or tiledb.cloud.user_profile().default_namespace_charged
    tiledb_uri = f"tiledb://{namespace}/{register_name}"

    with tiledb.scope_ctx(config):
        found = False
        try:
            object_type = tiledb.object_type(tiledb_uri)
            if object_type == "group":
                found = True
            elif object_type is not None:
                raise ValueError(
                    f"Another object is already registered at '{tiledb_uri}'."
                )

        except Exception:
            # tiledb.object_type raises an exception if the namespace does not exist
            logger.error(
                "Error checking if %r is registered. Bad namespace?", tiledb_uri
            )
            raise

        if found:
            logger.info("Dataset already registered at %r.", tiledb_uri)
        else:
            logger.info("Registering dataset at %r.", tiledb_uri)
            tiledb.cloud.groups.register(
                dataset_uri,
                name=register_name,
                namespace=namespace,
            )


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

    logger = get_logger_wrapper(verbose)

    with tiledb.scope_ctx(config):
        with Profiler(group_uri=dataset_uri, group_member=LOG_ARRAY):
            result = []
            vfs = tiledb.VFS()
            for line in vfs.open(list_uri):
                result.append(line.decode().strip())
                if max_files and len(result) == max_files:
                    break

            logger.info("Found %d VCF files.", len(result))

        return result


def read_metadata_uris_udf(
    dataset_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    metadata_uri: str,
    metadata_attr: str = "uri",
    max_files: Optional[int] = None,
    verbose: bool = False,
) -> Sequence[str]:
    """
    Read a list of URIs from a TileDB array. The URIs will be read from the
    attribute specified in the `metadata_attr` argument.

    :param dataset_uri: dataset URI
    :param config: TileDB config, defaults to None
    :param metadata_uri: metadata array URI
    :param metadata_attr: name of metadata attribute containing URIs, defaults to "uri"
    :param max_files: maximum number of URIs returned, defaults to None
    :param verbose: verbose logging, defaults to False
    :return: list of URIs
    """
    logger = get_logger_wrapper(verbose)

    with tiledb.scope_ctx(config):
        with Profiler(group_uri=dataset_uri, group_member=LOG_ARRAY) as prof:
            with tiledb.open(metadata_uri) as A:
                df = A.query(dims=[], attrs=[metadata_attr]).df[:]
            results = df[metadata_attr].to_list()

            if max_files:
                results = results[:max_files]

            logger.info("Read %d VCF URIs from the metadata array.", len(results))
            prof.write("count", len(results))

        return results


def find_uris_udf(
    dataset_uri: str,
    search_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    include: Optional[str] = None,
    exclude: Optional[str] = None,
    max_files: Optional[int] = None,
    verbose: bool = False,
) -> Sequence[str]:
    """
    Find URIs matching a pattern in the `search_uri` path.

    `include` and `exclude` patterns are Unix shell style (see fnmatch module).

    :param dataset_uri: dataset URI
    :param search_uri: URI to search for VCF files
    :param config: config dictionary, defaults to None
    :param include: include pattern used in the search, defaults to None
    :param exclude: exclude pattern applied to the search results, defaults to None
    :param max_files: maximum number of URIs returned, defaults to None
    :param verbose: verbose logging, defaults to False
    :return: list of URIs
    """

    logger = get_logger_wrapper(verbose)

    with tiledb.scope_ctx(config):
        with Profiler(group_uri=dataset_uri, group_member=LOG_ARRAY) as prof:
            vfs = tiledb.VFS(config=config, ctx=tiledb.Ctx(config))

            def find(
                uri: str,
                *,
                include: Optional[str] = None,
                exclude: Optional[str] = None,
                max_count: Optional[int] = None,
            ):
                logger.debug("Searching %r", uri)
                listing = vfs.ls(uri)
                logger.debug("  %d items", len(listing))

                results = []
                for f in listing:
                    # Avoid infinite recursion
                    if f == uri:
                        continue

                    if vfs.is_dir(f):
                        next_max_count = (
                            max_count - len(results) if max_count is not None else None
                        )
                        results += find(
                            f,
                            include=include,
                            exclude=exclude,
                            max_count=next_max_count,
                        )

                    else:
                        # Skip files that do not match the include pattern or match
                        # the exclude pattern.
                        if include and not fnmatch(f, include):
                            continue
                        if exclude and fnmatch(f, exclude):
                            continue

                        results.append(f)
                        logger.debug("  found %r", f)

                    # Stop if we have found max_count files
                    if max_count is not None and len(results) >= max_count:
                        results = results[:max_count]
                        break

                return results

            # Add one trailing slash to search_uri
            search_uri = search_uri.rstrip("/") + "/"

            results = find(
                search_uri, include=include, exclude=exclude, max_count=max_files
            )

            logger.info("Found %d VCF files.", len(results))
            prof.write("count", len(results))

            return results


def find_uris_aws_udf(
    dataset_uri: str,
    search_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    include: Optional[str] = None,
    exclude: Optional[str] = None,
    max_files: Optional[int] = None,
    verbose: bool = False,
) -> Sequence[str]:
    """
    Find URIs matching a pattern in the `search_uri` path with an efficient
    implementation for S3.

    `include` and `exclude` patterns are Unix shell style (see fnmatch module).

    :param dataset_uri: dataset URI
    :param search_uri: URI to search for VCF files
    :param config: config dictionary, defaults to None
    :param include: include pattern used in the search, defaults to None
    :param exclude: exclude pattern applied to the search results, defaults to None
    :param max_files: maximum number of URIs returned, defaults to None
    :param verbose: verbose logging, defaults to False
    :return: list of URIs
    """

    set_aws_context(config)

    logger = get_logger_wrapper(verbose)

    with tiledb.scope_ctx(config):
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
                    include,
                    search_uri,
                    ".",
                ]
            else:
                cmd = ["find", search_uri, "-name", include]

            logger.debug(cmd)
            p1 = subprocess.Popen(
                cmd,
                text=True,
                stdout=subprocess.PIPE,
            )

            # Optionally ignore URIs and limit the number returned
            if exclude:
                cmd = ["grep", "-Ev", exclude]
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

    logger = get_logger_wrapper(verbose)

    with tiledb.scope_ctx(config):
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

    logger = get_logger_wrapper(verbose)
    logger.debug("tiledbvcf=%s", tiledbvcf.version)

    with tiledb.scope_ctx(config):
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
                manifest_df = A.query(
                    cond="status == 'ok' or status == 'missing index'"
                ).df[:]

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

    logger = get_logger_wrapper(verbose)

    with tiledb.scope_ctx(config):
        with Profiler(group_uri=dataset_uri, group_member=LOG_ARRAY, id=id):
            group = tiledb.Group(dataset_uri)
            manifest_uri = group[MANIFEST_ARRAY].uri

            vfs = tiledb.VFS()

            def file_size(uri: str) -> int:
                try:
                    return vfs.file_size(uri)
                except Exception:
                    return 0

            with tiledb.open(manifest_uri, "w") as A:
                keys = []
                values = defaultdict(list)

                for vcf_uri in sample_uris:
                    status = "ok"

                    # Check for sample name issues
                    try:
                        sample_name = get_sample_name(vcf_uri)
                    except Exception:
                        logger.warning(
                            "Skipping invalid VCF file: %r",
                            vcf_uri,
                        )
                        continue

                    if not sample_name:
                        status = "missing sample name"
                    elif len(sample_name.split()) > 1:
                        status = "multiple samples"
                    elif sample_name in keys:
                        # TODO: check for duplicate sample names across all
                        # ingest_manifest_udf calls
                        status = "duplicate sample name"
                        # Generate a unique sample name for the manifest
                        sample_name_base = sample_name
                        i = 0
                        while sample_name in keys:
                            sample_name = f"{sample_name_base}-dup{i}"
                            i += 1

                    # Check for index issues
                    index_uri = find_index(vcf_uri)
                    if not index_uri:
                        status = "" if status == "ok" else status + ","
                        status += "missing index"
                        records = 0
                    else:
                        records = get_record_count(vcf_uri, index_uri)
                        if records is None:
                            status = "" if status == "ok" else status + ","
                            status += "bad index"

                    keys.append(sample_name)
                    values["status"].append(status)
                    values["vcf_uri"].append(vcf_uri)
                    values["vcf_bytes"].append(str(file_size(vcf_uri)))
                    values["index_uri"].append(index_uri)
                    values["index_bytes"].append(str(file_size(index_uri)))
                    values["records"].append(str(records))

                # Write to TileDB array, if any samples were found
                if keys:
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
    resume: bool = True,
    create_index: bool = True,
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
    :param resume: enable resume ingestion mode, defaults to True
    :param create_index: force creation of a local index file, defaults to True
    :param id: profiler event id, defaults to "samples"
    :param verbose: verbose logging, defaults to False
    :param trace_id: trace ID for logging, defaults to None
    """
    import tiledbvcf

    logger = get_logger_wrapper(verbose)
    logger.debug("tiledbvcf=%s", tiledbvcf.version)

    trace = trace_id == id

    with tiledb.scope_ctx(config):
        with Profiler(
            group_uri=dataset_uri, group_member=LOG_ARRAY, id=id, trace=trace
        ) as prof:
            prof.write("uris", str(len(sample_uris)), ",".join(sample_uris))

            def create_index_file_worker(uri: str) -> None:
                with tiledb.scope_ctx(config):
                    if create_index or not find_index(uri):
                        logger.info("indexing %r", uri)
                        create_index_file(uri)

            # Create index files
            with ThreadPool(threads) as pool:
                pool.map(create_index_file_worker, sample_uris)

            # TODO: Handle un-bgzipped files

            level = "debug" if verbose else "info"
            tiledbvcf.config_logging(level, "ingest.log")
            ds = tiledbvcf.Dataset(
                uri=dataset_uri,
                mode="w",
                cfg=tiledbvcf.ReadConfig(tiledb_config=config),
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

            prof.write("log", extra=read_file("ingest.log"))


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

    get_logger_wrapper(verbose)

    with tiledb.scope_ctx(config):
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


def consolidate_fragments_udf(
    dataset_uri: str,
    *,
    group_member: str,
    config: Optional[Mapping[str, Any]] = None,
    id: str = "consolidate",
    verbose: bool = False,
    unique_dim_index: int = 0,
) -> None:
    """
    Consolidate fragments for an array in the dataset using a bin packing consolidation
    algorithm that packs fragments into bins based on their size and the target size of
    the consolidated fragment.

    Fragments are first grouped by the nonempty-domain of the dimension with index
    `unique_dim_index`. This ensures that fragments with the same nonempty-domain are
    consolidated together. For example, fragments with `contig=chr1` will be
    consolidated together, and fragments with `contig=chr2` will be consolidated
    together, but fragments with `contig=chr1` and `contig=chr2` will not be
    consolidated together.

    :param dataset_uri: dataset URI
    :param group_member: array group member
    :param config: config dictionary, defaults to None
    :param id: profiler event id, defaults to "consolidate"
    :param verbose: verbose logging, defaults to False
    :param unique_dim_index: index of the dimension used to group fragments,
        defaults to 0
    """

    logger = get_logger_wrapper(verbose)

    # Define a method to pack and consolidate fragments.
    def consolidate_fragments(
        fragment_info_list: Sequence[tiledb.FragmentInfo],
        config: Optional[Mapping[str, Any]] = None,
    ) -> None:
        """
        Run a bit packing algorithm to select fragments to be consolidated together
        into a single fragment.

        :param fragment_info_list: list of fragment info objects
        :param config: config dictionary, defaults to None
        """

        # Return if there are no fragments to consolidate.
        if len(fragment_info_list) < 2:
            return

        total_size = []
        fragment_bins = []
        vfs = tiledb.VFS(config=config)

        for fi in fragment_info_list:
            # Get the size of the fragment.
            size = vfs.dir_size(fi.uri)
            logger.debug("Packing fragment with size: %d", size)

            packed = False
            for i in range(len(total_size)):
                # Add fragment to the first bin that has enough space.
                if total_size[i] + size < TARGET_FRAGMENT_BYTES:
                    total_size[i] += size
                    fragment_bins[i].append(basename(fi.uri))
                    logger.debug(
                        "  packed into bin %d, new size = %f MiB",
                        i,
                        total_size[-1] / (1 << 20),
                    )
                    packed = True
                    break

            # If fragment was not packed into any bin, create a new bin.
            if not packed:
                total_size.append(size)
                fragment_bins.append([basename(fi.uri)])
                logger.debug(
                    "  packed into new bin, new size = %f MiB",
                    total_size[-1] / (1 << 20),
                )

        logger.debug("Total bins = %d", len(total_size))

        # Consolidate the fragments in each bin.
        for i, fragment_uris in enumerate(fragment_bins):
            logger.debug(
                "  %d: num_uris = %d size = %.3f MiB",
                i,
                len(fragment_uris),
                total_size[i] / (1 << 20),
            )

            # If there is only one fragment, skip consolidation.
            if len(fragment_uris) > 1:
                logger.debug("Consolidating %d fragments", len(fragment_uris))

                # Set config to consolidate fragments.
                config = tiledb.Config(config)
                config["sm.consolidation.mode"] = "fragments"
                config["sm.consolidation.buffer_size"] = f"{CONSOLIDATION_BUFFER_SIZE}"

                # Consolidate fragments.
                with tiledb.open(array_uri, "w", config=config) as array:
                    array.consolidate(fragment_uris=fragment_uris)

    with tiledb.scope_ctx(config):
        with Profiler(group_uri=dataset_uri, group_member=LOG_ARRAY, id=id):
            with tiledb.Group(dataset_uri) as group:
                array_uri = group[group_member].uri

            # Build list of fragments to be consolidated for each unique nonempty-domain
            # in the unique dimension.
            fragment_info_lists = defaultdict(list)

            fis = tiledb.FragmentInfoList(array_uri)
            for fi in fis:
                fragment_info_lists[fi.nonempty_domain[unique_dim_index]].append(fi)

            logger.debug(
                "Consolidating %d fragments into %d fragments",
                len(fis),
                len(fragment_info_lists),
            )

            # Run consolidation on each list of fragments.
            with ThreadPool(CONSOLIDATION_THREADS) as pool:
                pool.map(
                    partial(consolidate_fragments, config=config),
                    fragment_info_lists.values(),
                )

            # Vacuum fragments.
            logger.debug("Vacuuming fragments")
            config = tiledb.Config(config)
            config["sm.vacuum.mode"] = "fragments"
            tiledb.vacuum(array_uri, config=config)


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
    metadata_uri: Optional[str] = None,
    metadata_attr: str = "uri",
    max_files: Optional[int] = None,
    batch_size: int = MANIFEST_BATCH_SIZE,
    workers: int = MANIFEST_WORKERS,
    extra_attrs: Optional[Union[Sequence[str], str]] = None,
    vcf_attrs: Optional[str] = None,
    anchor_gap: Optional[int] = None,
    compression_level: Optional[int] = None,
    verbose: bool = False,
    batch_mode: bool = True,
    access_credentials_name: Optional[str] = None,
    aws_find_mode: bool = False,
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
    :param metadata_uri: URI of metadata array holding VCF URIs, defaults to None
    :param metadata_attr: name of metadata attribute containing URIs, defaults to "uri"
    :param max_files: maximum number of URIs to ingest, defaults to None
    :param batch_size: manifest batch size, defaults to MANIFEST_BATCH_SIZE
    :param workers: maximum number of parallel workers, defaults to MANIFEST_WORKERS
    :param extra_attrs: INFO/FORMAT fields to materialize, defaults to None
    :param vcf_attrs: VCF with all INFO/FORMAT fields to materialize, defaults to None
    :param anchor_gap: anchor gap for VCF dataset, defaults to None
    :param compression_level: zstd compression level for the VCF dataset,
        defaults to None (uses the default level in TileDB-VCF)
    :param verbose: verbose logging, defaults to False
    :param batch_mode: run all DAGs in batch mode, defaults to True
    :param access_credentials_name: name of role in TileDB Cloud to use in tasks
    :param aws_find_mode: use AWS CLI to find VCFs, defaults to False
    """

    logger = get_logger()

    batch_mode = batch_mode or bool(access_credentials_name)
    dag_mode = dag.Mode.BATCH if batch_mode else dag.Mode.REALTIME

    # Only pass `access_credentials_name` to `submit` when running in batch mode.
    kwargs = {"access_credentials_name": access_credentials_name} if batch_mode else {}

    graph = dag.DAG(
        name="vcf-filter-uris",
        namespace=namespace,
        mode=dag_mode,
    )
    submit = graph.submit_local if local_ingest else graph.submit

    dataset_uri_result = submit(
        create_dataset_udf,
        dataset_uri,
        config=config,
        extra_attrs=extra_attrs,
        vcf_attrs=vcf_attrs,
        anchor_gap=anchor_gap,
        compression_level=compression_level,
        verbose=verbose,
        name="Create VCF dataset ",
        **kwargs,
    )

    if sample_list_uri:
        sample_uris = submit(
            read_uris_udf,
            dataset_uri_result,
            sample_list_uri,
            config=config,
            max_files=max_files,
            verbose=verbose,
            name="Read VCF URIs ",
            **kwargs,
        )

    if search_uri:
        sample_uris = submit(
            find_uris_udf if not aws_find_mode else find_uris_aws_udf,
            dataset_uri_result,
            search_uri,
            config=config,
            include=pattern,
            exclude=ignore,
            max_files=max_files,
            verbose=verbose,
            name="Find VCF URIs ",
            **kwargs,
        )

    if metadata_uri:
        sample_uris = submit(
            read_metadata_uris_udf,
            dataset_uri_result,
            config=config,
            metadata_uri=metadata_uri,
            metadata_attr=metadata_attr,
            verbose=verbose,
            name="Read VCF URIs from metadata ",
            **kwargs,
        )

    filtered_sample_uris = submit(
        filter_uris_udf,
        dataset_uri_result,
        sample_uris,
        config=config,
        verbose=verbose,
        name="Filter VCF URIs ",
        **kwargs,
    )

    run_dag(graph)

    sample_uris = filtered_sample_uris.result()

    if not sample_uris:
        logger.info("All samples found are already in the manifest.")
        return

    logger.info("Found %d new URIs.", len(sample_uris))

    graph = dag.DAG(
        name="vcf-populate-manifest",
        namespace=namespace,
        mode=dag_mode,
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
                resources=CONSOLIDATE_RESOURCES,
                name=f"Consolidate VCF Manifest {i//workers + 1}/{num_consolidates} ",
                **kwargs,
            )

        ingest = submit(
            ingest_manifest_udf,
            dataset_uri,
            sample_uris[i * batch_size : (i + 1) * batch_size],
            config=config,
            verbose=verbose,
            id=f"manifest-ingest-{i}",
            resources=MANIFEST_RESOURCES,
            name=f"Ingest VCF Manifest {i+1}/{num_partitions} ",
            **kwargs,
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
    max_samples: Optional[int] = None,
    resume: bool = True,
    ingest_resources: Optional[Mapping[str, str]] = None,
    verbose: bool = False,
    create_index: bool = True,
    trace_id: Optional[str] = None,
    batch_mode: bool = True,
    access_credentials_name: Optional[str] = None,
    compute: bool = True,
    consolidate_stats: bool = False,
) -> Tuple[Optional[dag.DAG], Sequence[str]]:
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
    :param max_samples: maximum number of samples to ingest, defaults to None (no limit)
    :param resume: enable resume ingestion mode, defaults to True
    :param ingest_resources: manual override for ingest UDF resources, defaults to None
    :param verbose: verbose logging, defaults to False
    :param create_index: force creation of a local index file, defaults to True
    :param trace_id: trace ID for logging, defaults to None
    :param batch_mode: run all DAGs in batch mode, defaults to True
    :param access_credentials_name: name of role in TileDB Cloud to use in tasks
    :param compute: when True the DAG will be computed before it is returned,
        defaults to True
    :param consolidate_stats: consolidate the stats arrays, defaults to False
    :return: sample ingestion DAG and list of sample URIs ingested
    """

    logger = get_logger_wrapper(verbose)

    batch_mode = batch_mode or bool(access_credentials_name)
    dag_mode = dag.Mode.BATCH if batch_mode else dag.Mode.REALTIME

    # Only pass `access_credentials_name` to `submit` when running in batch mode.
    kwargs = {"access_credentials_name": access_credentials_name} if batch_mode else {}

    graph = dag.DAG(
        name="vcf-filter-samples",
        namespace=namespace,
        mode=dag_mode,
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
        resource_class="large",
        **kwargs,
    )

    run_dag(graph)

    sample_uris = sample_uris.result()

    if not sample_uris:
        logger.info("No new samples to ingest.")
        return None, []

    # Limit number of samples to ingest
    if max_samples:
        sample_uris = sample_uris[:max_samples]

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
        retry_strategy=RetryStrategy(
            limit=3,
            retry_policy="Always",
        ),
    )
    submit = graph.submit_local if local_ingest else graph.submit

    # Reduce batch size if there are fewer sample URIs
    batch_size = min(batch_size, len(sample_uris))

    num_partitions = ceil(len(sample_uris) / batch_size)
    num_consolidates = ceil(num_partitions / workers)

    # Calculate resources for ingest nodes
    # 2GB per thread + VCF_HEADER_MB per sample per thread
    node_memory_mb = threads * (2048 + batch_size * VCF_HEADER_MB)
    vcf_memory_mb = 1024 * threads

    if ingest_resources is None:
        ingest_resources = {"cpu": f"{threads}", "memory": f"{node_memory_mb}Mi"}

    logger.debug("partitions=%d, consolidates=%d", num_partitions, num_consolidates)
    logger.debug("ingest_resources=%s", ingest_resources)
    logger.debug("consolidate_resources=%s", CONSOLIDATE_RESOURCES)

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
                resources=CONSOLIDATE_RESOURCES,
                name=f"Consolidate VCF {i//workers + 1}/{num_consolidates} ",
                **kwargs,
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
            create_index=create_index,
            trace_id=trace_id,
            resources=ingest_resources,
            name=f"Ingest VCF {i+1}/{num_partitions} ",
            **kwargs,
        )

        if prev_consolidate:
            ingest.depends_on(prev_consolidate)

        if consolidate:
            consolidate.depends_on(ingest)

    # Consolidate fragments in the stats arrays, if enabled
    if consolidate_stats:
        consolidate_ac = submit(
            consolidate_fragments_udf,
            dataset_uri,
            group_member="allele_count",
            config=config,
            id="vcf-consol-ac",
            verbose=verbose,
            resources=CONSOLIDATE_FRAGMENT_RESOURCES,
            name="Consolidate allele_count ",
            **kwargs,
        )

        consolidate_vs = submit(
            consolidate_fragments_udf,
            dataset_uri,
            group_member="variant_stats",
            config=config,
            id="vcf-consol-vs",
            verbose=verbose,
            resources=CONSOLIDATE_FRAGMENT_RESOURCES,
            name="Consolidate variant stats ",
            **kwargs,
        )

        consolidate_ac.depends_on(consolidate)
        consolidate_vs.depends_on(consolidate)

        consolidate = submit(
            consolidate_dataset_udf,
            dataset_uri,
            config=config,
            id="vcf-consol-final",
            verbose=verbose,
            resources=CONSOLIDATE_RESOURCES,
            name="Consolidate VCF final ",
            **kwargs,
        )

        consolidate.depends_on(consolidate_ac)
        consolidate.depends_on(consolidate_vs)

    if compute:
        logger.info("Ingesting %d samples.", len(sample_uris))
        run_dag(graph, wait=local_ingest)

        if not local_ingest:
            logger.info(
                "Batch ingestion submitted -"
                " https://cloud.tiledb.com/activity/taskgraphs/%s/%s",
                graph.namespace,
                graph.server_graph_uuid,
            )

    return graph, sample_uris


# --------------------------------------------------------------------
# User functions
# --------------------------------------------------------------------


def ingest(
    dataset_uri: str,
    *,
    config=None,
    namespace: Optional[str] = None,
    register_name: Optional[str] = None,
    search_uri: Optional[str] = None,
    pattern: Optional[str] = None,
    ignore: Optional[str] = None,
    sample_list_uri: Optional[str] = None,
    metadata_uri: Optional[str] = None,
    metadata_attr: str = "uri",
    max_files: Optional[int] = None,
    max_samples: Optional[int] = None,
    contigs: Optional[Union[Sequence[str], Contigs]] = Contigs.ALL,
    resume: bool = True,
    extra_attrs: Optional[Union[Sequence[str], str]] = DEFAULT_ATTRIBUTES,
    vcf_attrs: Optional[str] = None,
    anchor_gap: Optional[int] = None,
    compression_level: Optional[int] = None,
    manifest_batch_size: int = MANIFEST_BATCH_SIZE,
    manifest_workers: int = MANIFEST_WORKERS,
    vcf_batch_size: int = VCF_BATCH_SIZE,
    vcf_workers: int = VCF_WORKERS,
    vcf_threads: int = VCF_THREADS,
    ingest_resources: Optional[Mapping[str, str]] = None,
    verbose: bool = False,
    create_index: bool = True,
    trace_id: Optional[str] = None,
    batch_mode: bool = True,
    access_credentials_name: Optional[str] = None,
    compute: bool = True,
    consolidate_stats: bool = False,
    aws_find_mode: bool = False,
) -> Tuple[Optional[dag.DAG], Sequence[str]]:
    """
    Ingest samples into a dataset.

    :param dataset_uri: dataset URI
    :param config: config dictionary, defaults to None
    :param namespace: TileDB-Cloud namespace, defaults to None
    :param register_name: name to register the dataset with on TileDB Cloud,
        defaults to None
    :param search_uri: URI to search for VCF files, defaults to None
    :param pattern: Unix shell style pattern to match when searching for VCF files,
        defaults to None
    :param ignore: Unix shell style pattern to ignore when searching for VCF files,
        defaults to None
    :param sample_list_uri: URI with a list of VCF URIs, defaults to None
    :param metadata_uri: URI of metadata array holding VCF URIs, defaults to None
    :param metadata_attr: name of metadata attribute containing URIs, defaults to "uri"
    :param max_files: maximum number of VCF URIs to read/find,
        defaults to None (no limit)
    :param max_samples: maximum number of samples to ingest, defaults to None (no limit)
    :param contigs: contig mode
        (Contigs.ALL | Contigs.CHROMOSOMES | Contigs.OTHER | Contigs.ALL_DISABLE_MERGE)
        or list of contigs to ingest, defaults to Contigs.ALL
    :param resume: enable resume ingestion mode, defaults to True
    :param extra_attrs: INFO/FORMAT fields to materialize,
        defaults to `repr(DEFAULT_ATTRIBUTES)`
    :param vcf_attrs: VCF with all INFO/FORMAT fields to materialize,
        defaults to None
    :param anchor_gap: anchor gap for VCF dataset, defaults to None
    :param compression_level: zstd compression level for the VCF dataset,
        defaults to None (uses the default level in TileDB-VCF)
    :param manifest_batch_size: batch size for manifest ingestion,
        defaults to MANIFEST_BATCH_SIZE
    :param manifest_workers: number of workers for manifest ingestion,
        defaults to MANIFEST_WORKERS
    :param vcf_batch_size: batch size for VCF ingestion, defaults to VCF_BATCH_SIZE
    :param vcf_workers: number of workers for VCF ingestion, defaults to VCF_WORKERS
    :param vcf_threads: number of threads for VCF ingestion, defaults to VCF_THREADS
    :param ingest_resources: manual override for ingest UDF resources, defaults to None
    :param verbose: verbose logging, defaults to False
    :param create_index: force creation of a local index file, defaults to True
    :param trace_id: trace ID for logging, defaults to None
    :param batch_mode: run all DAGs in batch mode, only set to False for dev or demos,
        defaults to True
    :param access_credentials_name: name of role in TileDB Cloud to use in tasks
    :param compute: when True the DAG will be computed before it is returned,
        defaults to True
    :param consolidate_stats: consolidate the stats arrays, defaults to False
    :param aws_find_mode: use AWS CLI to find VCFs, defaults to False
    :return: sample ingestion DAG and list of sample URIs ingested
    """

    # Validate user input
    if sum([bool(search_uri), bool(sample_list_uri), bool(metadata_uri)]) != 1:
        raise ValueError(
            "Exactly one of `search_uri`, `sample_list_uri`, or `metadata_uri`"
            " must be provided."
        )

    if not search_uri and (pattern or ignore):
        raise ValueError("Only specify `pattern` or `ignore` with `search_uri`.")

    if not batch_mode and access_credentials_name:
        raise ValueError(
            "Cannot specify `access_credentials_name` with `batch_mode=False`."
        )

    # Remove any trailing slashes
    dataset_uri = dataset_uri.rstrip("/")

    logger = get_logger_wrapper(verbose)
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
        metadata_uri=metadata_uri,
        metadata_attr=metadata_attr,
        max_files=max_files,
        batch_size=manifest_batch_size,
        workers=manifest_workers,
        extra_attrs=extra_attrs,
        vcf_attrs=vcf_attrs,
        anchor_gap=anchor_gap,
        compression_level=compression_level,
        verbose=verbose,
        batch_mode=batch_mode,
        access_credentials_name=access_credentials_name,
        aws_find_mode=aws_find_mode,
    )

    # Ingest VCFs using URIs in the manifest
    dag, sample_uris = ingest_samples_dag(
        dataset_uri,
        config=config,
        namespace=namespace,
        batch_size=vcf_batch_size,
        workers=vcf_workers,
        threads=vcf_threads,
        contigs=contigs,
        max_samples=max_samples,
        resume=resume,
        ingest_resources=ingest_resources,
        verbose=verbose,
        create_index=create_index,
        trace_id=trace_id,
        batch_mode=batch_mode,
        access_credentials_name=access_credentials_name,
        compute=compute,
        consolidate_stats=consolidate_stats,
    )

    # Register the dataset on TileDB Cloud
    if register_name:
        register_dataset_udf(
            dataset_uri,
            namespace=namespace,
            register_name=register_name,
            config=config,
            verbose=verbose,
        )

    return dag, sample_uris
