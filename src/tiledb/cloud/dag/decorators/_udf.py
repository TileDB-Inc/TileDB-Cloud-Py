import enum
import webbrowser
from functools import wraps
from typing import Any, Callable, Mapping, Optional, Sequence, Union

from attrs import define

from tiledb.cloud import models
from tiledb.cloud.dag import DAG
from tiledb.cloud.dag import Mode
from tiledb.cloud.dag.decorators._context import _dag_context
from tiledb.cloud.dag.decorators._inputs import UDFInput
from tiledb.cloud.dag.decorators._log import log_node_submission
from tiledb.cloud.dag.decorators._log import log_tg_submission
from tiledb.cloud.dag.decorators._resources import Resources
from tiledb.cloud.udf import exec as udf_exec
from tiledb.cloud.utilities.logging import get_logger

logger = get_logger()


@define
class UDFHandler:
    """Orchestrate UDF mode to run:"""

    func: Union[callable, str]
    """Function to execute."""
    args: Sequence[Any]
    """Positional arguments to pass to function."""
    kwargs: Mapping[str, Any]
    """Keyword arguments to pass to function."""
    input: UDFInput
    """UDF input configuration."""
    log_url: str = "https://cloud.tiledb.com/activity/taskgraphs/{}/{}"
    """Task graph log URL."""

    def __attrs_post_init__(self) -> None:
        # fix name if not set
        if self.input.name is None:
            try:
                self.input.name = self.func.__name__
            except AttributeError:
                if isinstance(self.func, str):
                    self.input.name = self.func

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
            task_name=self.input.name,
            namespace=self.input.namespace,
            resource_class=self.input.resources.resource_class
            if self.input.resources
            else None,
            image_name=self.input.image_name,
            timeout=self.input.timeout,
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
            name=f"batch->{self.input.name}",
            namespace=self.input.namespace,
            mode=Mode.BATCH,
            retry_strategy=models.RetryStrategy(
                limit=self.input.retry_limit,
                retry_policy="Always",
            ),
            deadline=self.input.timeout,
        )

        graph.submit(
            self.func,
            *self.args,
            name=self.input.name,
            access_credentials_name=self.input.acn,
            resources={
                "cpu": str(self.input.resources.cpu),
                "memory": f"{self.input.resources.memory_gb}Gi",
            }
            if self.input.resources
            else None,
            image_name=self.input.image_name,
            **self.kwargs,
        )

        graph.compute()

        task_uri = log_tg_submission(
            namespace=graph.namespace,
            server_graph_uuid=graph.server_graph_uuid,
        )

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

        self.input.resources.validate(self.input.mode)

        if self.input.mode == "local":
            return self.exec_local()
        else:
            return (
                self.exec_realtime()
                if self.input.mode == Mode.REALTIME
                else self.exec_batch()
            )

    def run_in_dag(self, dag: DAG) -> Union[Any, DAG]:
        self.input.resources.validate(self.input.mode)

        if self.input.mode != Mode.LOCAL:
            # Prepare dynamic parameters
            dyn_params = {}
            if self.input.mode == Mode.REALTIME:
                rkey = "resource_class"
                if self.input.resources and self.input.resources.resource_class:
                    dyn_params[rkey] = self.input.resources.resource_class
                if self.input.expand:
                    raise ValueError("'expand' is only supported in batch task graphs")
                submit = dag.submit
            # batch
            else:
                if self.input.resources:
                    rkey = "resources"
                    dyn_params[rkey] = {
                        "cpu": str(self.input.resources.cpu),
                        "memory": f"{self.input.resources.memory_gb}Gi",
                    }
                if self.input.expand:
                    dyn_params["expand_node_output"] = self.input.expand
                submit = dag.submit_udf_stage if self.input.expand else dag.submit

            log_node_submission(
                name=self.input.name,
                dag=dag,
                args=self.args,
                kwargs=self.kwargs,
                resources=dyn_params[rkey],
            )

            # Submit the task to the DAG with dynamic parameters
            return submit(
                self.func,
                name=self.input.name,
                image_name=self.input.image_name,
                access_credentials_name=self.input.acn,
                *self.args,
                **dyn_params,
                **self.kwargs,
            )

        else:
            # submit = dag.submit_local
            return dag.submit_local(
                self.func,
                name=self.input.name,
                *self.args,
                **self.kwargs,
            )


