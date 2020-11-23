from ..dag.dag import Node, DAG

from ..array import apply as array_apply
from ..sql import exec as sql_exec
from ..udf import exec as udf_exec

import numbers


class DelayedBase(Node):
    def __init__(self, func, *args, name=None, dag=None, local_mode=False, **kwargs):
        self.timeout = None
        super().__init__(
            func, *args, name=name, dag=dag, local_mode=local_mode, **kwargs
        )

    def set_timeout(self, timeout):
        if timeout is not None and not isinstance(timeout, numbers.Number):
            raise TypeError(
                "timeout must be numeric value representing seconds to wait"
            )
        self.timeout = timeout

    def compute(self, namespace=None):
        """
        Execute function for node
        :param namespace: optional namespace to use for task
        :return: results
        """
        if self.dag is None:
            self.__set_all_parent_nodes_same_dag(DAG(namespace=namespace))

        if namespace is not None:
            self.dag.namespace = namespace

        self.dag.compute()
        super().wait(self.timeout)

        if not super().done():
            self.dag.cancel()

        return super().result()

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
        :param notebook: Is the visualization inside a jupyter notebook? If so we'll use a widget
        :param auto_update: Should the diagram be auto updated with each status change
        :param force_plotly: Force the use of plotly graphs instead of TileDB Plot Widget
        :return: returns plotly figure
        """
        if self.dag is None:
            self.__set_all_parent_nodes_same_dag(DAG())

        if self.dag is not None:
            return self.dag.visualize(
                notebook=notebook, auto_update=auto_update, force_plotly=force_plotly
            )

        return None

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
    def __init__(self, func_exec, *args, local=False, **kwargs):
        self.func_exec = func_exec
        if func_exec is not None and not callable(func_exec):
            raise TypeError("func_exec argument to `Node` must be callable!")

        if not local:
            super().__init__(udf_exec, func_exec, *args, local_mode=local, **kwargs)
        else:
            super().__init__(func_exec, *args, local_mode=local, **kwargs)

        # Set name of task if it won't interfere with user args
        if not self.local_mode:
            if "task_name" not in self.kwargs:
                self.kwargs["task_name"] = self.name

    def __call__(self, *args, **kwargs):
        if not self.local_mode:
            self.args = [self.func_exec, *args]
        else:
            self.args = args
        self.kwargs.update(kwargs)

        # Loop through non-default parameters and find any Node objects
        # Node objects will be used to automatically add dependencies
        if self.args is not None:
            super()._build_dependencies_list(self.args)

        # Loop through defaulted named parameters and find any Node objects
        # Node objects will be used to automatically add dependencies
        if self.kwargs is not None:
            super()._build_dependencies_list(self.kwargs)

        # Set name of task if it won't interfere with user args
        if not self.local_mode:
            if "task_name" not in self.kwargs:
                self.kwargs["task_name"] = self.name

        return self


class DelayedSQL(DelayedBase):
    def __init__(self, *args, **kwargs):
        super().__init__(sql_exec, *args, **kwargs)

        # Set name of task if it won't interfere with user args
        if "task_name" not in self.kwargs:
            self.kwargs["task_name"] = self.name

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs.update(kwargs)
        # Loop through non-default parameters and find any Node objects
        # Node objects will be used to automatically add dependencies
        if self.args is not None:
            super()._build_dependencies_list(self.args)

        # Loop through defaulted named parameters and find any Node objects
        # Node objects will be used to automatically add dependencies
        if self.kwargs is not None:
            super()._build_dependencies_list(self.kwargs)

        # Set name of task if it won't interfere with user args
        if "task_name" not in self.kwargs:
            self.kwargs["task_name"] = self.name

        return self


class DelayedArrayUDF(DelayedBase):
    def __init__(self, uri, func_exec, *args, **kwargs):
        self.func_exec = func_exec
        self.uri = uri

        if func_exec is not None and not callable(func_exec):
            raise TypeError("func_exec argument to `Node` must be callable!")

        super().__init__(array_apply, self.uri, self.func_exec, *args, **kwargs)

        # Set name of task if it won't interfere with user args
        if "task_name" not in self.kwargs:
            self.kwargs["task_name"] = self.name

    def __call__(self, *args, **kwargs):
        self.args = [self.uri, self.func_exec, *args]
        self.kwargs.update(kwargs)
        # Loop through non-default parameters and find any Node objects
        # Node objects will be used to automatically add dependencies
        if self.args is not None:
            super()._build_dependencies_list(self.args)

        # Loop through defaulted named parameters and find any Node objects
        # Node objects will be used to automatically add dependencies
        if self.kwargs is not None:
            super()._build_dependencies_list(self.kwargs)

        # Set name of task if it won't interfere with user args
        if "task_name" not in self.kwargs:
            self.kwargs["task_name"] = self.name

        return self
