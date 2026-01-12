"""
Unit tests for triangular block generation.

Tests the algorithm against known results and validates properties.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import networkx as nx
from src.triangular_blocks import generate_triangular_blocks, get_block_info
from src.validation import validate_triangular_block


def test_n_equals_2():
    """Test generation for n=2 (single edge)."""
    print("\n=== Testing n=2 ===")
    blocks = generate_triangular_blocks(2)

    print(f"Found {len(blocks)} block(s)")
    assert len(blocks) == 1, f"Expected 1 block for n=2, got {len(blocks)}"

    block = blocks[0]
    assert block.number_of_nodes() == 2
    assert block.number_of_edges() == 1

    print("✓ n=2 test passed")


def test_n_equals_3():
    """Test generation for n=3 (should be single triangle K3)."""
    print("\n=== Testing n=3 ===")
    blocks = generate_triangular_blocks(3)

    print(f"Found {len(blocks)} block(s)")
    assert len(blocks) == 1, f"Expected 1 block for n=3, got {len(blocks)}"

    block = blocks[0]
    assert block.number_of_nodes() == 3
    assert block.number_of_edges() == 3

    # Verify it's K3 (complete graph on 3 vertices)
    for u in range(3):
        for v in range(u+1, 3):
            assert block.has_edge(u, v), f"Missing edge ({u},{v})"

    print("  Block 1: K3 (triangle)")
    print("✓ n=3 test passed")


def test_n_equals_4():
    """Test generation for n=4."""
    print("\n=== Testing n=4 ===")
    blocks = generate_triangular_blocks(4)

    print(f"Found {len(blocks)} block(s)")

    # Print info about each block
    for i, block in enumerate(blocks):
        info = get_block_info(block)
        print(f"  Block {i+1}: {info['edges']} edges, "
              f"degree sequence {info['degree_sequence']}")

        # Validate each block
        is_valid, msg = validate_triangular_block(block)
        print(f"    Validation: {msg}")
        assert is_valid, f"Block {i+1} failed validation: {msg}"

    print("✓ n=4 test passed")


def test_n_equals_5():
    """Test generation for n=5."""
    print("\n=== Testing n=5 ===")
    blocks = generate_triangular_blocks(5)

    print(f"Found {len(blocks)} block(s)")

    for i, block in enumerate(blocks):
        info = get_block_info(block)
        print(f"  Block {i+1}: {info['edges']} edges, "
              f"degree sequence {info['degree_sequence']}")

        # Validate each block
        is_valid, msg = validate_triangular_block(block)
        print(f"    Validation: {msg}")
        assert is_valid, f"Block {i+1} failed validation: {msg}"

    print("✓ n=5 test passed")


def test_block_properties():
    """Test that all generated blocks satisfy required properties."""
    print("\n=== Testing Block Properties ===")

    for n in [3, 4, 5]:
        print(f"\nTesting properties for n={n}")
        blocks = generate_triangular_blocks(n)

        for i, block in enumerate(blocks):
            # Test connectivity
            assert nx.is_connected(block), \
                f"Block {i+1} for n={n} is not connected"

            # Test planarity
            is_planar, _ = nx.check_planarity(block)
            assert is_planar, \
                f"Block {i+1} for n={n} is not planar"

            # Test vertex count
            assert block.number_of_nodes() == n, \
                f"Block {i+1} for n={n} has wrong number of vertices"

            # Test edge count is reasonable (at least n-1 for connectivity)
            assert block.number_of_edges() >= n-1, \
                f"Block {i+1} for n={n} has too few edges"

    print("✓ All property tests passed")


def test_no_isomorphic_duplicates():
    """Test that no isomorphic duplicates are generated."""
    print("\n=== Testing for Isomorphic Duplicates ===")

    for n in [3, 4, 5]:
        print(f"\nTesting n={n}")
        blocks = generate_triangular_blocks(n)

        # Check pairwise for isomorphisms
        for i in range(len(blocks)):
            for j in range(i+1, len(blocks)):
                assert not nx.is_isomorphic(blocks[i], blocks[j]), \
                    f"Blocks {i+1} and {j+1} for n={n} are isomorphic"

        print(f"  No duplicates found among {len(blocks)} block(s)")

    print("✓ No isomorphic duplicates test passed")


def run_all_tests():
    """Run all test functions."""
    print("="*60)
    print("Triangular Block Generation - Test Suite")
    print("="*60)

    tests = [
        test_n_equals_2,
        test_n_equals_3,
        test_n_equals_4,
        test_n_equals_5,
        test_block_properties,
        test_no_isomorphic_duplicates
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n✗ {test_func.__name__} FAILED:")
            print(f"  {str(e)}")
            failed += 1

    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)

    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
