from typing import Optional, Tuple, Union

from tiledb.cloud.rest_api import models


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
    DEPRECATED METHOD: Will be removed from version 0.12.16.
    Use `tiledb.cloud.files.utils.create_file instead.

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
    raise DeprecationWarning(
        "This method is deprecated. "
        "Use `tiledb.cloud.files.utils.create_file instead."
    )


def export_file_local(
    uri: str,
    output_uri: str,
    timestamp: Union[Tuple[int, int], int, None] = None,
    async_req: bool = False,
) -> models.FileExported:
    """
    DEPRECATED METHOD: Will be removed from version 0.12.16.
    Use `tiledb.cloud.files.utils.export_file_local` instead.

    Exports a TileDB File back to its original file format
    :param uri: The ``tiledb://...`` URI of the file to export
    :param output_uri: output file uri
    :param tuple timestamp: (default None) If int, open the array at a given TileDB
        timestamp. If tuple, open at the given start and end TileDB timestamps.
    :param async_req: return future instead of results for async support
    :return: FileExported details, including output_uri
    """
    raise DeprecationWarning(
        "This is deprecated. "
        "Use `tiledb.cloud.files.utils.export_file_local` instead."
    )


def export_file(
    uri: str,
    output_uri: str,
    async_req: bool = False,
) -> models.FileExported:
    """
    DEPRECATED METHOD: Will be removed from version 0.12.16.
    Use `tiledb.cloud.files.utils.export_file` instead.

    Exports a TileDB File back to its original file format
    :param uri: The ``tiledb://...`` URI of the file to export
    :param output_uri: output file uri
    :param async_req: return future instead of results for async support
    :return: FileExported details, including output_uri
    """
    raise DeprecationWarning(
        "This method is deprecated. "
        "Use `tiledb.cloud.files.utils.export_file` instead."
    )
