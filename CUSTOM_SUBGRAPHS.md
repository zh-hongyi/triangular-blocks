# Using Custom Forbidden Subgraphs

This guide shows you how to test triangular blocks with **any** custom forbidden subgraph.

## Quick Start

### 1. Using Predefined Graph Types (Command-Line)

```bash
# Avoid cycles
python example_avoid_subgraph.py 6 C4     # 4-cycle
python example_avoid_subgraph.py 6 C5     # 5-cycle

# Avoid complete graphs
python example_avoid_subgraph.py 6 K3     # Triangle
python example_avoid_subgraph.py 6 K4     # K4

# Avoid paths
python example_avoid_subgraph.py 6 P3     # 3-path
python example_avoid_subgraph.py 6 P4     # 4-path

# Avoid complete bipartite
python example_avoid_subgraph.py 6 K2_3   # K_{2,3}
python example_avoid_subgraph.py 6 K3_3   # K_{3,3}
```

**Supported types:** Kn (complete), Cn (cycles), Pn (paths), Km_n (complete bipartite)

### 2. Using Custom Graphs (Python API)

Create any NetworkX graph and pass it to `generate_triangular_blocks_avoiding_subgraph()`:

```python
import networkx as nx
from src.triangular_blocks import generate_triangular_blocks_avoiding_subgraph

# Define your forbidden graph
forbidden = nx.Graph()
forbidden.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])  # 4-cycle

# Generate blocks avoiding it
blocks = generate_triangular_blocks_avoiding_subgraph(n=6, forbidden_graph=forbidden)

print(f"Found {len(blocks)} blocks")
```

## Methods to Create Custom Forbidden Graphs

### Method 1: Add Edges One by One

```python
G = nx.Graph()
G.add_edge(0, 1)
G.add_edge(1, 2)
G.add_edge(2, 0)  # Triangle
```

### Method 2: Add from Edge List

```python
G = nx.Graph()
G.add_edges_from([
    (0, 1), (1, 2), (2, 3),  # Path
    (3, 0),                   # Close to cycle
    (1, 3)                    # Add diagonal
])
```

### Method 3: Use NetworkX Built-in Generators

```python
# Common graphs
G = nx.complete_graph(4)                    # K4
G = nx.cycle_graph(5)                       # C5
G = nx.path_graph(4)                        # P4
G = nx.star_graph(3)                        # Star K_{1,3}
G = nx.complete_bipartite_graph(2, 3)       # K_{2,3}

# Special graphs
G = nx.wheel_graph(5)                       # Wheel W4
G = nx.ladder_graph(3)                      # Ladder
G = nx.petersen_graph()                     # Petersen graph

# Disjoint unions
G = nx.disjoint_union(nx.cycle_graph(3), nx.cycle_graph(3))  # Two triangles
```

### Method 4: Modify Existing Graphs

```python
# Start with K4
G = nx.complete_graph(4)
# Remove one edge to create diamond
G.remove_edge(0, 3)

# Or start from scratch
diamond = nx.Graph()
diamond.add_edges_from([(0,1), (0,2), (0,3), (1,2), (1,3)])  # K4 - e
```

## Example Custom Graphs

### Diamond (K4 minus one edge)

```python
diamond = nx.Graph()
diamond.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])

blocks = generate_triangular_blocks_avoiding_subgraph(5, diamond)
```

### Paw (Triangle with pendant edge)

```python
paw = nx.Graph()
paw.add_edges_from([
    (0, 1), (1, 2), (2, 0),  # Triangle
    (0, 3)                    # Pendant
])

blocks = generate_triangular_blocks_avoiding_subgraph(6, paw)
```

### House (C5 with one chord)

```python
house = nx.Graph()
house.add_edges_from([
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),  # 5-cycle
    (0, 2)                                    # Chord
])

blocks = generate_triangular_blocks_avoiding_subgraph(6, house)
```

### Theta Graph

```python
theta = nx.Graph()
theta.add_edges_from([
    (0, 1),                    # Direct edge
    (0, 2), (2, 3), (3, 1),   # Path 1
    (0, 4), (4, 5), (5, 1),   # Path 2
])

blocks = generate_triangular_blocks_avoiding_subgraph(7, theta)
```

### Bowtie (Two triangles sharing a vertex)

```python
bowtie = nx.Graph()
bowtie.add_edges_from([
    (0, 1), (0, 2), (1, 2),   # Triangle 1
    (2, 3), (2, 4), (3, 4)    # Triangle 2
])

blocks = generate_triangular_blocks_avoiding_subgraph(6, bowtie)
```

## Complete Example Script

```python
#!/usr/bin/env python3
import networkx as nx
from src.triangular_blocks import generate_triangular_blocks_avoiding_subgraph

# Define your custom forbidden graph
my_forbidden = nx.Graph()
my_forbidden.add_edges_from([
    (0, 1), (1, 2), (2, 3), (3, 0),  # 4-cycle
    (0, 2)                            # Add diagonal
])

# Set parameters
n = 6  # Number of vertices

# Generate blocks
print(f"Forbidden: {my_forbidden.number_of_nodes()} vertices, "
      f"{my_forbidden.number_of_edges()} edges")
print(f"Edges: {sorted(my_forbidden.edges())}")
print()

blocks = generate_triangular_blocks_avoiding_subgraph(n, my_forbidden)

# Results
print(f"Found {len(blocks)} non-isomorphic blocks on {n} vertices")

if blocks:
    max_edges = max(b.number_of_edges() for b in blocks)
    print(f"Maximum edges: {max_edges}")
    
    for i, block in enumerate(blocks):
        print(f"Block {i+1}: {block.number_of_edges()} edges")
```

## Testing Examples

Test predefined types:
```bash
./venv/bin/python example_avoid_subgraph.py 6 C4
./venv/bin/python example_avoid_subgraph.py 6 K4
./venv/bin/python example_avoid_subgraph.py 6 P4
./venv/bin/python example_avoid_subgraph.py 6 K2_3
```

Test custom examples:
```bash
./venv/bin/python quick_custom_demo.py
./venv/bin/python example_custom_forbidden.py
./venv/bin/python demo.py
```

## Key Points

1. **Any NetworkX Graph works** - The forbidden graph can be any `nx.Graph` object
2. **Subgraph isomorphism** - The algorithm checks if the forbidden graph appears anywhere as a subgraph
3. **Vertex labels don't matter** - Only the structure matters, not the vertex numbering
4. **Early pruning** - If a partial block contains the forbidden subgraph, that branch is abandoned

## NetworkX Resources

- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [Graph Generators](https://networkx.org/documentation/stable/reference/generators.html)
- [Classic Graphs](https://networkx.org/documentation/stable/reference/generators.html#classic)

## Notes

- For large forbidden graphs, the algorithm may be slower due to subgraph isomorphism checking
- The algorithm guarantees finding ALL non-isomorphic blocks avoiding the pattern
- Works with both connected and disconnected forbidden graphs
