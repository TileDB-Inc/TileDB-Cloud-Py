import numbers
import random
from typing import Any, Callable, Optional, Union

from tiledb.cloud._common import functions
from tiledb.cloud.array import ArrayList
from tiledb.cloud.array import apply as array_apply
from tiledb.cloud.array import exec_multi_array_udf
from tiledb.cloud.dag.dag import DAG
from tiledb.cloud.dag.dag import Mode
from tiledb.cloud.dag.dag import Node
from tiledb.cloud.sql import exec as sql_exec
from tiledb.cloud.udf import exec as udf_exec


class DelayedBase(Node):
    def __init__(
        self,
        func,
        *args,
        name=None,
        dag=None,
        local_mode=False,
        mode=Mode.REALTIME,
        **kwargs,
    ):
        self.timeout = None

        if local_mode:
            mode = Mode.LOCAL
        super().__init__(func, *args, name=name, dag=dag, mode=mode, **kwargs)

    def __call__(self, *args, **kwargs):
        self.args += args
        self.kwargs.update(kwargs)
        self._find_deps()

        return self

    def set_timeout(self, timeout):
        if timeout is not None and not isinstance(timeout, numbers.Number):
            raise TypeError(
                "timeout must be numeric value representing seconds to wait"
            )
        self.timeout = timeout

    def compute(
        self, namespace: Optional[str] = None, name: Optional[str] = None
    ) -> Any:
        """
        Starts execution of all Delayed tasks associated with this node.

        :param namespace: The namespace to execute tasks under, if different
            than the user's default.
        :param name: An optional name to identify the task graph in logs.
        :return: results
        """
        if self.dag is None:
            mode = self.mode
            if self.mode == Mode.LOCAL:
                mode = Mode.REALTIME
            self.__set_all_parent_nodes_same_dag(
                DAG(namespace=namespace, name=name, mode=mode)
            )
        else:
            if namespace is not None:
                self.dag.namespace = namespace
            if name is not None:
                self.dag.name = name

        assert self.dag

        self.dag.compute()
        return self.result(self.timeout)

    def __set_all_parent_nodes_same_dag(self, dag):
        # If this node already has the day we have reached a base case
        if self.dag == dag:
            return

        self.dag = dag
        self.dag.add_node_obj(self)
        for node in self.parents.values():
            node.__set_all_parent_nodes_same_dag(dag)
        for node in self.children.values():
            node.__set_all_parent_nodes_same_dag(dag)

    def visualize(self, notebook=True, auto_update=True, force_plotly=False):
        """
        Build and render a tree diagram of the DAG.
        :param notebook: Is the visualization inside a jupyter notebook?
            If so we'll use a widget
        :param auto_update: Should the diagram be auto updated with each status change
        :param force_plotly: Force the use of plotly graphs instead of
            TileDB Plot Widget
        :return: returns plotly figure
        """
        if self.dag is None:
            self.__set_all_parent_nodes_same_dag(DAG())

        return self.dag.visualize(
            notebook=notebook, auto_update=auto_update, force_plotly=force_plotly
        )

    @staticmethod
    def all(futures, namespace=None):
        """
        Run a list of Delayed object all in parallel
        :param futures: list of Delayed objects to run
        :param namespace: optional namespace to run all tasks in
        :return: list of results in order of futures
        """
        if futures is None:
            raise ValueError("list of delayed object must not be null")

        dag = DAG()

        for delayed in futures:
            dag.add_node_obj(delayed)

        dag.namespace = namespace
        dag.compute()

        ret = []
        for delayed in futures:
            ret.append(delayed.result())

        return ret


class Delayed(DelayedBase):
    def __init__(self, func_exec, *args, local=False, mode=Mode.REALTIME, **kwargs):
        functions.check_funcable(func_exec=func_exec)
        self.func_exec = func_exec

        kwargs.setdefault("name", functions.full_name(func_exec) + _random_suffix())

        if local:
            mode = Mode.LOCAL

        if not local:
            super().__init__(
                udf_exec, func_exec, *args, local_mode=local, mode=mode, **kwargs
            )
        elif callable(func_exec):
            super().__init__(func_exec, *args, local_mode=local, mode=mode, **kwargs)
        else:
            raise TypeError(
                "When running a function locally, it must be a callable "
                "and not the registered name of a UDF."
            )


class DelayedSQL(DelayedBase):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("name", "SQL query" + _random_suffix())

        super().__init__(sql_exec, *args, **kwargs)


class DelayedArrayUDF(DelayedBase):
    def __init__(self, uri, func_exec, *args, **kwargs):
        functions.check_funcable(func_exec=func_exec)
        self.func_exec = func_exec
        self.uri = uri
        kwargs.setdefault("name", functions.full_name(func_exec) + _random_suffix())

        super().__init__(array_apply, self.uri, self.func_exec, *args, **kwargs)


class DelayedMultiArrayUDF(DelayedBase):
    def __init__(
        self,
        func: Union[str, Callable],
        array_list: ArrayList,
        *args,
        **kwargs,
    ):
        functions.check_funcable(func=func)
        self.func_exec = func
        self.array_list = array_list
        kwargs.setdefault("name", functions.full_name(func) + _random_suffix())

        super().__init__(
            exec_multi_array_udf, self.func_exec, self.array_list, *args, **kwargs
        )


def _random_suffix() -> str:
    """Generates a random suffix for node names.

    Because Delayed objects don't have access to a DAG when they are created,
    it's impossible for them to know what names have or have not been used.
    To work around this, we generate a random suffix and assume it works.
    """
    # Alphanumerics with no ambiguous symbols and no vowels.
    letters = (random.choice("3479bcdfghjkmnpqrstvwxz") for _ in range(4))
    return f" ({''.join(letters)})"
