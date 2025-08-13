"""Task graph and udf decorators."""

from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
from typing import Callable, Optional, Union

import tiledb.cloud
from tiledb.cloud.utilities.logging import get_logger

logger = get_logger()

MODES = ["local", "realtime", "batch"]


# Context variable to hold the active (and potentially nested) DAG contexts.
_dag_context: ContextVar[tiledb.cloud.dag.DAG] = ContextVar("current_dag")


# TODO: add timeout, result_format, retry_strategy, deadline


@contextmanager
def taskgraph_context(
    acn: Optional[str] = None,
    max_workers: Optional[int] = None,
    mode: str = "realtime",
    name: Optional[str] = None,
    namespace: Optional[str] = None,
):
    """
    Context manager for task graphs, which creates a DAG with the specified parameters
    and pushes the DAG onto the context stack.

    :param acn: TileDB access credentials name, defaults to None
    :param max_workers: max parallel workers, defaults to None
    :param mode: task graph mode, "realtime"|"batch"|"local", defaults to None
    :param name: task graph name, defaults to None
    :param namespace: TileDB namespace, defaults to None
    :yield: the DAG
    """

    # Validate user input and set the mode.
    if mode == "realtime" or mode == "local":
        mode_enum = tiledb.cloud.dag.Mode.REALTIME
    elif mode == "batch":
        mode_enum = tiledb.cloud.dag.Mode.BATCH
    else:
        raise ValueError(f"Invalid mode: {mode}")

    # Create the DAG.
    dag = tiledb.cloud.dag.DAG(
        max_workers=max_workers,
        mode=mode_enum,
        name=name,
        namespace=namespace,
    )

    # Add state used when submitting tasks.
    dag._acn = acn if mode == "batch" else None
    dag._is_realtime = mode == "realtime"
    dag._is_local = mode == "local"
    dag._is_batch = mode == "batch"

    # Add the DAG to the context variable.
    token = _dag_context.set(dag)
    try:
        logger.info(f"Create DAG: {name}, mode={mode}, namespace={namespace}")
        yield dag
    finally:
        logger.info(f"Destroy DAG: {name}")
        # Remove the DAG from the context variable.
        _dag_context.reset(token)


def taskgraph(
    func: Optional[Union[Callable, str]] = None,
    acn: Optional[str] = None,
    max_workers: Optional[int] = None,
    mode: str = "realtime",
    name: Optional[str] = None,
    namespace: Optional[str] = None,
    wait: bool = True,
    return_dag: bool = False,
):
    """Function decorator for a TileDB task graph. When a function wrapped
    with this decorator is executed:

        1. A new DAG is created.
        2. Calls to @task wrapped functions are submitted to the DAG.
        3. The DAG is executed.
        4. Optionally wait for the DAG to complete.
        5. Return the results and optionally the DAG.

    Kwargs to the wrapped function can override kwargs in the original
        decorator following the convention of prepending the arg name
        with an underscore. For example:

        ```python
        @taskgraph(mode="realtime")
        def compute_taskgraph(a):
            # Do some work.
            pass

        # Override the original task graph mode
        compute_taskgraph(16, _mode="local")
        ```

    :param acn: TileDB access credentials name, defaults to None
    :param max_workers: max parallel workers, defaults to None
    :param mode: task graph mode, "realtime"|"batch"|"local", defaults to None
    :param name: task graph name, defaults to None
    :param namespace: TileDB namespace, defaults to None
    :param wait: wait for the task graph to complete, defaults to True
    :param return_dag: return the DAG object with the result, defaults to False
    """

    def decorator(func):
        """Return a function wrapper configured with the decorator arguments."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Optionally override decorator args with function kwargs.
            _acn = kwargs.pop("_acn", acn)
            _max_workers = kwargs.pop("_max_workers", max_workers)
            _mode = kwargs.pop("_mode", mode)
            _name = kwargs.pop("_name", name or func.__name__)
            _namespace = kwargs.pop("_namespace", namespace)
            _wait = kwargs.pop("_wait", wait)
            _return_dag = kwargs.pop("_return_dag", return_dag)

            # Validate user input.
            if _mode not in MODES:
                raise ValueError(f"Invalid mode: {_mode}")

            # Create the DAG with the context manager.
            with taskgraph_context(
                acn=_acn,
                max_workers=_max_workers,
                mode=_mode,
                name=_name,
                namespace=_namespace,
            ) as dag:
                # Run the wrapped function, which submits tasks to the task graph.
                result = func(*args, **kwargs)

                # Execute the DAG.
                dag.compute()

                # Optionally wait for the DAG to complete.
                if _wait:
                    dag.wait()

                    # Get the result from the Node, if needed.
                    if isinstance(result, tiledb.cloud.dag.Node):
                        result = result.result()

                # Return the DAG and result, if requested.
                if _return_dag:
                    return dag, result

                return result

        return wrapper

    # when no args passed to decorator
    if callable(func):
        return decorator(func)
    elif isinstance(func, str):
        raise ValueError("Calling registered UDF not yet supported.")
    else:
        return decorator


def get_arg_index(fn, arg_name):
    """Get the index of a functions arg by name."""
    # TODO: implement for expand
    pass
