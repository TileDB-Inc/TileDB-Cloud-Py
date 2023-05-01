"""
Python support for notebook I/O on Tiledb Cloud. All notebook JSON content
is assumed to be encoded as UTF-8.

"""
import datetime
import enum
import posixpath
import time
from typing import Optional, Tuple, Union

import numpy

import tiledb
from tiledb.cloud import array
from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud import tiledb_cloud_error
from tiledb.cloud._common import utils
from tiledb.cloud.rest_api import ApiException as GenApiException

RESERVED_NAMESPACES = frozenset(["cloud", "owned", "public", "shared"])
CHARACTER_ENCODING = "utf-8"


class OnExists(enum.Enum):
    """Action to take if the array already exists."""

    FAIL = enum.auto()
    OVERWRITE = enum.auto()
    # TODO: Add the AUTO_INCREMENT logic in future cycles


def rename_notebook(
    tiledb_uri,
    notebook_name=None,
    access_credentials_name=None,
    async_req=False,
):
    """
    Update an array's info
    :param str tiledb_uri: such as "tiledb://TileDB-Inc/quickstart_dense".
    :param str notebook_name: such as "quickstart_dense_new_name".
    :param str access_credentials_name: optional name of access credentials to
      use. If left blank. default for namespace will be used.
    :param bool async_req: return future instead of results for async support.
    """
    api_instance = client.build(rest_api.NotebookApi)
    (namespace, current_notebook_name) = array.split_uri(tiledb_uri)

    try:
        return api_instance.update_notebook_name(
            namespace=namespace,
            array=current_notebook_name,
            notebook_metadata=rest_api.ArrayInfoUpdate(
                name=notebook_name,
                uri=tiledb_uri,
                access_credentials_name=access_credentials_name,
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.check_exc(exc) from None


def download_notebook_to_file(
    tiledb_uri: str,
    ipynb_file_name: str,
    *,
    timestamp: Union[int, datetime.datetime, None] = None,
) -> None:
    """Downloads a notebook file from TileDB Cloud to local disk.

    :param tiledb_uri: such as "tiledb://TileDB-Inc/quickstart_dense".
    :param ipynb_file_name: path to save to, such as "./mycopy.ipynb". Must be
        local; no other VFS backends are currently supported.
    :param timestamp: If set, the timestamp to download the notebook as of.
    """
    ipynb_file_contents = download_notebook_contents(tiledb_uri, timestamp=timestamp)
    vfs = tiledb.VFS(ctx=client.Ctx())
    with vfs.open(ipynb_file_name, mode="wb") as fio:
        fio.write(bytes(ipynb_file_contents, "utf-8"))


def download_notebook_contents(
    tiledb_uri: str, *, timestamp: Union[int, datetime.datetime, None] = None
) -> str:
    """
    Downloads a notebook file from TileDB Cloud to contents as a string,
      nominally in JSON format.

    :param tiledb_uri: such as "tiledb://TileDB-Inc/quickstart_dense".
    :param timestamp: If set, the timestamp to download the notebook as of.
    :return: contents of the notebook file as a string, nominally in JSON format.
    """
    ctx = client.Ctx()
    with tiledb.open(
        tiledb_uri, "r", ctx=ctx, timestamp=utils.datetime_to_msec(timestamp)
    ) as arr:
        size = arr.meta["file_size"]
        data = arr.query(attrs=["contents"])[slice(0, size)]
        json = data["contents"].tobytes().decode("utf-8")
        return json


def upload_notebook_from_file(
    ipynb_file_name: str,
    *,
    namespace: Optional[str] = None,
    array_name: str,
    storage_path: Optional[str] = None,
    storage_credential_name: Optional[str] = None,
    on_exists: OnExists = OnExists.FAIL,
) -> str:
    """
    Uploads a local-disk notebook file to TileDB Cloud.
    :param ipnyb_file_name: such as "./mycopy.ipynb". Must be local; no S3 URI
      support at present.
    :param namespace: such as "janedoe".
    :param array_name : name to be seen in the UI, such as "testing-upload".
    :param storage_path: such as "s3://acmecorp-janedoe", typically from the
      user's account settings.
    :param storage_credential_name: such as "janedoe-creds", typically from the
      user's account settings.
    :param on_exists: such as OnExists.FAIL (default), OVERWRITE or AUTO-INCREMENT
    :return: TileDB array name, such as "tiledb://janedoe/testing-upload".
    """

    vfs = tiledb.VFS(ctx=client.Ctx())
    with vfs.open(ipynb_file_name, mode="rb") as fio:
        ipynb_file_contents = fio.read()

    return upload_notebook_contents(
        str(ipynb_file_contents, "utf-8"),
        namespace=namespace,
        array_name=array_name,
        storage_path=storage_path,
        storage_credential_name=storage_credential_name,
        on_exists=on_exists,
    )


def upload_notebook_contents(
    ipynb_file_contents: str,
    *,
    namespace: Optional[str] = None,
    array_name: str,
    storage_path: Optional[str] = None,
    storage_credential_name: Optional[str] = None,
    on_exists: OnExists,
) -> str:
    """
    Uploads a notebook file to TileDB Cloud.
    :param ipynb_file_contents: The contents of the notebook file as a string,
      nominally in JSON format.
    :param storage_path: such as "s3://acmecorp-janedoe", typically from the
      user's account settings.
    :param array_name : name to be seen in the UI, such as "testing-upload"
    :param namespace: such as "janedoe".
    :param storage_credential_name: such as "janedoe-creds", typically from the
      user's account settings.
    :param on_exists: such as OnExists.FAIL (default), OVERWRITE or AUTO-INCREMENT
    :return: TileDB array name, such as "tiledb://janedoe/testing-upload".
    """

    storage_credential_name = storage_credential_name or (
        client.default_user().default_s3_path_credentials_name
    )
    storage_path = storage_path or client.default_user().default_s3_path
    namespace = namespace or client.default_user().username

    if not storage_credential_name:
        raise tiledb_cloud_error.TileDBCloudError(
            "No storage credentials found in account."
            " Please add them there, or pass them in explicitly here."
        )
    if not storage_path:
        raise tiledb_cloud_error.TileDBCloudError(
            "No storage path found in account."
            " Please add it there, or pass it in explicitly here."
        )
    if not namespace:
        raise tiledb_cloud_error.TileDBCloudError("Namespace to store notebook unset.")

    ctx = client.Ctx({"rest.creation_access_credentials_name": storage_credential_name})

    tiledb_uri = f"tiledb://{namespace}/{array_name}"
    try:
        arr = tiledb.open(tiledb_uri, ctx=ctx)
    except tiledb.TileDBError:
        already_exists = False
    else:
        arr.close()
        already_exists = True
    if already_exists:
        if on_exists is OnExists.FAIL:
            raise tiledb_cloud_error.TileDBCloudError(
                f"Array {tiledb_uri!r} already exists"
            )
    else:
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
    retries: int = 0,
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

    # The array will be be 1-dimensional with domain of 0 to max uint64. We
    # use a tile extent of 1024 bytes.
    dom = tiledb.Domain(
        tiledb.Dim(
            name="position",
            domain=(0, numpy.iinfo(numpy.uint64).max - 1025),
            tile=1024,
            dtype=numpy.uint64,
            ctx=ctx,
            filters=tiledb.FilterList([tiledb.ZstdFilter()]),
        ),
        ctx=ctx,
    )

    tries = 1 + retries  # 1st + rest
    while True:
        try:
            return _create_notebook_array_retry_helper(
                storage_path,
                array_name,
                namespace,
                dom,
                ctx,
            )
        except tiledb.TileDBError as e:
            if "Error while listing with prefix" in str(e):
                # It is possible to land here if user sets wrong default S3
                # credentials with respect to default S3 path.
                raise tiledb_cloud_error.TileDBCloudError(
                    f"Error creating file: {e}. Are your credentials valid?"
                ) from e
            if "Cannot create array" in str(e) and "already exists" in str(e):
                raise tiledb_cloud_error.TileDBCloudError(
                    f"Error creating file: {array_name!r} already exists"
                    f" in namespace {namespace!r}."
                )
            # Retry other TileDB errors
            tries -= 1
            if tries <= 0:
                raise tiledb_cloud_error.check_exc(e) from None


def _create_notebook_array_retry_helper(
    storage_path: str,
    array_name: str,
    namespace: str,
    dom: tiledb.Domain,
    ctx: tiledb.Ctx,
) -> Tuple[str, str]:
    """
    See _create_notebook_array -- exists only for retry logic.
    :return: tuple of succeeded, tiledb_uri, and array_name
    """

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
    tiledb_uri_s3 = "tiledb://" + posixpath.join(namespace, storage_path, array_name)

    # Create the (empty) array on disk.
    tiledb.Array.create(tiledb_uri_s3, schema)
    tiledb_uri = "tiledb://" + posixpath.join(namespace, array_name)
    time.sleep(0.25)

    file_properties = {}

    array.update_info(uri=tiledb_uri, array_name=array_name)

    array.update_file_properties(
        uri=tiledb_uri,
        file_type=rest_api.FileType.NOTEBOOK,
        # If file_properties is empty, don't send anything at all.
        file_properties=file_properties or None,
    )

    return tiledb_uri, array_name


def _write_notebook_to_array(
    tiledb_uri: str, ipynb_file_contents: str, ctx: tiledb.Ctx
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
        arr.meta["type"] = rest_api.FileType.NOTEBOOK
        arr.meta["format"] = "json"
