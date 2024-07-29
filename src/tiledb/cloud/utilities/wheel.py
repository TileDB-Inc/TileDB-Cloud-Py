"""Install and upload Python packages via a wheel path or from PyPI.

Please be aware, this module is experimental as we explore installing
private Python wheels at runtime.
"""

import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from dataclasses import field
from typing import Any, List, Mapping, Optional, Sequence

import tiledb
from tiledb.cloud.utilities import get_logger

logger = get_logger()
logger.propagate = False


def upload_wheel(
    *,
    wheel_path: str,
    dest_uri: str,
    config: Optional[Mapping[str, Any]] = None,
    overwrite: bool = False,
) -> None:
    """Upload a local wheel to TileDB Filestore.

    Note: THIS IS AN EXPERIMENTAL API. IT MAY CHANGE IN THE FUTURE.

    The filestore will be registered when `dest_uri` uses the
    `tiledb://...s3://...` format.

    If the wheel filestore exists, it will be updated with the new wheel file.

    NOTE: The local `wheel_path` must match the file name convention specified by
    the python packaging specification:
    https://packaging.python.org/en/latest/specifications/binary-distribution-format

      {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl

    For example, a pure python wheel compatible with python 3:

      udflib-0.1-py3-none-any.whl

    :param wheel_path: Path to the local wheel file.
    :param dest_uri: URI where the wheel filestore will be created or updated.
    :param config: TileDB config.
    :param overwrite: Whether to overwrite a registered wheel if one exists.
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
            logger.info(f"Created filestore at '{dest_uri}'")
        elif object_type == "group":
            raise ValueError(f"A TileDB group exists at '{dest_uri}'")
        elif object_type == "array" and not overwrite:
            raise ValueError(
                f"Wheel already exists at URI: {dest_uri}, toggle 'overwrite'"
                " to overwrite existing wheel."
            )

        # Copy the wheel to the array
        tiledb.Filestore.copy_from(dest_uri, wheel_path)
        logger.info(f"Uploaded '{wheel_path}' to '{dest_uri}'")


@dataclass
class PipInstall:
    """Pip installer."""

    wheel: str
    """Wheel URI or alternatively library name."""
    in_venv: bool
    """Whether in an active env."""
    no_deps: bool = True
    """Whether to install dependencies."""
    runtime: str = field(init=False)
    """Path to python runtime exec."""

    def __post_init__(self) -> None:
        from sys import executable

        self.runtime = executable

    @property
    def wheel_ext(self) -> bool:
        """Verify self.wheel has proper wheel extension.

        :returns: Whether wheel is formatted properly.
        """

        parsed = os.path.splitext(self.wheel)
        if parsed[-1] in (".whl", ".wheel"):
            return True
        else:
            return False

    @staticmethod
    def rm_from_cache(cached_libs: Sequence[str]) -> List[str]:
        """Libraries to remove from Python cache after install.

        In cases where the interpreter cannot be refreshed between install
        and execution (UDFs, task graphs), cached Python libraries
        from the image they were installed in during build will be
        prioritized over libraries installed as part of this class. This method To
        removes these libraries so that a cached library does not conflict with a
        new library installed at runtime.

        :param cached_libs: Libraries in cache to remove.
        :returns: Libraries that were found and deleted from Python cache.
        """

        deleted = []
        for lib in cached_libs:
            try:
                del sys.modules[lib]
                deleted.append(lib)
            except KeyError:
                logger.debug(f"{lib} not in cache, skipping cache removal.")
                continue

        logger.info("Cached libraries removed:\n\t> %s" % "\n\t> ".join(deleted))

        return deleted

    def install(
        self,
        wheel: str,
        deps_to_refresh: Optional[Sequence[str]] = None,
    ) -> subprocess.CompletedProcess:
        """Install wheel.

        :param wheel: URI to registered wheel or name of library to install
            from PyPI.
        :returns: Completed process signature.
        """

        cmd = [
            self.runtime,
            "-m",
            "pip",
            "install",
            "--force-reinstall",
        ]

        if not self.in_venv:
            cmd += ["--user"]
        if self.no_deps:
            cmd += ["--no-deps"]

        cmd += [wheel]

        # Capture stdout/stderr to reduce noise from pip for a successful install.
        # (subprocess.check_output always displays stderr)
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if deps_to_refresh:
            PipInstall.rm_from_cache(cached_libs=deps_to_refresh)

        return res


def install_wheel(
    wheel_uri: str,
    config: Optional[Mapping[str, Any]] = None,
    verbose: bool = False,
    no_deps: bool = True,
    deps_to_refresh: Optional[Sequence[str]] = None,
) -> None:
    """Install at runtime a Python wheel from TiileDB Filestore or PyPI.

    Note: THIS IS AN EXPERIMENTAL API. IT MAY CHANGE IN THE FUTURE.

    Attempt to install a wheel file from a TileDB Filestore. If `wheel_uri`
    does not point to a .wheel file, assume it is the name of a public
    Python library and attempt to install from PyPI.

    :param wheel_uri: URI of the wheel file or name of library in PyPI.
    :param config: TileDB Config.
    :param verbose: Verbose output, defaults to False.
    :param no_deps: Do not install dependencies, defaults to True.
    :param deps_to_refresh: Dependencies to refresh from cache.
    """

    installer = PipInstall(
        wheel=wheel_uri,
        in_venv=sys.prefix != sys.base_prefix,
        no_deps=no_deps,
    )

    if installer.wheel_ext:
        with tiledb.scope_ctx(config):
            # Get the original wheel file name from metadata.
            with tiledb.open(wheel_uri) as A:
                wheel_file = (
                    A.meta["original_file_name"] + "." + A.meta["file_extension"]
                )

            with tempfile.TemporaryDirectory() as tmpdir:
                # Copy the wheel to a temporary directory
                wheel_path = os.path.join(tmpdir, wheel_file)
                tiledb.Filestore.copy_to(wheel_uri, wheel_path)

    # attempt to install from PyPI, assume library name given
    else:
        wheel_path = None

    res = installer.install(
        wheel=wheel_path or wheel_uri,
        deps_to_refresh=deps_to_refresh,
    )

    if res.returncode != 0:
        logger.info(f"Failed to install wheel '{wheel_uri}'")
        print(res.stdout)
        print(res.stderr)
    elif verbose:
        print(res.stdout)
        print(res.stderr)

    # Modify sys.path if the wheel was installed with --user
    from site import USER_SITE

    if not installer.in_venv and sys.path[0] != USER_SITE:
        logger.debug(f"Inserting {USER_SITE} into sys.path")
        sys.path.insert(0, USER_SITE)
