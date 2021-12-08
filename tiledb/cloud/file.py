from typing import Optional, Tuple, Union

import tiledb
from tiledb.cloud import array
from tiledb.cloud import client
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud.rest_api import ApiException as GenApiException
from tiledb.cloud.rest_api import models


def create_file(
    namespace: str,
    input_uri: str,
    output_uri: str,
    name: Optional[str] = None,
    async_req: bool = False,
) -> models.FileCreated:
    """
    Creates a TileDB file at the specified location
    :param namespace: namespace the create file operation belongs to
    :param name: name to use for registration in TileDB Cloud
    :param input_uri: input file uri
    :param output_uri: output array uri
    :param async_req: return future instead of results for async support
    :return: FileCreated details, including file_uuid and output_uri
    """
    try:
        api_instance = client.client.file_api

        file_create = models.FileCreate(
            input_uri=input_uri,
            output_uri=output_uri,
            name=name,
        )

        return api_instance.handle_create_file(
            namespace,
            file_create,
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def export_file_local(
    uri: str,
    output_uri: str,
    timestamp: Union[Tuple[int, int], int, None] = None,
    async_req: bool = False,
) -> models.FileExported:
    """
    Exports a TileDB File back to its original file format
    :param uri: The ``tiledb://...`` URI of the file to export
    :param output_uri: output file uri
    :param tuple timestamp: (default None) If int, open the array at a given TileDB
        timestamp. If tuple, open at the given start and end TileDB timestamps.
    :param async_req: return future instead of results for async support
    :return: FileExported details, including output_uri
    """
    try:
        ctx = client.Ctx()
        vfs = tiledb.VFS(ctx=ctx)
        with tiledb.open(uri, ctx=ctx, timestamp=timestamp) as A:
            file_size = A.meta["file_size"]
            # Row major partial export of single attribute
            iterable = A.query(
                attrs=["contents"], return_incomplete=True, order="C"
            ).multi_index[0:file_size]

            fh = vfs.open(output_uri, "wb")
            for part in iterable:
                vfs.write(fh, part["contents"])

            vfs.close(fh)

        return models.FileExported(output_uri=output_uri)

    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def export_file(
    uri: str,
    output_uri: str,
    async_req: bool = False,
) -> models.FileExported:
    """
    Exports a TileDB File back to its original file format
    :param uri: The ``tiledb://...`` URI of the file to export
    :param output_uri: output file uri
    :param async_req: return future instead of results for async support
    :return: FileExported details, including output_uri
    """
    try:
        (namespace, name) = array.split_uri(uri)

        api_instance = client.client.file_api

        if output_uri.startswith("file://") or "://" not in output_uri:
            return export_file_local(
                uri=uri, output_uri=output_uri, async_req=async_req
            )

        file_export = models.FileExport(
            output_uri=output_uri,
        )

        return api_instance.handle_export_file(
            namespace,
            name,
            file_export,
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None
