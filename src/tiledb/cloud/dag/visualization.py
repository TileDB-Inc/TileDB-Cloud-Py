import json
import random

from tiledb.cloud.dag import status as st


def build_graph_node_details(nodes):
    """
    :param nodes: List of nodes to get status of
    :return: tuple of node_colors and node_text
    """
    # Loop over statuses to set color and label.
    # If you rerun this cell and the one below you can update the graph
    node_colors = []
    node_text = []
    for node in nodes:
        status = node.status
        if status == st.Status.NOT_STARTED:
            node_text.append("{} - Not Started".format(node.name))
            node_colors.append("black")
        elif status == st.Status.RUNNING:
            node_text.append("{} - Running".format(node.name))
            node_colors.append("blue")
        elif status == st.Status.COMPLETED:
            node_text.append("{} - Completed".format(node.name))
            node_colors.append("green")
        elif status == st.Status.FAILED:
            node_text.append("{} - Failed".format(node.name))
            node_colors.append("red")
        elif status == st.Status.CANCELLED:
            node_text.append("{} - Cancelled".format(node.name))
            node_colors.append("yellow")

    return (node_colors, node_text)


def update_plotly_graph(nodes, fig=None):
    """
    Update a graph based on based node status and figure
    :param nodes: list of notes to update
    :param fig:
    :return:
    """

    (node_colors, node_text) = build_graph_node_details(nodes)

    if fig is not None:
        fig.update_traces(
            marker=dict(color=node_colors),
            text=node_text,
            selector=dict(mode="markers"),
        )


def update_tiledb_graph(nodes, edges, node_details, positions, fig):
    """
    Update a tiledb plot widge graph
    :param nodes: nodes of graph
    :param edges: edges for graph
    :param node_details: Node details
    :param positions: positions for graph
    :param fig: figure
    :return:
    """
    if fig is not None:
        fig.setData(
            json.dumps(
                dict(
                    nodes=nodes,
                    edges=edges,
                    node_details=node_details,
                    positions=positions,
                )
            )
        )


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

    **width** horizontal space allocated for this branch -
        avoids overlap with other branches

    **vert_gap** gap between levels of hierarchy

    **vert_loc** vertical location of root

    **leaf_vs_root_factor**

    xcenter: horizontal location of root
    """  # noqa: E501
    import networkx as nx

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
    xmax = max(x for x, y in pos.values())
    for node in pos:
        pos[node] = (pos[node][0] * width / xmax, pos[node][1])
    return pos


def build_visualization_positions(network):
    """
    Builds the positional spacing of all nodes(markers) based on either pydot
    if available or falling back to a python computation
    :param network:
    :return: position array
    """
    try:
        # First try to use pydot and dot, as it produces
        # the most aesthetically pleasing trees
        from networkx.drawing.nx_pydot import pydot_layout

        return pydot_layout(network, prog="dot")
    except Exception:
        # Fall back to python function so we don't have to require users
        # to install graphviz
        return hierarchy_pos(network, width=2.0, leaf_vs_root_factor=1.0)
