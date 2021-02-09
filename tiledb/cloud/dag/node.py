import numbers
import time
import uuid
from collections import abc
from concurrent.futures import CancelledError

from .status import Status


class Node:
    def __init__(self, func, *args, name=None, dag=None, local_mode=False, **kwargs):
        """
        Node is a class that represents a function to run in a DAG
        :param func: function to run
        :param args: tuple of arguments to run
        :param name: optional name of dag
        :param dag: dag this node is associated with
        :param kwargs: dictionary for keyword arguments
        """
        self.id = uuid.uuid4()
        self.future = None
        self.status = Status.NOT_STARTED
        self.dag = dag
        self.local_mode = local_mode

        if func is not None and not callable(func):
            raise TypeError("func argument to `Node` must be callable!")
        self.func = func

        self.args = args
        self.kwargs = kwargs
        self.parents = {}
        self.children = {}
        if name is None:
            name = self.id
        self.name = str(name)

        # Loop through non-default parameters and find any Node objects
        # Node objects will be used to automatically add dependencies
        if self.args is not None:
            self._build_dependencies_list(self.args)

        # Loop through defaulted named parameters and find any Node objects
        # Node objects will be used to automatically add dependencies
        if self.kwargs is not None:
            self._build_dependencies_list(self.kwargs)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def __ne__(self, other):
        return not (self == other)

    def depends_on(self, node):
        """
        Create dependency chain for node, useful when there is a dependency that does not rely directly on passing
        results from one to another
        :param node: node to mark as a dependency of this node
        :return:
        """
        self.parents[node.id] = node
        node.children[self.id] = self

        if self.dag is None and node.dag is not None:
            self.dag = node.dag

    def cancel(self):
        self.status = Status.CANCELLED
        if self.future is not None:
            self.future.cancel()

    def done(self):
        """Return True if the the node's function was cancelled or finished executing."""
        return self.status in (Status.COMPLETED, Status.FAILED, Status.CANCELLED)

    def _build_dependencies_list(self, arg):
        """
        Recursively check arg for any Node instances and create graph edges (dependency links)
        """
        if isinstance(arg, Node):
            self.depends_on(arg)
        elif isinstance(arg, abc.Iterable) and not isinstance(arg, str):
            if isinstance(arg, abc.Mapping):
                arg = arg.values()
            for v in arg:
                self._build_dependencies_list(v)

    def _replace_nodes_with_results(self, arg):
        """
        Recursively find arguments of Node instance and replace with the node results
        """
        if isinstance(arg, Node):
            return arg.result()

        if isinstance(arg, abc.Mapping):
            return {k: self._replace_nodes_with_results(v) for k, v in arg.items()}

        if isinstance(arg, abc.Collection) and not isinstance(arg, str):
            return arg.__class__(map(self._replace_nodes_with_results, arg))

        return arg

    def exec(self, namespace=None):
        """
        Execute function for node
        :return: None
        """
        self.status = Status.RUNNING

        # Override namespace if passed
        if namespace is not None and not self.local_mode:
            self.kwargs["namespace"] = namespace

        # First loop though any non-default parameter arguments to find any nodes
        # If there is a node as an argument, the user really just wants the results, so let's fetch them
        # and swap out the parameter
        if self.args is not None:
            self.args = self._replace_nodes_with_results(self.args)

        # First loop though any default named parameter arguments to find any nodes
        # If there is a node as an argument, the user really just wants the results, so let's fetch them
        # and swap out the parameter
        if self.kwargs is not None:
            self.kwargs = self._replace_nodes_with_results(self.kwargs)

        # Execute user function with the parameters that the user requested
        # The function is executed on the dag's worker pool
        self.future = self.dag.executor.submit(self.func, *self.args, **self.kwargs)
        self.future.add_done_callback(self.__update_status)

    def __update_status(self, future):
        try:
            future.result()
        except CancelledError:
            self.status = Status.CANCELLED
        except:
            self.status = Status.FAILED
        else:
            if self.status == Status.RUNNING:
                self.status = Status.COMPLETED
        self.dag.report_node_complete(self)

    def result(self):
        """
        Fetch results of function, block if not complete
        :return:
        """
        return self.future.result() if self.future is not None else None

    def wait(self, timeout=None):
        """
        Wait for node to be completed
        :param timeout: optional timeout in seconds to wait for DAG to be completed
        :return: None or raises TimeoutError if timeout occurs
        """

        if timeout is not None and not isinstance(timeout, numbers.Number):
            raise TypeError(
                "timeout must be numeric value representing seconds to wait"
            )

        start_time = time.time()
        end_time = None
        if timeout is not None:
            end_time = start_time + timeout
        while not self.done():
            time.sleep(0.5)
            if end_time is not None and time.time() >= end_time:
                raise TimeoutError(
                    "timeout of {} reached and dag is not complete".format(timeout)
                )
