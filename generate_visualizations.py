#!/usr/bin/env python3
"""
Generate clean visualizations for triangular blocks avoiding the custom forbidden graph.
Only generates essential, publication-ready figures.
"""

import networkx as nx
import matplotlib.pyplot as plt
from src.triangular_blocks import (
    generate_triangular_blocks_avoiding_subgraph,
    get_block_info
)
from src.isomorphism import get_canonical_form
from collections import Counter

# Define the forbidden graph (6 vertices, 9 edges)
forbidden = nx.Graph()
forbidden.add_edges_from([
    (0, 1), (0, 2), (1, 2),
    (1, 3), (2, 3),
    (3, 4), (2, 4),
    (1, 5), (5, 3)
])

print("="*70)
print("Generating Triangular Blocks (n=6, Avoiding Forbidden Subgraph)")
print("="*70)
print()

# Generate blocks
print("Computing all triangular blocks...")
blocks = generate_triangular_blocks_avoiding_subgraph(n=6, forbidden_graph=forbidden)
print(f"Found {len(blocks)} non-isomorphic blocks\n")

# Identify the strip
strip = nx.Graph()
strip.add_edges_from([
    (0, 1), (1, 2), (0, 2),
    (1, 3), (2, 3),
    (2, 4), (3, 4),
    (3, 5), (4, 5)
])

strip_canonical = get_canonical_form(strip)
strip_idx = None
for i, block in enumerate(blocks):
    if get_canonical_form(block) == strip_canonical:
        strip_idx = i
        break

# ==============================================================================
# Figure 1: All Blocks Grid
# ==============================================================================
print("Generating Figure 1: All blocks overview...")

num_blocks = len(blocks)
cols = 4
rows = (num_blocks + cols - 1) // cols

fig = plt.figure(figsize=(14, 3.5*rows))

for i, block in enumerate(blocks):
    ax = plt.subplot(rows, cols, i+1)

    # Use planar layout
    try:
        is_planar, embedding = nx.check_planarity(block)
        if is_planar:
            pos = nx.planar_layout(block)
        else:
            pos = nx.spring_layout(block, seed=42)
    except:
        pos = nx.spring_layout(block, seed=42)

    # Highlight the strip
    is_strip = (i == strip_idx)
    node_color = '#ff6b6b' if is_strip else '#4dabf7'
    edge_color = '#c92a2a' if is_strip else '#495057'
    width = 3 if is_strip else 2.5

    # Draw
    nx.draw(block, pos, ax=ax,
            with_labels=True,
            node_color=node_color,
            node_size=500,
            font_size=11,
            font_weight='bold',
            edge_color=edge_color,
            width=width,
            font_color='white')

    # Title
    info = get_block_info(block)
    title = f'Block {i+1}: {info["edges"]} edges'
    if is_strip:
        title = f'Block {i+1}: {info["edges"]} edges ★'

    ax.set_title(title, fontsize=10, fontweight='bold',
                 color='#c92a2a' if is_strip else 'black')
    ax.axis('off')

plt.suptitle(f'Triangular Blocks on 6 Vertices (n={len(blocks)})',
             fontsize=15, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('all_blocks.png', dpi=300, bbox_inches='tight', facecolor='white')
print("  Saved: all_blocks.png")

# ==============================================================================
# Figure 2: Statistics Summary
# ==============================================================================
print("Generating Figure 2: Statistics and distribution...")

edge_counts = [b.number_of_edges() for b in blocks]
distribution = Counter(edge_counts)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Left: Distribution bar chart
ax1 = axes[0]
edges = sorted(distribution.keys())
counts = [distribution[e] for e in edges]
bars = ax1.bar(edges, counts, color='#4dabf7', edgecolor='black', linewidth=1.5)

ax1.set_xlabel('Number of Edges', fontsize=13, fontweight='bold')
ax1.set_ylabel('Number of Blocks', fontsize=13, fontweight='bold')
ax1.set_title('Edge Distribution', fontsize=14, fontweight='bold')
ax1.set_xticks(edges)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.set_axisbelow(True)

# Add count labels
for bar, count in zip(bars, counts):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{int(count)}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# Right: Summary information
ax2 = axes[1]
ax2.axis('off')

summary_text = "SUMMARY\n" + "="*50 + "\n\n"
summary_text += f"Vertices: 6\n"
summary_text += f"Total blocks found: {len(blocks)}\n"
summary_text += f"Edge range: {min(edge_counts)} - {max(edge_counts)}\n\n"
summary_text += "Distribution:\n"
for e in sorted(distribution.keys()):
    summary_text += f"  {e} edges: {distribution[e]:2d} blocks\n"

if strip_idx is not None:
    summary_text += f"\n" + "="*50 + "\n"
    summary_text += f"STRIP FOUND: Block #{strip_idx + 1}\n"
    summary_text += "="*50 + "\n"
    info = get_block_info(blocks[strip_idx])
    summary_text += f"Edges: {info['edges']}\n"
    summary_text += f"Degree sequence: {info['degree_sequence']}\n"
    summary_text += f"Edge list:\n  {sorted(blocks[strip_idx].edges())}\n"

summary_text += f"\n" + "="*50 + "\n"
summary_text += "Forbidden subgraph:\n"
summary_text += f"  Vertices: {forbidden.number_of_nodes()}\n"
summary_text += f"  Edges: {forbidden.number_of_edges()}\n"

ax2.text(0.1, 0.5, summary_text,
         ha='left', va='center',
         fontsize=11,
         bbox=dict(boxstyle='round,pad=1', facecolor='#e9ecef', edgecolor='black', linewidth=2),
         family='monospace',
         verticalalignment='center')

plt.suptitle('Triangular Blocks Statistics', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('statistics.png', dpi=200, bbox_inches='tight', facecolor='white')
print("  Saved: statistics.png")

# ==============================================================================
# Figure 3: Strip Detail
# ==============================================================================
if strip_idx is not None:
    print("Generating Figure 3: Strip detail...")

    fig, ax = plt.subplots(figsize=(8, 8))

    strip_block = blocks[strip_idx]

    # Use planar layout
    try:
        is_planar, embedding = nx.check_planarity(strip_block)
        if is_planar:
            pos = nx.planar_layout(strip_block)
        else:
            pos = nx.spring_layout(strip_block, seed=42)
    except:
        pos = nx.spring_layout(strip_block, seed=42)

    # Draw
    nx.draw(strip_block, pos, ax=ax,
            with_labels=True,
            node_color='#ff6b6b',
            node_size=1200,
            font_size=16,
            font_weight='bold',
            edge_color='#c92a2a',
            width=4,
            font_color='white',
            edgecolors='black',
            linewidths=2)

    # Title with details
    info = get_block_info(strip_block)
    title = f'Strip of Triangles (Block #{strip_idx + 1})\n'
    title += f'{info["edges"]} edges, Degree sequence: {info["degree_sequence"]}\n'
    title += f'Edges: {sorted(strip_block.edges())}'

    ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig('strip_detail.png', dpi=200, bbox_inches='tight', facecolor='white')
    print("  Saved: strip_detail.png")

print()
print("="*70)
print("Visualization Complete")
print("="*70)
print("\nGenerated files:")
print("  1. all_blocks.png       - Grid of all blocks (strip highlighted in red)")
print("  2. statistics.png       - Distribution chart and summary")
print("  3. strip_detail.png     - Detailed view of the strip")
print()
