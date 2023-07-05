import logging
from typing import ContextManager, Dict, Optional
from unittest import mock

import tiledb
from tiledb.cloud import dag
from tiledb.cloud._common import functions

_DEFAULT_RESOURCES = {"cpu": "8", "memory": "8Gi"}
"""Default resource size; equivalent to a "large" UDF container."""


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
    extra_tiledb_config: Optional[Dict[str, object]],
    platform_config: Optional[Dict[str, object]],
    ingest_mode: str,
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
    """

    import anndata
    import tiledbsoma
    import tiledbsoma.logging as somalog
    from tiledbsoma import io

    logging.basicConfig(level=logging.INFO)
    somalog.info()

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
    with tiledb.VFS().open(input_uri) as input_file:
        with _hack_patch_anndata():
            input_data = anndata.read_h5ad(_FSPathWrapper(input_file, input_uri), "r")
        output_uri = io.from_anndata(
            experiment_uri=output_uri,
            anndata=input_data,
            measurement_name=measurement_name,
            context=soma_ctx,
            ingest_mode=ingest_mode,
            platform_config=platform_config,
        )
    logging.info("Successfully wrote data from %r to %r", input_uri, output_uri)


# Until we fully get this version of tiledb.cloud deployed server-side, we want
# to refer to `ingest_h5ad` by value rather than by reference.
_ingest_h5ad_byval = functions.to_register_by_value(ingest_h5ad)


def run_ingest_workflow(
    *,
    output_uri: str,
    input_uri: str,
    measurement_name: str,
    extra_tiledb_config: Optional[Dict[str, object]] = None,
    platform_config: Optional[Dict[str, object]] = None,
    ingest_mode: str = "write",
    resources: Optional[Dict[str, object]] = None,
    namespace: Optional[str] = None,
    access_credentials_name: Optional[str] = None,
) -> Dict[str, str]:
    """Starts a workflow to ingest H5AD data into SOMA.

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
    :param resources: A specification for the amount of resources to provide
        to the UDF executing the ingestion process, to override the default.
    :param namespace: An alternate namespace to run the ingestion process under.
    :param access_credentials_name: If provided, the name of the credentials
        to pass to the executing UDF.
    :return: A dictionary of ``{"status": "started", "graph_id": ...}``,
        with the UUID of the graph on the server side, which can be used to
        manage execution and monitor progress.
    """

    grf = dag.DAG(
        name="ingest-h5ad-file",
        mode=dag.Mode.BATCH,
        namespace=namespace,
    )
    grf.submit(
        _ingest_h5ad_byval,
        output_uri=output_uri,
        input_uri=input_uri,
        measurement_name=measurement_name,
        extra_tiledb_config=extra_tiledb_config,
        ingest_mode=ingest_mode,
        platform_config=platform_config,
        resources=_DEFAULT_RESOURCES if resources is None else resources,
        access_credentials_name=access_credentials_name,
    )
    grf.compute()
    return {
        "status": "started",
        "graph_id": str(grf.server_graph_uuid),
    }
