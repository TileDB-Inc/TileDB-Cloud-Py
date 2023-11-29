import logging
import os
import re
from typing import Any, Callable, ContextManager, Dict, Optional, Sequence, Tuple
from unittest import mock

import tiledbsoma
import tiledb
from tiledb.cloud import dag
from tiledb.cloud._common import functions
import tiledb.cloud.taskgraphs as tg
from tiledb.cloud.compute import Delayed

import anndata as ad

import tiledb

_DEFAULT_RESOURCES = {"cpu": "8", "memory": "8Gi"}
"""Default resource size; equivalent to a "large" UDF container."""

def run_collection_mapper_workflow(
    *,
    # Input data:
    soma_collection_uri: Optional[str]=None,
    soma_experiment_uris: Optional[Sequence[str]] = None,
    measurement_name: str,
    X_layer_name: str,
    experiment_names: Optional[Sequence[str]] = None,
    # Query parameters:
    obs_query_string: Optional[str] = None,
    var_query_string: Optional[str] = None,
    obs_attrs: Optional[Sequence[str]] = None,
    var_attrs: Optional[Sequence[str]] = None,
    # Processing:
    callback: Callable = lambda x: x,
    args_dict: Optional[Dict[str, Any]] = None,
    reducer: Callable = lambda x: x,
    # Misc. tiledb configs:
    extra_tiledb_config: Optional[Dict[str, object]] = None,
    platform_config: Optional[Dict[str, object]] = None,
    # Misc. cloud configs:
    task_graph_name: Optional[str] = None,
    counts_only: Optional[bool] = False,
    # XXX need a flag for real-time or batch-mode
    resources: Optional[Dict[str, object]] = None,
    namespace: Optional[str] = None,
    access_credentials_name: Optional[str] = None,
) -> Dict[str, str]:
    """
    XXX TODO
    """

    # ----------------------------------------------------------------
    # XXX soma_experiment_uris as dict from name to URI, or, just URIs ...
    if soma_collection_uri is None and soma_experiment_uris is None:
        raise Exception("Need just one of soma_collection_uri or soma_experiment_uris")
    if soma_collection_uri is not None and soma_experiment_uris is not None:
        raise Exception("Need just one of soma_collection_uri or soma_experiment_uris")
    assert isinstance(task_graph_name, str) or task_graph_name is None
    if task_graph_name is None:
        task_graph_name = "SOMAExperiment Collection Mapper"
    if resources is None:
        resources = _DEFAULT_RESOURCES

    args_dict = args_dict or {}
    obs_attrs = obs_attrs or []
    var_attrs = var_attrs or []

    # # Create context that enables faster array open
    # cfg_dict = cfg_dict or {}
    # cfg_dict["rest.use_refactored_array_open"] = True

    logging.basicConfig(level=logging.INFO)

    # ----------------------------------------------------------------
    if soma_experiment_uris is None:
        logging.info(f"Retrieving SOMA Experiment URIs from SOMACollection {soma_collection_uri}")
        with tiledbsoma.Collection.open(soma_collection_uri) as soco:
            soma_experiment_uris = {k: v.uri for k, v in soco.items()}

    if experiment_names is not None:
        logging.info("Filtering SOMA Experiment URIs for specified names")
        soma_experiment_uris = {
            k: v for k, v in soma_experiment_uris.items() if k in experiment_names
        }
    logging.info(f"Retrieved {len(soma_experiment_uris)} SOMA Experiment URIs")

    # ----------------------------------------------------------------
    # Set log formatting

    logging.info("Constructing task graph")

    grf = dag.DAG(
        name=task_graph_name,
        mode=dag.Mode.BATCH,
        ###mode=dag.Mode.REALTIME,
        namespace=namespace,
    )

    collector = grf.submit(
        lambda x: 0,
        x=0,
    )

    for _, soma_experiment_uri in soma_experiment_uris.items():
        node = grf.submit(
            _function_for_node,

            soma_experiment_uri,
            measurement_name=measurement_name,
            X_layer_name=X_layer_name,

            callback=callback,
            args_dict=args_dict,
            # cfg_dict=cfg_dict, # XXX

            obs_query_string=obs_query_string,
            var_query_string=var_query_string,
            obs_attrs=obs_attrs,
            var_attrs=var_attrs,
            counts_only=counts_only,

            ####platform_config=platform_config,

            resources=_DEFAULT_RESOURCES if resources is None else resources,
            # tiledb.cloud.tiledb_cloud_error.TileDBCloudError:
            # Cannot set resources for REALTIME task graphs, please use "resource_class" to
            # set a predefined option for "standard" or "large"
            ###resource_class="large",

            access_credentials_name=access_credentials_name,
        )

        collector.depends_on(node)

    grf.compute()
    return {
        "status": "started",
        "graph_id": str(grf.server_graph_uuid),
    }

