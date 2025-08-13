import enum
import webbrowser
from contextvars import ContextVar
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Mapping, Optional, Sequence, Union

from attrs import define
from attrs import field

from tiledb.cloud import models
from tiledb.cloud.dag import DAG
from tiledb.cloud.dag import Mode
from tiledb.cloud.dag.decorators._resources import Resources
from tiledb.cloud.dag.decorators._resources import load_defaults
from tiledb.cloud.udf import exec as udf_exec
from tiledb.cloud.utilities.logging import get_logger

logger = get_logger()

# Context variable to hold the active (and potentially nested) DAG contexts.
_dag_context: ContextVar[DAG] = ContextVar("current_dag")


@dataclass(frozen=True)
class UDFConfig:
    """Configuration for UDF decorator execution."""

    expand: Optional[str] = None
    image_name: Optional[str] = None
    name: Optional[str] = None
    mode: enum.Enum = Mode.REALTIME
    namespace: Optional[str] = None
    acn: Optional[str] = None
    retry_limit: int = 0
    resources: Optional[Resources] = None
    timeout: Optional[int] = None


@define
class UDFHandler:
    """Orchestrate UDF mode to run:"""

    func: Union[callable, str]
    """Function to execute."""
    args: Sequence[Any]
    """Positional arguments to pass to function."""
    kwargs: Mapping[str, Any]
    """Keyword arguments to pass to function."""
    config: UDFConfig
    """UDF configuration."""
    mode_opts: Sequence[str] = field(
        factory=lambda: load_defaults(
            file="modes.toml",
            toml_key="mode_options",
        )
    )
    """Valid execution modes."""
    log_url: str = "https://cloud.tiledb.com/activity/taskgraphs/{}/{}"
    """Task graph log URL."""

    def __attrs_post_init__(self) -> None:
        if str(self.config.mode).lower() not in self.mode_opts:
            raise ValueError(f"Invalid UDF mode: {self.config.mode}")

    def exec_local(self) -> Any:
        """Exec local UDF.

        :return: Return value of function.
        """

        self.func(*self.args, **self.kwargs)

    def exec_realtime(self) -> Any:
        """Exec realtime UDF.

        :return: Return value of function.
        """

        return udf_exec(
            self.func,
            *self.args,
            task_name=self.config.name,
            namespace=self.config.namespace,
            resource_class=self.config.resources.resource_class
            if self.config.resources
            else None,
            image_name=self.config.image_name,
            timeout=self.config.timeout,
            **self.kwargs,
        )

    def exec_batch(
        self,
        open_browser: bool = False,
    ) -> DAG:
        """Exec batch UDF.

        Async execution, obtain results from DAG.

        `open_browser` is not yet wired from caller. TBD if this feature is suitable.

        :param open_browser: Whether to open browser to batch UDF logs.
        :return: Running DAG object.
        """

        graph = DAG(
            name=f"batch->{self.config.name}",
            namespace=self.config.namespace,
            mode=Mode.BATCH,
            retry_strategy=models.RetryStrategy(
                limit=self.config.retry_limit,
                retry_policy="Always",
            ),
            deadline=self.config.timeout,
        )

        graph.submit(
            self.func,
            *self.args,
            name=self.config.name,
            access_credentials_name=self.config.acn,
            resources={
                "cpu": str(self.config.resources.cpu),
                "memory": f"{self.config.resources.memory_gb}Gi",
            }
            if self.config.resources
            else None,
            image_name=self.config.image_name,
            **self.kwargs,
        )

        graph.compute()

        task_uri = self.log_url.format(
            graph.namespace,
            graph.server_graph_uuid,
        )

        logger.info(f"TileDB Cloud task submitted - {task_uri}")

        if open_browser:
            try:
                webbrowser.open_new_tab(task_uri)
            except webbrowser.Error:
                logger.debug("Unable to access webrowser.")

        return graph

    def run(self) -> Union[Any, DAG]:
        """Run UDF.

        :return: Return value of function or a running DAG.
        """

        if self.config.mode == "local":
            return self.exec_local()
        else:
            return (
                self.exec_realtime()
                if self.config.mode == Mode.REALTIME
                else self.exec_batch()
            )


def exec_registered_udf(
    func: str,
    *args: Any,
    name: Optional[str] = None,
    mode: str = "realtime",
    namespace: Optional[str] = None,
    acn: Optional[str] = None,
    resources: Optional[Resources] = None,
    image_name: Optional[str] = None,
    retry_limit: int = 0,
    **kwargs: Mapping[str, Any],
) -> Union[Any, DAG]:
    """Execute a registered UDF.

    :param func: UDF name (e.g. namespace/udf-name).
    :param args: Positional arguments to pass to function.
    :param name: Task name.
    :param mode: Execution mode.
    :param namespace: Namespace to run registered UDF in.
    :param acn: TileDB access credential name.
    :param resources: Resources to apply to UDF.
    :param image_name: UDF image name.
    :param retry_limit: Maximum retry attempts.
    :param kwargs: Keyword arguments to pass to function.
    :return: Return value of function or a running DAG.
    """

    config = UDFConfig(
        name=name,
        mode=mode,
        namespace=namespace,
        acn=acn,
        image_name=image_name,
        retry_limit=retry_limit,
        resources=resources,
    )

    runner = UDFHandler(
        func=func,
        args=args,
        kwargs=kwargs,
        config=config,
    )

    return runner.run()


