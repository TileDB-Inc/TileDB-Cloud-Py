"""TileDB UDF execution.
"""

from functools import wraps
from logging import INFO
from typing import Callable, Mapping, Optional, Union

from ..dag import DAG
from ..dag import Mode
from ._di_container import DIContainer


def _exec_udf(
    func: Optional[Union[Callable, str]] = None,
    name: Optional[str] = None,
    namespace: Optional[str] = None,
    acn: Optional[str] = None,
    resources: Optional[Union[str, Mapping[str, str]]] = "standard",
    image_name: Optional[str] = None,
    *args,
    **kwargs,
) -> DAG:
    di = DIContainer(mode=Mode.REALTIME if isinstance(resources, str) else Mode.BATCH)

    logger = di.logger(level=INFO)

    structured_name = di.name(name=name)

    udf_runner = di.graph(
        name=structured_name.taskgraph,
        namespace=namespace,
    )

    # TODO: check if realtime can accept access_credentials_name keyword
    # arg or if I need to set to None

    resource_class = resources if di.mode == Mode.REALTIME else None
    udf_runner.submit(
        func,
        *args,
        **kwargs,
        name=structured_name.task,
        access_credentials_name=acn,
        resource_class=resource_class,
        resources=resources if not resource_class else None,
        image_name=image_name,
    )

    udf_runner.compute()

    logger.info(
        "{} submitted: https://cloud.tiledb.com/taskgraphlogs/{}/{}".format(
            udf_runner.name,
            udf_runner.namespace,
            udf_runner.server_graph_uuid,
        )
    )

    return udf_runner


def udf(
    func: Optional[Union[Callable, str]] = None,
    name: Optional[str] = None,
    namespace: Optional[str] = None,
    acn: Optional[str] = None,
    resources: Optional[Union[str, Mapping[str, str]]] = "standard",
    image_name: Optional[str] = None,
    *args,
    **kwargs,
) -> DAG:
    """Execute a TileDB UDF.

    For in-memory executables, use as a decorator.
    For registered UDFs, pass <namespace>/<udf_name> to `func`.

    Examples:

    .. code-block:: python

        @udf
        def hello_world(world: str) -> str:
            msg = f"Hello {world}!"

            return msg

        graph = hello_world(world="earth")

    .. code-block:: python

        @udf(
            namespace="foo",
            name="batch_hello_world",
            acn="my-role",
            resources={"cpu": "1", "memory": "1Gi"},
        )
        def hello_world(world: str) -> str:
            msg = f"Hello {world}!"

            return msg

        graph = hello_world(world="earth")

    .. code-block:: python

        graph = udf(
            func="TileDB-Inc/ls_uri",
            uri="s3://bucket/object",
            name="Registered UDF exec.",
            acn="my-role",
            namespace="TileDB-Inc",
            resources={"cpu": "1", "memory": "1Gi"},
        )

    :param func: Executable or path to registered UDF to execute.
    :param name: Name of UDF.
    :param namespace: TileDB namespace to execute in.
    :param acn: TileDB access credential name.
    :param resources: Resources for UDF.
    :param image_name: Docker image name.
    :param *args: Positional args to pass to func.
    :param **kwargs: Keyword args to pass to func.
    :return: Running task graph instance.
    """

    def _udf(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*wrapper_args, **wrapper_kwargs) -> DAG:
            graph = _exec_udf(
                func=func,
                name=name,
                namespace=namespace,
                acn=acn,
                resources=resources,
                image_name=image_name,
                *wrapper_args,
                **wrapper_kwargs,
            )

            return graph

        return wrapper

    # in cases where no optional args passed to decorator
    if callable(func):
        return _udf(func)
    elif isinstance(func, str):
        return _exec_udf(
            func=func.replace("tiledb://", "")
            if func.startswith("tiledb://")
            else func,
            name=name,
            namespace=namespace,
            acn=acn,
            resources=resources,
            image_name=image_name,
            *args,
            **kwargs,
        )
    else:
        return _udf
