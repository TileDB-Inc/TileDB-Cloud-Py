import numpy as np
import pytest

import tiledb.cloud.vcf as vcf
import tiledb.cloud.vcf.vcf_toolbox as vtb
from tiledb.cloud._vendor import cloudpickle

# Pickle the vcf module by value, so tests run on the latest code.
cloudpickle.register_pickle_by_value(vcf)


# Run VCF tests with:
#   pytest -m vcf --run-vcf -n 8


@vtb.df_transform
def filter_vcf(df, *, filter=None):
    return df.query(filter)


@pytest.mark.vcf
@pytest.mark.parametrize("batch_mode", [False, True])
def test_vcf_transform(batch_mode):
    vcf_uri = "tiledb://TileDB-Inc/vcf-1kg-dragen-v376"

    regions = [
        "chr21:26973732-27213386",  # APP (Amyloid Beta Precursor Protein)
    ]

    # VCF attributes to read
    vcf_attrs = [
        "sample_name",
        "contig",
        "pos_start",
        "alleles",
        "fmt_DP",
        "fmt_GQ",
        "fmt_GT",
    ]

    # Filter to apply to VCF data
    filter = "fmt_DP > 20 and fmt_GQ > 25"

    # Run the VCF query with the transform function
    vcf_table = vcf.read(
        dataset_uri=vcf_uri,
        attrs=vcf_attrs,
        regions=regions,
        samples="NA12878",
        transform_result=filter_vcf(filter=filter),
        batch_mode=batch_mode,
    )

    assert vcf_table.num_rows == 336
    assert vcf_table.num_columns == 8


@pytest.mark.vcf
def test_vcf_zygosity():
    vcf_uri = "tiledb://TileDB-Inc/vcf-1kg-dragen-v376"

    regions = "chrY:2700000-2800000"

    # Configure the annotation transform function
    transform_result = vtb.annotate(
        ann_uri="tiledb://tiledb-genomics-dev/vep_20230726_6",
        ann_regions=regions,
        add_zygosity=True,
    )

    # Run the VCF query with annotation
    vcf_table = vcf.read(
        dataset_uri=vcf_uri,
        regions=regions,
        samples="HG00096",
        transform_result=transform_result,
    )

    assert vcf_table.num_rows == 3
    assert vcf_table.num_columns == 49


@pytest.mark.vcf
@pytest.mark.parametrize(
    "split_multiallelic,attr_list,expected_rows,expected_columns",
    [(False, True, 336, 15), (True, False, 340, 53)],
)
def test_vcf_annotation(
    split_multiallelic,
    attr_list,
    expected_rows,
    expected_columns,
):
    vcf_uri = "tiledb://TileDB-Inc/vcf-1kg-dragen-v376"

    regions = [
        "chr21:26973732-27213386",  # APP (Amyloid Beta Precursor Protein)
    ]

    # VCF attributes to read
    vcf_attrs = [
        "sample_name",
        "contig",
        "pos_start",
        "alleles",
        "info_TILEDB_IAF",
        "fmt_DP",
        "fmt_GQ",
        "fmt_GT",
    ]

    # Filter to apply to VCF data
    vcf_filter = "fmt_DP > 20 and fmt_GQ > 25"

    # Add a zygosity column based on fmt_GT
    add_zygosity = True

    # Annotation array URI
    ann_uri = "tiledb://tiledb-genomics-dev/vep_20230726_6"

    # Annotation attributes to read
    ann_attrs = ["Gene", "Feature", "VARIANT_CLASS"] if attr_list else None

    # Configure the annotation transform function
    transform_result = vtb.annotate(
        ann_uri=ann_uri,
        ann_attrs=ann_attrs,
        ann_regions=regions,
        vcf_filter=vcf_filter,
        add_zygosity=add_zygosity,
        split_multiallelic=split_multiallelic,
        reorder=["sample_name", "contig", "pos_start", "ref", "alt"],
        rename={"sample_name": "sample", "contig": "chrom", "pos_start": "pos"},
    )

    # Run the VCF query with annotation
    vcf_table = vcf.read(
        dataset_uri=vcf_uri,
        attrs=vcf_attrs,
        regions=regions,
        samples="NA12878",
        transform_result=transform_result,
    )

    assert vcf_table.num_rows == expected_rows
    assert vcf_table.num_columns == expected_columns


@pytest.mark.vcf
def test_vcf_iaf():
    vcf_uri = "tiledb://TileDB-Inc/vcf-1kg-dragen-v376"

    regions = "chr21:26980001-26980001"

    # VCF attributes to read
    vcf_attrs = [
        "sample_name",
        "contig",
        "pos_start",
        "alleles",
        "info_TILEDB_IAF",
        "fmt_DP",
        "fmt_GQ",
        "fmt_GT",
    ]

    # Annotation array URI
    ann_uri = "tiledb://tiledb-genomics-dev/vep_20230726_6"

    # Annotation attributes to read
    ann_attrs = ["Gene", "Feature", "VARIANT_CLASS"]

    # Configure the annotation transform function
    transform_result = vtb.annotate(
        ann_uri=ann_uri,
        ann_attrs=ann_attrs,
        ann_regions=regions,
    )

    # Run the VCF query with annotation
    vcf_table = vcf.read(
        dataset_uri=vcf_uri,
        attrs=vcf_attrs,
        regions=regions,
        samples="NA12878",
        transform_result=transform_result,
    )

    assert vcf_table.num_rows == 2
    assert vcf_table.num_columns == 14


@pytest.mark.vcf
def test_vcf_zygosity_value():
    from tiledb.cloud.vcf.vcf_toolbox.annotate import zygosity

    assert zygosity(np.array([])) == "MISSING"
    assert zygosity(np.array([0])) == "HOM_REF"
    assert zygosity(np.array([1])) == "HEMI"
    assert zygosity(np.array([2])) == "HEMI"
    assert zygosity(np.array([0, 0])) == "HOM_REF"
    assert zygosity(np.array([0, 1])) == "HET"
    assert zygosity(np.array([1, 0])) == "HET"
    assert zygosity(np.array([2, 0])) == "HET"
    assert zygosity(np.array([1, 1])) == "HOM_ALT"
    assert zygosity(np.array([1, 2])) == "HET"
    assert zygosity(np.array([2, 2])) == "HOM_ALT"
    assert zygosity(np.array([-1, -1])) == "MISSING"
    assert zygosity(np.array([1, 2, 3])) == "HET"
