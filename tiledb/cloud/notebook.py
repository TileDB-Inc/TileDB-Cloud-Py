from . import rest_api
from . import client
from . import tiledb_cloud_error
from . import array
from .rest_api import ApiException as GenApiException
from .rest_api import rest


def rename_notebook(
    uri,
    notebook_name=None,
    access_credentials_name=None,
    async_req=False,
):
    """
    Update an array's info
    :param str namespace: optional username or organization array should be registered under. If unset will default to the user
    :param str array_name: name of notebook to rename to
    :param str access_credentials_name: optional name of access credentials to use, if left blank default for namespace will be used
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
