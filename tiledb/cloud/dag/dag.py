import functools
import numbers
import time
import uuid
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures._base import Future, CancelledError
from enum import Enum

from ..array import apply as array_apply
from ..sql import exec as sql_exec
from ..udf import exec as udf_exec

from tiledb.cloud import TileDBCloudError


class Status(Enum):
    NOT_STARTED = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4
    CANCELLED = 5


def handle_complete_node(node, future):
    node.handle_completed_future()


class Node:
    def __init__(self, func, args, name=None, dag=None, kwargs=None):
        """
        Node is a class that represents a function to run in a DAG
        :param func: function to run
        :param args: tuple of arguments to run
        :param name: optional name of dag
        :param dag: dag this node is associated with
        :param kwards: dictionary for keyword arguments
        """
        self.id = uuid.uuid4()
        self.error = None
        self.future = None
        self.status = Status.NOT_STARTED
        self.dag = dag

        if func is not None and not callable(func):
            raise TypeError("func argument to `Node` must be callable!")
        self.func = func

        self.args = args
        self.kwargs = kwargs
        self.__results = None
        self.parents = {}
        self.children = {}
        if name is None:
            name = self.id
        self.name = name

        # Loop through non-default parameters and find any Node objects
        # Node objects will be used to automatically add dependencies
        if self.args is not None:
            self.__build_dependencies_list(self.args)

        # Loop through defaulted named parameters and find any Node objects
        # Node objects will be used to automatically add dependencies
        if self.kwargs is not None:
            self.__build_dependencies_list(self.kwargs)

    def __build_dependencies_list(self, arg):
        """
        Recursively check arg for any Node instances and create graph edges (dependency links)
        :param arg:
        :return:
        """
        if isinstance(arg, tuple) or isinstance(arg, list):
            for a in arg:
                if isinstance(a, Node):
                    self.depends_on(a)
                elif isinstance(a, tuple) or isinstance(a, list) or isinstance(a, dict):
                    self.__build_dependencies_list(a)
        elif isinstance(arg, dict):
            for a in arg.values():
                if isinstance(a, Node):
                    self.depends_on(a)
                elif isinstance(a, tuple) or isinstance(a, list) or isinstance(a, dict):
                    self.__build_dependencies_list(a)
        elif isinstance(arg, Node):
            self.depends_on(arg)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

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

    def __report_finished_running(self):
        """
        Report the node as finished to the dag
        :return:
        """

        if self.future is not None:
            try:
                self.error = self.future.exception()
            except CancelledError as cancelledExc:
                pass
            except Exception as exc:
                self.error = exc

        if self.error is not None:
            self.status = Status.FAILED

        if self.dag is not None and isinstance(self.dag, DAG):
            self.dag.report_node_complete(self)

    def __handle_complete_results(self):
        """
        Handle complete results
        :return:
        """
        # Set status if it has not already been set for cancelled or failed
        if self.status == Status.RUNNING:
            self.status = Status.COMPLETED

        self.__report_finished_running()

    def handle_completed_future(self):
        """

        :return:
        """

        if self.future is not None:
            try:
                self.__results = self.future.result()
            except CancelledError as exc:
                self.status = Status.CANCELLED

        self.__handle_complete_results()

    def cancel(self):

        self.status = Status.CANCELLED
        if self.future is not None:
            self.future.cancel()

    def finished(self):
        """
        Is the node finished
        :return: True if the node's function is finished
        """
        if self.status == Status.COMPLETED or self.status == Status.FAILED:
            return True
        elif self.status == Status.RUNNING:
            if self.future is not None and self.future.done():
                return True
        return False

    def __replace_nodes_with_results(self, arg):
        """
        Recursively find arguments of Node instance and replace with the node results
        :param arg:
        :return: converted argument
        """
        tuple_conversion = False
        if isinstance(arg, tuple):
            arg = list(arg)
            tuple_conversion = True

        if isinstance(arg, tuple) or isinstance(arg, list):
            for index in range(len(arg)):
                a = arg[index]
                if isinstance(a, Node):
                    arg[index] = a.result()
                elif isinstance(a, tuple) or isinstance(a, list) or isinstance(a, dict):
                    arg[index] = self.__replace_nodes_with_results(a)
        elif isinstance(arg, dict):
            for k, a in arg.items():
                if isinstance(a, Node):
                    arg[k] = a.result()
                elif isinstance(a, tuple) or isinstance(a, list) or isinstance(a, dict):
                    arg[k] = self.__replace_nodes_with_results(a)
        elif isinstance(arg, Node):
            arg = arg.result()

        if tuple_conversion:
            arg = tuple(arg)

        return arg

    def exec(self):
        """
        Execute function for node
        :return:
        """
        self.status = Status.RUNNING
        # First loop though any non-default parameter arguments to find any nodes
        # If there is a node as an argument, the user really just wants the results, so let's fetch them
        # and swap out the parameter
        if self.args is not None:
            self.args = self.__replace_nodes_with_results(self.args)

        # First loop though any default named parameter arguments to find any nodes
        # If there is a node as an argument, the user really just wants the results, so let's fetch them
        # and swap out the parameter
        if self.kwargs is not None:
            self.kwargs = self.__replace_nodes_with_results(self.kwargs)

        # Execute user function with the parameters that the user requested
        # The function is executed on the dag's worker pool
        if self.dag is not None:
            if len(self.kwargs) > 0 and len(self.args) > 0:
                res = self.dag.executor.submit(self.func, *self.args, **self.kwargs)
            elif len(self.args) > 0:
                res = self.dag.executor.submit(self.func, *self.args)
            elif len(self.kwargs) > 0:
                res = self.dag.executor.submit(self.func, **self.kwargs)
            else:
                res = self.dag.executor.submit(self.func)
        # Handle case when there is no dag, useful for testing
        else:
            try:
                if len(self.kwargs) > 0 and len(self.args) > 0:
                    res = self.func(*self.args, **self.kwargs)
                elif len(self.args) > 0:
                    res = self.func(*self.args)
                elif len(self.kwargs) > 0:
                    res = self.func(**self.kwargs)
                else:
                    res = self.func()
            except Exception as exc:
                self.status = Status.FAILED
                self.error = exc
                self.__report_finished_running()
                raise exc

        # If the results were a normal (blocking) function and we have the true results
        if isinstance(res, Future):
            self.future = res
            # If the node is already finished by the time we get here, call complete function directly
            # In python 3.7 if we add a call back to a future with an exception it throws an exception
            if self.future.done():
                self.handle_completed_future()
            else:
                self.future.add_done_callback(
                    functools.partial(handle_complete_node, self)
                )
        else:
            self.__results = res
            self.__handle_complete_results()

    def ready_to_exec(self):
        """
        Is the node ready to execute? Are all dependencies completed?
        :return: True if node is able to be run
        """
        if self.status != Status.NOT_STARTED:
            return False

        for node in self.parents.values():
            if not node.finished() or node.status != Status.COMPLETED:
                return False
        return True

    def result(self):
        """
        Fetch results of function, block if not complete
        :return:
        """
        if self.future is not None:
            # If future, catch exception to store error on node, then raise
            try:
                self.__results = self.future.result()
            except Exception as exc:
                self.error = exc
                raise exc

        return self.__results

    def result_or_future(self):
        """
        Fetch results of functions or return future if incomplete
        :return:
        """
        if not self.finished() and self.future is not None:
            return self.future

        return self.__results


