from collections import defaultdict
from os.path import basename
from typing import Any, Mapping, Optional, Sequence

import tiledb
from tiledb.cloud import dag
from tiledb.cloud.rest_api.models import RetryStrategy
from tiledb.cloud.utilities import get_logger
from tiledb.cloud.utilities import max_memory_usage
from tiledb.cloud.utilities import run_dag

MAX_FRAGMENT_SIZE_BYTES = 1 << 30


def group_fragments(
    array_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    group_by_first_dim: bool = True,
) -> Sequence[Sequence[tiledb.FragmentInfo]]:
    """
    Get a list of fragment info objects, optionally grouping fragments that have the
    same value for the first dimension.

    :param array_uri: array URI
    :param config: config dictionary, defaults to None
    :param group_by_first_dim: group by first dimension, defaults to True
    :return: list of lists of fragment info objects
    """

    logger = get_logger()
    logger.info("Grouping fragments for array %r", array_uri)

    with tiledb.scope_ctx(config):
        fragment_info_lists = defaultdict(list)

        fis = tiledb.FragmentInfoList(array_uri)

        for fi in fis:
            if group_by_first_dim:
                fragment_info_lists[fi.nonempty_domain[0]].append(fi)
            else:
                fragment_info_lists["all"].append(fi)

        # Create a list of lists of fragment info objects.
        results = list(fragment_info_lists.values())

        logger.info("%d fragments grouped into %d groups", len(fis), len(results))
        logger.info("max memory usage: %.3f GiB", max_memory_usage() / (1 << 30))

        return results


def consolidate(
    array_uri: str,
    fragments: Sequence[tiledb.FragmentInfo],
    *,
    config: Optional[Mapping[str, Any]] = None,
    max_fragment_size: int = MAX_FRAGMENT_SIZE_BYTES,
) -> None:
    """
    Consolidate fragments

    :param array_uri: array URI
    :param fragments: list of fragments
    :param config: config dictionary, defaults to None
    :param max_fragment_size: max size of consolidated fragments,
        defaults to MAX_FRAGMENT_SIZE_BYTES
    """

    logger = get_logger()
    logger.info("Consolidating %d fragments", len(fragments))

    config = tiledb.Config(config)
    config["sm.consolidation.mode"] = "fragments"
    config["sm.consolidation.max_fragment_size"] = max_fragment_size

    # Consolidate fragments.
    fragment_names = [basename(fi.uri) for fi in fragments]
    with tiledb.open(array_uri, "w", config=config) as array:
        array.consolidate(fragment_uris=fragment_names)

    logger.info("max memory usage: %.3f GiB", max_memory_usage() / (1 << 30))


def consolidate_and_vacuum(
    array_uri: str,
    *,
    config: Optional[Mapping[str, Any]] = None,
    vacuum_fragments: bool = False,
) -> None:
    """
    Consolidate and vacuum commits and fragment metadata, with an option to
    vacuum fragments as the first step.

    :param array_uri: array URI
    :param config: config dictionary, defaults to None
    :param vacuum_fragments: vacuum fragments first, defaults to False
    """

    logger = get_logger()

    with tiledb.scope_ctx(config):
        is_remote = array_uri.startswith("tiledb://")
        if not is_remote and vacuum_fragments:
            logger.info("Vacuuming fragments")
            tiledb.vacuum(
                array_uri,
                config=tiledb.Config({"sm.vacuum.mode": "fragments"}),
            )

        # Modes for consolidate and vacuum
        modes = ["commits", "fragment_meta"]

        for mode in modes:
            logger.info("Consolidating %s", mode)
            tiledb.consolidate(
                array_uri,
                config=tiledb.Config({"sm.consolidation.mode": mode}),
            )

        for mode in modes:
            logger.info("Vacuuming %s", mode)
            tiledb.vacuum(
                array_uri,
                config=tiledb.Config({"sm.vacuum.mode": mode}),
            )

    logger.info("max memory usage: %.3f GiB", max_memory_usage() / (1 << 30))


def consolidate_fragments(
    array_uri: str,
    *,
    acn: Optional[str] = None,
    config: Optional[Mapping[str, Any]] = None,
    group_by_first_dim: bool = False,
    graph: Optional[dag.DAG] = None,
    dependencies: Optional[Sequence[dag.Node]] = None,
    consolidate_resources: Optional[Mapping[str, str]] = None,
    namespace: Optional[str] = None,
    max_fragment_size: int = MAX_FRAGMENT_SIZE_BYTES,
) -> None:
    """
    Consolidate fragments in an array.

    If `group_by_first_dim` is True, fragments with the same value for the first
    dimension will be consolidated together. Otherwise, all fragments will be
    consolidated together.

    If `graph` is provided, the consolidation task nodes will be submitted to the graph.
    If `dependencies` is provided, the consolidation nodes will depend on the nodes in
    the list.

    If `graph` is not provided, a new graph will be created and submitted to TileDB
    Cloud.

    :param array_uri: array URI
    :param acn: Access Credentials Name (ACN) registered in TileDB Cloud (ARN type),
        defaults to None
    :param config: config dictionary, defaults to None
    :param group_by_first_dim: group fragment by first dimension, defaults to True
    :param graph: graph to submit nodes to, defaults to None
    :param dependencies: list of nodes in the graph to depend on, defaults to None
    :param consolidate_resources: resources for the consolidate node, defaults to None
    :param namespace: TileDB Cloud namespace, defaults to the user's default namespace
    :param max_fragment_size: max size of consolidated fragments,
        defaults to MAX_FRAGMENT_SIZE_BYTES
    """

    graph_omitted = graph is None

    # If a graph is not provided, create a new graph and run it at the end of this
    # function.
    if graph_omitted:
        if dependencies is not None:
            raise ValueError("Graph must be provided if dependencies are provided")

        graph = dag.DAG(
            name="distributed-consolidation",
            namespace=namespace,
            mode=dag.Mode.BATCH,
            max_workers=40,
            retry_strategy=RetryStrategy(
                limit=3,
                retry_policy="Always",
            ),
        )
    elif graph.mode != dag.Mode.BATCH:
        raise ValueError("Graph mode must be BATCH")

    # Set resources for the consolidate node, if not provided.
    consolidate_resources = consolidate_resources or {
        "cpu": "4",
        "memory": "16Gi",
    }

    name = basename(array_uri)

    fragment_groups = graph.submit(
        group_fragments,
        array_uri,
        config=config,
        group_by_first_dim=group_by_first_dim,
        name=f"Groups Fragments - {name}",
        access_credentials_name=acn,
        resources={
            "cpu": "1",
            "memory": "1Gi",
        },
    )

    if dependencies:
        for node in dependencies:
            fragment_groups.depends_on(node)

    consolidate_node = graph.submit_udf_stage(
        consolidate,
        array_uri,
        fragment_groups,
        config=config,
        max_fragment_size=max_fragment_size,
        expand_node_output=fragment_groups,
        name=f"Consolidate Fragments - {name}",
        access_credentials_name=acn,
        resources=consolidate_resources,
    )

    vacuum_node = graph.submit(
        consolidate_and_vacuum,
        array_uri,
        config=config,
        vacuum_fragments=True,
        name=f"Consolidate and Vacuum - {name}",
        access_credentials_name=acn,
        resources=consolidate_resources,
    )

    vacuum_node.depends_on(consolidate_node)

    if graph_omitted:
        run_dag(graph, wait=False)
        print(
            "Consolidate fragments submitted - ",
            f"https://cloud.tiledb.com/activity/taskgraphs/{graph.namespace}/{graph.server_graph_uuid}",
        )
