import fnmatch
import logging
import os.path
import pathlib
import warnings
from typing import Any, ContextManager, Dict, Mapping, Optional
from unittest import mock

import tiledb
from tiledb.cloud import dag
from tiledb.cloud._common import utils
from tiledb.cloud.utilities import as_batch
from tiledb.cloud.utilities import get_logger_wrapper
from tiledb.cloud.utilities import run_dag

_DEFAULT_RESOURCES = {"cpu": "8", "memory": "8Gi"}
"""Default resource size; equivalent to a "large" UDF container."""


def register_dataset_udf(
    dataset_uri: str,
    *,
    register_name: str,
    acn: str,
    namespace: Optional[str] = None,
    config: Optional[Mapping[str, Any]] = None,
    verbose: bool = False,
    logging_level: int = logging.INFO,
) -> None:
    """
    Register the dataset on TileDB Cloud.

    :param dataset_uri: dataset URI
    :param register_name: name to register the dataset with on TileDB Cloud
    :param namespace: TileDB Cloud namespace, defaults to the user's default namespace
    :param config: config dictionary, defaults to None
    :param verbose: verbose logging, defaults to False
    """
    logger = get_logger_wrapper(level=logging_level)
    namespace = namespace or tiledb.cloud.user_profile().default_namespace_charged
    tiledb_uri = f"tiledb://{namespace}/{register_name}"

    with tiledb.scope_ctx(config):
        found = False
        try:
            object_type = tiledb.object_type(tiledb_uri)
            if object_type == "group":
                found = True
            elif object_type is not None:
                raise ValueError(
                    f"Another object is already registered at '{tiledb_uri}'."
                )

        except Exception:
            # tiledb.object_type raises an exception if the namespace does not exist
            logger.error(
                "Error checking if %r is registered. Bad namespace?", tiledb_uri
            )
            raise

        if found:
            logger.info("Dataset already registered at %r.", tiledb_uri)
        else:
            logger.info("Registering dataset at %r.", tiledb_uri)

            tiledb.cloud.groups.register(
                dataset_uri,
                name=register_name,
                namespace=namespace,
                credentials_name=acn,
            )


def run_ingest_workflow_udf(
    *,
    output_uri: str,
    input_uri: str,
    measurement_name: str,
    pattern: Optional[str] = None,
    extra_tiledb_config: Optional[Dict[str, object]] = None,
    platform_config: Optional[Dict[str, object]] = None,
    ingest_mode: str = "write",
    ingest_resources: Optional[Dict[str, object]] = None,
    namespace: Optional[str] = None,
    register_name: Optional[str] = None,
    acn: Optional[str] = None,
    logging_level: int = logging.INFO,
    dry_run: bool = False,
    **kwargs,
) -> Dict[str, str]:
    """
    This is the highest-level ingestor component that runs on-node. Only here
    can we do VFS with access_credentials_name -- that does not work correctly
    on the client.
    """

    # Some kwargs are eaten by the tiledb.cloud package, and won't reach
    # our child. In order to propagate these to a _grandchild_ we need to
    # package these up with different names. We use a dict as a single bag.
    carry_along: Dict[str, str] = kwargs.pop("carry_along", {})

    # For more information on "that does not work correctly on the client" please see
    # https://github.com/TileDB-Inc/TileDB-Cloud-Py/pull/512

    logger = get_logger_wrapper(level=logging_level)
    vfs = tiledb.VFS(config=extra_tiledb_config)

    input_files = []

    if vfs.is_dir(input_uri):
        for input_item in vfs.ls(input_uri):
            logger.debug(
                "Filtering directory items: input_uri=%r, input_item=%r, pattern=%r",
                input_uri,
                input_item,
                pattern,
            )

            # Subdirectories/subfolders can't be ingested.
            # Use the pattern "*.h5ad" to select only .h5ad files.
            if not vfs.is_dir(input_item) and (
                not pattern or fnmatch.fnmatch(input_item, pattern)
            ):
                logger.debug("Identified input file: input_item=%r", input_item)
                input_files.append(input_item)

    elif vfs.is_file(input_uri):
        input_files.append(input_uri)
    else:
        raise ValueError("input_uri %r is neither a file nor a directory", input_uri)

    logger.info("Building DAG for SOMA ingestion: input_files=%r", input_files)
    grf = dag.DAG(
        name=f"{'dry-run' if dry_run else 'ingest'}-h5ad-files",
        mode=dag.Mode.BATCH,
        namespace=carry_along.get("namespace", namespace),
    )
    collector = grf.submit(
        lambda output_uri: output_uri,
        output_uri=output_uri,
    )

    for input_file in input_files:
        stem = pathlib.Path(input_file).stem
        output_group_uri = os.path.join(output_uri, stem)
        logger.info(
            "Building task for h5ad file: input_file=%r, output_group_uri=%r",
            input_file,
            output_group_uri,
        )
        node = grf.submit(
            ingest_h5ad,
            output_uri=output_group_uri,
            input_uri=input_file,
            measurement_name=measurement_name,
            extra_tiledb_config=extra_tiledb_config,
            ingest_mode=ingest_mode,
            platform_config=platform_config,
            resources=ingest_resources,  # Apply propagated resources here.
            access_credentials_name=carry_along.get("access_credentials_name", acn),
            logging_level=logging_level,
            name=f"H5ad ingestion: {stem}",
            dry_run=dry_run,
        )
        collector.depends_on(node)

        if not dry_run:
            register_soma = grf.submit(
                register_dataset_udf,
                output_group_uri,
                namespace=namespace,
                register_name=register_name
                if len(input_files) == 1
                else f"{register_name} - {stem}",
                config=extra_tiledb_config,
                verbose=logging_level == logging.DEBUG,
                access_credentials_name=carry_along.get("access_credentials_name", acn),
                acn=carry_along.get("access_credentials_name", acn),
                logging_level=logging_level,
                name=f"H5ad registration: {stem}",
            )
            register_soma.depends_on(collector)

    logger.info("Computing DAG: grf=%r", grf)
    grf.compute()
    return grf.server_graph_uuid


