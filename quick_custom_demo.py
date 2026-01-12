#!/usr/bin/env python3
"""
Quick demonstration of custom forbidden subgraphs.
"""

import networkx as nx
from src.triangular_blocks import generate_triangular_blocks_avoiding_subgraph


print("="*70)
print("CUSTOM FORBIDDEN SUBGRAPH DEMONSTRATION")
print("="*70)
print()

# Example 1: Diamond (K4 minus one edge)
print("Example 1: Diamond Graph (K4 - e)")
print("-" * 70)
diamond = nx.Graph()
diamond.add_edges_from([
    (0, 1), (0, 2), (0, 3),
    (1, 2), (1, 3)
    # Missing: (2, 3)
])
print(f"Diamond: {diamond.number_of_nodes()} vertices, {diamond.number_of_edges()} edges")
print(f"Edges: {sorted(diamond.edges())}")

blocks = generate_triangular_blocks_avoiding_subgraph(5, diamond)
print(f"Result: {len(blocks)} diamond-free blocks on 5 vertices")
if blocks:
    print(f"Max edges: {max(b.number_of_edges() for b in blocks)}")
print()

# Example 2: Theta graph (simpler version)
print("Example 2: Theta-3 Graph (two nodes, 3 parallel edges worth of structure)")
print("-" * 70)
# Simplified: just two triangles sharing an edge
theta = nx.Graph()
theta.add_edges_from([
    (0, 1), (0, 2), (1, 2),  # First triangle
    (1, 2), (1, 3), (2, 3)   # Second triangle (shares edge 1-2)
])
print(f"Theta-3: {theta.number_of_nodes()} vertices, {theta.number_of_edges()} edges")
print(f"Edges: {sorted(theta.edges())}")

blocks = generate_triangular_blocks_avoiding_subgraph(5, theta)
print(f"Result: {len(blocks)} theta-free blocks on 5 vertices")
if blocks:
    print(f"Max edges: {max(b.number_of_edges() for b in blocks)}")
print()

# Example 3: Completely custom from edge list
print("Example 3: Custom Graph from Edge List")
print("-" * 70)
custom_edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]  # Square with diagonal
custom = nx.Graph()
custom.add_edges_from(custom_edges)
print(f"Custom: {custom.number_of_nodes()} vertices, {custom.number_of_edges()} edges")
print(f"Edges: {sorted(custom.edges())}")

blocks = generate_triangular_blocks_avoiding_subgraph(5, custom)
print(f"Result: {len(blocks)} custom-free blocks on 5 vertices")
if blocks:
    print(f"Max edges: {max(b.number_of_edges() for b in blocks)}")
print()

# Example 4: Using NetworkX built-in graphs
print("Example 4: Using NetworkX Built-ins")
print("-" * 70)
print("Available built-in graphs:")
print("  - nx.complete_graph(n)")
print("  - nx.cycle_graph(n)")
print("  - nx.path_graph(n)")
print("  - nx.star_graph(n)")
print("  - nx.wheel_graph(n)")
print("  - nx.complete_bipartite_graph(m, n)")
print("  - nx.petersen_graph()")
print("  - nx.ladder_graph(n)")
print("  - And many more!")
print()

star4 = nx.star_graph(4)  # One center node connected to 4 others
print(f"Star graph K_{1,4}: {star4.number_of_nodes()} vertices, {star4.number_of_edges()} edges")

blocks = generate_triangular_blocks_avoiding_subgraph(6, star4)
print(f"Result: {len(blocks)} star-free blocks on 6 vertices")
if blocks:
    print(f"Max edges: {max(b.number_of_edges() for b in blocks)}")
print()

print("="*70)
print("KEY POINTS:")
print("="*70)
print("""
✓ You can use ANY networkx Graph as forbidden subgraph
✓ Create graphs by:
  1. G.add_edge(u, v) one by one
  2. G.add_edges_from([(u,v), ...]) from list
  3. Use NetworkX built-in graph generators

✓ The algorithm checks for SUBGRAPH ISOMORPHISM
  - It finds if the forbidden graph appears anywhere in the block
  - Vertex labels don't matter, only the structure

✓ Examples of interesting forbidden patterns:
  - K_n (complete graphs)
  - C_n (cycles)
  - Theta graphs
  - Diamond (K4 - edge)
  - House, Paw, Bull graphs
  - Stars, wheels, ladders
  - Any custom structure you define!
""")
