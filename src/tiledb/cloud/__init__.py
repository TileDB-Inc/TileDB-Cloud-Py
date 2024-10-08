# This file imports specifically to re-export.

from . import array
from . import asset
from . import compute
from . import dag
from . import files
from . import groups
from . import sql
from . import udf
from ._common import pickle_compat as _pickle_compat
from .array import array_activity
from .array import deregister_array
from .array import info
from .array import list_shared_with
from .array import register_array
from .array import share_array
from .array import unshare_array
from .asset import list as list_assets
from .asset import list_public as list_public_assets
from .client import Config
from .client import Ctx
from .client import list_arrays
from .client import list_groups
from .client import list_public_arrays
from .client import list_public_groups
from .client import list_shared_arrays
from .client import list_shared_groups
from .client import login
from .client import organization
from .client import organizations
from .client import user_profile
from .notebook import download_notebook_contents
from .notebook import download_notebook_to_file
from .notebook import rename_notebook
from .notebook import upload_notebook_contents
from .notebook import upload_notebook_from_file
from .rest_api import models
from .tasks import fetch_results
from .tasks import fetch_results_pandas
from .tasks import fetch_tasks
from .tasks import last_sql_task
from .tasks import last_udf_task
from .tasks import task
from .tiledb_cloud_error import TileDBCloudError

_pickle_compat.patch_cloudpickle()
_pickle_compat.patch_pandas()

try:
    from tiledb.cloud.version import version as __version__
except ImportError:
    __version__ = "0.0.0.local"

ResultFormat = models.ResultFormat
UDFResultType = ResultFormat

__all__ = (
    "array",
    "asset",
    "compute",
    "dag",
    "files",
    "groups",
    "sql",
    "udf",
    "array_activity",
    "deregister_array",
    "info",
    "list_shared_with",
    "register_array",
    "share_array",
    "unshare_array",
    "Config",
    "Ctx",
    "list_arrays",
    "list_assets",
    "list_public_arrays",
    "list_public_assets",
    "list_public_groups",
    "list_shared_arrays",
    "list_shared_groups",
    "list_groups",
    "login",
    "organization",
    "organizations",
    "user_profile",
    "rename_notebook",
    "upload_notebook_from_file",
    "upload_notebook_contents",
    "download_notebook_to_file",
    "download_notebook_contents",
    "last_sql_task",
    "last_udf_task",
    "task",
    "fetch_tasks",
    "fetch_results",
    "fetch_results_pandas",
    "TileDBCloudError",
)