def _hack_patch_anndata() -> ContextManager[object]:
    from anndata._core import file_backing

    @file_backing.AnnDataFileManager.filename.setter
    def filename(self, filename) -> None:
        self._filename = filename

    return mock.patch.object(file_backing.AnnDataFileManager, "filename", filename)


def ingest_h5ad(
    *,
    output_uri: str,
    input_uri: str,
    measurement_name: str,
    extra_tiledb_config: Optional[Dict[str, object]] = None,
    platform_config: Optional[Dict[str, object]] = None,
    ingest_mode: str = "write",
    logging_level: int = logging.INFO,
    dry_run: bool = False,
) -> None:
    """Performs the actual work of ingesting H5AD data into TileDB.

    :param output_uri: The output URI to write to. This will probably look like
        ``tiledb://namespace/some://storage/uri``.
    :param input_uri: The URI of the H5AD file to read from. This file is read
        using TileDB VFS, so any path supported (and accessible) will work.
    :param measurement_name: The name of the Measurement within the Experiment
        to store the data.
    :param extra_tiledb_config: Extra configuration for TileDB.
    :param platform_config: The SOMA ``platform_config`` value to pass in,
        if any.
    :param ingest_mode: One of the ingest modes supported by
        ``tiledbsoma.io.read_h5ad``.
    :param dry_run: If provided and set to ``True``, does the input-path
        traversals without ingesting data.
    """

    import anndata
    import tiledbsoma
    import tiledbsoma.logging
    from tiledbsoma import io

    # Oddly, "higher" debug levels (more verbose) are smaller numbers within
    # the Python logging package.
    logging.basicConfig(level=logging_level)
    if logging_level <= logging.DEBUG:
        tiledbsoma.logging.debug()
    elif logging_level <= logging.INFO:
        tiledbsoma.logging.info()

    # While h5ad supports any file-like object, annndata specifically
    # wants only an `os.PathLike` object. The only thing it does with
    # the PathLike is to use it to get the filename.
    class _FSPathWrapper:
        """Tricks anndata into thinking a file-like object is an os.PathLike.

        While h5ad supports any file-like object, anndata specifically wants
        an os.PathLike object, which it uses *exclusively* to get the "filename"
        of the opened file.

        We need to provide ``__fspath__`` as a real class method, so simply
        setting ``some_file_obj.__fspath__ = lambda: "some/path"`` won't work,
        so here we just proxy all attributes except ``__fspath__``.
        """

        def __init__(self, obj: object, path: str) -> None:
            self._obj = obj
            self._path = path

        def __fspath__(self) -> str:
            return self._path

        def __getattr__(self, name: str) -> object:
            return getattr(self._obj, name)

    soma_ctx = tiledbsoma.SOMATileDBContext()
    if extra_tiledb_config:
        soma_ctx = soma_ctx.replace(tiledb_config=extra_tiledb_config)

    with tiledb.VFS(ctx=soma_ctx.tiledb_ctx).open(input_uri) as input_file:
        if dry_run:
            logging.info("Dry run for %s to %s", input_uri, output_uri)
            return

        with _hack_patch_anndata():
            try:
                input_data = anndata.read_h5ad(
                    _FSPathWrapper(input_file, input_uri), "r"
                )
            except Exception as h5exc:
                raise RuntimeError(
                    f"Failed to read file {input_file!r} wrapping {input_uri!r}"
                ) from h5exc

        output_uri = io.from_anndata(
            experiment_uri=output_uri,
            anndata=input_data,
            measurement_name=measurement_name,
            context=soma_ctx,
            ingest_mode=ingest_mode,
            platform_config=platform_config,
        )
    logging.info("Successfully wrote data from %s to %s", input_uri, output_uri)