# ----------------------------------------------------------------
def experiment_to_axis_counts(
    exp: tiledbsoma.Experiment,
    *,
    measurement_name: str,
    X_layer_name: str,
    obs_query_string: Optional[str] = None,
    var_query_string: Optional[str] = None,
    obs_attrs: Optional[Sequence[str]] = None,
    var_attrs: Optional[Sequence[str]] = None,
    # ctx,
) -> Tuple[int, int]:
    """Returns a tuple of (obs_counts, var_counts) if counts_only is True."""
    import tiledbsoma

    obs_query = None
    if obs_query_string is not None:
        obs_query = tiledbsoma.AxisQuery(value_filter=obs_query_string)

    var_query = None
    if var_query_string is not None:
        var_query = tiledbsoma.AxisQuery(value_filter=var_query_string)

    query = exp.axis_query(
        measurement_name, obs_query=obs_query, var_query=var_query
    )

    return (query.n_obs, query.n_vars)


# ----------------------------------------------------------------
def experiment_to_anndata_slice(
    exp: tiledbsoma.Experiment,
    *,
    measurement_name: str,
    X_layer_name: str,
    obs_query_string: Optional[str] = None,
    var_query_string: Optional[str] = None,
    obs_attrs: Optional[Sequence[str]] = None,
    var_attrs: Optional[Sequence[str]] = None,
    # ctx,
) -> ad.AnnData:
    import tiledbsoma

    obs_query = None
    if obs_query_string is not None:
        obs_query = tiledbsoma.AxisQuery(value_filter=obs_query_string)

    var_query = None
    if var_query_string is not None:
        var_query = tiledbsoma.AxisQuery(value_filter=var_query_string)

    query = exp.axis_query(
        measurement_name, obs_query=obs_query, var_query=var_query
    )

    column_names = {}
    if obs_attrs is not None:
        column_names["obs"] = obs_attrs
    if var_attrs is not None:
        column_names["var"] = var_attrs

    adata = query.to_anndata(X_name=X_layer_name, column_names=column_names)

    return adata

# ----------------------------------------------------------------
def function_for_node(
    experiment_uri: str,
    *,
    measurement_name: str,
    X_layer_name: str,
    callback: Callable,
    args_dict: Dict[str, Any],
    # cfg_dict: Dict[str, Any],
    obs_query_string: Optional[str] = None,
    var_query_string: Optional[str] = None,
    obs_attrs: Optional[Sequence[str]] = None,
    var_attrs: Optional[Sequence[str]] = None,
    counts_only: bool = False,
):
    import anndata as ad
    import tiledbsoma

    if counts_only:
        experiment_query_func = _experiment_to_axis_counts
    else:
        experiment_query_func = _experiment_to_anndata_slice

    # ctx = tiledb.Ctx(cfg_dict)
    # exp = tiledbsoma.Experiment.open(experiment_uri, ctx=ctx)
    print("EXPERIMENT_URI IS", experiment_uri)
    exp = tiledbsoma.Experiment.open(experiment_uri)
    result = experiment_query_func(
        exp,
        measurement_name=measurement_name,
        X_layer_name=X_layer_name,
        obs_query_string=obs_query_string,
        var_query_string=var_query_string,
        obs_attrs=obs_attrs,
        var_attrs=var_attrs,
        # ctx=ctx,
    )

    if counts_only:
        return result
    else:
        if result is None:
            return None
        else:
            if not args_dict:  # if dictionary is empty
                return callback(result)
            else:
                return callback(result, **args_dict)

# ----------------------------------------------------------------
# Until we fully get this version of tiledb.cloud deployed server-side, we must
# refer to all functions by value rather than by reference -- which is a fancy way
# of saying these functions _will not work at all_ until and unless they are
# checked into tiledb-cloud-py and deployed server-side. _All_ dev work _must_
# use this idiom.
_run_collection_mapper_workflow = functions.to_register_by_value(run_collection_mapper_workflow)
_function_for_node = functions.to_register_by_value(function_for_node)
_experiment_to_anndata_slice = functions.to_register_by_value(experiment_to_anndata_slice)
_experiment_to_axis_counts = functions.to_register_by_value(experiment_to_axis_counts)

# ================================================================
# #!/usr/bin/env python
#
# import tiledb.cloud
# import tiledb.cloud.soma
#
# soma_experiment_uris = {
#     "tsiq": "tiledb://johnkerl-tiledb/tabula-sapiens-immune-registered",
#     "tsir": "tiledb://johnkerl-tiledb/tabula-sapiens-immune-registered",
# }
# soma_collection_uri = "tiledb://TileDB-Inc/stack-small-soco-prod"
# measurement_name = "RNA"
#
# g = tiledb.cloud.soma.run_collection_mapper_workflow(
#     #soma_experiment_uris=soma_experiment_uris,
#     soma_collection_uri=soma_collection_uri,
#     measurement_name=measurement_name,
#     X_layer_name="data",
#     callback=lambda x: x.shape,
#     resources={"cpu": "8", "memory": "32Gi"},
#     extra_tiledb_config={"config.logging_level": "5"},
#     namespace="TileDB-Inc",
# )
# print("https://cloud.tiledb.com/activity/taskgraphs/TileDB-Inc/" + g["graph_id"])
