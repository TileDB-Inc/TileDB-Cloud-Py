import pytest

import tiledb.cloud.vcf as vcf
import tiledb.cloud.vcf.vcf_toolbox as vtb


@pytest.mark.vcf
def test_vcf_annotation():
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
    vcf_filter = "fmt_DP > 20 and fmt_GQ > 25"

    # Add a zygosity column based on fmt_GT
    add_zygosity = True

    # Annotation array URI
    ann_uri = "tiledb://tiledb-genomics-dev/vep_20230726_6"

    # Annotation attributes to read
    ann_attrs = [
        "SYMBOL",
        "Gene",
        "Feature",
        "VARIANT_CLASS",
        "Consequence",
        "Codons",
        "Amino_acids",
    ]

    # Configure the annotation transform function
    transform_result = vtb.annotate(
        ann_uri=ann_uri,
        ann_attrs=ann_attrs,
        ann_regions=regions,
        vcf_filter=vcf_filter,
        add_zygosity=add_zygosity,
    )

    # Run the VCF query with annotation
    vcf_table = vcf.read(
        dataset_uri=vcf_uri,
        attrs=vcf_attrs,
        regions=regions,
        samples="NA12878",
        transform_result=transform_result,
    )

    assert vcf_table.num_rows == 557