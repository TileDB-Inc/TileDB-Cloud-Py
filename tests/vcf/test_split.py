"""Unit tests for tiledb.cloud.vcf.split module."""

import os
from unittest.mock import MagicMock
from unittest.mock import patch

import tiledb.cloud
from tiledb.cloud.vcf.split import ls_samples
from tiledb.cloud.vcf.split import split_one_sample
from tiledb.cloud.vcf.split import split_vcf

# test constants
_vcf_uri = "source_vcf.vcf.gz"
_output_uri = "output"


@patch("tiledb.VFS")
@patch("gzip.GzipFile")
def test_ls_samples(mocked_gz_file: MagicMock, mocked_vfs: MagicMock) -> None:
    """Test tiledb.cloud.vcf.split.ls_samples"""

    expected = ["SampleA", "SampleB"]
    binary_exp = "\t".join(expected).encode()

    mocked_lines = [b"##SKIPME1", b"##SKIPME2", b"#CHROM\tFORMAT\t" + binary_exp]

    mocked_gz_file.return_value = mocked_lines

    observed = ls_samples(vcf_uri=_vcf_uri)

    assert observed == expected


@patch("tiledb.cloud.utilities.process_stream")
def test_split_one_sample(mock_process_stream: MagicMock) -> None:
    """Test tiledb.cloud.vcf.split.split_one_sample"""

    print(type(mock_process_stream))

    sample = "SampleA"
    mock_process_stream.return_value = (
        0,
        "stream output",
    )

    observed = split_one_sample(
        vcf_uri=_vcf_uri,
        sample=sample,
        output_uri=_output_uri,
    )

    assert observed == os.path.join(_output_uri, sample + ".vcf.gz")


@patch.object(tiledb.cloud.dag.DAG, "submit")
def test_split_vcf(mock_submit_1: MagicMock) -> None:
    """Test tiledb.cloud.vcf.split.split_vcf

    Pretty basic function that just prepares the DAG.
    Need to confirm it adds nodes based on inputs.
    """

    obs = split_vcf(
        vcf_uri=_vcf_uri,
        output_uri=_output_uri,
        namespace="namespace",
        acn="acn",
        samples=["SampleA"],
        compute=False,
    )

    assert isinstance(obs, tiledb.cloud.dag.DAG)

    # should have submitted just one node, with just one sample passed
    mock_submit_1.assert_called_once()

    assert not obs.nodes

    # call again with two samples
    # have to init a new mock
    with patch.object(tiledb.cloud.dag.DAG, "submit") as mock_submit_2:
        obs = split_vcf(
            vcf_uri=_vcf_uri,
            output_uri=_output_uri,
            namespace="namespace",
            acn="acn",
            samples=["SampleA", "SampleB"],
            compute=False,
        )

        assert mock_submit_2.call_count == 2

    # test without any samples for dynamic sample discovery
    with (
        patch.object(tiledb.cloud.dag.DAG, "submit") as mock_submit_3,
        patch.object(tiledb.cloud.dag.DAG, "submit_udf_stage") as mock_submit_udf_stage,
        patch("tiledb.cloud.utilities.run_dag") as mock_run_dag,
    ):
        # also testing with compute == True
        obs = split_vcf(
            vcf_uri=_vcf_uri,
            output_uri=_output_uri,
            namespace="namespace",
            acn="acn",
            compute=True,
        )

        mock_submit_3.assert_called_once()
        mock_submit_udf_stage.assert_called_once()
        mock_run_dag.assert_called_once()
