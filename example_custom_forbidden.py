#!/usr/bin/env python3
"""
Examples of using custom/complicated forbidden subgraphs.

This demonstrates how to create and use arbitrary forbidden subgraphs
beyond the standard ones (Kn, Cn, Pn).
"""

import networkx as nx
from src.triangular_blocks import generate_triangular_blocks_avoiding_subgraph


def example_1_theta_graph():
    """Theta graph: two vertices connected by 3 internally disjoint paths."""
    print("="*70)
    print("Example 1: Avoiding Theta Graph (θ_3)")
    print("="*70)
    print()

    # Create theta graph manually
    theta = nx.Graph()
    theta.add_edges_from([
        (0, 1),  # Direct edge
        (0, 2), (2, 3), (3, 1),  # Path of length 3
        (0, 4), (4, 5), (5, 1),  # Another path of length 3
    ])

    print(f"Theta graph: {theta.number_of_nodes()} vertices, {theta.number_of_edges()} edges")
    print(f"Edges: {sorted(theta.edges())}")
    print()

    # Generate blocks avoiding theta
    blocks = generate_triangular_blocks_avoiding_subgraph(6, theta)
    print(f"Found {len(blocks)} theta-free triangular blocks on 6 vertices")

    if blocks:
        max_edges = max(b.number_of_edges() for b in blocks)
        print(f"Maximum edges: {max_edges}")
    print()


def example_2_diamond():
    """Diamond graph: K4 minus one edge."""
    print("="*70)
    print("Example 2: Avoiding Diamond (K4 - e)")
    print("="*70)
    print()

    # Create diamond graph
    diamond = nx.Graph()
    diamond.add_edges_from([
        (0, 1), (0, 2), (0, 3),
        (1, 2), (1, 3)
        # Missing: (2, 3) - this would complete K4
    ])

    print(f"Diamond graph: {diamond.number_of_nodes()} vertices, {diamond.number_of_edges()} edges")
    print(f"Edges: {sorted(diamond.edges())}")
    print()

    blocks = generate_triangular_blocks_avoiding_subgraph(5, diamond)
    print(f"Found {len(blocks)} diamond-free triangular blocks on 5 vertices")

    if blocks:
        max_edges = max(b.number_of_edges() for b in blocks)
        print(f"Maximum edges: {max_edges}")
    print()


def example_3_paw():
    """Paw graph: Triangle with a pendant edge (K3 + edge)."""
    print("="*70)
    print("Example 3: Avoiding Paw Graph (K3 + pendant edge)")
    print("="*70)
    print()

    # Create paw graph
    paw = nx.Graph()
    paw.add_edges_from([
        (0, 1), (1, 2), (2, 0),  # Triangle
        (0, 3)  # Pendant edge
    ])

    print(f"Paw graph: {paw.number_of_nodes()} vertices, {paw.number_of_edges()} edges")
    print(f"Edges: {sorted(paw.edges())}")
    print()

    blocks = generate_triangular_blocks_avoiding_subgraph(6, paw)
    print(f"Found {len(blocks)} paw-free triangular blocks on 6 vertices")

    if blocks:
        max_edges = max(b.number_of_edges() for b in blocks)
        print(f"Maximum edges: {max_edges}")
    print()


def example_4_house():
    """House graph: 5-cycle with a chord."""
    print("="*70)
    print("Example 4: Avoiding House Graph (C5 + chord)")
    print("="*70)
    print()

    # Create house graph
    house = nx.Graph()
    house.add_edges_from([
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),  # 5-cycle
        (0, 2)  # Chord forming the "roof"
    ])

    print(f"House graph: {house.number_of_nodes()} vertices, {house.number_of_edges()} edges")
    print(f"Edges: {sorted(house.edges())}")
    print()

    blocks = generate_triangular_blocks_avoiding_subgraph(6, house)
    print(f"Found {len(blocks)} house-free triangular blocks on 6 vertices")

    if blocks:
        max_edges = max(b.number_of_edges() for b in blocks)
        print(f"Maximum edges: {max_edges}")
    print()


def example_5_wheel():
    """Wheel graph: Cycle with a central hub."""
    print("="*70)
    print("Example 5: Avoiding Wheel Graph W4 (4-cycle + center)")
    print("="*70)
    print()

    # Create wheel graph W4
    wheel = nx.wheel_graph(5)  # Creates W4 (4-cycle with center)

    print(f"Wheel W4: {wheel.number_of_nodes()} vertices, {wheel.number_of_edges()} edges")
    print(f"Edges: {sorted(wheel.edges())}")
    print()

    blocks = generate_triangular_blocks_avoiding_subgraph(6, wheel)
    print(f"Found {len(blocks)} W4-free triangular blocks on 6 vertices")

    if blocks:
        max_edges = max(b.number_of_edges() for b in blocks)
        print(f"Maximum edges: {max_edges}")
    print()