class DAG:
    def __init__(self, max_workers=None, use_processes=False):
        """
        DAG is a class for creating and managing direct acyclic graphs
        :param max_workers: how many workers should be used to execute the dag
        :param use_processes: if true will use processes instead of threads, defaults to threads
        """
        self.nodes = {}
        self.completed_nodes = {}
        self.failed_nodes = {}
        self.running_nodes = {}
        self.not_started_nodes = {}
        self.cancelled_nodes = {}
        if use_processes:
            self.executor = ProcessPoolExecutor(max_workers=max_workers)
        else:
            self.executor = ThreadPoolExecutor(max_workers=max_workers)

        self.status = Status.NOT_STARTED

    def done(self):
        """
        Checks if DAG is complete
        :return: True if complete, False otherwise
        """
        if self.status == Status.NOT_STARTED:
            raise TileDBCloudError(
                "Can't call done for DAG before starting DAG with `exec()`"
            )

        if len(self.running_nodes) > 0:
            return False

        # If there is no running nodes we can assume it is complete and check if we should mark as failed or successful
        if len(self.failed_nodes) > 0:
            self.status = Status.FAILED
        elif len(self.cancelled_nodes) > 0:
            self.status = Status.CANCELLED
        elif len(self.not_started_nodes) > 0:
            return False
        else:
            self.status = Status.COMPLETED

        return True

    def __add_node(self, node):
        """
        Add node to DAG
        :param node: to add to dag
        :return: node
        """
        self.nodes[node.id] = node
        self.not_started_nodes[node.id] = node
        return node

    def add_node(self, func_exec, *args, name=None, **kwargs):
        """
        Create and add a node
        :param func_exec: function to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        node = Node(func_exec, args, dag=self, name=name, kwargs=kwargs)
        return self.__add_node(node)

    def submit_array_udf(self, *args, **kwargs):
        """
        Submit a function that will be executed in the cloud serverlessly
        :param func_exec: function to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self.add_node(array_apply, *args, **kwargs)

    def submit_udf(self, *args, **kwargs):
        """
        Submit a function that will be executed in the cloud serverlessly
        :param func_exec: function to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self.add_node(udf_exec, *args, **kwargs)

    def submit_sql(self, *args, **kwargs):
        """
        Submit a sql query to run serverlessly in the cloud
        :param sql: query to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self.add_node(sql_exec, *args, **kwargs)

    def submit_local(self, *args, **kwargs):
        """
        Submit a function that will run locally
        :param func_exec: function to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self.add_node(*args, **kwargs)

    def report_node_complete(self, node):
        """
        Report a node as complete
        :param node: to mark as complete
        :return
        """
        del self.running_nodes[node.id]

        if node.status == Status.COMPLETED:
            self.completed_nodes[node.id] = node

            for child in node.children.values():
                if child.ready_to_exec():
                    self.__exec_node(child)
        elif node.status == Status.CANCELLED:
            self.cancelled_nodes[node.id] = node
        else:
            self.failed_nodes[node.id] = node

        # Check if DAG is done to change status
        self.done()

    def __find_root_nodes(self):
        """
        Find all root nodes
        :return: list of root nodes
        """
        roots = []
        for node in self.nodes.values():
            if node.parents is None or len(node.parents) == 0:
                roots.append(node)

        return roots

    def exec(self):
        """
        Start the DAG by executing root nodes
        :return:
        """
        roots = self.__find_root_nodes()
        if len(roots) == 0:
            raise TileDBCloudError("DAG is circular, there are no root nodes")

        self.status = Status.RUNNING
        for node in roots:
            self.__exec_node(node)

    def __exec_node(self, node):
        """
        Execute a node
        :param node: node to execute
        :return:
        """
        if node.ready_to_exec():
            del self.not_started_nodes[node.id]
            self.running_nodes[node.id] = node
            # Execute the node, the node will launch it's task with a worker pool from this dag
            node.exec()

    def wait(self, timeout):
        """
        Wait for DAG to be completed
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

    def cancel(self):

        self.status = Status.CANCELLED
        for node in self.running_nodes.values():
            node.cancel()

    def find_end_nodes(self):
        """
        Find all end nodes
        :return: list of end nodes
        """
        end = []
        for node in self.nodes.values():
            if node.children is None or len(node.children) == 0:
                end.append(node)

        return end

    def stats(self):

        return {
            "percent_complete": len(self.completed_nodes) / len(self.nodes) * 100,
            "running": len(self.running_nodes),
            "failed": len(self.failed_nodes),
            "completed": len(self.completed_nodes),
            "cancelled": len(self.cancelled_nodes),
            "not_started": len(self.not_started_nodes),
            "total_count": len(self.nodes),
        }
