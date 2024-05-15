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
    storage_uri: str,
    wheel_name: Optional[str] = None,
    config: Optional[Mapping[str, Any]] = None,
    acn: Optional[str] = None,
    namespace: Optional[str] = None,
    register: bool = True,
):
    """
    THIS IS AN EXPERIMENTAL API. IT MAY CHANGE IN THE FUTURE.

    Upload a local wheel file to a remote TileDB Filestore and optionally register
    it on TileDB Cloud.

    If the wheel filestore exists, it will be updated with the new wheel file.

    NOTE: The local `wheel_path` must match the file name convention specified by
    the python packaging specification:
    https://packaging.python.org/en/latest/specifications/binary-distribution-format

      {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl

    For example, a pure python wheel compatible with python 3:

      udflib-0.1-py3-none-any.whl

    :param wheel_path: path to the local wheel file
    :param storage_uri: URI where the wheel filestore will be created or updated
    :param wheel_name: name of registered wheel, defaults to a name based on the
        wheel file
    :param config: config dictionary, defaults to None
    :param acn: TileDB Cloud access credentials name, defaults to None
    :param namespace: TileDB Cloud namespace, defaults to the user's default namespace
    :param register: register the wheel on TileDB Cloud, defaults to True
    """

    # The wheel path may contain '+' characters, which are not allowed in TileDB URL
    # encoded URIs and array names. Replace the '+' with '.' in `wheel_file`, which
    # is used to create the storage URI and the array name. When installing the wheel,
    # the original wheel file name will be recovered from metadata.
    wheel_file = wheel_name or os.path.basename(wheel_path)
    wheel_file = wheel_file.replace("+", ".")
    array_uri = storage_uri.rstrip("/") + f"/{wheel_file}"

    namespace = namespace or tiledb.cloud.user_profile().default_namespace_charged
    tiledb_uri = f"tiledb://{namespace}/{wheel_file}"

    with tiledb.scope_ctx(config):
        # Create the array if it doesn't exist
        object_type = tiledb.object_type(array_uri)
        if object_type is None:
            print(f"Creating wheel filestore - '{array_uri}'")
            tiledb.Array.create(array_uri, tiledb.ArraySchema.from_file(wheel_path))
        elif object_type == "group":
            raise ValueError(f"A TileDB group exists at '{array_uri}'")

        if register:
            try:
                info = tiledb.cloud.info(tiledb_uri)
            except Exception as e:
                if "602" in str(e):
                    raise ValueError(f"Unrecognized namespace - '{namespace}'")
                info = None

            if info is None:
                print(f"Registering wheel filestore - '{tiledb_uri}'")
                tiledb.cloud.array.register_array(
                    array_uri,
                    namespace=namespace,
                    array_name=wheel_file,
                    access_credentials_name=acn,
                )
            elif info.uri != array_uri:
                raise ValueError(
                    f"Registered URI mismatch: '{tiledb_uri}' URI '{info.uri}' "
                    f"does not match '{array_uri}'"
                )
            else:
                print(f"Wheel filestore already registered - '{tiledb_uri}'")

        # Copy the wheel to the array
        tiledb.Filestore.copy_from(array_uri, wheel_path)
        print(f"Uploaded '{wheel_path}' to '{array_uri}'")


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
