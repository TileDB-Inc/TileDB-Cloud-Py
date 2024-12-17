"""TileDB UDF execution.
"""

from functools import wraps
from logging import INFO
from typing import Any, Callable, Mapping, Optional, Union

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
    """Execute a TileDB UDF."""

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
) -> Any:
    """Execute a TileDB UDF."""

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
            func=func,
            name=name,
            namespace=namespace,
            acn=acn,
            resources=resources,
            image_name=image_name,
            *args,
            **kwargs,
        )

    else:
        _udf


if __name__ == "__main__":
    # testing pathways

    # @udf(
    #     namespace="spencerseale",
    #     name="hello_world",
    #     resources={"cpu": "1", "memory": "1Gi"},
    # )
    # def hello_world(world: str) -> str:
    #     msg = f"Hello {world}!"

    #     print(msg)

    #     return msg

    # graph = hello_world(world="earth")

    udf(
        func="tiledb://TileDB-Inc/ls_uri",
        uri="s3://tiledb-spencer/junk",
        config={"vfs.s3.region": "us-west-2"},
        namespace="TileDB-Inc",
        acn="tiledb-cloud-sandbox-role",
        resources={"cpu": "1", "memory": "1Gi"},
    )