def example_6_custom_arbitrary():
    """Completely custom arbitrary graph."""
    print("="*70)
    print("Example 6: Custom Arbitrary Graph")
    print("="*70)
    print()

    # Create any graph you want!
    custom = nx.Graph()
    custom.add_edges_from([
        (0, 1), (1, 2), (2, 3),  # Path
        (3, 4), (4, 0),  # Complete the cycle
        (1, 4),  # Cross connection
        (2, 5), (5, 3)  # Extra triangle
    ])

    print(f"Custom graph: {custom.number_of_nodes()} vertices, {custom.number_of_edges()} edges")
    print(f"Edges: {sorted(custom.edges())}")
    print()

    blocks = generate_triangular_blocks_avoiding_subgraph(7, custom)
    print(f"Found {len(blocks)} custom-forbidden triangular blocks on 7 vertices")

    if blocks:
        max_edges = max(b.number_of_edges() for b in blocks)
        print(f"Maximum edges: {max_edges}")
    print()


def example_7_from_edge_list():
    """Create forbidden graph from a simple edge list."""
    print("="*70)
    print("Example 7: From Edge List")
    print("="*70)
    print()

    # You can define graphs by just listing edges
    edge_list = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),  # 6-cycle
        (0, 3), (1, 4), (2, 5)  # Three chords
    ]

    forbidden = nx.Graph()
    forbidden.add_edges_from(edge_list)

    print(f"Graph from edge list: {forbidden.number_of_nodes()} vertices, "
          f"{forbidden.number_of_edges()} edges")
    print(f"Edges: {sorted(forbidden.edges())}")
    print()

    blocks = generate_triangular_blocks_avoiding_subgraph(7, forbidden)
    print(f"Found {len(blocks)} triangular blocks avoiding this pattern on 7 vertices")

    if blocks:
        max_edges = max(b.number_of_edges() for b in blocks)
        print(f"Maximum edges: {max_edges}")
    print()


def example_8_disjoint_union():
    """Disjoint union of graphs (multiple components)."""
    print("="*70)
    print("Example 8: Disjoint Union (2 × K3)")
    print("="*70)
    print()

    # Avoid having two disjoint triangles
    forbidden = nx.disjoint_union(nx.complete_graph(3), nx.complete_graph(3))

    print(f"2 × K3: {forbidden.number_of_nodes()} vertices, {forbidden.number_of_edges()} edges")
    print(f"Components: 2 disconnected triangles")
    print()

    blocks = generate_triangular_blocks_avoiding_subgraph(7, forbidden)
    print(f"Found {len(blocks)} blocks avoiding two disjoint triangles on 7 vertices")

    if blocks:
        max_edges = max(b.number_of_edges() for b in blocks)
        print(f"Maximum edges: {max_edges}")
    print()


def example_9_petersen_graph():
    """Famous Petersen graph."""
    print("="*70)
    print("Example 9: Petersen Graph")
    print("="*70)
    print()

    # NetworkX has many famous graphs built-in
    petersen = nx.petersen_graph()

    print(f"Petersen graph: {petersen.number_of_nodes()} vertices, "
          f"{petersen.number_of_edges()} edges")
    print(f"Properties: 3-regular, 10 vertices")
    print()

    # This will likely find no blocks since Petersen is quite large
    blocks = generate_triangular_blocks_avoiding_subgraph(11, petersen)
    print(f"Found {len(blocks)} Petersen-free triangular blocks on 11 vertices")
    print()


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("CUSTOM FORBIDDEN SUBGRAPH EXAMPLES")
    print("="*70)
    print("\nYou can use ANY networkx Graph as a forbidden subgraph!")
    print()

    examples = [
        example_1_theta_graph,
        example_2_diamond,
        example_3_paw,
        example_4_house,
        example_5_wheel,
        example_6_custom_arbitrary,
        example_7_from_edge_list,
        example_8_disjoint_union,
        example_9_petersen_graph,
    ]

    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"Error in {example_func.__name__}: {e}")
            print()

    print("="*70)
    print("KEY TAKEAWAY:")
    print("="*70)
    print("""
You can forbid ANY graph structure! Just create a networkx Graph:

    # Method 1: Add edges one by one
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_edge(1, 2)
    ...

    # Method 2: Add from edge list
    G = nx.Graph()
    G.add_edges_from([(0,1), (1,2), (2,3), ...])

    # Method 3: Use networkx built-ins
    G = nx.wheel_graph(5)
    G = nx.petersen_graph()
    ...

Then pass it to generate_triangular_blocks_avoiding_subgraph(n, G)
""")


if __name__ == '__main__':
    main()
