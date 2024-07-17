from typing import Any, Callable, Dict, Optional, Sequence, Tuple

import anndata as ad
import tiledbsoma

import tiledb
from tiledb.cloud import dag
from tiledb.cloud._common import functions
from tiledb.cloud.utilities import get_logger_wrapper

_DEFAULT_RESOURCES = {"cpu": "8", "memory": "8Gi"}
"""Default resource size; equivalent to a "large" UDF container."""


def run_collection_mapper_workflow(
    *,
    # Input data:
    soma_collection_uri: Optional[str] = None,
    soma_experiment_uris: Optional[Sequence[str]] = None,
    experiment_names: Optional[Sequence[str]] = None,
    measurement_name: str,
    X_layer_name: str,
    # Query parameters:
    obs_query_string: Optional[str] = None,
    var_query_string: Optional[str] = None,
    obs_attrs: Optional[Sequence[str]] = None,
    var_attrs: Optional[Sequence[str]] = None,
    # Processing:
    callback: Callable = lambda x: x,
    args_dict: Optional[Dict[str, Any]] = None,
    # TileDB configs:
    extra_tiledb_config: Optional[Dict[str, object]] = None,
    platform_config: Optional[Dict[str, object]] = None,
    # Cloud configs:
    namespace: Optional[str] = None,
    task_graph_name: str = "SOMAExperiment Collection Mapper",
    counts_only: Optional[bool] = False,
    # Real-time vs batch modes:
    use_batch_mode: bool = False,
    resource_class: Optional[str] = None,  # only valid for real-time mode
    resources: Optional[Dict[str, object]] = None,  # only valid for batch mode
    access_credentials_name: Optional[str] = None,  # only valid for batch mode,
    verbose: bool = False,
) -> Dict[str, str]:
    """
    This is an asynchronous entry point, which launches the task graph and returns
    tracking information. Nominally this is not the primary use-case.
    Please see ``build_collection_mapper_workflow_graph`` for information about
    arguments and return value.
    """

    grf = build_collection_mapper_workflow_graph(
        soma_collection_uri=soma_collection_uri,
        soma_experiment_uris=soma_experiment_uris,
        experiment_names=experiment_names,
        measurement_name=measurement_name,
        X_layer_name=X_layer_name,
        obs_query_string=obs_query_string,
        var_query_string=var_query_string,
        obs_attrs=obs_attrs,
        var_attrs=var_attrs,
        callback=callback,
        args_dict=args_dict,
        namespace=namespace,
        extra_tiledb_config=extra_tiledb_config,
        platform_config=platform_config,
        task_graph_name=task_graph_name,
        counts_only=counts_only,
        use_batch_mode=use_batch_mode,
        resource_class=resource_class,
        resources=resources,
        access_credentials_name=access_credentials_name,
        verbose=verbose,
    )
    grf.compute()
    return {
        "status": "started",
        "graph_id": str(grf.server_graph_uuid),
    }


