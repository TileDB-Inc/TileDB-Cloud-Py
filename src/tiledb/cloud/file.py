from logging import warning
from typing import Optional, Tuple, Union

from tiledb.cloud.files import utils
from tiledb.cloud.rest_api import models

warning(
    DeprecationWarning(
        "Module `file` will be deprecated from version 0.12.15 onwards. "
        "Use `tiledb.cloud.files.utils` instead."
    ),
)


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
    warning(
        DeprecationWarning(
            "This method will be deprecated from version 0.12.15 onwards. "
            "Use `tiledb.cloud.files.utils.create_file` instead."
        ),
    )
    utils.create_file(
        namespace=namespace,
        input_uri=input_uri,
        output_uri=output_uri,
        name=name,
        access_credentials_name=access_credentials_name,
        access_credential_name=access_credential_name,
        async_req=async_req,
    )


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
    warning(
        DeprecationWarning(
            "This method will be deprecated from version 0.12.15 onwards. "
            "Use `tiledb.cloud.files.utils.export_file_local` instead."
        ),
    )
    utils.export_file_local(
        uri=uri, output_uri=output_uri, timestamp=timestamp, async_req=async_req
    )


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
    warning(
        DeprecationWarning(
            "This method will be deprecated from version 0.12.15 onwards. "
            "Use `tiledb.cloud.files.utils.export_file` instead."
        ),
    )
    utils.export_file(uri=uri, output_uri=output_uri, async_req=async_req)
