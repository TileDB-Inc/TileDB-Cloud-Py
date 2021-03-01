import functools
import numbers
import time
import uuid
import networkx as nx

from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures._base import Future, CancelledError
from enum import Enum

from .visualization import (
    build_graph_node_details,
    update_plotly_graph,
    update_tiledb_graph,
    build_visualization_positions,
)
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

    def __str__(self):
        if self == self.NOT_STARTED:
            return "Not Started"
        elif self == self.RUNNING:
            return "Running"
        elif self == self.COMPLETED:
            return "Completed"
        elif self == self.FAILED:
            return "Failed"
        elif self == self.CANCELLED:
            return "Cancelled"

        return "Unknown Status"


def handle_complete_node(node, future):
    node.handle_completed_future()


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
        self.error = None
        self.future = None
        self.status = Status.NOT_STARTED
        self.dag = dag
        self.local_mode = local_mode

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
        self.name = str(name)

        # Loop through non-default parameters and find any Node objects
        # Node objects will be used to automatically add dependencies
        if self.args is not None:
            self._build_dependencies_list(self.args)

        # Loop through defaulted named parameters and find any Node objects
        # Node objects will be used to automatically add dependencies
        if self.kwargs is not None:
            self._build_dependencies_list(self.kwargs)

    def _build_dependencies_list(self, arg):
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
                    self._build_dependencies_list(a)
        elif isinstance(arg, dict):
            for a in arg.values():
                if isinstance(a, Node):
                    self.depends_on(a)
                elif isinstance(a, tuple) or isinstance(a, list) or isinstance(a, dict):
                    self._build_dependencies_list(a)
        elif isinstance(arg, Node):
            self.depends_on(arg)

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

    done = finished

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

    compute = exec

    def ready_to_compute(self):
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