def run_ingest_workflow(
    *,
    output_uri: str,
    input_uri: str,
    measurement_name: str,
    pattern: Optional[str] = None,
    extra_tiledb_config: Optional[Dict[str, object]] = None,
    platform_config: Optional[Dict[str, object]] = None,
    ingest_mode: str = "write",
    ingest_resources: Optional[Dict[str, object]] = None,
    namespace: Optional[str] = None,
    register_name: Optional[str] = None,
    acn: Optional[str] = None,
    logging_level: int = logging.INFO,
    dry_run: bool = False,
    **kwargs,
) -> Dict[str, str]:
    """Starts a workflow to ingest H5AD data into SOMA.

    :param output_uri: The output URI to write to. This will probably look like
        ``tiledb://namespace/some://storage/uri``.
    :param input_uri: The URI of the H5AD file(s) to read from. These are read
        using TileDB VFS, so any path supported (and accessible) will work.  If the
        ``input_uri`` passes ``vfs.is_file``, it's ingested.  If the ``input_uri``
        passes ``vfs.is_dir``, then all first-level entries are ingested .  In the
        latter, directory case, an input file is skipped if ``pattern`` is provided
        and doesn't match the input file. As well, in the directory case, each entry's
        basename is appended to the ``output_uri`` to form the entry's output URI.
        For example, if ``a.h5ad` and ``b.h5ad`` are present within ``input_uri`` of
        ``s3://bucket/h5ads/`` and ``output_uri`` is
        ``tiledb://namespace/s3://bucket/somas``, then
        ``tiledb://namespace/s3://bucket/somas/a`` and
        ``tiledb://namespace/s3://bucket/somas/b`` are written.
    :param measurement_name: The name of the Measurement within the Experiment
        to store the data.
    :param pattern: As described for ``input_uri``.
    :param extra_tiledb_config: Extra configuration for TileDB.
    :param platform_config: The SOMA ``platform_config`` value to pass in,
        if any.
    :param ingest_mode: One of the ingest modes supported by
        ``tiledbsoma.io.read_h5ad``.
    :param ingest_resources: A specification for the amount of resources to provide
        to the UDF executing the ingestion process, to override the default.
    :param namespace: An alternate namespace to run the ingestion process under.
    :param register_name: name to register the dataset with on TileDB Cloud.
    :param acn: The name of the credentials to pass to the executing UDF.
    :param dry_run: If provided and set to ``True``, does the input-path
        traversals without ingesting data.
    :return: A dictionary of ``{"status": "started", "graph_id": ...}``,
        with the UUID of the graph on the server side, which can be used to
        manage execution and monitor progress.
    """
    ingest_resources = ingest_resources or _DEFAULT_RESOURCES

    # Demand for mutual exclusion of the two arguments and existence.
    access_credentials_name = kwargs.pop("access_credentials_name", None)
    if bool(acn) == bool(access_credentials_name):
        raise ValueError(
            "Ingestion graph requires either 'acn' or 'access_credentials_name'"
            " (deprecated), cannot decipher correct credential when both specified."
        )
    # Backwards compatibility: Assign when only access_credentials_name is set
    if not acn:
        acn = access_credentials_name
        warnings.warn(
            DeprecationWarning(
                "The 'access_credentials_name' parameter is about to be"
                "deprecated and will be removed in future versions."
                "Please use the 'acn' parameter instead."
            )
        )

    try:
        ns, dst = utils.split_uri(output_uri)
        namespace = namespace or ns
        # Ensure compatibility with "tiledb://<namespace>/<bucket-path>"
        # style URIs
        if "://" in dst:
            output_uri = dst
    except ValueError:
        pass

    if not register_name:
        register_name = pathlib.Path(output_uri).stem

    # Graph init
    grf = dag.DAG(
        name="ingest-h5ad-launcher",
        namespace=namespace,
        mode=dag.Mode.BATCH,
    )

    # Step 1: Ingest workflow UDF
    carry_along: Dict[str, str] = {
        "access_credentials_name": acn,
    }

    grf.submit(
        run_ingest_workflow_udf,
        output_uri=output_uri,
        input_uri=input_uri,
        measurement_name=measurement_name,
        pattern=pattern,
        extra_tiledb_config=extra_tiledb_config,
        platform_config=platform_config,
        ingest_mode=ingest_mode,
        ingest_resources=ingest_resources,
        namespace=namespace,
        register_name=register_name,
        access_credentials_name=acn,
        carry_along=carry_along,
        logging_level=logging_level,
        dry_run=dry_run,
    )

    # Start the ingestion process
    verbose = logging_level == logging.DEBUG
    run_dag(grf, debug=verbose)

    # Get the initial graph node UUID
    the_node = next(iter(grf.nodes.values()))
    real_graph_uuid = the_node.result()
    return {
        "status": "started",
        "graph_id": str(real_graph_uuid),
    }


ingest = as_batch(run_ingest_workflow)
