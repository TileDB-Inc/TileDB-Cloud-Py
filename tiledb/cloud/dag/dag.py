import multiprocessing
import uuid
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from enum import Enum

from tiledb.cloud import TileDBCloudError


class Status(Enum):
    NOT_STARTED = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4


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
        if self.dag is not None and isinstance(self.dag, DAG):
            self.dag.report_node_complete(self)

    def __handle_complete_results(self):
        """
        Handle complete results
        :return:
        """
        self.status = Status.COMPLETED
        self.__report_finished_running()

    def __get_future_result(self):
        """
        If the results are a future we try to get them
        :return: True if the results can be gotten, false if not finished or not a future
        """
        if self.future is not None:
            self.__results = self.future.get()
            self.__handle_complete_results()
            return True

        return False

    def finished(self):
        """
        Is the node finished
        :return: True if the node's function is finished
        """
        if self.status == Status.COMPLETED or self.status == Status.FAILED:
            return True
        elif self.status == Status.RUNNING:
            if self.future is not None and self.future.is_ready():
                return self.__get_future_result()
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
                    arg[index] = a.results()
                elif isinstance(a, tuple) or isinstance(a, list) or isinstance(a, dict):
                    arg[index] = self.__replace_nodes_with_results(a)
        elif isinstance(arg, dict):
            for k, a in arg.items():
                if isinstance(a, Node):
                    arg[k] = a.results()
                elif isinstance(a, tuple) or isinstance(a, list) or isinstance(a, dict):
                    arg[k] = self.__replace_nodes_with_results(a)
        elif isinstance(arg, Node):
            arg = arg.results()

        if tuple_conversion:
            arg = tuple(arg)

        return arg

    def exec(self):
        """
        Execute function for node
        :return:
        """
        self.status = Status.RUNNING
        try:
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
            if len(self.kwargs) > 0 and len(self.args) > 0:
                res = self.func(*self.args, **self.kwargs)
            elif len(self.args) > 0:
                res = self.func(*self.args)
            elif len(self.kwargs) > 0:
                res = self.func(**self.kwargs)
            else:
                res = self.func()

            # If the results of the function are a future, we need to account for that
            if isinstance(res, multiprocessing.pool.ApplyResult):
                # TODO: not sure if this works or not
                res._callback = self.__handle_complete_results
                self.future = res
            # Else the results were a normal (blocking) function and we have the true results
            else:
                self.__results = res
                self.__handle_complete_results()

        except Exception as exc:
            self.status = Status.FAILED
            self.error = exc
            self.__report_finished_running()

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

    def results(self):
        """
        Fetch results of functions
        :return:
        """
        if not self.finished() and self.future is not None:
            self.__get_future_result()

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
        if use_processes:
            self.executor = ProcessPoolExecutor(max_workers=max_workers)
        else:
            self.executor = ThreadPoolExecutor(max_workers=max_workers)

        self.status = Status.NOT_STARTED

    def __check_complete(self):
        """
        Checks if DAG is complete
        :return: True if complete, False otherwise
        """
        if len(self.running_nodes) > 0:
            return False

        # If there is no running nodes we can assume it is complete and check if we should mark as failed or successful
        if len(self.failed_nodes) > 0:
            self.status = Status.FAILED
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
        else:
            self.failed_nodes[node.id] = node

        self.__check_complete()

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
            # Submit it async so we can move on
            self.executor.submit(node.exec())