def _udf(
    func: Optional[Union[Callable, str]] = None,
    *args: Any,
    name: Optional[str] = None,
    mode: enum.Enum = Mode.REALTIME,
    namespace: Optional[str] = None,
    retry_limit: int = 0,
    timeout: Optional[int] = None,
    wait: bool = True,
    acn: Optional[str] = None,
    resource_class: Optional[str] = None,
    cpu: Optional[int] = None,
    memory_gb: Optional[int] = None,
    expand: Optional[str] = None,
    image_name: Optional[str] = None,
    **kwargs: Mapping[str, Any],
) -> Any:
    logger.debug(f"args: {args}")
    logger.debug(f"kwargs: {kwargs}")

    resources = Resources(
        resource_class=resource_class,
        cpu=cpu,
        memory_gb=memory_gb,
    )

    input = UDFInput(
        name=name,
        mode=mode,
        namespace=namespace,
        retry_limit=retry_limit,
        timeout=timeout,
        wait=wait,
        acn=acn,
        resources=resources,
        expand=expand,
        image_name=image_name,
    )

    # sub in private overrides if any
    input.sub_private(**kwargs)

    udf_runner = UDFHandler(
        func=func,
        args=args,
        kwargs=kwargs,
        input=input,
    )

    # Get the current DAG from the context variable.
    # only applicable when udf included in @taskgraph
    try:
        dag = _dag_context.get()
        logger.debug(f"DAG context found: {_dag_context}")
    except LookupError:
        dag = None
        logger.debug("No DAG in context.")

    # task is being run outside of a DAG context, run standalone UDF
    if dag is None:
        logger.debug("Running UDF in standalone")
        return udf_runner.run()
    else:
        logger.debug("Running UDF within DAG context")

        # inherit dag mode to override udf mode if conflict
        if input.mode != dag.mode:
            logger.warning(
                f"UDF mode: {input.mode} != DAG mode: {dag.mode}. Inheriting DAG mode."
            )
            input.mode = dag.mode

        return udf_runner.run_in_dag(dag)


def udf(
    func: Optional[Union[Callable, str]] = None,
    *args: Any,
    resource_class: Optional[str] = None,
    cpu: Optional[int] = None,
    memory_gb: Optional[int] = None,
    expand: Optional[str] = None,
    image_name: Optional[str] = None,
    name: Optional[str] = None,
    mode: enum.Enum = Mode.REALTIME,
    namespace: Optional[str] = None,
    acn: Optional[str] = None,
    retry_limit: int = 0,
    **kwargs: Mapping[str, Any],
) -> Any:
    """Execute or decorate a function as a TileDB UDF.

    Example:

        ```python
        @udf
        def compute_task(a):
            return result

        # Run the UDF.
        compute_task(16)
        ```

    Kwargs to the wrapped function can override kwargs in the original decorator
    following the convention of prepending the arg name with an underscore.

    For example:

        ```python
        @udf(resource_class="standard")
        def compute_task(a):
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
            return _udf(
                func,
                *args,
                resource_class=resource_class,
                cpu=cpu,
                memory_gb=memory_gb,
                expand=expand,
                image_name=image_name,
                name=name,
                mode=mode,
                namespace=namespace,
                acn=acn,
                retry_limit=retry_limit,
                **kwargs,
            )

        return wrapper

    # when no args passed to decorator
    if callable(func):
        return decorator(func)
    elif isinstance(func, str):
        return _udf(
            func,
            *args,
            resource_class=resource_class,
            cpu=cpu,
            memory_gb=memory_gb,
            expand=expand,
            image_name=image_name,
            name=name,
            mode=mode,
            namespace=namespace,
            acn=acn,
            retry_limit=retry_limit,
            **kwargs,
        )
    else:
        return decorator
