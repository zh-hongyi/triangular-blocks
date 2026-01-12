#!/usr/bin/env python3
"""
Example demonstrating triangular block generation while avoiding a forbidden subgraph.

This is useful for Turán-type problems where we want maximal graphs avoiding
certain patterns.

Usage:
    python example_avoid_subgraph.py <n> <forbidden_graph_name>

Examples:
    python example_avoid_subgraph.py 6 K3      # Avoid triangles
    python example_avoid_subgraph.py 6 C4      # Avoid 4-cycles
    python example_avoid_subgraph.py 6 P3      # Avoid paths of length 3
"""

import sys
import networkx as nx
from src.triangular_blocks import (
    generate_triangular_blocks_avoiding_subgraph,
    get_block_info
)
from src.validation import validate_triangular_block


def create_forbidden_graph(name):
    """
    Create a forbidden graph by name.

    Supported names:
    - K3, K4, K5: Complete graphs
    - C3, C4, C5, C6: Cycles
    - P3, P4: Paths
    - K2_3: Complete bipartite graph K_{2,3}
    """
    name = name.upper()

    # Complete graphs
    if name.startswith('K') and name[1:].isdigit():
        k = int(name[1:])
        return nx.complete_graph(k)

    # Cycles
    if name.startswith('C') and name[1:].isdigit():
        c = int(name[1:])
        return nx.cycle_graph(c)

    # Paths
    if name.startswith('P') and name[1:].isdigit():
        p = int(name[1:])
        return nx.path_graph(p)

    # Complete bipartite
    if name.startswith('K') and '_' in name:
        parts = name[1:].split('_')
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            m, n = int(parts[0]), int(parts[1])
            return nx.complete_bipartite_graph(m, n)

    raise ValueError(f"Unknown forbidden graph: {name}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python example_avoid_subgraph.py <n> <forbidden_graph_name>")
        print()
        print("Examples:")
        print("  python example_avoid_subgraph.py 6 K3      # Avoid triangles")
        print("  python example_avoid_subgraph.py 6 C4      # Avoid 4-cycles")
        print("  python example_avoid_subgraph.py 6 P3      # Avoid 3-paths")
        print()
        print("Supported forbidden graphs:")
        print("  K3, K4, K5, ...  (Complete graphs)")
        print("  C3, C4, C5, ...  (Cycles)")
        print("  P3, P4, P5, ...  (Paths)")
        print("  K2_3, K3_3, ...  (Complete bipartite)")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Error: n must be an integer")
        sys.exit(1)

    if n < 2:
        print("Error: n must be at least 2")
        sys.exit(1)

    forbidden_name = sys.argv[2]

    try:
        forbidden_graph = create_forbidden_graph(forbidden_name)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("="*60)
    print(f"Generating Triangular Blocks with {n} Vertices")
    print(f"Avoiding subgraph: {forbidden_name}")
    print("="*60)
    print()
    print(f"Forbidden graph: {forbidden_graph.number_of_nodes()} vertices, "
          f"{forbidden_graph.number_of_edges()} edges")
    print(f"Forbidden edges: {sorted(forbidden_graph.edges())}")
    print()

    # Generate blocks
    print(f"Generating blocks avoiding {forbidden_name}...")
    blocks = generate_triangular_blocks_avoiding_subgraph(n, forbidden_graph)

    print(f"Found {len(blocks)} non-isomorphic triangular block(s)")
    print()

    print("="*60)
    print("Detailed Information")
    print("="*60)

    for i, block in enumerate(blocks):
        print(f"\nBlock {i+1}:")
        print("-" * 40)

        # Get info
        info = get_block_info(block)
        print(f"  Vertices: {info['vertices']}")
        print(f"  Edges: {info['edges']}")
        print(f"  Degree sequence: {info['degree_sequence']}")
        print(f"  Is planar: {info['is_planar']}")
        print(f"  Is connected: {info['is_connected']}")

        # List edges
        print(f"  Edge list: {sorted(block.edges())}")

        # Validate
        _, msg = validate_triangular_block(block)
        print(f"  Validation: {msg}")

    print()
    print("="*60)
    print(f"Summary: Found {len(blocks)} block(s) on {n} vertices avoiding {forbidden_name}")
    print("="*60)

    # Find maximal block (most edges)
    if blocks:
        max_edges = max(b.number_of_edges() for b in blocks)
        maximal_blocks = [b for b in blocks if b.number_of_edges() == max_edges]

        print()
        print(f"Extremal result: Maximum {max_edges} edges in {forbidden_name}-free "
              f"triangular blocks on {n} vertices")
        if len(maximal_blocks) > 1:
            print(f"  (achieved by {len(maximal_blocks)} non-isomorphic blocks)")


if __name__ == '__main__':
    main()
