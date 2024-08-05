"""Split samples from multi-sample VCF."""

import gzip
import logging
import os
from typing import Mapping, Optional, Sequence

from attrs import define
from attrs import field

import tiledb
from tiledb.cloud.dag import DAG
from tiledb.cloud.dag import Mode
from tiledb.cloud.rest_api import RetryStrategy
from tiledb.cloud.utilities import get_logger
from tiledb.cloud.utilities import process_stream
from tiledb.cloud.utilities import run_dag
from tiledb.cloud.version import version


def ls_samples(
    vcf_uri: str,
    config: Optional[Mapping[str, str]] = None,
) -> list[str]:
    """List samples in an aggregate VCF.

    :param vcf_uri: S3 path to aggregate VCF.
    :param config: TileDB config params.
    :return: Samples included in VCF.
    """

    logger = get_logger()

    @define
    class FindSamples:
        """Query samples included in multi-sample VCF."""

        source: str
        """Aggregate VCF containing multiple-samples to be used as source to
        isolate from."""
        line_key: str = "#CHROM"
        """indicator to search lines for containing row with sample names."""
        search_key: str = "FORMAT"
        """Indicator within sample name row that just-precedes names."""
        config: tiledb.Config = field(factory=tiledb.Config)
        """Config."""
        vfs: tiledb.vfs.VFS = field(init=False)
        """Virtual filesystem instance."""

        def __attrs_post_init__(self) -> None:
            # config VFS constructor for region
            self.vfs = tiledb.VFS(config=self.config)

        def sample_names(self) -> list[str]:
            """ID samples in VCF.

            Size conscience to limit memory use.

            :return: Samples included in aggregate VCF.
            """

            with self.vfs.open(self.source, mode="rb") as op_gz:
                op = gzip.GzipFile(fileobj=op_gz)
                for line in op:
                    line = line.decode("utf-8").strip()
                    if line.startswith(self.line_key):
                        samples = line[
                            line.index(self.search_key) + len(self.search_key) :
                        ].split()
                        return samples

    finder = FindSamples(source=vcf_uri, config=config)
    all_samples = finder.sample_names()

    if all_samples:
        pretty_log = "\n\t>>> ".join(all_samples)
        logger.info(f"Samples Identified:\n\t>>> {pretty_log}")

    logger.info(f"\n{len(all_samples)} samples aggregated in {finder.source}.")

    return all_samples


def split_one_sample(
    vcf_uri: str,
    sample: str,
    output_uri: str,
    config: Optional[Mapping[str, str]] = None,
) -> str:
    """Split one sample from multi-sample VCF.

    :param vcf_uri: URI of VCF to isolate from.
    :param sample: Sample name to isolate.
    :param output_uri: URI to deposit isolated VCF.
    :param config: TileDB config object.
    :return: URI of isolated sample.
    """

    logger = get_logger()

    @define
    class IsolateVCF:
        """Isolate a sample VCF from multi-sample VCF"""

        source: str
        """Aggregate VCF containing multiple-samples to
        be used as source to isolate from."""
        config: Mapping[str, str] = field(factory=dict)
        """TileDB configuration settings."""
        bcftools: str = "/opt/conda/bin/bcftools"
        """bcftools path."""
        vfs: tiledb.vfs.VFS = field(init=False)
        """Virtual filesystem instance."""

        def __attrs_post_init__(self) -> None:
            self.vfs = tiledb.VFS(config=self.config)

        def _remote_bcftools(
            self,
            args: Sequence[str],
            output_uri: str = None,
        ) -> str:
            """Run bcftools on (remote) URI.

            :param args: Arguments to pass to bcftools. Don't include bcftools
                in this command.
            :param output_uri: URI to write results.
            :return: return code, stdout, stderr
            """

            cmd = [self.bcftools] + args

            stream = process_stream(self.source, cmd, output_uri=output_uri)

            if stream[0] != 0:
                raise RuntimeError(f"bcftools command error: {stream[2]}")
            return stream[1]

        def isolate(self, sample: str, output_uri: str) -> str:
            """Isolate a single sample from a multi-sample VCF.

            :param sample: Sample name to isolate from VCF.
            :param output_uri: URI to write results.
            :return: URI to isolated VCF.
            """

            # write directly to file if given
            if output_uri.endswith(".vcf.gz"):
                isolated_uri = output_uri
            else:
                isolated_uri = os.path.join(output_uri, sample + ".vcf.gz")

            logger.info(f"Isolating {sample} from {self.source}")

            self._remote_bcftools(
                args=[
                    "view",
                    "-Oz",
                    "-s",
                    sample,
                ],
                output_uri=isolated_uri,
            )

            logger.info(f"{sample} isolated and written to {isolated_uri}")

            return isolated_uri

    isolater = IsolateVCF(source=vcf_uri, config=config)
    result_uri = isolater.isolate(sample=sample, output_uri=output_uri)

    return result_uri


