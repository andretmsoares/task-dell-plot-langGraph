import networkx as nx

def generate_node_positions(edges):
    G = nx.DiGraph()

    for src, dst, _ in edges:
        G.add_edge(src, dst)

    pos = nx.nx_pydot.graphviz_layout(G, prog="dot")

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    norm_pos = {}
    for node, (x, y) in pos.items():
        norm_pos[node] = (
            (x - min_x) / (max_x - min_x + 1e-9),
            (y - min_y) / (max_y - min_y + 1e-9)
        )

    return norm_pos