from types import MappingProxyType

from tiledb.cloud.dag import dag
from tiledb.cloud.dag import mode
from tiledb.cloud.dag import status

# Globals
MIN_BATCH_RESOURCES = MappingProxyType({"cpu": "1", "memory": "2Gi"})

# Re-exports.
Mode = mode.Mode
DAG = dag.DAG
Node = dag.Node
Status = status.Status
list_logs = dag.list_logs
server_logs = dag.server_logs


__all__ = (
    "DAG",
    "MIN_BATCH_RESOURCES",
    "Mode",
    "Node",
    "Status",
    "list_logs",
    "server_logs",
)