def split_vcf(
    vcf_uri: str,
    output_uri: str,
    namespace: str,
    acn: str,
    resources: Mapping[str, str] = {"cpu": "2", "memory": "30Gi"},
    compute: bool = True,
    verbose: bool = False,
    samples: Optional[Sequence[str]] = None,
    retry_count: int = 1,
    max_workers: int = 100,
    config: Optional[Mapping[str, int]] = None,
) -> DAG:
    """Split individual sample VCFs from an aggreate VCF.

    Given an aggregate VCF file containing multiple samples, split
    all samples into isolated VCFs, one per sample. Alternatively,
    specify sample(s) to split apart from VCF if not all isolated
    VCFs are needed.

    :param vcf_uri: Aggregate VCF URI.
    :param output_uri: Output URI to write isolated VCFs.
    :param namespace: TileDB Cloud namespace to process task graph.
    :param acn: Access credential friendly name to auth storage i/o.
    :param resources: Resources applied to splitting UDF (start with default).
    :param compute: Whether to execute DAG.
    :param verbose: Logging verbosity.
    :param samples: Indicate a batch of sample names within `vcf_uri` to isolate
        if it is undesired to isolate all samples (default).
    :param retry_count: Number of Node retries.
    :param max_workers: Max workers to engage simultaneously.
    :param config: TileDB configuration parameters used to configure virtual
        filesystem handler.
    :return: DAG instantiated as specified.
    """

    logger = get_logger(level=logging.DEBUG if verbose else logging.INFO)

    logger.debug(
        "tiledb.cloud=%s, tiledb=%s, libtiledb=%s",
        version,
        tiledb.version(),
        tiledb.libtiledb.version(),
    )

    graph = DAG(
        mode=Mode.BATCH,
        namespace=namespace,
        name="Split VCF",
        max_workers=max_workers,
        retry_strategy=RetryStrategy(
            limit=retry_count,
            retry_policy="Always",
        ),
    )

    if not samples:
        logger.debug("Isolating all samples from aggregate VCF.")

        samples = graph.submit(
            ls_samples,
            vcf_uri=vcf_uri,
            config=config,
            access_credentials_name=acn,
            name="List Samples",
            resources={
                "cpu": "1",
                "memory": "5Gi",
            },
        )

        graph.submit_udf_stage(
            split_one_sample,
            vcf_uri=vcf_uri,
            sample=samples,
            output_uri=output_uri,
            config=config,
            expand_node_output=samples,
            access_credentials_name=acn,
            name="Split Sample From VCF",
            resources=resources,
        )
    else:
        logger.debug(f"Isolating {len(samples)} samples from aggregate VCF.")

        # isolate specified samples only
        for s in samples:
            graph.submit(
                split_one_sample,
                vcf_uri=vcf_uri,
                sample=s,
                output_uri=output_uri,
                config=config,
                access_credentials_name=acn,
                name="Split Sample From VCF",
                resources=resources,
            )

    if compute:
        run_dag(graph, wait=False, debug=verbose)

        logger.info(
            "Task Graph submitted -"
            " https://cloud.tiledb.com/activity/taskgraphs/%s/%s",
            graph.namespace,
            graph.server_graph_uuid,
        )

    logger.debug(f"Returning DAG: {graph.name}")

    return graph
