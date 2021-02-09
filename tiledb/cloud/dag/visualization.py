import networkx as nx
import random
import json

from .status import Status

STATUS_COLOR = {
    Status.NOT_STARTED: "black",
    Status.RUNNING: "blue",
    Status.COMPLETED: "green",
    Status.FAILED: "red",
    Status.CANCELLED: "yellow",
}


def visualize_plotly(dag, notebook=True, auto_update=True):
    """

    :param notebook: Is the visualization inside a jupyter notebook? If so we'll use a widget
    :param auto_update: Should the diagram be auto updated with each status change
    :return: figure
    """
    import plotly.graph_objects as go

    G = dag.networkx_graph()
    pos = build_visualization_positions(G)

    # Convert to plotly scatter plot
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend((x0, x1, None))
        edge_y.extend((y0, y1, None))

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    # Build node x,y and also build a mapping of the graph market numbers to actual
    # node objects so we can fetch status. The graph ends up with each market on a
    # list, so we need to map from this list's order to actual nodes so we can look things up
    node_x = []
    node_y = []
    nodes = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        nodes.append(dag.nodes_by_name[node])

    def get_node_colors():
        return [STATUS_COLOR[node.status] for node in nodes]

    def get_node_labels():
        return [f"{node.name} - {node.status.value}" for node in nodes]

    # Build node scatter plot
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        marker=dict(size=15, line_width=2),
    )

    node_trace.marker.color = get_node_colors()
    node_trace.text = get_node_labels()

    fig_cls = go.FigureWidget if notebook else go.Figure
    # Create plot
    fig = fig_cls(
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

    if auto_update:

        @dag.add_update_callback
        def update_callback(_):
            fig.update_traces(
                marker={"color": get_node_colors()},
                text=get_node_labels(),
                selector={"mode": "markers"},
            )

    return fig


def visualize_tiledb(dag, auto_update=True):
    """
    Create graph visualization with tiledb.plot.widget
    :param auto_update: Should the diagram be auto updated with each status change
    :return: figure
    """
    import tiledb.plot.widget

    def get_node_details():
        return {
            name: dict(name=name, status=node.status.value)
            for name, node in dag.nodes_by_name.items()
        }

    G = dag.networkx_graph()
    visualization = {
        "nodes": list(G.nodes()),
        "edges": list(G.edges()),
        "node_details": get_node_details(),
        "positions": build_visualization_positions(G),
    }
    fig = tiledb.plot.widget.Visualize(data=json.dumps(visualization))

    if auto_update:

        @dag.add_update_callback
        def update_callback(_):
            visualization["node_details"] = get_node_details()
            fig.setData(json.dumps(visualization))

    return fig


def build_visualization_positions(network):
    """
    Builds the positional spacing of all nodes(markers) based on either pydot if available or falling back
    to a python computation
    :param network:
    :return: position array
    """
    try:
        # First try to use pydot and dot, as it produces the most aesthetically pleasing trees
        from networkx.drawing.nx_pydot import pydot_layout

        return pydot_layout(network, prog="dot")
    except:
        # Fall back to python function so we don't have to require users to install graphviz
        return hierarchy_pos(network, width=2.0, leaf_vs_root_factor=1.0)


def hierarchy_pos(
    G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, leaf_vs_root_factor=0.5
):
    """
    Taken from https://epidemicsonnetworks.readthedocs.io/en/latest/_modules/EoN/auxiliary.html#hierarchy_pos
    Licensed under MIT: https://epidemicsonnetworks.readthedocs.io/en/latest/_downloads/8e9c8138fef49ddba8102fa7799c29d7/license.txt

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    Based on Joel's answer at https://stackoverflow.com/a/29597209/2966723,
    but with some modifications.

    We include this because it may be useful for plotting transmission trees,
    and there is currently no networkx equivalent (though it may be coming soon).

    There are two basic approaches we think of to allocate the horizontal
    location of a node.

    - Top down: we allocate horizontal space to a node.  Then its ``k``
      descendants split up that horizontal space equally.  This tends to result
      in overlapping nodes when some have many descendants.
    - Bottom up: we allocate horizontal space to each leaf node.  A node at a
      higher level gets the entire space allocated to its descendant leaves.
      Based on this, leaf nodes at higher levels get the same space as leaf
      nodes very deep in the tree.

    We use use both of these approaches simultaneously with ``leaf_vs_root_factor``
    determining how much of the horizontal space is based on the bottom up
    or top down approaches.  ``0`` gives pure bottom up, while 1 gives pure top
    down.


    :Arguments:

    **G** the graph (must be a tree)

    **root** the root node of the tree
    - if the tree is directed and this is not given, the root will be found and used
    - if the tree is directed and this is given, then the positions will be
      just for the descendants of this node.
    - if the tree is undirected and not given, then a random choice will be used.

    **width** horizontal space allocated for this branch - avoids overlap with other branches

    **vert_gap** gap between levels of hierarchy

    **vert_loc** vertical location of root

    **leaf_vs_root_factor**

    xcenter: horizontal location of root
    """
    if not nx.is_tree(G):
        raise TypeError("cannot use hierarchy_pos on a graph that is not a tree")

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(
                iter(nx.topological_sort(G))
            )  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(
        G,
        root,
        leftmost,
        width,
        leafdx=0.2,
        vert_gap=0.2,
        vert_loc=0,
        xcenter=0.5,
        rootpos=None,
        leafpos=None,
        parent=None,
    ):
        """
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        """

        if rootpos is None:
            rootpos = {root: (xcenter, vert_loc)}
        else:
            rootpos[root] = (xcenter, vert_loc)
        if leafpos is None:
            leafpos = {}
        children = list(G.neighbors(root))
        leaf_count = 0
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            rootdx = width / len(children)
            nextx = xcenter - width / 2 - rootdx / 2
            for child in children:
                nextx += rootdx
                rootpos, leafpos, newleaves = _hierarchy_pos(
                    G,
                    child,
                    leftmost + leaf_count * leafdx,
                    width=rootdx,
                    leafdx=leafdx,
                    vert_gap=vert_gap,
                    vert_loc=vert_loc - vert_gap,
                    xcenter=nextx,
                    rootpos=rootpos,
                    leafpos=leafpos,
                    parent=root,
                )
                leaf_count += newleaves

            leftmostchild = min((x for x, y in [leafpos[child] for child in children]))
            rightmostchild = max((x for x, y in [leafpos[child] for child in children]))
            leafpos[root] = ((leftmostchild + rightmostchild) / 2, vert_loc)
        else:
            leaf_count = 1
            leafpos[root] = (leftmost, vert_loc)
        #        pos[root] = (leftmost + (leaf_count-1)*dx/2., vert_loc)
        #        print(leaf_count)
        return rootpos, leafpos, leaf_count

    xcenter = width / 2.0
    if isinstance(G, nx.DiGraph):
        leafcount = len(
            [node for node in nx.descendants(G, root) if G.out_degree(node) == 0]
        )
    elif isinstance(G, nx.Graph):
        leafcount = len(
            [
                node
                for node in nx.node_connected_component(G, root)
                if G.degree(node) == 1 and node != root
            ]
        )
    rootpos, leafpos, leaf_count = _hierarchy_pos(
        G,
        root,
        0,
        width,
        leafdx=width * 1.0 / leafcount,
        vert_gap=vert_gap,
        vert_loc=vert_loc,
        xcenter=xcenter,
    )
    pos = {}
    for node in rootpos:
        pos[node] = (
            leaf_vs_root_factor * leafpos[node][0]
            + (1 - leaf_vs_root_factor) * rootpos[node][0],
            leafpos[node][1],
        )
    #    pos = {node:(leaf_vs_root_factor*x1+(1-leaf_vs_root_factor)*x2, y1) for ((x1,y1), (x2,y2)) in (leafpos[node], rootpos[node]) for node in rootpos}
    xmax = max(x for x, y in pos.values())
    for node in pos:
        pos[node] = (pos[node][0] * width / xmax, pos[node][1])
    return pos
