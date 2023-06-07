import logging
from math import ceil
from typing import Any, Callable, List, Mapping, Optional, Sequence, Tuple, Union

import pyarrow as pa
import pandas


def calc_af(df) -> pandas.DataFrame:
    """Consolidate AC and compute AN, AF
    :param pandas.Dataframe df
    """
    # Allele Count (AC) = sum of all AC at the same locus
    # This step consolidates ACs from all ingested batches
    df = df.groupby(["pos", "allele"], sort=True).sum()

    # Allele Number (AN) = sum of AC at the same locus
    an = df.groupby(["pos"], sort=True).ac.sum().rename("an")
    df = df.join(an, how="inner")

    # Allele Frequency (AF) = AC / AN
    df["af"] = df.ac / df.an
    return df

claculate_allele_frequency = calc_af


def read_variant_stats(dataset_uri: str, region: str) -> pandas.DataFrame():
    """
    Read variant status

    :param dataset_uri: dataset URI
    :param region: genomics region to read
    """
    import tiledb

    # Get the variant stats uri
    with tiledb.Group(uri) as g:
        alleles_uri = g["variant_stats"].uri

        contig = region.split(":")[0]
        region_positions = region.split(":")[1].split("-")

        with tiledb.open(alleles_uri) as A:
            df = A.query(attrs=["ac", "allele"], dims=["pos", "contig"]).df[
                contig, slice(region_positions[0], region_positions[1])
            ]
            return calc_af(df)
