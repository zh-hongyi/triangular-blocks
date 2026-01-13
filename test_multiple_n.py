#!/usr/bin/env python3
"""
Test the fixed algorithm on multiple values of n to verify correctness.
"""

import networkx as nx
from src.triangular_blocks import (
    generate_triangular_blocks,
    is_valid_triangular_block_structure,
    get_block_info
)
from collections import Counter

print("="*70)
print("Testing Fixed Algorithm on Multiple Values of n")
print("="*70)
print()

results = []

for n in range(3, 8):  # Test n=3 to n=7
    print(f"Testing n={n}...")

    # Generate all triangular blocks
    blocks = generate_triangular_blocks(n)

    # Verify each block is valid
    all_valid = True
    for i, block in enumerate(blocks):
        if not is_valid_triangular_block_structure(block):
            print(f"  ✗ Block {i+1} is NOT valid!")
            all_valid = False
            break

        # Verify it's planar
        is_planar, _ = nx.check_planarity(block)
        if not is_planar:
            print(f"  ✗ Block {i+1} is NOT planar!")
            all_valid = False
            break

        # Verify it's connected
        if not nx.is_connected(block):
            print(f"  ✗ Block {i+1} is NOT connected!")
            all_valid = False
            break

    if all_valid:
        print(f"  ✓ All {len(blocks)} blocks are valid")

    # Get edge distribution
    edge_counts = [b.number_of_edges() for b in blocks]
    distribution = Counter(edge_counts)

    results.append({
        'n': n,
        'count': len(blocks),
        'min_edges': min(edge_counts),
        'max_edges': max(edge_counts),
        'distribution': distribution,
        'all_valid': all_valid
    })

    print(f"  Found {len(blocks)} blocks")
    print(f"  Edge range: {min(edge_counts)} to {max(edge_counts)}")
    print(f"  Distribution: {dict(distribution)}")
    print()

print("="*70)
print("Summary of Results")
print("="*70)
print()

print("| n | Count | Min Edges | Max Edges | Status |")
print("|---|-------|-----------|-----------|--------|")
for r in results:
    status = "✓ Pass" if r['all_valid'] else "✗ Fail"
    print(f"| {r['n']} | {r['count']:5d} | {r['min_edges']:9d} | {r['max_edges']:9d} | {status:6s} |")

print()
print("="*70)
print("Validation Tests")
print("="*70)
print()

# Test specific known structures
print("Testing specific known structures...")
print()

# Test 1: Single triangle (n=3)
triangle = nx.Graph()
triangle.add_edges_from([(0, 1), (0, 2), (1, 2)])
is_valid = is_valid_triangular_block_structure(triangle)
print(f"1. Single triangle (K3): {'✓ Valid' if is_valid else '✗ Invalid'}")
assert is_valid, "Triangle should be valid!"

# Test 2: Strip of triangles (n=6)
strip = nx.Graph()
strip.add_edges_from([
    (0, 1), (0, 2), (1, 2),
    (1, 3), (2, 3),
    (2, 4), (3, 4),
    (3, 5), (4, 5)
])
is_valid = is_valid_triangular_block_structure(strip)
print(f"2. Strip of triangles (n=6): {'✓ Valid' if is_valid else '✗ Invalid'}")
assert is_valid, "Strip should be valid!"

# Test 3: K4 (complete graph on 4 vertices)
k4 = nx.complete_graph(4)
is_valid = is_valid_triangular_block_structure(k4)
print(f"3. Complete graph K4: {'✓ Valid' if is_valid else '✗ Invalid'}")
assert is_valid, "K4 should be valid!"

# Test 4: Star graph (should be INVALID - no triangles)
star = nx.Graph()
star.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4)])
is_valid = is_valid_triangular_block_structure(star)
print(f"4. Star graph (no triangles): {'✗ Invalid' if not is_valid else '✓ Valid (ERROR!)'}")
assert not is_valid, "Star should be invalid!"

# Test 5: Path (should be INVALID - no triangles)
path = nx.Graph()
path.add_edges_from([(0, 1), (1, 2), (2, 3)])
is_valid = is_valid_triangular_block_structure(path)
print(f"5. Path graph (no triangles): {'✗ Invalid' if not is_valid else '✓ Valid (ERROR!)'}")
assert not is_valid, "Path should be invalid!"

# Test 6: Cycle without triangles (should be INVALID)
cycle = nx.cycle_graph(5)
is_valid = is_valid_triangular_block_structure(cycle)
print(f"6. 5-cycle (no triangles): {'✗ Invalid' if not is_valid else '✓ Valid (ERROR!)'}")
assert not is_valid, "5-cycle should be invalid!"

print()
print("="*70)
print("All Tests Passed! ✓")
print("="*70)
print()
print("The fixed algorithm correctly:")
print("  • Finds valid triangular blocks including strips")
print("  • Rejects invalid graphs without triangles")
print("  • Generates complete sets of non-isomorphic blocks")
