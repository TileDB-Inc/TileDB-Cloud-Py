"""A batch server-side implementation of a task graph Executor.

This module implements a task graph Executor that coordinates the execution of
graph nodes on the server-side side.
"""

# This file collects all the names into one re-exportable namespace.

from tiledb.cloud.taskgraphs import executor
from tiledb.cloud.taskgraphs.batch_executor import impl
from tiledb.cloud.taskgraphs.batch_executor import input_node
from tiledb.cloud.taskgraphs.batch_executor import udf_node

Status = executor.Status
BatchExecutor = impl.BatchExecutor

InputNode = input_node.InputNode
UDFNode = udf_node.UDFNode


__all__ = (
    "Status",
    "BatchExecutor",
    "InputNode",
    "UDFNode",
)
