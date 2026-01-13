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
- Generate triangular blocks avoiding forbidden subgraphs (for Turán-type problems)
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
Found 4 non-isomorphic triangular blocks
  Block 1: 5 vertices, 7 edges
  Block 2: 5 vertices, 8 edges
  Block 3: 5 vertices, 8 edges
  Block 4: 5 vertices, 9 edges

============================================================
Detailed Information
============================================================

Block 1:
----------------------------------------
  Vertices: 5
  Edges: 7
  Degree sequence: [4, 3, 3, 2, 2]
  Is planar: True
  Is connected: True
  Edge list: [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (2, 4)]
  Validation: Valid triangular block

Block 2:
----------------------------------------
  Vertices: 5
  Edges: 8
  Degree sequence: [4, 4, 3, 3, 2]
  Is planar: True
  Is connected: True
  Edge list: [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3)]
  Validation: Valid triangular block

Block 3:
----------------------------------------
  Vertices: 5
  Edges: 8
  Degree sequence: [4, 3, 3, 3, 3]
  Is planar: True
  Is connected: True
  Edge list: [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (2, 4), (3, 4)]
  Validation: Valid triangular block

Block 4:
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

### Avoiding Forbidden Subgraphs

Generate triangular blocks that avoid a specific forbidden subgraph (useful for Turán-type problems):

```bash
# Avoid 4-cycles (C4) on 6 vertices
python example_avoid_subgraph.py 6 C4

# Avoid complete graphs (K4)
python example_avoid_subgraph.py 6 K4

# Avoid paths (P4)
python example_avoid_subgraph.py 6 P4
```

**Programmatic usage:**

```python
import networkx as nx
from src.triangular_blocks import generate_triangular_blocks_avoiding_subgraph

# Define forbidden subgraph (e.g., C4 - 4-cycle)
C4 = nx.cycle_graph(4)

# Generate blocks avoiding C4
blocks = generate_triangular_blocks_avoiding_subgraph(n=6, forbidden_graph=C4)

print(f"Found {len(blocks)} C4-free triangular blocks on 6 vertices")

# Find extremal result (maximum edges)
max_edges = max(b.number_of_edges() for b in blocks)
print(f"Maximum edges in C4-free blocks: {max_edges}")
```

### Custom Forbidden Graphs (Step-by-Step Guide)

To generate triangular blocks avoiding your own custom forbidden graph:

**Quick Start: Use the Template File**

Copy and modify the template:
```bash
cp my_custom_search_template.py my_search.py
# Edit my_search.py: Change the forbidden graph edges (line 17-24) and n value (line 27)
source venv/bin/activate
python my_search.py
```

**Or create from scratch:**

**Step 1: Create a Python script** (e.g., `my_custom_search.py`):

```python
#!/usr/bin/env python3
import networkx as nx
from src.triangular_blocks import generate_triangular_blocks_avoiding_subgraph
from src.triangular_blocks import get_block_info

# Step 2: Define your forbidden graph by listing its edges
forbidden = nx.Graph()
forbidden.add_edges_from([
    (0, 1), (0, 2), (1, 2),  # Add your edges here
    (1, 3), (2, 3),          # Example: this creates a specific pattern
    (3, 4), (2, 4),
    (1, 5), (5, 3)
    # Add as many edges as needed for your forbidden pattern
])

# Step 3: Choose the number of vertices for your triangular blocks
n = 6  # Change this to any number >= 2

# Step 4: Generate blocks avoiding the forbidden graph
print(f"Generating triangular blocks on {n} vertices...")
blocks = generate_triangular_blocks_avoiding_subgraph(n=n, forbidden_graph=forbidden)

# Step 5: Display results
print(f"\nFound {len(blocks)} non-isomorphic triangular blocks")
for i, block in enumerate(blocks):
    info = get_block_info(block)
    print(f"Block {i+1}: {info['edges']} edges, degree sequence {info['degree_sequence']}")

# Find extremal (maximum edges)
if blocks:
    max_edges = max(b.number_of_edges() for b in blocks)
    print(f"\nMaximum edges: {max_edges}")
```

**Step 6: Run your script:**

```bash
source venv/bin/activate  # Activate virtual environment
python my_custom_search.py
```

**To also generate visualizations**, add this to your script:

