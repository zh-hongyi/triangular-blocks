#!/usr/bin/env python3
"""
Template for generating triangular blocks avoiding a custom forbidden graph.

INSTRUCTIONS:
1. Modify the forbidden graph edges below (lines 17-24)
2. Change the number of vertices n (line 27)
3. Run: source venv/bin/activate && python my_custom_search_template.py
"""

import networkx as nx
from src.triangular_blocks import generate_triangular_blocks_avoiding_subgraph
from src.triangular_blocks import get_block_info

# ============================================================
# STEP 1: Define your forbidden graph by listing its edges
# ============================================================
forbidden = nx.Graph()
forbidden.add_edges_from([
    # Add your edges here, e.g.:
    (0, 1), (0, 2), (1, 2),  # Triangle on vertices 0,1,2
    (1, 3), (2, 3),          # Connect to vertex 3
    (3, 4), (2, 4),          # Connect to vertex 4
    (1, 5), (5, 3)           # Connect to vertex 5
    # Add as many edges as needed for your forbidden pattern
])

# ============================================================
# STEP 2: Choose the number of vertices for triangular blocks
# ============================================================
n = 6  # Change this to any number >= 2 (e.g., 7, 8, 10)

# ============================================================
# STEP 3: Generate and display results
# ============================================================
print("="*70)
print(f"Generating Triangular Blocks on {n} Vertices")
print(f"Avoiding Custom Forbidden Subgraph")
print("="*70)
print()

print("Forbidden graph:")
print(f"  Vertices: {forbidden.number_of_nodes()}")
print(f"  Edges: {forbidden.number_of_edges()}")
print(f"  Edge list: {sorted(forbidden.edges())}")
print()

print(f"Generating triangular blocks on {n} vertices...")
blocks = generate_triangular_blocks_avoiding_subgraph(n=n, forbidden_graph=forbidden)

print(f"\nFound {len(blocks)} non-isomorphic triangular blocks")
print()

if len(blocks) == 0:
    print("No triangular blocks found!")
    print("This means every triangular block on {n} vertices contains your forbidden pattern.")
else:
    print("Detailed Results:")
    print("-" * 70)
    for i, block in enumerate(blocks):
        info = get_block_info(block)
        print(f"Block {i+1}: {info['edges']} edges, degree sequence {info['degree_sequence']}")

    # Find extremal (maximum edges)
    max_edges = max(b.number_of_edges() for b in blocks)
    min_edges = min(b.number_of_edges() for b in blocks)

    print()
    print("="*70)
    print("Summary:")
    print("="*70)
    print(f"Total blocks found: {len(blocks)}")
    print(f"Edge range: {min_edges} to {max_edges}")
    print(f"Maximum edges (extremal): {max_edges}")

    maximal_count = sum(1 for b in blocks if b.number_of_edges() == max_edges)
    if maximal_count > 1:
        print(f"  (achieved by {maximal_count} non-isomorphic blocks)")

# ============================================================
# OPTIONAL: Uncomment below to generate visualizations
# ============================================================
"""
import matplotlib.pyplot as plt

if len(blocks) > 0:
    print("\nGenerating visualizations...")

    # Combined view
    num_blocks = len(blocks)
    cols = 3
    rows = (num_blocks + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(12, 4*rows))
    if num_blocks == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for i, block in enumerate(blocks):
        ax = axes[i]
        pos = nx.planar_layout(block)
        nx.draw(block, pos, ax=ax, with_labels=True,
                node_color='lightblue', node_size=600,
                font_weight='bold', font_size=12)

        info = get_block_info(block)
        ax.set_title(f'Block {i+1}: {info["edges"]} edges\\n{info["degree_sequence"]}')

    # Hide unused subplots
    for i in range(num_blocks, len(axes)):
        axes[i].axis('off')

    plt.suptitle(f'Triangular Blocks on {n} Vertices Avoiding Custom Subgraph',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('my_custom_results.png', dpi=200, bbox_inches='tight')
    print("Visualization saved to: my_custom_results.png")
"""
