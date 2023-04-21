import json
from typing import Any, Dict, Optional, Tuple

import urllib3

from tiledb.cloud import client
from tiledb.cloud import rest_api
from tiledb.cloud._common import json_safe
from tiledb.cloud._common import utils
from tiledb.cloud.taskgraphs import builder


def register(
    graph: builder.TaskGraphBuilder,
    name: Optional[str] = None,
    *,
    namespace: Optional[str] = None,
) -> None:
    """Registers the graph constructed by the TaskGraphBuilder.

    :param graph: The graph to register.
    :param name: The name to register the graph with. By default, will use the
        ``name`` specified in ``graph``. This must be a bare name, with no
        namespace (i.e. ``my-graph``, not ``me/my-graph``).
    :param namespace: The namespace, if not your own, to register the graph in.
    """
    api_client = client.build(rest_api.RegisteredTaskGraphsApi)
    namespace = namespace or client.default_user().username
    name = name or graph.name

    api_client.register_registered_task_graph(
        namespace=namespace,
        name=name,
        graph=json_safe.Value(graph._tdb_to_json(override_name=name)),
    )


def load(
    name_or_nsname: str,
    *,
    namespace: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieves the given task graph from the server.

    :param name_or_nsname: The graph's identifier, either in the form
        ``namespace/name``, or just ``name`` to use the ``namespace`` param.
    :param namespace: If set, the namespace of the graph.
        If ``name_or_nsname`` is of the form ``namespace/name``, must be None.
        If ``name_or_nsname`` is just a name and this is None, will use the
        current user's namespace.
    """
    name, namespace = _canonicalize(name_or_nsname, namespace)
    api_client = client.build(rest_api.RegisteredTaskGraphsApi)

    result: urllib3.HTTPResponse = api_client.get_registered_task_graph(
        namespace=namespace,
        name=name,
        _preload_content=False,
    )
    try:
        return json.loads(result.data)
    finally:
        utils.release_connection(result)


def update(
    graph: builder.TaskGraphBuilder,
    old_name: Optional[str] = None,
    *,
    namespace: Optional[str] = None,
) -> None:
    """Updates the registered task graph at the given location.

    :param graph: The new graph to replace the old value.
    :param old_name: The name of the graph to rename from, if present.
        If ``graph`` is to be renamed, the new name of the graph must appear
        in ``graph.name``.
    :param namespace: The namespace, if not your own, where the graph will
        be updated.
    """
    api_client = client.build(rest_api.RegisteredTaskGraphsApi)
    namespace = namespace or client.default_user().username
    name = old_name or graph.name
    api_client.update_registered_task_graph(
        name=name,
        namespace=namespace,
        graph=json_safe.Value(graph._tdb_to_json()),
    )


def delete(name_or_nsname: str, *, namespace: Optional[str] = None) -> None:
    """Deletes the given task graph.

    This deregisters the graph and also removes the graph array from storage.

    :param name_or_nsname: The graph's identifier, either in the form
        ``namespace/name``, or just ``name`` to use the ``namespace`` param.
    :param namespace: If set, the namespace of the graph.
        If ``name_or_nsname`` is of the form ``namespace/name``, must be None.
        If ``name_or_nsname`` is just a name and this is None, will use the
        current user's namespace.
    """
    name, namespace = _canonicalize(name_or_nsname, namespace)
    api_client = client.build(rest_api.RegisteredTaskGraphsApi)
    api_client.delete_registered_task_graph(namespace, name)


def _canonicalize(
    name_or_nsname: str,
    namespace: Optional[str],
) -> Tuple[str, str]:
    """Canonicalizes the inputs into the actual (name, namespace) pair."""
    if "/" in name_or_nsname:
        if namespace:
            raise ValueError(
                "If `namespace` is set, `name_or_nsname` cannot be of the form"
                " namespace/name"
            )
        namespace, _, name = name_or_nsname.partition("/")
        return name, namespace
    return (
        name_or_nsname,
        namespace or client.default_user().username,
    )
