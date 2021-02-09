from . import array, sql, udf
from .dag import DAG, Node, Status

import numbers


class DelayedBase(Node):
    def __init__(self, func, *args, **kwargs):
        self.timeout = None
        super().__init__(func, *args, **kwargs)
        # Set name of task if it won't interfere with user args
        if not self.local_mode:
            self.kwargs.setdefault("task_name", self.name)

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
        if not self.local_mode:
            self.kwargs.setdefault("task_name", self.name)

        return self

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
        self.dag.wait(self.timeout)

        if self.dag.status == Status.FAILED:
            # reraise the first failed node exception
            raise next(iter(self.dag.failed_nodes.values())).future.exception()

        return self.result()

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

        dag = DAG(namespace=namespace)
        for future in futures:
            dag.add_node_obj(future)
        dag.compute()

        return [future.result() for future in futures]


class Delayed(DelayedBase):
    def __init__(self, func_exec, *args, **kwargs):
        if func_exec is not None and not callable(func_exec):
            raise TypeError("func_exec argument to `Node` must be callable!")

        kwargs["local_mode"] = kwargs.pop("local", False)
        if kwargs["local_mode"]:
            super().__init__(func_exec, *args, **kwargs)
        else:
            super().__init__(udf.exec, func_exec, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.local_mode:
            return super().__call__(*args, **kwargs)
        else:
            return super().__call__(self.args[0], *args, **kwargs)


class DelayedSQL(DelayedBase):
    def __init__(self, *args, **kwargs):
        super().__init__(sql.exec, *args, **kwargs)


class DelayedArrayUDF(DelayedBase):
    def __init__(self, uri, func_exec, *args, **kwargs):
        if func_exec is not None and not callable(func_exec):
            raise TypeError("func_exec argument to `Node` must be callable!")
        super().__init__(array.apply, uri, func_exec, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return super().__call__(self.args[0], self.args[1], *args, **kwargs)
