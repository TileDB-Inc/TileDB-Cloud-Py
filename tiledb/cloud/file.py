from tiledb.cloud import client
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud.rest_api import ApiException as GenApiException
from tiledb.cloud.rest_api import models


def create_file(
    namespace: str,
    input_uri: str,
    output_uri: str,
    async_req: bool = False,
) -> models.FileCreated:
    """
    Creates a TileDB file at the specified location
    :param namespace: namespace the create file operation belongs to
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
        )

        return api_instance.handle_create_file(
            namespace,
            file_create,
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def export_file(
    namespace: str,
    file_identifier: str,
    output_uri: str,
    async_req: bool = False,
) -> models.FileExported:
    """
    Exports a TileDB File back to its original file format
    :param namespace: namespace the create file operation belongs to
    :param file_identifier: the file identifier
    :param output_uri: output file uri
    :param async_req: return future instead of results for async support
    :return: FileExported details, including output_uri
    """
    try:
        api_instance = client.client.file_api

        file_export = models.FileExport(
            output_uri=output_uri,
        )

        return api_instance.handle_export_file(
            namespace,
            file_identifier,
            file_export,
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None
