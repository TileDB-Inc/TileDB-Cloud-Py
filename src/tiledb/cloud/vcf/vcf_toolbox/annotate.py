import logging
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

import tiledb
from tiledb.cloud.utilities import get_logger
from tiledb.cloud.utilities import max_memory_usage

from .transform import df_transform


def split_region(region):
    if not isinstance(region, str) or ":" not in region or "-" not in region:
        raise ValueError("Region must be in the format 'contig:start-end'")
    contig, range = region.split(":")
    start, end = range.split("-")
    return contig, slice(int(start), int(end))


def split_regions(regions):
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


def zygosity(x):
    if tuple(x) == tuple([0, 0]):
        return "HOM_REF"
    if tuple(x) == tuple([".", "."]):
        return "UNKNOWN"
    # check for any tuple where any element is 0
    elif len(tuple(x)) == 2 and (tuple(x)[0] == 0 or tuple(x)[1] == 0):
        return "HET"
    elif tuple(x)[0] != 0 and tuple(x)[1] != 0:
        return "HOM_ALT"
    elif len(tuple(x)) == 1 and tuple(x)[0] != 0:
        return "HEMI"
    else:
        return str(x)


@df_transform
def annotate(
    vcf_df,
    *,
    ann_uri,
    ann_attrs,
    ann_regions,
    vcf_filter=None,
    add_zygosity=False,
    reorder=["sample_name", "contig", "pos_start", "ref", "alt"],
    rename={"sample_name": "sample", "contig": "chrom", "pos_start": "pos"},
    verbose=False,
):
    """
    Annotate a VCF DataFrame with annotations from a TileDB array.

    Parameters
    ----------
    vcf_df
        The input VCF DataFrame, passed in automatically by `tiledb.cloud.vcf.query`.
    ann_uri
        The URI of the annotation array.
    ann_attrs
        The attributes to query.
    ann_regions
        The regions to query. All regions must be in the same chromosome/contig.
    vcf_filter, optional
        A pandas filter to apply to the VCF DataFrame before annotation, by default None
    add_zygosity, optional
        Add a zygosity column to the DataFrame, by default False
    reorder, optional
        List of columns to reorder, by default
            ["sample_name", "contig", "pos_start", "ref", "alt"]
    rename, optional
        Dict of columns to rename, by default
            {"sample_name": "sample", "contig": "chrom", "pos_start": "pos"}
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
    vcf_df["alt"] = vcf_df["alleles"].apply(lambda x: ",".join(x[1:]))
    vcf_df = vcf_df.drop("alleles", axis=1)
    t_prev = log_event("split ref/alt", t_prev)

    # Add zygosity
    if add_zygosity:
        vcf_df["zygosity"] = vcf_df["fmt_GT"].apply(zygosity)
        t_prev = log_event("add zygosity", t_prev)

    # Wait for annotation query
    ann_df = ann_future.result()
    t_prev = log_event("wait on annotation query", t_prev)

    # Merge VCF and annotations
    vcf_df = pd.merge(
        ann_df,
        vcf_df,
        how="inner",
        left_on=["contig", "pos_start", "ref", "alt"],
        right_on=["contig", "pos_start", "ref", "alt"],
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
