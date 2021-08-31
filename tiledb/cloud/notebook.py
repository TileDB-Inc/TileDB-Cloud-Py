"""
Python support for notebook I/O on Tiledb Cloud. All notebook JSON content
is assumed to be encoded as UTF-8.

"""

import posixpath
import time
from typing import Optional, Tuple

import numpy
import tiledb

from . import array, client, rest_api, tiledb_cloud_error
from .rest_api import ApiException as GenApiException
from .rest_api import rest


RESERVED_NAMESPACES = frozenset(["cloud", "owned", "public", "shared"])
CHARACTER_ENCODING = "utf-8"


def rename_notebook(
    uri,
    notebook_name=None,
    access_credentials_name=None,
    async_req=False,
):
    """
    Update an array's info
    :param str namespace: optional username or organization array should be
      registered under. If unset will default to the user
    :param str array_name: name of notebook to rename to
    :param str access_credentials_name: optional name of access credentials to
      use, if left blank default for namespace will be used
    :param async_req: return future instead of results for async support
    """
    api_instance = client.client.notebook_api
    (namespace, current_notebook_name) = array.split_uri(uri)

    try:
        return api_instance.update_notebook_name(
            namespace=namespace,
            array=current_notebook_name,
            notebook_metadata=rest_api.models.ArrayInfoUpdate(
                name=notebook_name,
                uri=uri,
                access_credentials_name=access_credentials_name,
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def download_ipnyb_file_name_from_cloud(
    tiledb_uri: str,
    storage_credential_name: str,
    ipynb_file_name: str,
) -> None:
    """
    Downloads a notebook file from TileDB Cloud to local disk.
    :param tiledb_uri: such as "tiledb://TileDB-Inc/quickstart_dense".
    :param storage_credential_name: such as "janedoe-creds", typically from the
      user's account settings.
    :param ipnyb_file_name: path to save to, such as "./mycopy.ipynb". Must be
      local; no S3 URI support at present.
    """
    ipynb_file_contents = download_ipnyb_file_contents_from_cloud(
        tiledb_uri,
        storage_credential_name,
    )
    with open(ipynb_file_name, "w") as handle:
        handle.write(ipynb_file_contents)


def download_ipnyb_file_contents_from_cloud(
    tiledb_uri: str,
    storage_credential_name: str,
) -> str:
    """
    Downloads a notebook file from TileDB Cloud to contents as a string,
      nominally in JSON format.
    :param tiledb_uri: such as "tiledb://TileDB-Inc/quickstart_dense".
    :param storage_credential_name: such as "janedoe-creds", typically from the
      user's account settings.
    :return: contents of the notebook file as a string, nominally in JSON format.
    """
    ctx = tiledb.cloud.Ctx(
        {
            "rest.creation_access_credentials_name": storage_credential_name,
        }
    )
    with tiledb.open(tiledb_uri, "r", ctx=ctx) as arr:
        size = arr.meta["file_size"]
        data = arr.query(attrs=["contents"])[slice(0, size)]
        json = data["contents"].tobytes().decode("utf-8", "backslashreplace")
        return json


# TODO: auto-increment/overwrite logic
# If the destination array name already exists -- e.g. uploading 'foo.ipynb' to
# 'testing-upload' -- there are three options:
# 1. Fail the upload with 'already exists' and require the user to supply a
#    different path. No clobbering
# 2. Auto-increment the array name, e.g. from 'testing-upload' to 'testing-upload-1'
#    and then 'testing-upload-2' the next time, and so on.
# 3. Overwrite
#
# Thoughts:
# * Option 3 isn't a safe default -- for those who want it it's fine but for
#   those who don't it can be seen as unwelcome data loss.
# * Option 2 is a not-bad default -- there is no data loss, but some users
#   might be left feeling 'Why are you creating all these versions? I just
#   want to update one notebook, not have twenty copies."
# * Option 1 is a safe default -- there is no data loss and no profusion of
#   copies. However, it is more frictional for the user, requiring them to
#   make the decision.
#
# Implementation:
#
# * We could have a force-overwrite argument, optional, default False.
# * We could have a behavior-on-exist argument, of enum type, 3 cases, one
#   for each of the options above.
#
# Status: As of this writing: we have implemented option 1, and we don't have
# an overwrite/update-in-place flag.
def upload_ipnyb_file_name_to_cloud(
    ipynb_file_name: str,
    namespace: str,
    array_name: str,
    storage_path: str,
    storage_credential_name: str,
) -> str:
    """
    Uploads a local-disk notebook file to TileDB Cloud.
    :param ipnyb_file_name: such as "./mycopy.ipynb". Must be local; no S3 URI
      support at present.
    :param namespace: such as "janedoe"
    :param array_name : name to be seen in the UI, such as "testing-upload"
    :param storage_path: such as "s3://acmecorp-janedoe", typically from the
      user's account settings.
    :param storage_credential_name: such as "janedoe-creds", typically from the
      user's account settings.
    :return: TileDB array name, such as "tiledb://janedoe/testing-upload".
    """

    with open(ipynb_file_name, "r") as handle:
        ipynb_file_contents = handle.read()

    return upload_ipnyb_file_contents_to_cloud(
        ipynb_file_contents,
        storage_path,
        array_name,
        namespace,
        storage_credential_name,
    )


def upload_ipnyb_file_contents_to_cloud(
    ipynb_file_contents: str,
    storage_path: str,
    array_name: str,
    namespace: str,
    storage_credential_name: str,
) -> str:
    """
    Uploads a notebook file to TileDB Cloud.
    :param ipnyb_file_contents: The contents of the notebook file as a string,
      nominally in JSON format.
    :param storage_path: such as "s3://acmecorp-janedoe", typically from the
      user's account settings.
    :param array_name : name to be seen in the UI, such as "testing-upload"
    :param namespace: such as "janedoe".
    :param storage_credential_name: such as "janedoe-creds", typically from the
      user's account settings.
    :return: TileDB array name, such as "tiledb://janedoe/testing-upload".
    """

    ctx = tiledb.cloud.Ctx(
        {
            "rest.creation_access_credentials_name": storage_credential_name,
        }
    )

    tiledb_uri, array_name = _create_notebook_array(
        storage_path,
        array_name,
        namespace,
        ctx,
    )

    _write_notebook_to_array(tiledb_uri, ipynb_file_contents, ctx)

    return tiledb_uri


def _create_notebook_array(
    storage_path: str,
    array_name: str,
    namespace: str,
    ctx: tiledb.Ctx,
    *,
    retries: Optional[int] = 0,
) -> Tuple[str, str]:
    """
    Creates a new array for storing a notebook file.
    :param storage_path: such as "s3://acmecorp-janedoe", typically from the
      user's account settings.
    :param array_name : name to be seen in the UI, such as "testing-upload"
    :param namespace: such as "janedoe".
    :param ctx: cloud context for the operation.
    :return: tuple of tiledb_uri and array_name
    """

    if namespace in RESERVED_NAMESPACES:
        raise ValueError(
            f"{namespace!r} is not a valid folder to create notebooks. "
            "Please select a proper namespace (username or organization name).",
        )

    tries = 1 + retries  # 1st + rest
    while tries > 0:
        succeeded, tiledb_uri, array_name = _create_notebook_array_retry_helper(
            storage_path,
            array_name,
            namespace,
            ctx,
        )
        if succeeded:
            return (tiledb_uri, array_name)
        tries -= 1
    raise ValueError(
        f"Out of retries uploading to namespace {namespace} array name {array_name}"
    )


def _create_notebook_array_retry_helper(
    storage_path: str,
    array_name: str,
    namespace: str,
    ctx: tiledb.Ctx,
) -> Tuple[bool, str, str]:
    """
    See _create_notebook_array -- exists only for retry logic.
    :return: tuple of succeeded, tiledb_uri, and array_name
    """

    try:
        # The array will be be 1-dimensional with domain of 0 to max uint64. We
        # use a tile extent of 1024 bytes.
        dom = tiledb.Domain(
            tiledb.Dim(
                name="position",
                domain=(0, numpy.iinfo(numpy.uint64).max - 1025),
                tile=1024,
                dtype=numpy.uint64,
                ctx=ctx,
            ),
            ctx=ctx,
        )

        schema = tiledb.ArraySchema(
            domain=dom,
            sparse=False,
            attrs=[
                tiledb.Attr(
                    name="contents",
                    dtype=numpy.uint8,
                    filters=tiledb.FilterList([tiledb.ZstdFilter()]),
                )
            ],
            ctx=ctx,
        )

        # Goal: tiledb://my_username/s3://my_bucket/my_array
        # https://docs.tiledb.com/cloud/how-to/arrays/create-arrays
        tiledb_uri_s3 = "tiledb://" + posixpath.join(
            namespace, storage_path, array_name
        )

        # Create the (empty) array on disk.
        tiledb.DenseArray.create(tiledb_uri_s3, schema)
        tiledb_uri = "tiledb://" + posixpath.join(namespace, array_name)
        time.sleep(0.25)

        file_properties = {}

        tiledb.cloud.array.update_info(uri=tiledb_uri, array_name=array_name)

        tiledb.cloud.array.update_file_properties(
            uri=tiledb_uri,
            file_type=tiledb.cloud.rest_api.models.FileType.NOTEBOOK,
            # If file_properties is empty, don't send anything at all.
            file_properties=file_properties or None,
        )

        return True, tiledb_uri, array_name
    except tiledb.TileDBError as e:
        if "Error while listing with prefix" in str(e):
            # It is possible to land here if user sets wrong default S3
            # credentials with respect to default S3 path.
            raise ValueError(
                f"Error creating file: {e}. Are your credentials valid?"
            ) from e
        raise # Note: the important already-exists case raises here

    # Let anything else bubble up


def _write_notebook_to_array(
    tiledb_uri: str,
    ipynb_file_contents: str,
    ctx: tiledb.Ctx,
) -> None:
    """Writes the given bytes to the array.
    :param tiledb_uri: such as "tiledb://TileDB-Inc/quickstart_dense".
    :param ipnyb_file_contents: The contents of the notebook file as a string,
      nominally in JSON format.
    :param ctx: cloud context for the operation.
    """

    # Note: every array is opened at a particular timestamp.  Data and metadata
    # writes are separate: write of metadata doesn't happen until the array is
    # closed.  But in Python, it's in a "with" context so data and metadata
    # writes get the same timestamp.

    # Why character-encoding is needed: in Python, len("Doppelgänger") is 12
    # but len(bytes("Doppelgänger", "utf-8")) is 13.  We store the file
    # contents as an array of bytes, so we need the encoding to get the right
    # byte-count for the file-contents string.

    contents_as_array = numpy.array(bytearray(ipynb_file_contents, CHARACTER_ENCODING))

    with tiledb.open(tiledb_uri, mode="w", ctx=ctx) as arr:
        arr[0 : len(contents_as_array)] = {"contents": contents_as_array}
        arr.meta["file_size"] = len(contents_as_array)
        arr.meta["type"] = file_type = tiledb.cloud.rest_api.models.FileType.NOTEBOOK
        arr.meta["format"] = "json"

    return
