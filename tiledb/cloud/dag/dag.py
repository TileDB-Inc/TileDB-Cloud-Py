import abc
import collections.abc as cabc
import dataclasses
import json
import numbers
import time
import uuid
from concurrent import futures
from typing import Any, Dict, Optional

import networkx as nx

from tiledb.cloud import array
from tiledb.cloud import sql
from tiledb.cloud import tiledb_cloud_error as tce
from tiledb.cloud import udf
from tiledb.cloud.dag import status as st
from tiledb.cloud.dag import stored_params
from tiledb.cloud.dag import visualization as viz

Status = st.Status  # Re-export for compabitility.


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
        self.status = st.Status.NOT_STARTED
        self.dag = dag
        self.local_mode = local_mode

        if func is not None and not callable(func):
            raise TypeError("func argument to `Node` must be callable!")
        self.func = func

        self.args = args
        self.kwargs = kwargs
        self._results = None
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

    def cancel(self):
        self.status = st.Status.CANCELLED
        if self.future is not None:
            self.future.cancel()

    def finished(self):
        """
        Is the node finished
        :return: True if the node's function is finished
        """
        return self.status in (
            st.Status.COMPLETED,
            st.Status.FAILED,
            st.Status.CANCELLED,
        )

    done = finished

    def exec(self, namespace=None):
        """
        Execute function for node
        :return: None
        """
        self.status = st.Status.RUNNING

        # Override namespace if passed
        if namespace is not None and not self.local_mode:
            self.kwargs["namespace"] = namespace

        # First loop though any non-default parameter arguments to find any nodes
        # If there is a node as an argument, the user really just wants the results, so let's fetch them
        # and swap out the parameter
        if self.args is not None:
            self.args = _replace_nodes_with_results(self.args)

        # First loop though any default named parameter arguments to find any nodes
        # If there is a node as an argument, the user really just wants the results, so let's fetch them
        # and swap out the parameter
        if self.kwargs is not None:
            self.kwargs = _replace_nodes_with_results(self.kwargs)

        # Execute user function with the parameters that the user requested
        # The function is executed on the dag's worker pool
        self.future = self.dag.executor.submit(self.func, *self.args, **self.kwargs)
        self.future.add_done_callback(self._handle_completed_future)

    compute = exec

    def _handle_completed_future(self, future):
        try:
            self._results = future.result()
            if self.status == st.Status.RUNNING:
                self.status = st.Status.COMPLETED
        except futures.CancelledError:
            self.status = st.Status.CANCELLED
        except Exception as exc:
            self.error = exc
            self.status = st.Status.FAILED
        self.dag.report_node_complete(self)

    def ready_to_compute(self):
        """
        Is the node ready to execute? Are all dependencies completed?
        :return: True if node is able to be run
        """
        if self.status != st.Status.NOT_STARTED:
            return False

        for node in self.parents.values():
            if not node.finished() or node.status != st.Status.COMPLETED:
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
                self._results = self.future.result()
            except Exception as exc:
                self.error = exc
                raise exc

        return self._results

    def result_or_future(self):
        """
        Fetch results of functions or return future if incomplete
        :return:
        """
        if not self.finished() and self.future is not None:
            return self.future

        return self._results

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
            self.executor = futures.ProcessPoolExecutor(max_workers=max_workers)
        else:
            self.executor = futures.ThreadPoolExecutor(max_workers=max_workers)

        self.status = st.Status.NOT_STARTED

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
        if self.status == st.Status.NOT_STARTED:
            raise tce.TileDBCloudError(
                "Can't call done for DAG before starting DAG with `exec()`"
            )

        if len(self.running_nodes) > 0:
            return False

        # If there is no running nodes we can assume it is complete and check if we should mark as failed or successful
        if len(self.failed_nodes) > 0:
            self.status = st.Status.FAILED
        elif len(self.cancelled_nodes) > 0:
            self.status = st.Status.CANCELLED
        elif len(self.not_started_nodes) > 0:
            return False
        else:
            self.status = st.Status.COMPLETED

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
        return self.add_node(array.apply, *args, **kwargs)

    def submit_udf(self, *args, **kwargs):
        """
        Submit a function that will be executed in the cloud serverlessly
        :param func_exec: function to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self.add_node(udf.exec, *args, **kwargs)

    def submit(self, *args, **kwargs):
        """
        Submit a function that will be executed in the cloud serverlessly
        This function is analogous to submit_udf
        :param func_exec: function to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self.add_node(udf.exec, *args, **kwargs)

    def submit_sql(self, *args, **kwargs):
        """
        Submit a sql query to run serverlessly in the cloud
        :param sql: query to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self.add_node(sql.exec, *args, **kwargs)

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

        if node.status == st.Status.COMPLETED:
            self.completed_nodes[node.id] = node
            for child in node.children.values():
                self._exec_node(child)
        elif node.status == st.Status.CANCELLED:
            self.cancelled_nodes[node.id] = node
        else:
            self.failed_nodes[node.id] = node
            self.cancel()

        self.execute_update_callbacks()

        # Check if DAG is done to change status
        if self.done():
            self.execute_done_callbacks()

    def _find_root_nodes(self):
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
        roots = self._find_root_nodes()
        if len(roots) == 0:
            raise tce.TileDBCloudError("DAG is circular, there are no root nodes")

        self.status = st.Status.RUNNING
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

        # in case of failure reraise the first failed node exception
        if self.status == st.Status.FAILED:
            raise next(iter(self.failed_nodes.values())).error

    def cancel(self):
        self.status = st.Status.CANCELLED
        for node in self.running_nodes.values():
            node.cancel()
        for node in self.not_started_nodes.values():
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
        graph = nx.DiGraph()

        for n in self.nodes.values():
            graph.add_node(n.name)
            for child in n.children.values():
                graph.add_node(child.name)
                graph.add_edge(n.name, child.name)

        return graph

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
    def _update_dag_tiledb_graph(graph):
        graph.visualization["node_details"] = graph.get_tiledb_plot_node_details()
        viz.update_tiledb_graph(
            graph.visualization["nodes"],
            graph.visualization["edges"],
            graph.visualization["node_details"],
            graph.visualization["positions"],
            graph.visualization["fig"],
        )

    @staticmethod
    def _update_dag_plotly_graph(graph):
        viz.update_plotly_graph(
            graph.visualization["nodes"], graph.visualization["fig"]
        )

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
            return self._visualize_tiledb(auto_update=auto_update)
        except ImportError:
            return self._visualize_plotly(notebook=notebook, auto_update=auto_update)

    def _visualize_tiledb(self, auto_update=True):
        """
        Create graph visualization with tiledb.plot.widget
        :param auto_update: Should the diagram be auto updated with each status change
        :return: figure
        """

        import tiledb.plot.widget

        graph = self.networkx_graph()
        nodes = list(graph.nodes())
        edges = list(graph.edges())
        node_details = self.get_tiledb_plot_node_details()
        positions = viz.build_visualization_positions(graph)

        self.visualization = {
            "nodes": nodes,
            "edges": edges,
            "node_details": node_details,
            "positions": positions,
        }
        fig = tiledb.plot.widget.Visualize(data=json.dumps(self.visualization))
        self.visualization["fig"] = fig

        if auto_update:
            self.add_update_callback(self._update_dag_tiledb_graph)

        return fig

    def _visualize_plotly(self, notebook=True, auto_update=True):
        """

        :param notebook: Is the visualization inside a jupyter notebook? If so we'll use a widget
        :param auto_update: Should the diagram be auto updated with each status change
        :return: figure
        """
        import plotly.graph_objects as go

        graph = self.networkx_graph()
        pos = viz.build_visualization_positions(graph)

        # Convert to plotly scatter plot
        edge_x = []
        edge_y = []
        for edge in graph.edges():
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
        for node in graph.nodes():
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

        (node_trace.marker.color, node_trace.text) = viz.build_graph_node_details(nodes)

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

        self.visualization = dict(fig=fig, network=graph, nodes=nodes)

        if auto_update:
            self.add_update_callback(self._update_dag_plotly_graph)

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


def replace_stored_params(tree, loader: stored_params.ParamLoader) -> Any:
    """Descends into data structures and replaces Stored Params with results."""

    return _StoredParamReplacer(loader).visit(tree)


def _replace_nodes_with_results(tree):
    """Descends into data structures and replaces Node IDs with their values."""

    return _NodeResultReplacer().visit(tree)


@dataclasses.dataclass(frozen=True)
class _Replacement:
    """A sentinel return value to indicate that the value should be replaced.

    This wrapper ensures that we are able to replace nodes with `None`
    or other falsey values if needed.
    """

    value: Any


class _ReplacingVisitor(metaclass=abc.ABCMeta):
    """An abstract class to descend through data structure, replacing values.

    An instance of this class should be used in a one-shot manner to descend
    into a data structure and return a new, equivalent structure, but with
    nodes (specified by :meth:`maybe_replace`) replaced in the output.

    See implementations immediately below, or Doubler in the tests.
    """

    def __init__(self):
        # A dictionary mapping the ID of every object we have seen in our
        # traversal to the object it is replaced with, to avoid duplicating
        # work or getting caught in self-referential structures.
        self.seen: Dict[int, Any] = {}

    def visit(self, arg):
        """Visits a single node of the data structure and returns its new value.

        This function recursively descends through a data structure to transform
        it into a new value. It is both the entry point (i.e., the caller
        passes in the value it wants to transform) and the internal recursive
        step (i.e., each sub-node of that value is passed here to be transformed
        as well).

        It returns the value that the input is transformed into, which may be
        the same value as was passed in.
        """
        if isinstance(arg, (str, bytes)):
            # Special-case these since they're weird sequences.
            return arg

        original_id = id(arg)
        try:
            # If we have already seen this exact instance,
            # return the one we calculated before.
            return self.seen[original_id]
        except KeyError:
            pass  # We haven't seen this object yet; continue.

        # First, handle if this is something to replace directly.
        replacement = self.maybe_replace(arg)
        if replacement:
            self.seen[original_id] = replacement.value
            return replacement.value

        # Descend into sequences and mappings.
        # Potential improvement: Do a first pass to see if anything *needs*
        # replacing, and only create new instances if one is found.
        if isinstance(arg, cabc.MutableSequence):
            # Mutable types may contain self references, so we create one and
            # store it as the canonical substitution for this instance in case
            # we see this original again.
            replaced = type(arg)()
            self.seen[original_id] = replaced
            replaced.extend(map(self.visit, arg))
            return replaced
        if isinstance(arg, cabc.Sequence):
            replaced = type(arg)(map(self.visit, arg))
            self.seen[original_id] = replaced
            return replaced
        if isinstance(arg, cabc.MutableMapping):
            # As before, create the mapping in advance to allow self references.
            replaced = type(arg)()
            self.seen[original_id] = replaced
            replaced.update((k, self.visit(v)) for k, v in arg.items())
            return replaced
        if isinstance(arg, cabc.Mapping):
            replaced = type(arg)((k, self.visit(v)) for k, v in arg.items())
            self.seen[original_id] = replaced
            return replaced

        # Otherwise, we just return the original thing.
        self.seen[original_id] = arg
        return arg

    @abc.abstractmethod
    def maybe_replace(self, arg) -> Optional[_Replacement]:
        """Abstract function returning a value if it should be replaced.

        This will be called as the visitor visits every node of the data
        structure. If the node should be replaced with some value, it should
        return that value wrapped in a :class:`_Replacement`. If it returns
        None, the replacer will visit the node as normal.
        """
        raise NotImplementedError()


class _NodeResultReplacer(_ReplacingVisitor):
    """Replaces :class:`Node`s with their results."""

    def maybe_replace(self, arg) -> Optional[_Replacement]:
        if isinstance(arg, Node):
            return _Replacement(arg.result())
        return None


class _StoredParamReplacer(_ReplacingVisitor):
    """Replaces stored parameters with their values."""

    def __init__(self, loader: stored_params.ParamLoader):
        super().__init__()
        self._loader = loader

    def maybe_replace(self, arg) -> Optional[_Replacement]:
        if isinstance(arg, stored_params.StoredParam):
            return _Replacement(self._loader.load(arg))
        return None
