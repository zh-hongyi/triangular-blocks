"""
Visualization utilities for triangular blocks.

Provides functions to visualize generated triangular blocks using matplotlib.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import networkx as nx
import matplotlib.pyplot as plt
from src.triangular_blocks import generate_triangular_blocks, get_block_info


def visualize_blocks(blocks, n, save_path=None):
    """
    Visualize all generated triangular blocks.

    Args:
        blocks: List of networkx Graph objects
        n: Number of vertices
        save_path: Optional path to save the figure
    """
    num_blocks = len(blocks)

    if num_blocks == 0:
        print("No blocks to visualize")
        return

    # Calculate grid layout
    cols = min(5, num_blocks)
    rows = (num_blocks + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(3*cols, 3*rows))

    # Handle single subplot case
    if num_blocks == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for i, block in enumerate(blocks):
        ax = axes[i]

        # Try to use planar layout if possible
        try:
            is_planar, embedding = nx.check_planarity(block)
            if is_planar:
                pos = nx.planar_layout(block)
            else:
                pos = nx.spring_layout(block, seed=42)
        except:
            pos = nx.spring_layout(block, seed=42)

        # Draw the graph
        nx.draw(block, pos, ax=ax,
                with_labels=True,
                node_color='lightblue',
                node_size=500,
                font_size=10,
                font_weight='bold',
                edge_color='gray',
                width=2)

        # Add title with info
        info = get_block_info(block)
        ax.set_title(f'Block {i+1}\n{info["edges"]} edges, deg seq {info["degree_sequence"]}',
                     fontsize=9)

    # Hide unused subplots
    for i in range(num_blocks, len(axes)):
        axes[i].axis('off')

    plt.suptitle(f'All Non-Isomorphic Triangular Blocks with {n} Vertices',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Figure saved to {save_path}")

    plt.show()


def visualize_single_block(block, title=None):
    """
    Visualize a single triangular block with detailed information.

    Args:
        block: networkx Graph
        title: Optional title for the plot
    """
    fig, ax = plt.subplots(figsize=(8, 8))

    # Try planar layout
    try:
        is_planar, embedding = nx.check_planarity(block)
        if is_planar:
            pos = nx.planar_layout(block)
        else:
            pos = nx.spring_layout(block, seed=42)
    except:
        pos = nx.spring_layout(block, seed=42)

    # Draw graph
    nx.draw(block, pos, ax=ax,
            with_labels=True,
            node_color='lightblue',
            node_size=800,
            font_size=12,
            font_weight='bold',
            edge_color='gray',
            width=2)

    # Get and display info
    info = get_block_info(block)

    info_text = f"Vertices: {info['vertices']}\n"
    info_text += f"Edges: {info['edges']}\n"
    info_text += f"Degree Sequence: {info['degree_sequence']}\n"
    info_text += f"Planar: {info['is_planar']}\n"
    info_text += f"Connected: {info['is_connected']}"

    ax.text(0.02, 0.98, info_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    else:
        ax.set_title(f'Triangular Block with {info["vertices"]} Vertices',
                     fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.show()


def export_blocks(blocks, n, output_dir='.', format='graphml'):
    """
    Export triangular blocks to files.

    Args:
        blocks: List of networkx Graph objects
        n: Number of vertices
        output_dir: Directory to save files
        format: File format ('graphml', 'edgelist', 'adjlist', 'gexf')
    """
    os.makedirs(output_dir, exist_ok=True)

    for i, block in enumerate(blocks):
        filename = os.path.join(output_dir, f'block_n{n}_{i+1}')

        if format == 'graphml':
            nx.write_graphml(block, filename + '.graphml')
        elif format == 'edgelist':
            nx.write_edgelist(block, filename + '.edgelist')
        elif format == 'adjlist':
            nx.write_adjlist(block, filename + '.adjlist')
        elif format == 'gexf':
            nx.write_gexf(block, filename + '.gexf')
        else:
            print(f"Unknown format: {format}")
            return

    print(f"Exported {len(blocks)} blocks to {output_dir} in {format} format")


def main():
    """Example usage of visualization functions."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Visualize triangular blocks for a given n')
    parser.add_argument('n', type=int, help='Number of vertices')
    parser.add_argument('--save', type=str, help='Path to save figure',
                        default=None)
    parser.add_argument('--export', type=str, help='Directory to export blocks',
                        default=None)
    parser.add_argument('--format', type=str, help='Export format',
                        choices=['graphml', 'edgelist', 'adjlist', 'gexf'],
                        default='graphml')

    args = parser.parse_args()

    print(f"Generating triangular blocks with {args.n} vertices...")
    blocks = generate_triangular_blocks(args.n)
    print(f"Found {len(blocks)} non-isomorphic blocks\n")

    # Print info
    for i, block in enumerate(blocks):
        info = get_block_info(block)
        print(f"Block {i+1}: {info['vertices']} vertices, {info['edges']} edges, "
              f"degree sequence {info['degree_sequence']}")

    # Visualize
    visualize_blocks(blocks, args.n, save_path=args.save)

    # Export if requested
    if args.export:
        export_blocks(blocks, args.n, output_dir=args.export, format=args.format)


if __name__ == '__main__':
    main()
