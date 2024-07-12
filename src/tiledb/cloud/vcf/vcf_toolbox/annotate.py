import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Mapping, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd

import tiledb
from tiledb.cloud.utilities import get_logger
from tiledb.cloud.utilities import max_memory_usage

from .transform import df_transform


def split_region(region: str) -> Tuple[str, slice]:
    """
    Split a region string into contig and slice.

    The format of the region string is 'contig:start-end'.

    :param region: region to split
    :raises ValueError: if region is not in the format 'contig:start-end'
    :return: contig and slice
    """

    if not isinstance(region, str) or ":" not in region or "-" not in region:
        raise ValueError("Region must be in the format 'contig:start-end'")
    contig, range = region.split(":")
    start, end = range.split("-")
    return contig, slice(int(start), int(end))


def split_regions(regions: Union[str, Sequence[str]]) -> Tuple[str, Sequence[slice]]:
    """
    Split a region or list of regions into a contig and list of slices.

    :param regions: regions to split
    :raises ValueError: if regions are not in the same contig
    :return: contig and list of slices
    """

    if isinstance(regions, str):
        regions = [regions]

    contig = None
    ranges = []
    for region in regions:
        c, r = split_region(region)
        if contig is None:
            contig = c
        elif contig != c:
            raise ValueError("All regions must be in the same contig")
        ranges.append(r)

    return contig, ranges


def zygosity(gt: np.ndarray) -> str:
    """
    Convert genotype to a zygosity string.

    :param gt: genotype
    :return: zygosity string
    """
    gt = list(gt)

    # All genotypes are missing
    if len(gt) == 0 or all(allele == -1 for allele in gt):
        return "MISSING"

    # One allele
    if len(gt) == 1:
        if gt[0] == 0:
            return "HOM_REF"
        return "HEMI"

    # More than one allele
    if all(allele == 0 for allele in gt):
        return "HOM_REF"
    if all(allele == gt[0] for allele in gt):
        return "HOM_ALT"
    return "HET"


def _annotate(
    vcf_df: pd.DataFrame,
    *,
    ann_uri: str,
    ann_regions: Union[str, Sequence[str]],
    ann_attrs: Optional[Union[str, Sequence[str]]] = None,
    vcf_filter: Optional[str] = None,
    split_multiallelic: bool = True,
    add_zygosity: bool = False,
    reorder: Optional[Sequence[str]] = None,
    rename: Optional[Mapping[str, str]] = None,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Annotate a VCF DataFrame with annotations from a TileDB array.

    :param vcf_df: VCF DataFrame to annotate
    :param ann_uri: URI of the annotation array
    :param ann_regions: regions to annotate. All regions must be in the same
        chromosome/contig.
    :param ann_attrs: annotation attributes to read,
        defaults to None which queries all attributes.
    :param vcf_filter: a pandas filter to apply to the VCF DataFrame before annotation,
        defaults to None
    :param split_multiallelic: split multiallelic variants into separate rows,
        defaults to True
    :param add_zygosity: add zygosity column to the DataFrame, defaults to False
    :param reorder: list of columns to reorder (before renaming), defaults to None
    :param rename: dict of columns to rename, defaults to None
    :param verbose: enable verbose logging, defaults to False
    :return: annotated VCF DataFrame
    """

    if isinstance(ann_attrs, str):
        ann_attrs = [ann_attrs]

    rename = dict(rename or {})

    # Add attributes required for join
    if ann_attrs is not None:
        for attr in ["ref", "alt"]:
            if attr not in ann_attrs:
                ann_attrs.append(attr)

    level = logging.DEBUG if verbose else logging.INFO
    logger = get_logger(level)

    def log_event(message, t_prev=None):
        if t_prev:
            message += f" {time.time() - t_prev:.3f} sec"
        logger.debug(message)
        return time.time()

    t_prev = log_event("start annotation")
    t_start = t_prev
    mem_start = max_memory_usage()

    # Split regions
    contig, regions = split_regions(ann_regions)

    # Start annotation query in a separate thread
    def read_ann():
        with tiledb.open(ann_uri) as A:
            df = A.query(attrs=ann_attrs).df[contig, regions]
        return df

    executor = ThreadPoolExecutor(1)
    ann_future = executor.submit(read_ann)

    # Filter the VCF data
    if vcf_filter:
        vcf_df = vcf_df.query(vcf_filter).reset_index(drop=True)
        t_prev = log_event("filter", t_prev)

    # Return if the filtered VCF data is empty
    if len(vcf_df) == 0:
        return vcf_df

    # Split alleles into ref and alt
    vcf_df["ref"] = vcf_df["alleles"].str[0]
    vcf_df["alt"] = vcf_df["alleles"].str[1:]
    vcf_df.drop("alleles", axis=1, inplace=True)
    t_prev = log_event("split ref/alt", t_prev)

    # Create an af column with the ALT IAF values
    alt_af = "info_TILEDB_ALT_IAF"
    if "info_TILEDB_IAF" in vcf_df:
        vcf_df[alt_af] = vcf_df["info_TILEDB_IAF"].str[1:]

    if split_multiallelic:
        # Split multiallelic variants
        explode_cols = ["alt"]

        if "info_TILEDB_IAF" in vcf_df:
            explode_cols.append(alt_af)

        vcf_df = vcf_df.explode(explode_cols)
        t_prev = log_event("split multiallelic", t_prev)
    else:
        # Convert alt to comma-separated string
        vcf_df["alt"] = vcf_df["alt"].str.join(",")
        t_prev = log_event("join multiallelic", t_prev)

    # Add zygosity
    if add_zygosity:
        vcf_df["zygosity"] = vcf_df["fmt_GT"].apply(zygosity)
        t_prev = log_event("add zygosity", t_prev)

    # Wait for annotation query
    ann_df = ann_future.result()
    t_prev = log_event("wait on annotation query", t_prev)

    # Drop annotation duplicates (for annotations that were ingested multiple times)
    ann_df.drop_duplicates(inplace=True)
    t_prev = log_event("drop duplicate annotations", t_prev)

    # Merge VCF and annotations
    vcf_df = vcf_df.merge(
        ann_df,
        how="left",
        on=["contig", "pos_start", "ref", "alt"],
    )
    t_prev = log_event("join", t_prev)

    # Reorder columns
    if reorder:
        ordered_columns = reorder + [c for c in vcf_df.columns if c not in reorder]
        vcf_df = vcf_df[ordered_columns]

    # Rename columns
    if rename:
        vcf_df = vcf_df.rename(columns=rename)

    annotation_mem_gib = (max_memory_usage() - mem_start) / (1 << 30)
    logger.debug(f"annotation memory usage: {annotation_mem_gib:.3f} GiB")
    logger.debug(f"max memory usage: {max_memory_usage() / (1<<30):.3f} GiB")
    log_event("total annotation time", t_start)

    return vcf_df


annotate = df_transform(_annotate)
