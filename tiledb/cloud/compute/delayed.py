from ..dag.dag import Node, DAG
from .. import array, sql, udf, retry_task

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
    def __init__(self, func_exec, *args, **kwargs):
        if func_exec is not None and not callable(func_exec):
            raise TypeError("func_exec argument to `Node` must be callable!")

        retrying = kwargs.pop("retrying", None)
        kwargs["local_mode"] = kwargs.pop("local", False)
        if not kwargs["local_mode"]:
            if retrying is None:
                func = udf.exec
            else:
                func = get_retriable_exec(udf.exec_async, retrying)
            super().__init__(func, func_exec, *args, **kwargs)
            # Set name of task if it won't interfere with user args
            self.kwargs.setdefault("task_name", self.name)
        else:
            if retrying is not None:
                func_exec = retrying.wraps(func_exec)
            super().__init__(func_exec, *args, **kwargs)

        self.func_exec = func_exec

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
            self.kwargs.setdefault("task_name", self.name)

        return self


class DelayedSQL(DelayedBase):
    def __init__(self, *args, **kwargs):
        retrying = kwargs.pop("retrying", None)
        if retrying is None:
            func = sql.exec
        else:
            func = get_retriable_exec(sql.exec_async, retrying)
        super().__init__(func, *args, **kwargs)
        # Set name of task if it won't interfere with user args
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
        self.kwargs.setdefault("task_name", self.name)

        return self


class DelayedArrayUDF(DelayedBase):
    def __init__(self, uri, func_exec, *args, **kwargs):
        if func_exec is not None and not callable(func_exec):
            raise TypeError("func_exec argument to `Node` must be callable!")

        self.uri = uri
        self.func_exec = func_exec
        retrying = kwargs.pop("retrying", None)
        if retrying is None:
            func = array.apply
        else:
            func = get_retriable_exec(array.apply_async, retrying)
        super().__init__(func, uri, func_exec, *args, **kwargs)
        # Set name of task if it won't interfere with user args
        self.kwargs.setdefault("task_name", self.name)

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
        self.kwargs.setdefault("task_name", self.name)

        return self


def get_retriable_exec(exec_async, retrying):
    def retriable_exec(*args, **kwargs):
        task_apply_result = exec_async(*args, **kwargs)
        retry_task_kwargs = {
            k: kwargs[k] for k in ("raw_results", "http_compressor") if k in kwargs
        }

        def get_or_retry():
            task_id = task_apply_result.task_id
            if task_id is None:
                return task_apply_result.get()
            return retry_task(task_id, **retry_task_kwargs)

        # override __module__ and __qualname__ so that logging logs the task name
        # instead of the func name
        get_or_retry.__module__ = None
        get_or_retry.__qualname__ = kwargs["task_name"]
        return retrying(get_or_retry)

    return retriable_exec
