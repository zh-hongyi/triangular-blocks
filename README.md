# Triangular Blocks Generator

Generate all non-isomorphic triangular blocks on n vertices with no repetition and omission.

## Overview

This project implements an algorithm to generate all structurally distinct (non-isomorphic) triangular blocks with exactly n vertices, based on the definition from "Planar Turán Numbers of Triangular Blocks" (Duvivier, Győri, Zhang, 2026).

### Triangular Block Definition

A **triangular block** is a subgraph of a planar graph obtained by:
1. Starting with a list L containing one edge in G
2. Adding edges that share a triangular face with some edge in L
3. Repeating until no more edges can be added; L spans the triangular block

## Features

- Generate all non-isomorphic triangular blocks for a given number of vertices
- Efficient canonical form checking (with optional pynauty support)
- Validation of generated blocks
- Visualization capabilities
- Comprehensive test suite

## Installation

### Basic Installation

```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Optional: Install pynauty for better performance

```bash
# Using pip (may require compilation)
pip install pynauty

# Or using conda
conda install -c conda-forge pynauty
```

## Usage

### Simple Example

```bash
python example.py <n>
```

Where `n` is the number of vertices (e.g., 3, 4, 5).

**Example:**
```bash
python example.py 5
```

**Output:**
```
============================================================
Generating Triangular Blocks with 5 Vertices
============================================================

Generating triangular blocks with 5 vertices...
Found 1 non-isomorphic triangular blocks
  Block 1: 5 vertices, 9 edges

============================================================
Detailed Information
============================================================

Block 1:
----------------------------------------
  Vertices: 5
  Edges: 9
  Degree sequence: [4, 4, 4, 3, 3]
  Is planar: True
  Is connected: True
  Edge list: [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4)]
  Validation: Valid triangular block
```

### Programmatic Usage

```python
from src.triangular_blocks import generate_triangular_blocks, get_block_info
from src.validation import validate_triangular_block

# Generate blocks
blocks = generate_triangular_blocks(n=5)

# Get information about each block
for i, block in enumerate(blocks):
    info = get_block_info(block)
    print(f"Block {i+1}:")
    print(f"  Vertices: {info['vertices']}")
    print(f"  Edges: {info['edges']}")
    print(f"  Degree sequence: {info['degree_sequence']}")

    # Validate
    is_valid, msg = validate_triangular_block(block)
    print(f"  Validation: {msg}")
```

### Visualization

```bash
# Visualize blocks for n=4
python examples/visualize_blocks.py 4

# Save visualization to file
python examples/visualize_blocks.py 4 --save blocks_n4.png

# Export blocks in various formats
python examples/visualize_blocks.py 4 --export output_dir --format graphml
```

## Algorithm

The implementation uses an **incremental construction** approach:

1. Start with a single edge (0, 1) for symmetry breaking
2. Use BFS/queue-based expansion
3. For each partial block, find all edges that can be added:
   - Edges that form triangles with existing edges, OR
   - Edges that connect to existing vertices (for growth)
   - **Must maintain planarity**
4. Continue until no more edges can be added (maximal blocks)
5. Use canonical form pruning to avoid exploring isomorphic branches
6. Final deduplication of complete blocks

### Key Properties Enforced

- **Connectivity**: All blocks are connected graphs
- **Planarity**: Planarity is checked during edge addition
- **Triangular structure**: Blocks must contain triangular faces
- **Maximality**: No more edges can be added following the rules
- **Uniqueness**: No isomorphic duplicates

## Project Structure

```
triangularblocks/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── triangular_blocks.py     # Core generation algorithm
│   ├── isomorphism.py           # Canonical form checking
│   └── validation.py            # Validation functions
├── tests/
│   └── test_generation.py       # Unit tests
├── examples/
│   └── visualize_blocks.py      # Visualization utilities
├── example.py                   # Simple usage example
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Testing

Run the test suite:

```bash
python tests/test_generation.py
```

**Test Results:**
```
============================================================
Triangular Block Generation - Test Suite
============================================================

=== Testing n=2 ===
Found 1 block(s)
✓ n=2 test passed

=== Testing n=3 ===
Found 1 block(s)
  Block 1: K3 (triangle)
✓ n=3 test passed

=== Testing n=4 ===
Found 1 block(s)
  Block 1: 6 edges, degree sequence [3, 3, 3, 3]
    Validation: Valid triangular block
✓ n=4 test passed

=== Testing n=5 ===
Found 1 block(s)
  Block 1: 9 edges, degree sequence [4, 4, 4, 3, 3]
    Validation: Valid triangular block
✓ n=5 test passed

============================================================
Test Results: 6 passed, 0 failed
============================================================
```

## Results

### Known Results

| n | Number of Blocks | Example Structures |
|---|------------------|-------------------|
| 2 | 1 | Single edge |
| 3 | 1 | K3 (triangle) |
| 4 | 1 | K4 (complete graph on 4 vertices) |
| 5 | 1 | K5 minus one edge (9 edges) |

## References

- Duvivier, J., Győri, E., Zhang, H. (2026). "Planar Turán Numbers of Triangular Blocks". Joint Math Meeting 2026.

## License

This project is part of a research implementation.

## Authors

Implementation by Claude Code, based on mathematical definitions from Duvivier, Győri, and Zhang.

## Notes

- For better performance with larger n, install pynauty for efficient canonical form computation
- The algorithm's runtime grows exponentially with n, but triangular block constraints limit the growth
- Generated blocks are guaranteed to be:
  - Planar
  - Connected
  - Built from triangular faces
  - Non-isomorphic (no structural duplicates)