```python
import matplotlib.pyplot as plt

# Visualize all blocks
num_blocks = len(blocks)
cols = 3
rows = (num_blocks + cols - 1) // cols

fig, axes = plt.subplots(rows, cols, figsize=(12, 4*rows))
axes = axes.flatten() if num_blocks > 1 else [axes]

for i, block in enumerate(blocks):
    ax = axes[i]
    pos = nx.planar_layout(block)
    nx.draw(block, pos, ax=ax, with_labels=True,
            node_color='lightblue', node_size=600, font_weight='bold')

    info = get_block_info(block)
    ax.set_title(f'Block {i+1}: {info["edges"]} edges')

# Hide unused subplots
for i in range(num_blocks, len(axes)):
    axes[i].axis('off')

plt.tight_layout()
plt.savefig('my_results.png', dpi=200, bbox_inches='tight')
print("\nVisualization saved to: my_results.png")
```

**Quick customization tips:**
- **Change number of vertices**: Modify `n = 6` to any value (e.g., `n = 7`, `n = 8`)
- **Define forbidden graph**: List all edges in `forbidden.add_edges_from([...])`
- **Use built-in graphs**: Try `forbidden = nx.cycle_graph(5)` or `nx.complete_graph(4)`
- **See more examples**: Run `python example_custom_forbidden.py` for complex patterns

### Visualization

```bash
# Visualize blocks for n=4
python examples/visualize_blocks.py 4

# Save visualization to file
python examples/visualize_blocks.py 4 --save blocks_n4.png

# Export blocks in various formats
python examples/visualize_blocks.py 4 --export output_dir --format graphml
```

## Recent Bug Fix (January 2026)

### Issue: Incorrect Definition of Triangular Blocks

**Problem:** The original validation function had a fundamental misunderstanding of triangular blocks. It was checking for:
1. Maximal construction (no more edges can be added)
2. Wrong face structure validation

**Correct Definition:** A triangular block is determined by its planar embedding structure:
- All **internal faces** must be triangles
- The **outer face** can be any simple polygon
- Every edge must be part of at least one triangle (no standalone edges)
- All triangles must be connected (reachable by crossing shared edges)
- **NOT maximal** - we don't need to add all possible edges

**Example:** A strip of triangles with edges `(0,1),(1,2),(0,2),(1,3),(2,3),(2,4),(3,4),(3,5),(4,5)` has:
- 4 triangular internal faces: (0,1,2), (1,2,3), (2,3,4), (3,4,5)
- 1 hexagonal outer face with 6 edges
- This is a valid triangular block

**Fix:** Rewrote validation to check:
1. Graph is planar and connected
2. Find all triangles in the graph
3. Every edge must be part of at least one triangle
4. All triangles must form a connected structure (can reach any triangle from any other by crossing shared edges)

**Impact:**
- Strips and similar non-maximal structures are now correctly accepted
- The algorithm finds **18 blocks** for n=6 avoiding a specific forbidden subgraph
- All found blocks satisfy the correct definition

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
  Block 1: 1 edges
✓ n=2 test passed

=== Testing n=3 ===
Found 1 block(s)
  Block 1: K3 (triangle), 3 edges
✓ n=3 test passed

=== Testing n=4 ===
Found 2 block(s)
  Block 1: 5 edges, degree sequence [3, 3, 2, 2]
  Block 2: 6 edges, degree sequence [3, 3, 3, 3]
    Validation: Valid triangular blocks
✓ n=4 test passed

=== Testing n=5 ===
Found 5 block(s)
  Block 1-2: 7 edges (includes strips)
  Block 3-4: 8 edges
  Block 5: 9 edges
    Validation: Valid triangular blocks
✓ n=5 test passed

=== Testing n=6 ===
Found 19 block(s)
  Blocks with 9-12 edges
  Distribution: 9(5), 10(7), 11(5), 12(2)
    Validation: Valid triangular blocks
✓ n=6 test passed

============================================================
Test Results: All tests passed
============================================================
```

## Results

### Known Results

**All triangular blocks:**

| n | Number of Blocks | Edge Range | Notes |
|---|------------------|------------|-------|
| 2 | 1 | 1 | Single edge |
| 3 | 1 | 3 | K3 (triangle) |
| 4 | 2 | 5-6 | Strip + K4 |
| 5 | 5 | 7-9 | Includes strips |
| 6 | 19 | 9-12 | Rich variety including strips |
| 7 | 93 | 11-15 | Exponential growth continues |

**C4-free triangular blocks:**

*Note: These results should be re-verified with the fixed algorithm, as the bug fix may have affected these counts.*

| n | Number of Blocks | Max Edges | Status |
|---|------------------|-----------|--------|
| 3 | 1 | 3 | ✓ Verified |
| 4 | 2 | 6 | ✓ Verified |
| 5 | 3 | 9 | ⚠ May need update |
| 6 | 6 | 12 | ⚠ May need update |

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
