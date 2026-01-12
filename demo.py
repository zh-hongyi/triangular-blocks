#!/usr/bin/env python3
"""
Quick demonstration of both triangular block generation algorithms.
"""

import networkx as nx
from src.triangular_blocks import (
    generate_triangular_blocks,
    generate_triangular_blocks_avoiding_subgraph
)

print("="*70)
print("Triangular Block Generation Demonstration")
print("="*70)
print()

# Example 1: Generate all triangular blocks on 4 vertices
print("Example 1: All triangular blocks on 4 vertices")
print("-" * 70)
blocks_4 = generate_triangular_blocks(4)
print(f"Found {len(blocks_4)} blocks:")
for i, block in enumerate(blocks_4):
    print(f"  Block {i+1}: {block.number_of_edges()} edges - {sorted(block.edges())}")
print()

# Example 2: Generate all triangular blocks on 5 vertices
print("Example 2: All triangular blocks on 5 vertices")
print("-" * 70)
blocks_5 = generate_triangular_blocks(5)
print(f"Found {len(blocks_5)} blocks:")
for i, block in enumerate(blocks_5):
    edges = block.number_of_edges()
    deg_seq = sorted([d for _, d in block.degree()], reverse=True)
    print(f"  Block {i+1}: {edges} edges, degree sequence {deg_seq}")
print()

# Example 3: Generate C4-free triangular blocks on 5 vertices
print("Example 3: C4-free triangular blocks on 5 vertices")
print("-" * 70)
C4 = nx.cycle_graph(4)
blocks_5_no_C4 = generate_triangular_blocks_avoiding_subgraph(5, C4)
print(f"Found {len(blocks_5_no_C4)} C4-free blocks:")
for i, block in enumerate(blocks_5_no_C4):
    edges = block.number_of_edges()
    deg_seq = sorted([d for _, d in block.degree()], reverse=True)
    print(f"  Block {i+1}: {edges} edges, degree sequence {deg_seq}")
print()

# Comparison
print("Comparison:")
print("-" * 70)
print(f"All blocks on 5 vertices: {len(blocks_5)}")
print(f"C4-free blocks on 5 vertices: {len(blocks_5_no_C4)}")
print(f"Blocks containing C4: {len(blocks_5) - len(blocks_5_no_C4)}")
print()

print("="*70)
print("Demonstration complete!")
print("="*70)