class DAG:
    def __init__(
        self,
        max_workers=None,
        use_processes=False,
        done_callback=None,
        update_callback=None,
        namespace=None,
    ):
        """
        DAG is a class for creating and managing direct acyclic graphs
        :param max_workers: how many workers should be used to execute the dag
        :param use_processes: if true will use processes instead of threads, defaults to threads
        :param done_callback: optional call back function to register for when dag is completed. Function will be passed reference to this dag
        :param update_callback: optional call back function to register for when dag status is updated. Function will be passed reference to this dag
        :param namespace: optional namespace to use for all tasks in DAG
        """
        self.id = uuid.uuid4()
        self.nodes = {}
        self.nodes_by_name = {}
        self.completed_nodes = {}
        self.failed_nodes = {}
        self.running_nodes = {}
        self.not_started_nodes = {}
        self.cancelled_nodes = {}
        self.namespace = namespace

        self.visualization = None

        if use_processes:
            self.executor = ProcessPoolExecutor(max_workers=max_workers)
        else:
            self.executor = ThreadPoolExecutor(max_workers=max_workers)

        self.status = Status.NOT_STARTED

        self.done_callbacks = []
        self.called_done_callbacks = False
        if done_callback is not None and callable(done_callback):
            self.done_callbacks.append(done_callback)

        self.update_callbacks = []
        if update_callback is not None and callable(update_callback):
            self.update_callbacks.append(update_callback)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def __ne__(self, other):
        return not (self == other)

    def add_update_callback(self, func):
        """
        Add a callback for when DAG status is updated
        :param func: Function to call when DAG status is updated. The function will be passed reference to this dag
        :return:
        """
        if not callable(func):
            raise TypeError("func to add_update_callback must be callable")

        self.update_callbacks.append(func)

    def add_done_callback(self, func):
        """
        Add a callback for when DAG is completed
        :param func: Function to call when DAG status is updated. The function will be passed reference to this dag
        :return:
        """
        if not callable(func):
            raise TypeError("func to add_done_callback must be callable")

        self.done_callbacks.append(func)

    def execute_update_callbacks(self):
        """
        Run user specified callbacks for status updates
        :return:
        """
        for func in self.update_callbacks:
            func(self)

    def execute_done_callbacks(self):
        """
        Run user specified callbacks for DAG completion
        :return:
        """
        if not self.called_done_callbacks:
            for func in self.done_callbacks:
                func(self)

        self.called_done_callbacks = True

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

    def add_node_obj(self, node):
        """
        Add node to DAG
        :param node: to add to dag
        :return: node
        """
        self.nodes[node.id] = node
        self.nodes_by_name[str(node.name)] = node
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
        node = Node(func_exec, *args, dag=self, name=name, **kwargs)
        return self.add_node_obj(node)

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

    def submit(self, *args, **kwargs):
        """
        Submit a function that will be executed in the cloud serverlessly
        This function is analogous to submit_udf
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
                if child.ready_to_compute():
                    self._exec_node(child)
        elif node.status == Status.CANCELLED:
            self.cancelled_nodes[node.id] = node
        else:
            self.failed_nodes[node.id] = node

        self.execute_update_callbacks()

        # Check if DAG is done to change status
        if self.done():
            self.execute_done_callbacks()

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

    def compute(self):
        """
        Start the DAG by executing root nodes
        :return:
        """
        self.called_done_callbacks = False
        roots = self.__find_root_nodes()
        if len(roots) == 0:
            raise TileDBCloudError("DAG is circular, there are no root nodes")

        self.status = Status.RUNNING
        for node in roots:
            self._exec_node(node)
            # Make sure to execute any callbacks to signal this node has started
            self.execute_update_callbacks()

        # Make sure to execute any callbacks to signal things have started
        self.execute_update_callbacks()

    def _exec_node(self, node):
        """
        Execute a node
        :param node: node to execute
        :return:
        """
        if node.ready_to_compute():
            del self.not_started_nodes[node.id]
            self.running_nodes[node.id] = node
            # Execute the node, the node will launch it's task with a worker pool from this dag
            node.exec(namespace=self.namespace)

    def wait(self, timeout=None):
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

    def networkx_graph(self):
        # Build networkx graph
        G = nx.DiGraph()

        for n in self.nodes.values():
            G.add_node(n.name)
            for child in n.children.values():
                G.add_node(child.name)
                G.add_edge(n.name, child.name)

        return G

    def get_tiledb_plot_node_details(self):
        """
        Build list of details needed for tiledb node graph
        :return:
        """
        node_details = {}

        for node_name, node in self.nodes_by_name.items():
            node_details[node_name] = dict(name=node_name, status=str(node.status))

        return node_details

    @staticmethod
    def __update_dag_tiledb_graph(graph):
        graph.visualization["node_details"] = graph.get_tiledb_plot_node_details()
        update_tiledb_graph(
            graph.visualization["nodes"],
            graph.visualization["edges"],
            graph.visualization["node_details"],
            graph.visualization["positions"],
            graph.visualization["fig"],
        )

    @staticmethod
    def __update_dag_plotly_graph(graph):
        update_plotly_graph(graph.visualization["nodes"], graph.visualization["fig"])

    def visualize(self, notebook=True, auto_update=True, force_plotly=False):
        """
        Build and render a tree diagram of the DAG.
        :param notebook: Is the visualization inside a jupyter notebook? If so we'll use a widget
        :param auto_update: Should the diagram be auto updated with each status change
        :param force_plotly: Force the use of plotly graphs instead of TileDB Plot Widget
        :return: returns figure
        """
        if not notebook or force_plotly:
            return self._visualize_plotly(notebook=notebook, auto_update=auto_update)

        try:
            import tiledb.plot.widget

            return self.__visualize_tiledb(auto_update=auto_update)

        except ImportError:
            import plotly.graph_objects as go

            return self._visualize_plotly(notebook=notebook, auto_update=auto_update)

    def __visualize_tiledb(self, auto_update=True):
        """
        Create graph visualization with tiledb.plot.widget
        :param auto_update: Should the diagram be auto updated with each status change
        :return: figure
        """
        import tiledb.plot.widget
        import json

        G = self.networkx_graph()
        nodes = list(G.nodes())
        edges = list(G.edges())
        node_details = self.get_tiledb_plot_node_details()
        positions = build_visualization_positions(G)

        self.visualization = {
            "nodes": nodes,
            "edges": edges,
            "node_details": node_details,
            "positions": positions,
        }
        fig = tiledb.plot.widget.Visualize(data=json.dumps(self.visualization))
        self.visualization["fig"] = fig

        if auto_update:
            self.add_update_callback(self.__update_dag_tiledb_graph)

        return fig

    def _visualize_plotly(self, notebook=True, auto_update=True):
        """

        :param notebook: Is the visualization inside a jupyter notebook? If so we'll use a widget
        :param auto_update: Should the diagram be auto updated with each status change
        :return: figure
        """
        import plotly.graph_objects as go

        G = self.networkx_graph()
        pos = build_visualization_positions(G)

        # Convert to plotly scatter plot
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=0.5, color="#888"),
            hoverinfo="none",
            mode="lines",
        )

        # Build node x,y and also build a mapping of the graph market numbers to actual node objects so we can fetch status
        # The graph ends up with each market on a list, so we need to map from this list's order to actual nodes so we can look things up
        node_x = []
        node_y = []
        nodes = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            nodes.append(self.nodes_by_name[node])

        # Build node scatter plot
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            hoverinfo="text",
            marker=dict(size=15, line_width=2),
        )

        (node_trace.marker.color, node_trace.text) = build_graph_node_details(nodes)

        fig_obj = go.Figure
        if notebook:
            fig_obj = go.FigureWidget
        # Create plot
        fig = fig_obj(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                # title="Status",
                # titlefont_size=16,
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[
                    dict(showarrow=True, xref="paper", yref="paper", x=0.005, y=-0.002)
                ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            ),
        )

        self.visualization = dict(fig=fig, network=G, nodes=nodes)

        if auto_update:
            self.add_update_callback(self.__update_dag_plotly_graph)

        return fig

    def end_nodes(self):
        """
        Find all ends nodes

        dag = DAG()
        dag.add_node(Node())

        end_nodes = dag.end_nodes()

        :return: list of root nodes
        """
        ends = []
        for node in self.nodes.values():
            if node.children is None or len(node.children) == 0:
                ends.append(node)

        return ends

    def end_results(self):
        """
        Get all end results, will block if all results are not ready

        dag = DAG()
        dag.add_node(Node())

        end_results = dag.end_results()

        :return: map of results by node ID
        """

        results = {}
        for node in self.end_nodes():
            results[node.id] = node.result()

        return results

    def end_results_by_name(self):
        """
        Get all end results, will block if all results are not ready

        dag = DAG()
        dag.add_node(Node())

        end_results = dag.end_results_by_name()

        :return: map of results by node name
        """

        results = {}
        for node in self.end_nodes():
            results[node.name] = node.result()

        return results
