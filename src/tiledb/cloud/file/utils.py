import io
import os
import re
import warnings
from fnmatch import fnmatch
from typing import Optional, Tuple, Union

import tiledb
from tiledb.cloud import array
from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud.rest_api import ApiException as GenApiException
from tiledb.cloud.rest_api import models

from tiledb.cloud._common import api_v2


def sanitize_filename(fname: str) -> str:
    """
    Sanitizes a filename by removing invalid characters.

    :param fname: A filename to sanitize
    :return str: The sanitized string
    """
    name, suffix = os.path.splitext(fname)
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[-_\s]+", "_", name).strip("-_")
    return name + suffix


def basename_match(file_uri: str, pattern: Optional[str] = None) -> bool:
    """
    Checks if the basename of a given file uri matches
    the given UNIX shell style pattern.

    :param file_uri: A file URI.
    :param pattern: A UNIX shell style pattern, defaults to None
    :return bool: Pattern matches the file basename or not.
    """
    return pattern is not None and fnmatch(os.path.basename(file_uri), pattern)


def upload_file_local(
    namespace: str,
    input_uri: str,
    output_uri: str,
    name: Optional[str] = None,
    access_credentials_name: Optional[str] = None,
    async_req: bool = False,
) -> api_v2.FileUploaded:
    try:
        import magic

        mime = magic.Magic(mime=True)

        files_client = client.build(api_v2.FilesApi)

        mimetype = mime.from_file(input_uri)
        with open(input_uri, mode="rb") as f:
            pos = f.tell()
            f.seek(0, io.SEEK_END)
            file_size = f.tell()
            f.seek(pos)

            kwargs = {}
            if access_credentials_name is not None:
                kwargs["x_tiledb_cloud_access_credentials_name"] = (
                    access_credentials_name
                )

            if name is not None:
                kwargs["name"] = name

            return files_client.handle_upload_file(
                namespace,
                array=output_uri,
                content_type="application/octet-stream",
                filesize=file_size,
                file=f.read(file_size),
                async_req=async_req,
                mimetype=mimetype,
                filename=os.path.basename(input_uri),
                **kwargs,
            )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def upload_file(
    namespace: str,
    input_uri: str,
    output_uri: str,
    name: Optional[str] = None,
    access_credentials_name: Optional[str] = None,
    access_credential_name: Optional[str] = None,
    async_req: bool = False,
) -> models.FileCreated:
    """
    Creates a TileDB file at the specified location
    :param namespace: namespace the create file operation belongs to
    :param name: name to use for registration in TileDB Cloud
    :param input_uri: input file uri
    :param output_uri: output array uri
    :param access_credential_name:
        DEPRECATED. Use ``access_credential_name`` instead.
    :param access_credentials_name: optional access credentials to use
    :param async_req: return future instead of results for async support
    :return: FileCreated details, including file_uuid and output_uri
    """

    if access_credential_name is not None:
        if access_credentials_name is not None:
            raise ValueError(
                "pass only access_credentials_name (plural);"
                " do not set access_credential_name (singular)"
            )
        warnings.warn(
            DeprecationWarning(
                "access_credential_name (singular) is deprecated;"
                " use access_credentials_name (plural)"
            )
        )
        access_credentials_name = access_credential_name
    del access_credential_name  # Make certain we don't use this later.

    if input_uri.startswith("file://") or "://" not in output_uri:
        return upload_file_local(
            namespace=namespace,
            input_uri=input_uri,
            output_uri=output_uri,
            name=name,
            access_credentials_name=access_credentials_name,
            async_req=async_req,
        )

    try:
        api_instance = client.build(rest_api.FilesApi)

        file_create = models.FileCreate(
            input_uri=input_uri,
            output_uri=output_uri,
            name=name,
        )

        kwargs = {}
        if access_credentials_name is not None:
            kwargs["x_tiledb_cloud_access_credentials_name"] = access_credentials_name

        return api_instance.handle_create_file(
            namespace, file_create, async_req=async_req, **kwargs
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


create_file = upload_file

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
            ).multi_index[: file_size - 1]
            # Most Python indices are [start, end), but TileDB indices are
            # [start, end], which is why we subtract 1 here.

            with vfs.open(output_uri, "wb") as fh:
                for part in iterable:
                    fh.write(part["contents"])

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

        api_instance = client.build(rest_api.FilesApi)

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
