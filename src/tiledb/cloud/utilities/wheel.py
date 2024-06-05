import os
import subprocess
import sys
import tempfile
from site import USER_SITE
from typing import Any, Mapping, Optional

import tiledb


def upload_wheel(
    *,
    wheel_path: str,
    dest_uri: str,
    config: Optional[Mapping[str, Any]] = None,
):
    """
    THIS IS AN EXPERIMENTAL API. IT MAY CHANGE IN THE FUTURE.

    Upload a local wheel file to a remote TileDB Filestore.

    The filestore will be registered when `dest_uri` uses the
    `tiledb://...s3://...` format.

    If the wheel filestore exists, it will be updated with the new wheel file.

    NOTE: The local `wheel_path` must match the file name convention specified by
    the python packaging specification:
    https://packaging.python.org/en/latest/specifications/binary-distribution-format

      {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl

    For example, a pure python wheel compatible with python 3:

      udflib-0.1-py3-none-any.whl

    :param wheel_path: path to the local wheel file
    :param dest_uri: URI where the wheel filestore will be created or updated
    :param config: config dictionary, defaults to None
    """

    # Replace '+' characters, which are not allowed in TileDB URL encoded URIs.
    # When installing the wheel, the original wheel file name will be recovered
    # from metadata.
    dest_uri = dest_uri.replace("+", ".")

    with tiledb.scope_ctx(config):
        # Create the array if it doesn't exist
        object_type = tiledb.object_type(dest_uri)
        if object_type is None:
            tiledb.Array.create(dest_uri, tiledb.ArraySchema.from_file(wheel_path))
            print(f"Created filestore at '{dest_uri}'")
        elif object_type == "group":
            raise ValueError(f"A TileDB group exists at '{dest_uri}'")

        # Copy the wheel to the array
        tiledb.Filestore.copy_from(dest_uri, wheel_path)
        print(f"Uploaded '{wheel_path}' to '{dest_uri}'")


def install_wheel(
    wheel_uri: str,
    config: Optional[Mapping[str, Any]] = None,
    verbose: bool = False,
    no_deps: bool = True,
):
    """
    THIS IS AN EXPERIMENTAL API. IT MAY CHANGE IN THE FUTURE.

    Install a wheel file from a TileDB Filestore in the current Python environment.

    :param wheel_uri: URI of the wheel file
    :param config: config dictionary, defaults to None
    :param verbose: verbose output, defaults to False
    :param no_deps: do not install dependencies, defaults to True
    """

    with tiledb.scope_ctx(config):
        # Get the original wheel file name from metadata.
        with tiledb.open(wheel_uri) as A:
            wheel_file = A.meta["original_file_name"] + "." + A.meta["file_extension"]

        with tempfile.TemporaryDirectory() as tmpdir:
            # Copy the wheel to a temporary directory
            wheel_path = os.path.join(tmpdir, wheel_file)

            tiledb.Filestore.copy_to(wheel_uri, wheel_path)

            # Install the wheel in a venv or user site
            in_venv = sys.prefix != sys.base_prefix

            cmd = [sys.executable, "-m", "pip", "install", "--force-reinstall"]
            if not in_venv:
                cmd += ["--user"]
            if no_deps:
                cmd += ["--no-deps"]
            cmd += [wheel_path]

            # Capture stdout/stderr to reduce noise from pip for a successful install.
            # (subprocess.check_output always displays stderr)
            res = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            if res.returncode != 0:
                print(f"Failed to install wheel '{wheel_path}'")
                print(res.stdout)
                print(res.stderr)
            elif verbose:
                print(res.stdout)
                print(res.stderr)

            # Modify sys.path if the wheel was installed with --user
            if not in_venv and USER_SITE not in sys.path:
                sys.path.insert(0, USER_SITE)
