"""Version 2 of the task graph API, allowing registration and sharing.

This namespace groups together all the classes, functions, and other resources
that a typical user will need when using task graphs. In most cases, you should
not need to import anything from the sub-modules directly.

By convention it is imported as ``tg``::

    import tiledb.cloud.taskgraphs as tg

These APIs are close to final, though still subject to minor changes. Consider
this a late-stage beta. We will endeavor to maintain compatibility but cannot
guarantee it 100%.
"""

from typing import Any, Union

from tiledb.cloud.taskgraphs import builder
from tiledb.cloud.taskgraphs import client_executor
from tiledb.cloud.taskgraphs import executor
from tiledb.cloud.taskgraphs import registration
from tiledb.cloud.taskgraphs import types

#
# Re-exports.
#

Builder = builder.TaskGraphBuilder
InvalidStateError = client_executor.InvalidStateError
ParentFailedError = executor.ParentFailedError
Status = executor.Status
args = types.args
Layout = types.Layout
ArrayMultiIndex = types.ArrayMultiIndex

register = registration.register
update = registration.update
load = registration.load
delete = registration.delete

#
# Helpers.
#

GraphOrRegistered = Union[executor.GraphStructure, str]
"""Either a graph structure, or the name of a registered task graph."""


def execute(
    __graph: GraphOrRegistered,
    **graph_inputs: Any,
) -> executor.Executor:
    """Executes this graph with default settings and the provided input values.

    This is an all-in-one convenience function which will set up the default
    executor (currently :class:`client_executor.LocalExecutor`), start execution
    with the given input values (provided in ``kwargs``), and return the
    :class:`executor.Executor` object that it built for inspection, use, and
    result retrieval.

    The graph can be specified as any of:

    - A task graph builder.
    - The output of a task graph builder.
    - The name of a registered task graph, in the form "namespace/name".

    For more advanced control, you should construct your own Executor and set
    the desired options manually.
    """

    grf = load(__graph) if isinstance(__graph, str) else __graph
    exec = client_executor.LocalExecutor(grf)
    exec.execute(**graph_inputs)
    return exec
