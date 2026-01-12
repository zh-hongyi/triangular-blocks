#!/usr/bin/env python3
"""
Catalog of interesting forbidden subgraph patterns.

This provides helper functions to create various named graphs that
you might want to forbid in triangular blocks.
"""

import networkx as nx


def create_diamond():
    """
    Diamond: K4 minus one edge.
    Also known as the graph K4 - e.
    """
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 3)
        # Missing: (2, 3)
    ])
    return G


def create_paw():
    """
    Paw: Triangle with a pendant edge.
    Also known as a 3-pan or claw with one edge subdivided.
    """
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (1, 2), (2, 0),  # Triangle
        (0, 3)  # Pendant edge
    ])
    return G


def create_bull():
    """
    Bull: Triangle with two pendant edges on different vertices.
    """
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (1, 2), (2, 0),  # Triangle
        (0, 3), (1, 4)  # Two pendant edges
    ])
    return G


def create_house():
    """
    House: 5-cycle with one chord (forms a "roof").
    """
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),  # 5-cycle
        (0, 2)  # Chord (roof)
    ])
    return G


def create_theta(k=3):
    """
    Theta graph: Two vertices connected by k internally disjoint paths.
    Default k=3 gives the classic theta graph.
    """
    G = nx.Graph()
    # Connect vertex 0 to vertex 1 through k different paths
    # Each path has one intermediate vertex
    for i in range(k):
        G.add_edge(0, 2 + i)
        G.add_edge(2 + i, 1)
    return G


def create_kite():
    """
    Kite: Diamond with a pendant edge.
    K4 minus one edge, with a pendant edge added.
    """
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 3),  # Diamond
        (2, 4)  # Pendant
    ])
    return G


def create_bowtie():
    """
    Bowtie (Butterfly): Two triangles sharing a vertex.
    """
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (1, 2), (2, 0),  # First triangle
        (0, 3), (3, 4), (4, 0)   # Second triangle (shares vertex 0)
    ])
    return G


def create_gem():
    """
    Gem: Diamond with a pendant edge on the non-adjacent pair.
    Also known as the fan graph F4.
    """
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (1, 2), (2, 3), (3, 0),  # 4-cycle
        (0, 2),  # Diagonal
        (1, 4)   # Pendant
    ])
    return G


def create_claw():
    """
    Claw: Star graph K_{1,3}.
    One center vertex connected to 3 leaves.
    """
    return nx.star_graph(3)


def create_fork():
    """
    Fork: Path of length 3 with a pendant edge in the middle.
    Also known as a Y-graph or the graph P4 + e.
    """
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (1, 2), (2, 3),  # Path
        (1, 4)  # Pendant from middle
    ])
    return G


def create_banner():
    """
    Banner: Triangle with two pendant edges from the same vertex.
    """
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (1, 2), (2, 0),  # Triangle
        (0, 3), (0, 4)  # Two pendants from vertex 0
    ])
    return G


def create_dart():
    """
    Dart: Kite without one pendant edge.
    Also known as diamond with a single pendant.
    """
    G = nx.Graph()
    G.add_edges_from([
        (0, 1), (0, 2), (1, 2),  # Triangle
        (2, 3), (3, 4), (4, 2),  # Another triangle sharing edge
    ])
    return G


def print_graph_info(name, graph):
    """Helper to print graph information."""
    print(f"\n{name}:")
    print(f"  Vertices: {graph.number_of_nodes()}")
    print(f"  Edges: {graph.number_of_edges()}")
    print(f"  Edges: {sorted(graph.edges())}")
    degree_seq = sorted([d for _, d in graph.degree()], reverse=True)
    print(f"  Degree sequence: {degree_seq}")


def main():
    """Display catalog of available graphs."""
    print("="*70)
    print("GRAPH CATALOG - Named Forbidden Subgraphs")
    print("="*70)

    graphs = {
        "Diamond (K4 - e)": create_diamond(),
        "Paw": create_paw(),
        "Bull": create_bull(),
        "House": create_house(),
        "Theta-3": create_theta(3),
        "Kite": create_kite(),
        "Bowtie": create_bowtie(),
        "Gem": create_gem(),
        "Claw (K_{1,3})": create_claw(),
        "Fork": create_fork(),
        "Banner": create_banner(),
        "Dart": create_dart(),
    }

    for name, graph in graphs.items():
        print_graph_info(name, graph)

    print("\n" + "="*70)
    print("USAGE:")
    print("="*70)
    print("""
from graph_catalog import create_diamond, create_house, create_paw
from src.triangular_blocks import generate_triangular_blocks_avoiding_subgraph

# Use any of these as forbidden subgraphs
diamond = create_diamond()
blocks = generate_triangular_blocks_avoiding_subgraph(6, diamond)

# Or create your own custom graph
custom = nx.Graph()
custom.add_edges_from([(0,1), (1,2), (2,3), ...])
blocks = generate_triangular_blocks_avoiding_subgraph(n, custom)
""")

    print("\n" + "="*70)
    print("NETWORKX BUILT-IN GENERATORS:")
    print("="*70)
    print("""
# Complete graphs
nx.complete_graph(n)
nx.complete_bipartite_graph(m, n)

# Cycles and paths
nx.cycle_graph(n)
nx.path_graph(n)

# Stars and wheels
nx.star_graph(n)
nx.wheel_graph(n)

# Regular graphs
nx.circulant_graph(n, offsets)
nx.ladder_graph(n)

# Famous graphs
nx.petersen_graph()
nx.tutte_graph()
nx.chvatal_graph()
nx.heawood_graph()

# Random graphs
nx.erdos_renyi_graph(n, p)
nx.barabasi_albert_graph(n, m)

# And many more! See: https://networkx.org/documentation/stable/reference/generators.html
""")


if __name__ == '__main__':
    main()
