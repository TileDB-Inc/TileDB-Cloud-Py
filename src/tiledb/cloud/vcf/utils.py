import os
import subprocess
import tempfile
import tiledb
from tiledb.cloud.utilities import process_stream


def find_index(vcf_uri: str) -> str:
    """
    Find the index file for a VCF file or an empty string if not found.

    :param vcf_uri: URI of the VCF file
    :return: URI of the index file
    """

    for ext in ["tbi", "csi"]:
        index = f"{vcf_uri}.{ext}"
        if tiledb.VFS().is_file(index):
            return index
    return ""


def is_bgzipped(vcf_uri: str) -> bool:
    """
    Returns True if the VCF file is bgzipped.

    :param vcf_uri: URI of the VCF file
    :return: True if the VCF file is bgzipped
    """

    cmd = "file -b -"
    stdout, stderr = process_stream(vcf_uri, cmd, read_size=1024)
    if stderr:
        raise RuntimeError(f"Failed to check file type: {stderr}")
    return "BGZF" in stdout


def get_sample_name(vcf_uri: str) -> str:
    """
    Returns the sample name in a VCF file.

    If there are multiple samples, return a comma-separated list of sample names.

    :param vcf_uri: URI of the VCF file
    :return: sample name
    """

    cmd = "bcftools query -l"
    stdout, stderr = process_stream(vcf_uri, cmd, read_size=1024)
    if stderr:
        raise RuntimeError(f"Failed to get sample names: {stderr}")
    return ",".join(stdout.splitlines())


def get_record_count(vcf_uri: str, index_uri: str) -> int:
    """
    Return the record count in a VCF file.

    :param vcf_uri: URI of the VCF file
    :param index_uri: URI of the VCF index file
    :return: record count or 0 if there is an error
    """

    # Create an empty VCF file in the current working directory
    # for `bcftools index -n`, which only reads the index file.
    vcf_file = os.path.basename(vcf_uri)
    open(vcf_file, "w").close()

    # Make a local copy of the index file.
    local_file = os.path.basename(index_uri)
    # tiledb.VFS().copy_file(index_uri, local_file)
    cmd = f"cp /dev/stdin {local_file}"
    _, stderr = process_stream(index_uri, cmd)
    if stderr:
        raise RuntimeError(f"Failed to create index: {stderr}")

    # Get the record count using bcftools
    cmd = f"bcftools index -n {vcf_file}##idx##{local_file}"
    res = subprocess.run(cmd.split(), capture_output=True, text=True)

    # If there is an error, this means there was a problem reading the
    # index file or the index file is an old format that does not
    # contain the required metadata. In either case, return 0 to
    # indicate a problem with the index that needs to be addressed
    # before ingesting the sample.
    if res.stderr:
        print(res.stderr)
        return 0

    return int(res.stdout)


def create_index_file(vcf_uri: str) -> str:
    """
    Create a VCF index file in the current working directory.

    :param vcf_uri: URI of the VCF file
    :return: index file name
    """

    index_file = f"{os.path.basename(vcf_uri)}.csi"

    cmd = f"bcftools index -f -o {index_file}"
    _, stderr = process_stream(vcf_uri, cmd, read_size=64 << 20)
    if stderr:
        raise RuntimeError(f"Failed to create index: {stderr}")

    return index_file


def bgzip_and_index(vcf_uri: str) -> str:
    """
    Create a bgzipped VCF file and index file in the current working directory.

    :param vcf_uri: URI of the VCF file
    :return: bgzipped VCF file name
    """

    bgzip_file = f"{os.path.basename(vcf_uri)}.gz"

    cmd = f"bcftools view -Oz -o {bgzip_file}"
    _, stderr = process_stream(vcf_uri, cmd)
    if stderr:
        raise RuntimeError(f"Failed to bgzip: {stderr}")

    create_index_file(bgzip_file)

    return bgzip_file
