#!/usr/bin/env python3
"""
Simple example demonstrating triangular block generation.

Usage:
    python example.py <n>

where n is the number of vertices.
"""

import sys
from src.triangular_blocks import generate_triangular_blocks_verbose, get_block_info
from src.validation import validate_triangular_block


def main():
    if len(sys.argv) < 2:
        print("Usage: python example.py <n>")
        print("  where n is the number of vertices (e.g., 3, 4, 5)")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Error: n must be an integer")
        sys.exit(1)

    if n < 2:
        print("Error: n must be at least 2")
        sys.exit(1)

    print("="*60)
    print(f"Generating Triangular Blocks with {n} Vertices")
    print("="*60)
    print()

    # Generate blocks
    blocks = generate_triangular_blocks_verbose(n, verbose=True)

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
    print(f"Summary: Found {len(blocks)} non-isomorphic triangular block(s)")
    print("="*60)


if __name__ == '__main__':
    main()
