import base64
import os
import re
import urllib.parse
import warnings
from fnmatch import fnmatch
from typing import Mapping, Optional, Tuple, Union

import tiledb
import tiledb.cloud.tiledb_cloud_error as tce
from tiledb.cloud import array
from tiledb.cloud import client
from tiledb.cloud import config
from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud._common import utils
from tiledb.cloud.rest_api import ApiException as GenApiException
from tiledb.cloud.rest_api import configuration
from tiledb.cloud.rest_api import models


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


def create_file(
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
        raise tiledb_cloud_error.maybe_wrap(exc) from None


_EXPORT_CHUNK_SIZE = 512 * 1024 * 1024
"""The number of bytes we will attempt to read at once when exporting a file."""


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
            with vfs.open(output_uri, "wb") as fh:
                # We can't multi_index with return_incomplete over a dense array
                # so here we manually chunk our request.
                for start in range(0, file_size, _EXPORT_CHUNK_SIZE):
                    end = min(start + _EXPORT_CHUNK_SIZE, file_size)
                    part = A.query(
                        attrs=["contents"],
                        order="C",
                    )[:end]
                    fh.write(part["contents"])
                    # Get rid of this immediately so the GC can claim it ASAP
                    # if needed.
                    del part

        return models.FileExported(output_uri=output_uri)

    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


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
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def upload_file(
    input_uri: str,
    output_uri: str,
    *,
    filename: Optional[str] = None,
    content_type: str = "application/octet-stream",
    access_credentials_name: Optional[str] = None,
) -> str:
    """Uploads a file to TileDB Cloud.

    :param input_uri: The URI or path of the input file. May be an ordinary path
        or any URI accessible via TileDB VFS.
    :param output_uri: The TileDB URI to write the file to.
    :param filename: If present, the value to store as the original filename.
    :param content_type: The MIME type of the file.
    :param access_credentials_name: If present, the name of the credentials
        to use when writing the uploaded file to backend storage instead of
        the defaults.
    :return: The ``tiledb://`` URI of the uploaded file.
    """
    namespace, name = array.split_uri(output_uri)
    client.user_profile
    vfs = tiledb.VFS()

    with vfs.open(input_uri, "rb") as infile:
        size = infile.seek(0, 2)
        infile.seek(0)
        headers = {
            "content-type": content_type,
            **_auth_headers(config.config),
        }
        if access_credentials_name:
            headers["x-tiledb-cloud-access-credentials-name"] = access_credentials_name

        pool = client.client._client_v2.rest_client.pool_manager

        query = urllib.parse.urlencode(
            {
                "filename": filename or os.path.basename(input_uri),
                "filesize": size,
            }
        )

        namespace = urllib.parse.quote(namespace)
        name = urllib.parse.quote(name, safe="")

        request_url = (
            f"{config.config.host}/v2/notebooks/{namespace}/{name}/upload?{query}"
        )

        while True:
            resp = pool.request(
                method="POST",
                url=request_url,
                body=infile,
                headers=headers,
                chunked=True,
                redirect=False,
            )
            try:
                request_url = resp.get_redirect_location()
                if request_url:
                    # If we got redirected, we need to rewind the file
                    # so we can send it to the actual location.
                    infile.seek(0)
                    continue
                json_response = resp.json()
                if not 200 <= resp.status < 300:
                    raise tce.TileDBCloudError(json_response["message"])
                return json_response["output_uri"]
            except (KeyError, ValueError) as base:
                raise tce.TileDBCloudError(resp.data) from base
            finally:
                utils.release_connection(resp)


def _auth_headers(cfg: configuration.Configuration) -> Mapping[str, object]:
    key = cfg.get_api_key_with_prefix("X-TILEDB-REST-API-KEY")
    if key:
        return {"x-tiledb-rest-api-key": key}
    if cfg.username and cfg.password:
        basic = base64.b64encode(f"{cfg.username}:{cfg.password}".encode("utf-8"))
        return {"authorization": basic}
    return {}
    # No authentication has been provided. Do nothing.