def build_collection_mapper_workflow_graph(
    *,
    # Input data:
    soma_collection_uri: Optional[str] = None,
    soma_experiment_uris: Optional[Sequence[str]] = None,
    experiment_names: Optional[Sequence[str]] = None,
    measurement_name: str,
    X_layer_name: str,
    # Query parameters:
    obs_query_string: Optional[str] = None,
    var_query_string: Optional[str] = None,
    obs_attrs: Optional[Sequence[str]] = None,
    var_attrs: Optional[Sequence[str]] = None,
    # Processing:
    callback: Callable = lambda x: x,
    args_dict: Optional[Dict[str, Any]] = None,
    # TileDB configs:
    extra_tiledb_config: Optional[Dict[str, object]] = None,
    platform_config: Optional[Dict[str, object]] = None,
    # Cloud configs:
    namespace: Optional[str] = None,
    task_graph_name: str = "SOMAExperiment Collection Mapper",
    counts_only: Optional[bool] = False,
    # Real-time vs batch modes:
    use_batch_mode: bool = False,
    resource_class: Optional[str] = None,  # only valid for real-time mode
    resources: Optional[Dict[str, object]] = None,  # only valid for batch mode
    access_credentials_name: Optional[str] = None,  # only valid for batch mode,
    verbose: bool = False,
) -> dag.DAG:
    """
    The primary entrypoint for the mapper module. The caller passes in either a
    sequence of ``SOMAExperiment`` URIs or a ``SOMACollection``, which is simply
    a collection of SOMAExperiment objects. The caller also passes in query
    terms and a callback lambda which will be called on the ``to_anndata``
    output of each experiment's query. The result will be a dictionary mapping
    experiment names to the callback lambda's output for each input experiment.

    For example, if the lambda maps an anndata object to its ``.shape``, then
    with SOMA experiments ``A`` and ``B``, the task graph would return the
    dict ``{"A": (56868, 43050), "B": (23539, 42044)}``.


    Parameters for input data:
    :param soma_collection_uri: URI of a ``SOMACollection`` containing
        ``SOMAExperiment`` objects to be processed.  Please specify only one of
        ``soma_collection_uri`` or ``soma_experiment_uris``.
    :param soma_experiment_uris: List/tuple of URIs of ``SOMAExperiment``
        objects to be processed.

    :param experiment_names: Optional list of experiment names. If not provided,
        all ``SOMAExperiment`` objects are processed as specified by
        ``soma_collection_uri`` or ``soma_experiment_uris``. If provided,
        ``experiment_names`` can be used to further subset/restrict which
        ``SOMAExperiment`` objects will be processed.
    :param measurement_name: Which ``SOMAMeasurement`` to query within the
        specified ``SOMAExperiment`` objects. For example, ``"RNA"``.
    :param X_layer_name: Which ``X`` layer to query within the specified
        ``SOMAMeasurement`` objects. For example, ``"data"``, ``"raw"``,
        ``"normalized"``.

    Query parameters:
    :param obs_query_string: Optional query string for ``obs``. For example:
        ``'cell_type == "liver"'``.
    :param var_query_string: Optional query string for ``var``. For example:
        ``'n_cells > 100'``.
    :param obs_attrs: Optional list of ``obs`` attributes to return as query
        output. Default: all.
    :param var_attrs: Optional list of ``var`` attributes to return as query
        output. Default: all.

    Parameters for data processing:
    :param callback: Your code to run on each UDF node, one for each
        ``SOMAExperiment``.  On each node, ``tiledbsoma.AxisQuery`` is run,
        using parameters you specify as above, and then ``query.to_anndata`` is
        run on that query output. Your ``callback`` function receives
        that query-output AnnData object.  For example: ``lambda ad:
        ad.obs.shape``.
    :param args_dict: Optional additional arguments to be passed to your
        callback.  If provided, this must be a dict from string experiment name,
        to dict of key-value pairs.
    :param counts_only: If specified, only return obs/var counts, not the
        result of the provided callback.

    TileDB configs:
    :param extra_tiledb_config: Currently unused; reserved for future use.
    :param platform_config: Currently unused; reserved for future use.

    Cloud configs:
    :param namespace: TileDB namespace in which to run the UDFs.
    :param task_graph_name: Optional name for your task graph, so you can
        find it more easily among other runs.

    Real-time vs batch modes:
    :param use_batch_mode: If false (the default), uses real-time UDFs.
        These have lower latency but fewer resource options.
    :param resource_class: ``"standard"`` or ``"large"``. Only valid when
        ``use_batch_mode`` is False.
    :param resources: Only valid when ``use_batch_mode`` is True.
        Example: ``resources={"cpu": "2", "memory": "8Gi"}``.
    :param access_credentials_name: Only valid when ``use_batch_mode`` is True.

    Other:
    :param verbose: If True, enable verbose logging. Default: False.

    Return value:
    A ``DAG`` object. If you've named this ``dag``, you'll need to call
        ``dag.compute()``, ``dag.wait()``, and ``dag.end_results()``.
    """

    if use_batch_mode:
        if resource_class is not None:
            raise ValueError(
                "The resource_class argument is not applicable to batch mode"
            )

        if resources is None:
            resources = _DEFAULT_RESOURCES
        mode = dag.Mode.BATCH
    else:
        if resources is not None:
            raise ValueError(
                "The resources argument is not applicable to realtime mode"
            )
        if access_credentials_name is not None:
            raise ValueError(
                "The access_credentials_name argument is not applicable "
                "to realtime mode"
            )

        if resource_class is None:
            resource_class = "standard"
        mode = dag.Mode.REALTIME

    if soma_collection_uri is None and soma_experiment_uris is None:
        raise Exception(
            "Need just one of soma_collection_uri or " "soma_experiment_uris"
        )
    if soma_collection_uri is not None and soma_experiment_uris is not None:
        raise Exception(
            "Need just one of soma_collection_uri or " "soma_experiment_uris"
        )
    assert isinstance(task_graph_name, str)

    args_dict = args_dict or {}
    obs_attrs = obs_attrs or []
    var_attrs = var_attrs or []

    # Create context that enables faster array open
    # cfg_dict = cfg_dict or {}
    # cfg_dict["rest.use_refactored_array_open"] = True

    logger = get_logger_wrapper(verbose)
    logger.debug("tiledbsoma=%s" % tiledbsoma.__version__)

    # ----------------------------------------------------------------
    if soma_experiment_uris is None:
        logger.info(
            "Retrieving SOMA Experiment URIs from SOMACollection %s"
            % soma_collection_uri
        )

        # Alternative:
        #
        # with tiledbsoma.Collection.open(soma_collection_uri) as soco:
        #     soma_experiment_uris = {k: v.uri for k, v in soco.items()}
        #
        # -- however, that opens all the members sequentially, and we don't need
        # that overhead here in the launcher node.
        #
        # See also: sc-49443
        with tiledb.Group(soma_collection_uri) as grp:
            soma_experiment_uris = {mbr.name: mbr.uri for mbr in grp}

    if experiment_names is not None:
        logger.info("Filtering SOMA Experiment URIs for specified names")
        soma_experiment_uris = {
            k: v for k, v in soma_experiment_uris.items() if k in experiment_names
        }
    logger.info("Retrieved %d SOMA Experiment URIs" % len(soma_experiment_uris))

    # ----------------------------------------------------------------
    # Set log formatting

    logger.info("Constructing task graph")

    grf = dag.DAG(
        name=task_graph_name,
        mode=mode,
        namespace=namespace,
    )

    for experiment_name, soma_experiment_uri in soma_experiment_uris.items():
        logger.debug(f"Processing experiment '{experiment_name}'")
        grf.submit(
            _function_for_node,
            soma_experiment_uri,
            measurement_name=measurement_name,
            X_layer_name=X_layer_name,
            callback=callback,
            args_dict=args_dict,
            obs_query_string=obs_query_string,
            var_query_string=var_query_string,
            obs_attrs=obs_attrs,
            var_attrs=var_attrs,
            counts_only=counts_only,
            # Eaten by UDF infra -- won't make it to our callee as kwarg:
            resources=resources,
            # Eaten by UDF infra -- won't make it to our callee as kwarg:
            resource_class=resource_class,
            # Eaten by UDF infra -- won't make it to our callee as kwarg:
            access_credentials_name=access_credentials_name,
            name=experiment_name,
        )

    return grf


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

    query = exp.axis_query(measurement_name, obs_query=obs_query, var_query=var_query)

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
    """
    This function is not to be called directly: please use
    ``run_collection_mapper_workflow`` or
    ``build_collection_mapper_workflow_graph``. This is the function that runs
    as a UDF node for each ``SOMAExperiment`` you specify.
    """
    import tiledbsoma

    obs_query = None
    if obs_query_string is not None:
        obs_query = tiledbsoma.AxisQuery(value_filter=obs_query_string)

    var_query = None
    if var_query_string is not None:
        var_query = tiledbsoma.AxisQuery(value_filter=var_query_string)

    query = exp.axis_query(measurement_name, obs_query=obs_query, var_query=var_query)

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
) -> Any:
    import tiledbsoma

    if counts_only:
        experiment_query_func = _experiment_to_axis_counts
    else:
        experiment_query_func = _experiment_to_anndata_slice

    # ctx = tiledb.Ctx(cfg_dict)
    # exp = tiledbsoma.Experiment.open(experiment_uri, ctx=ctx)
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

    if result is None:
        return None

    if not args_dict:  # if dictionary is empty
        return callback(result)

    return callback(result, **args_dict)


# ----------------------------------------------------------------
# Until we fully get this version of tiledb.cloud deployed server-side, we must
# refer to all functions by value rather than by reference -- which is a fancy way
# of saying these functions _will not work at all_ until and unless they are
# checked into tiledb-cloud-py and deployed server-side. _All_ dev work _must_
# use this idiom.
_run_collection_mapper_workflow = functions.to_register_by_value(
    run_collection_mapper_workflow
)
_function_for_node = functions.to_register_by_value(function_for_node)
_experiment_to_anndata_slice = functions.to_register_by_value(
    experiment_to_anndata_slice
)
_experiment_to_axis_counts = functions.to_register_by_value(experiment_to_axis_counts)
