"""Task graph and udf decorators."""

from contextlib import contextmanager
from functools import wraps
from typing import Callable, Optional, Union

import tiledb.cloud
from tiledb.cloud.dag.decorators._context import _dag_context
from tiledb.cloud.dag.decorators._inputs import TaskGraphInput
from tiledb.cloud.dag.decorators._log import log_tg_submission
from tiledb.cloud.utilities.logging import get_logger

logger = get_logger()


@contextmanager
def taskgraph_context(input: TaskGraphInput):
    """
    Context manager for task graphs, which creates a DAG with the specified parameters
    and pushes the DAG onto the context stack.

    :param input: TaskGraph input configuration
    :yield: the DAG
    """

    dag = tiledb.cloud.dag.DAG(
        max_workers=input.max_workers,
        mode=input.mode,
        name=input.name,
        namespace=input.namespace,
    )

    # add the DAG to the context variable.
    token = _dag_context.set(dag)
    logger.debug(f"DAG context object: {_dag_context}")
    try:
        # TODO: once in cararra, get the default namespace (get_self_user) and
        # use in logging
        logger.info(
            "Initialize DAG: "
            f"name={input.name}, mode={str(input.mode)}, namespace={input.namespace}"
        )
        yield dag
    finally:
        logger.debug(f"Destroyed DAG: name={input.name}")
        # remove DAG from the context variable.
        _dag_context.reset(token)


def taskgraph(
    func: Optional[Union[Callable, str]] = None,
    mode: str = "realtime",
    name: Optional[str] = None,
    namespace: Optional[str] = None,
    retry_limit: int = 0,
    timeout: Optional[int] = None,
    wait: bool = True,
    max_workers: Optional[int] = None,
    return_dag: bool = False,
):
    """Function decorator for a TileDB task graph. When a function wrapped
    with this decorator is executed:

        1. A new DAG is created.
        2. Calls to @udf wrapped functions are submitted to the DAG.
        3. The DAG is executed.
        4. Optionally wait for the DAG to complete.
        5. Return the results and optionally the DAG.

    example:

        ```python
        @udf
        def a(number):
            print(f"Received {number} from tg start")

            return number

        @udf(mode=Mode.BATCH)
        def b(number):
            print(f"Received {number} from a")

            return number

        @taskgraph(mode=Mode.REALTIME)
        def tg(number):

            o = a(number)
            o2 = b(o)  # batch mode overrided with taskgraph mode
            med = udf("TileDB-Inc/my_median", vals=[o2, 10])  # registered udf
            return med

        result = tg(1)
        ```

    Kwargs to the wrapped function can override kwargs in the original
        decorator following the convention of prepending the arg name
        with an underscore. For example:

        ```python
        @taskgraph(mode=Mode.REALTIME)
        def compute_taskgraph(a):
            # Do some work.
            pass

        # override the original task graph mode
        compute_taskgraph(16, _mode=Mode.LOCAL)
        ```

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
            input = TaskGraphInput(
                name=name,
                mode=mode,
                namespace=namespace,
                retry_limit=retry_limit,
                timeout=timeout,
                wait=wait,
                max_workers=max_workers,
                return_dag=return_dag,
            )

            input.sub_private(**kwargs)

            if input.name is None:
                input.name = func.__name__

            with taskgraph_context(input) as dag:
                # submits tasks to the task graph.
                result = func(*args, **kwargs)

                dag.compute()

                log_tg_submission(
                    namespace=dag.namespace,
                    server_graph_uuid=dag.server_graph_uuid,
                )

                if input.wait:
                    dag.wait()

                    # get the result from the Node, if needed.
                    if isinstance(result, tiledb.cloud.dag.Node):
                        result = result.result()

                # return the DAG and result, if requested.
                if input.return_dag:
                    return dag, result

                return result

        return wrapper

    # when no args passed to decorator
    if callable(func):
        return decorator(func)
    elif isinstance(func, str):
        raise ValueError("Calling registered taskgraph not yet supported.")
    else:
        return decorator


def get_arg_index(fn, arg_name):
    """Get the index of a functions arg by name."""
    # TODO: implement for expand
    pass
