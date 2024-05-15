import os
import shutil
import subprocess
from typing import Optional

import tiledb
from tiledb.cloud.utilities import process_stream


def find_index(vcf_uri: str) -> Optional[str]:
    """
    Find the index file for a VCF file or None if not found.

    :param vcf_uri: URI of the VCF file
    :return: URI of the index file
    """

    for ext in ["tbi", "csi"]:
        index = f"{vcf_uri}.{ext}"
        if tiledb.VFS().is_file(index):
            return index
    return None


def is_bgzipped(vcf_uri: str) -> bool:
    """
    Returns True if the VCF file is bgzipped.

    :param vcf_uri: URI of the VCF file
    :return: True if the VCF file is bgzipped
    """

    cmd = ("file", "-b", "-")
    rc, stdout, stderr = process_stream(vcf_uri, cmd, read_size=1024)
    if rc != 0:
        raise RuntimeError(f"Failed to check file type: {stderr}")
    return "BGZF" in stdout


def get_sample_name(vcf_uri: str) -> str:
    """
    Returns the sample name in a VCF file.

    If there are multiple samples, return a comma-separated list of sample names.

    :param vcf_uri: URI of the VCF file
    :return: sample name
    """

    cmd = ("bcftools", "query", "-l")
    rc, stdout, stderr = process_stream(vcf_uri, cmd, read_size=1024)

    if rc != 0:
        raise RuntimeError(f"Failed to get sample name: {stderr}")

    return ",".join(stdout.splitlines())


def get_record_count(vcf_uri: str, index_uri: str) -> Optional[int]:
    """
    Return the record count in a VCF file.

    :param vcf_uri: URI of the VCF file
    :param index_uri: URI of the VCF index file
    :return: record count or None if there is an error
    """

    # Create an empty VCF file in the current working directory
    # for `bcftools index -n`, which only reads the index file.
    vcf_file = os.path.basename(vcf_uri)
    open(vcf_file, "w").close()

    # Make a local copy of the index file
    local_file = os.path.basename(index_uri)
    with tiledb.VFS().open(index_uri) as infile:
        with open(local_file, "wb") as outfile:
            shutil.copyfileobj(infile, outfile, length=16 << 20)

    # Get the record count using bcftools
    cmd = ("bcftools", "index", "-n", f"{vcf_file}##idx##{local_file}")
    res = subprocess.run(cmd, capture_output=True, text=True)

    # If there is an error, this means there was a problem reading the
    # index file or the index file is an old format that does not
    # contain the required metadata. In either case, return None to
    # indicate a problem with the index that needs to be addressed
    # before ingesting the sample.
    if res.returncode != 0:
        print(res.stderr)
        return None

    return int(res.stdout)


def create_index_file(vcf_uri: str) -> str:
    """
    Create a VCF index file in the current working directory.

    :param vcf_uri: URI of the VCF file
    :return: index file name
    """

    index_file = f"{os.path.basename(vcf_uri)}.csi"

    cmd = ("bcftools", "index", "-f", "-o", index_file)
    rc, _, stderr = process_stream(vcf_uri, cmd, read_size=64 << 20)

    if rc != 0:
        raise RuntimeError(f"Failed to create index: {stderr}")

    return index_file


def sort_and_bgzip(
    vcf_uri: str,
    *,
    tmp_space: str = ".",
) -> str:
    """
    Sort and bgzip a VCF file storing the result in the tmp space.

    :param vcf_uri: URI of the VCF file
    :param tmp_space: tmp space URI, defaults to the current directory
    :return: URI of bgzipped VCF
    """

    # Normalize the tmp space URI
    tmp_space = tmp_space.rstrip("/") + "/"

    bgzip_uri = f"{os.path.basename(vcf_uri)}.gz"
    bgzip_uri = os.path.join(tmp_space, bgzip_uri)

    # Sort and bgzip the VCF file to stdout
    cmd = ("bcftools", "sort", "-Oz")
    rc, stdout, stderr = process_stream(vcf_uri, cmd, output_uri=bgzip_uri)

    if rc != 0:
        raise RuntimeError(f"Failed to sort and bgzip: {stderr}")

    return bgzip_uri