def udf(
    func: Optional[Union[Callable, str]] = None,
    *registered_args: Any,
    resource_class: Optional[str] = None,
    cpu: Optional[int] = None,
    memory_gb: Optional[int] = None,
    expand: Optional[str] = None,
    image_name: Optional[str] = None,
    name: Optional[str] = None,
    mode: enum.Enum = Mode.REALTIME,
    namespace: Optional[
        str
    ] = None,  # For UDF execution, separate from function namespace
    acn: Optional[str] = None,
    retry_limit: int = 0,
    **registered_kwargs: Mapping[str, Any],
) -> Any:
    """
    Function decorator for a TileDB task. When a function wrapped with this decorator
    is executed:

    1. Get the DAG from the current DAG context.
    2. Submit the task to the DAG using the specified parameters.

    If the decorated function is run outside of a DAG context, it will run locally.

    Kwargs to the wrapped function can override kwargs in the original decorator
    following the convention of prepending the arg name with an underscore.

    For example:

        ```python
        @udf(resource_class="standard")
        def compute_task(a):
            # Do some work.
            return result

        @taskgraph(mode="realtime")
        def compute_taskgraph(a):
            # Override the original resource class.
            return compute_task(a, _resource_class="large")

        # Run the task graph.
        compute_taskgraph(16)
        ```

    :param resource_class: TileDB resource class, "standard"|"large", defaults to None
    :param cpu: number of vCPUs required, defaults to None
    :param memory_gb: GiB of memory required, defaults to None
    :param expand: name of the argument to expand and create multiple tasks dynamically,
        defaults to None
    :param image_name: TileDB UDF image name, defaults to None
    :param name: the task name in TileDB logs, defaults to None, which uses the function
        name
    :param mode: execution mode when running as a single UDF,
        Mode.REALTIME|Mode.BATCH|Mode.LOCAL. defaults to Mode.REALTIME
    :param namespace: TileDB namespace when running as a single UDF, defaults to None
    :param acn: TileDB access credential name to authenticate batch UDF
        to access underingly storage backend. Not applicable to realtime mode.
    :param retry_limit: Maximum retry attempts for batch UDF.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f"args: {args}")
            logger.debug(f"kwargs: {kwargs}")

            _expand = kwargs.pop("_expand", expand)
            _image_name = kwargs.pop("_image_name", image_name)
            _name = kwargs.pop("_name", name or func.__name__)
            _mode = kwargs.pop("_mode", mode)
            _namespace = kwargs.pop("_namespace", namespace)
            _acn = kwargs.pop("_acn", acn)
            _retry_limit = kwargs.pop("_retry_limit", retry_limit)

            # Get the current DAG from the context variable.
            # only applicable when udf included in @taskgraph
            dag = _dag_context.get(None)

            _mode = _mode if not dag else str(dag.mode).lower()

            _resources = Resources(
                resource_class=kwargs.pop("_resource_class", resource_class),
                cpu=kwargs.pop("_cpu", cpu),
                memory_gb=kwargs.pop("_memory_gb", memory_gb),
                mode=_mode,
                validate_on_init=True,
            )

            # Create config for UDF execution
            config = UDFConfig(
                expand=_expand,
                image_name=_image_name,
                name=_name,
                mode=_mode,
                namespace=_namespace,
                acn=_acn,
                retry_limit=_retry_limit,
                resources=_resources,
            )

            # task is being run outside of a DAG context, run standalone UDF
            if dag is None:
                udf_runner = UDFHandler(
                    func=func,
                    args=args,
                    kwargs=kwargs,
                    config=config,
                )

                return udf_runner.run()
            else:
                if _expand is not None and _expand not in kwargs:
                    raise ValueError(f"Expand argument '{_expand}' must be a kwarg")

                logger.info(f"Running task: {_name} in '{dag}'")

                # Update kwargs for the submit.
                kwargs["name"] = _name
                if not dag._is_local:
                    if _image_name:
                        kwargs["image_name"] = _image_name

                    if dag._is_realtime:
                        kwargs["resource_class"] = _resources.resource_class
                        if _expand:
                            raise ValueError(
                                "Expand is only supported in batch task graphs"
                            )
                        submit = dag.submit
                    # batch
                    else:
                        kwargs["access_credentials_name"] = dag._acn
                        kwargs["resources"] = {
                            "cpu": str(_resources.cpu),
                            "memory": f"{_resources.memory_gb}Gi",
                        }
                        if _expand:
                            kwargs["expand_node_output"] = kwargs.get(_expand, None)
                            submit = dag.submit_udf_stage
                        submit = dag.submit_udf_stage if _expand else dag.submit

                else:
                    submit = dag.submit_local

                logger.info(f"Submit task: {_name}")
                logger.info(f"  args = {args}")
                logger.info(f"  kwargs = {kwargs}")

                # Submit the task to the DAG.
                return submit(func, *args, **kwargs)

        return wrapper

    # when no args passed to decorator
    if callable(func):
        return decorator(func)
    # TODO: registered udf cannot inherit DAG context.
    # can only be called standalone (e.g. udf("namespace/udf", ...))
    elif isinstance(func, str):
        return exec_registered_udf(
            func=func,
            *registered_args,
            name=name or func,
            mode=mode,
            namespace=namespace,
            acn=acn,
            resources=Resources(
                resource_class=resource_class,
                cpu=cpu,
                memory_gb=memory_gb,
                mode=mode,
            ),
            image_name=image_name,
            retry_limit=retry_limit,
            **registered_kwargs,
        )
    else:
        return decorator
