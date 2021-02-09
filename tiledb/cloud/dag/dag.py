import numbers
import time
import uuid
import networkx as nx

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from .node import Node
from .status import Status
from .visualization import visualize_plotly, visualize_tiledb

from tiledb.cloud import array, sql, udf, TileDBCloudError


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

        if use_processes:
            self.executor = ProcessPoolExecutor(max_workers=max_workers)
        else:
            self.executor = ThreadPoolExecutor(max_workers=max_workers)

        self.done_callbacks = []
        self.called_done_callbacks = False
        if done_callback is not None:
            self.add_done_callback(done_callback)

        self.update_callbacks = []
        if update_callback is not None:
            self.add_update_callback(update_callback)

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

    @property
    def status(self):
        return (
            # fmt: off
            Status.RUNNING if self.running_nodes else
            Status.FAILED if self.failed_nodes else
            Status.CANCELLED if self.cancelled_nodes else
            Status.COMPLETED if self.completed_nodes and not self.not_started_nodes else
            Status.NOT_STARTED
            # fmt: on
        )

    def done(self):
        """
        Checks if DAG is complete
        :return: True if complete, False otherwise
        """
        return self.status in (Status.COMPLETED, Status.FAILED, Status.CANCELLED)

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

    def submit_sql(self, *args, **kwargs):
        """
        Submit a sql query to run serverlessly in the cloud
        :param sql: query to execute
        :param args: arguments for function execution
        :param name: name
        :return: Node that is created
        """
        return self.add_node(sql.exec, *args, **kwargs)

    submit_local = add_node

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
                self._exec_node(child)
        elif node.status == Status.CANCELLED:
            self.cancelled_nodes[node.id] = node
        else:
            self.failed_nodes[node.id] = node
            self.cancel()

        for func in self.update_callbacks:
            func(self)

        # Check if DAG is done to change status
        if self.done() and not self.called_done_callbacks:
            for func in self.done_callbacks:
                func(self)
            self.called_done_callbacks = True

    def compute(self):
        """
        Start the DAG by executing root nodes
        :return:
        """
        self.called_done_callbacks = False
        roots = [node for node in self.nodes.values() if not node.parents]
        if not roots:
            raise TileDBCloudError("DAG is circular, there are no root nodes")
        for node in roots:
            self._exec_node(node)

    def _exec_node(self, node):
        """
        Execute a node
        :param node: node to execute
        """
        ready_to_compute = node.status == Status.NOT_STARTED and all(
            parent.status == Status.COMPLETED for parent in node.parents.values()
        )
        if ready_to_compute:
            del self.not_started_nodes[node.id]
            self.running_nodes[node.id] = node
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
        for node in self.running_nodes.values():
            node.cancel()
        for node in self.not_started_nodes.values():
            node.cancel()

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
        G = nx.DiGraph()
        for n in self.nodes.values():
            G.add_node(n.name)
            for child in n.children.values():
                G.add_node(child.name)
                G.add_edge(n.name, child.name)

        return G

    def visualize(self, notebook=True, auto_update=True, force_plotly=False):
        """
        Build and render a tree diagram of the DAG.
        :param notebook: Is the visualization inside a jupyter notebook? If so we'll use a widget
        :param auto_update: Should the diagram be auto updated with each status change
        :param force_plotly: Force the use of plotly graphs instead of TileDB Plot Widget
        :return: returns figure
        """
        if notebook and not force_plotly:
            try:
                return visualize_tiledb(self, auto_update=auto_update)
            except ImportError:
                pass
        return visualize_plotly(self, notebook=notebook, auto_update=auto_update)

    def end_nodes(self):
        """
        Find all ends nodes

        dag = DAG()
        dag.add_node(Node())

        end_nodes = dag.end_nodes()

        :return: list of root nodes
        """
        return [node for node in self.nodes.values() if not node.children]

    def end_results(self):
        """
        Get all end results, will block if all results are not ready

        dag = DAG()
        dag.add_node(Node())

        end_results = dag.end_results()

        :return: map of results by node ID
        """
        return {node.id: node.result() for node in self.end_nodes()}

    def end_results_by_name(self):
        """
        Get all end results, will block if all results are not ready

        dag = DAG()
        dag.add_node(Node())

        end_results = dag.end_results_by_name()

        :return: map of results by node name
        """
        return {node.name: node.result() for node in self.end_nodes()}
