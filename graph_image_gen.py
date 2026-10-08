from graphviz import Digraph, Graph

import networkx as nx
import matplotlib.pyplot as plt



def safe_node_name(name):
    return f'"{str(name).replace(":", ".")}"'



def triples_group_to_diagram_nx(triples, out_path, spread="balanced"):
    """
    Spring layout only.
    User only chooses: compact | balanced | spread
    """

    G = nx.DiGraph()

    # Build graph
    for s, p, o in triples:
        s, o, p = safe_node_name(s), safe_node_name(o), safe_node_name(p)
        G.add_edge(s, o, label=safe_node_name(p))

    # Single spread control (no config dict)


    # Spring layout
    pos = nx.spring_layout(G, k=1.3, seed=42, iterations=200)

    # Draw
    plt.figure(figsize=(14, 8))

    nx.draw_networkx_nodes(
        G, pos,
        node_color="#FFFFFF",
        edgecolors="#CBD5E1",
        node_size=1300,
        node_shape="s"
    )

    nx.draw_networkx_edges(
        G, pos,
        edge_color="#64748B",
        arrows=True,
        arrowsize=14,
        width=1
    )

    nx.draw_networkx_labels(
        G, pos,
        font_size=9,
        font_family="DejaVu Sans"
    )

    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_size=7,
        font_family="DejaVu Sans"
    )

    plt.axis("off")
    plt.tight_layout()

    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()

    return out_path + ".png"





def triples_group_to_diagram_chaos(triples, out_path):
    # Use force-directed layout instead of hierarchical "dot"
    dot = Graph(format="png", engine="neato")

    # Looser layout = more "messy / unstructured"
    dot.attr(
        bgcolor="white",
        overlap="false",
        splines="true",
        sep="+10",
        nodesep="0.8",
        ranksep="0.8",
    )

    # Minimal node styling
    dot.attr(
        "node",
        shape="box",
        style="rounded",
        color="#444444",
        fontname="Helvetica",
        fontsize="10",
    )

    # Very simple edges (no labels)
    dot.attr(
        "edge",
        color="#999999",
        penwidth="1",
        arrowsize="0.7",
    )

    # Collect nodes
    nodes = set()
    for s, p, o in triples:
        nodes.add(s)
        nodes.add(o)

    # Add nodes
    for n in nodes:
        dot.node(safe_node_name(n), label=str(n))

    # Add edges (NO predicate labels = less structure)
    for s, p, o in triples:
        dot.edge(safe_node_name(s), safe_node_name(o), label=str(p))

    return dot.render(out_path, cleanup=True)



def triples_group_to_diagram(triples, out_path, rankdir="LR"):
    dot = Digraph(format="png", engine="dot")

    dot.attr(
        rankdir=rankdir,
        bgcolor="white",
        splines="true",
        nodesep="0.35",
        ranksep="0.55",
        pad="0.2",
    )

    dot.attr(
        "node",
        shape="box",
        style="rounded,filled",
        fillcolor="#F8FAFC",
        color="#CBD5E1",
        fontname="Helvetica",
        fontsize="11",
        margin="0.12,0.08",
    )

    dot.attr(
        "edge",
        color="#64748B",
        fontname="Helvetica",
        fontsize="10",
        arrowsize="0.8",
    )

    nodes = set()
    for s, p, o in triples:
        nodes.add(s)
        nodes.add(o)

    for n in nodes:
        dot.node(safe_node_name(n), label=str(n))

    for s, p, o in triples:
        dot.edge(safe_node_name(s), safe_node_name(o), label=str(p))

    return dot.render(out_path, cleanup=True)
