import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Mapping, Optional, Sequence, Tuple, Union

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


def zygosity(gt: Tuple[int, int]) -> str:
    """
    Convert genotype to a zygosity string.

    :param gt: genotype
    :return: zygosity string
    """
    if tuple(gt) == tuple([0, 0]):
        return "HOM_REF"
    if tuple(gt) == tuple([".", "."]):
        return "UNKNOWN"
    elif len(tuple(gt)) == 2 and (tuple(gt)[0] == 0 or tuple(gt)[1] == 0):
        return "HET"
    elif tuple(gt)[0] != 0 and tuple(gt)[1] != 0:
        return "HOM_ALT"
    elif len(tuple(gt)) == 1 and tuple(gt)[0] != 0:
        return "HEMI"
    else:
        return str(gt)


@df_transform
def annotate(
    vcf_df: pd.DataFrame,
    *,
    ann_uri: str,
    ann_regions: Union[str, Sequence[str]],
    ann_attrs: Optional[Union[str, Sequence[str]]] = None,
    vcf_filter: Optional[str] = None,
    split_multiallelic: bool = True,
    add_zygosity: bool = False,
    reorder: Optional[Sequence[str]] = [
        "sample_name",
        "contig",
        "pos_start",
        "ref",
        "alt",
    ],
    rename: Optional[Mapping[str, str]] = {"sample_name": "sample"},
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Annotate a VCF DataFrame with annotations from a TileDB array.

    Parameters
    ----------
    vcf_df
        The input VCF DataFrame.
    ann_uri
        The URI of the annotation array.
    ann_regions
        The regions to query. All regions must be in the same chromosome/contig.
    ann_attrs
        The attributes to query.
    vcf_filter, optional
        A pandas filter to apply to the VCF DataFrame before annotation, by default None
    split_multiallelic, optional
        Split multiallelic variants into separate rows, by default True
    add_zygosity, optional
        Add a zygosity column to the DataFrame, by default False
    reorder, optional
        List of columns to reorder, by default
            ["sample_name", "contig", "pos_start", "ref", "alt"]
    rename, optional
        Dict of columns to rename, by default
            {"sample_name": "sample"}
    verbose, optional
        Enable verbose logging, by default False

    Returns
    -------
        The annotated VCF DataFrame.
    """

    if isinstance(ann_attrs, str):
        ann_attrs = [ann_attrs]

    # Add attributes required for join
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

    # Start annotation query
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
    vcf_df = vcf_df.drop("alleles", axis=1)
    t_prev = log_event("split ref/alt", t_prev)

    # Split multiallelic variants
    if split_multiallelic:
        vcf_df = vcf_df.explode("alt")
        vcf_df = vcf_df[vcf_df["alt"].notnull()]
        t_prev = log_event("split multiallelic", t_prev)
    else:
        vcf_df["alt"] = vcf_df["alt"].apply(lambda x: ",".join(x))

    # Add zygosity
    if add_zygosity:
        vcf_df["zygosity"] = vcf_df["fmt_GT"].apply(zygosity)
        t_prev = log_event("add zygosity", t_prev)

    # Wait for annotation query
    ann_df = ann_future.result()
    t_prev = log_event("wait on annotation query", t_prev)

    # Drop annotation duplicates
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
