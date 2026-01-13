"""
Generate all non-isomorphic triangular blocks on n vertices.

A triangular block is a subgraph of a planar graph obtained by:
1. Starting with one edge
2. Iteratively adding edges that share a triangular face with edges already in the block
3. Continuing until no more edges can be added (maximal)
"""

import networkx as nx
from collections import deque
from .isomorphism import get_canonical_form, remove_isomorphic_duplicates


def generate_triangular_blocks(n):
    """
    Generate all non-isomorphic triangular blocks with exactly n vertices.

    Uses a different approach: generate all possible planar graphs and check
    which ones are valid triangular blocks.

    Args:
        n: Number of vertices (must be >= 2)

    Returns:
        List of networkx Graph objects representing non-isomorphic triangular blocks

    Raises:
        ValueError: If n < 2
    """
    if n < 2:
        raise ValueError("n must be at least 2")

    # For small n, enumerate possible edge sets
    all_blocks = []
    visited_canonical = set()

    # Generate candidates by incremental construction
    # Start with edge (0, 1)
    initial_block = nx.Graph()
    initial_block.add_edge(0, 1)

    queue = deque([initial_block])

    while queue:
        current_block = queue.popleft()

        # Get canonical form for pruning
        canon_form = get_canonical_form(current_block)
        if canon_form in visited_canonical:
            continue
        visited_canonical.add(canon_form)

        # If we have n vertices, check if it's valid and track it
        if len(current_block.nodes()) == n:
            if is_valid_triangular_block_structure(current_block):
                all_blocks.append(current_block)
            # Continue to explore adding more edges (don't stop here!)

        # Try adding edges to grow the graph
        current_edges = set(tuple(sorted(e)) for e in current_block.edges())

        # Try all possible new edges
        for u in range(n):
            for v in range(u + 1, n):
                if (u, v) in current_edges:
                    continue

                # Add this edge and test
                new_block = current_block.copy()
                new_block.add_edge(u, v)

                # Check planarity
                is_planar, _ = nx.check_planarity(new_block)
                if not is_planar:
                    continue

                # Add to queue if still within n vertices
                if len(new_block.nodes()) <= n:
                    queue.append(new_block)

    # Remove isomorphic duplicates
    # Note: Returning ALL valid triangular blocks, not just maximal ones
    unique_blocks = remove_isomorphic_duplicates(all_blocks)

    return unique_blocks


def find_extendable_edges(block, n):
    """
    Find all edges that can be added to the block following triangular block rules.

    An edge (u, v) can be added if it shares a triangular face with an existing edge.
    This means adding (u,v) must either:
    1. Complete a triangle with two existing edges (forms a new triangular face), OR
    2. Be part of a triangular face in the planar embedding that includes an existing edge

    Args:
        block: Current networkx Graph
        n: Maximum number of vertices

    Returns:
        List of tuples (u, v) representing edges that can be added
    """
    extendable = []
    existing_edges = set(block.edges())

    # Normalize existing edges (ensure u < v)
    normalized_existing = set()
    for u, v in existing_edges:
        normalized_existing.add((min(u, v), max(u, v)))

    # Check all possible edges among vertices 0 to n-1
    for u in range(n):
        for v in range(u + 1, n):
            # Skip if edge already exists
            if (u, v) in normalized_existing:
                continue

            # Check if this edge can be added by testing if it forms
            # or shares a triangular face with existing edges
            test_block = block.copy()
            test_block.add_edge(u, v)

            # Must remain planar
            is_planar, _ = nx.check_planarity(test_block)
            if not is_planar:
                continue

            # Check if this edge shares a triangular face with existing edges
            if shares_triangular_face_with_block(block, u, v):
                extendable.append((u, v))

    return extendable


def shares_triangular_face_with_block(block, u, v):
    """
    Check if edge (u, v) would share a triangular face with existing edges.

    An edge shares a triangular face if there exists a vertex w such that
    both (u, w) and (v, w) are already in the block, meaning (u, v, w)
    forms a triangular face where (u,v) is the new edge.

    Args:
        block: Current networkx Graph
        u: First vertex of potential edge
        v: Second vertex of potential edge

    Returns:
        Boolean indicating if the edge shares a triangular face
    """
    # If block has no edges, only allow if it's the starting edge
    if block.number_of_edges() == 0:
        return True

    # Get neighbors of u and v in the block
    u_neighbors = set(block.neighbors(u)) if u in block.nodes() else set()
    v_neighbors = set(block.neighbors(v)) if v in block.nodes() else set()

    # Find common neighbors (vertices that complete triangles)
    common_neighbors = u_neighbors & v_neighbors

    # The new edge shares a triangular face with existing edges if
    # there's at least one common neighbor
    return len(common_neighbors) > 0


def forms_triangle_with_block(block, u, v):
    """
    Check if edge (u, v) forms at least one triangle with existing edges in the block.

    A triangle is formed if there exists a vertex w such that:
    - (u, w) is in block
    - (v, w) is in block

    Args:
        block: Current networkx Graph
        u: First vertex of potential edge
        v: Second vertex of potential edge

    Returns:
        Boolean indicating if the edge forms a triangle
    """
    # Get neighbors of u and v in the block
    u_neighbors = set(block.neighbors(u)) if u in block.nodes() else set()
    v_neighbors = set(block.neighbors(v)) if v in block.nodes() else set()

    # Find common neighbors (vertices that form triangles)
    common_neighbors = u_neighbors & v_neighbors

    return len(common_neighbors) > 0


def generate_triangular_blocks_avoiding_subgraph(n, forbidden_graph):
    """
    Generate all non-isomorphic triangular blocks with n vertices that do NOT
    contain the forbidden_graph as a subgraph.

    This is useful for Turán-type problems where we want to find extremal graphs
    avoiding certain subgraphs.

    Args:
        n: Number of vertices (must be >= 2)
        forbidden_graph: A networkx Graph that should not appear as a subgraph

    Returns:
        List of networkx Graph objects representing non-isomorphic triangular blocks
        that do not contain forbidden_graph as a subgraph

    Raises:
        ValueError: If n < 2
    """
    if n < 2:
        raise ValueError("n must be at least 2")

    # Generate all triangular blocks on n vertices
    all_blocks = []
    visited_canonical = set()

    # Start with edge (0, 1)
    initial_block = nx.Graph()
    initial_block.add_edge(0, 1)

    queue = deque([initial_block])

    while queue:
        current_block = queue.popleft()

        # Get canonical form for pruning
        canon_form = get_canonical_form(current_block)
        if canon_form in visited_canonical:
            continue
        visited_canonical.add(canon_form)

        # Check if current block contains forbidden subgraph
        # If it does, don't explore further from this state
        if contains_subgraph(current_block, forbidden_graph):
            continue  # Prune this branch

        # If we have n vertices, check if it's valid and doesn't contain forbidden subgraph
        if len(current_block.nodes()) == n:
            if is_valid_triangular_block_structure(current_block):
                # Double-check it doesn't contain forbidden subgraph
                if not contains_subgraph(current_block, forbidden_graph):
                    all_blocks.append(current_block)

        # Try adding edges to grow the graph
        current_edges = set(tuple(sorted(e)) for e in current_block.edges())

        # Try all possible new edges
        for u in range(n):
            for v in range(u + 1, n):
                if (u, v) in current_edges:
                    continue

                # Add this edge and test
                new_block = current_block.copy()
                new_block.add_edge(u, v)

                # Check planarity
                is_planar, _ = nx.check_planarity(new_block)
                if not is_planar:
                    continue

                # Check if adding this edge creates the forbidden subgraph
                if contains_subgraph(new_block, forbidden_graph):
                    continue  # Skip this edge

                # Add to queue if still within n vertices
                if len(new_block.nodes()) <= n:
                    queue.append(new_block)

    # Remove isomorphic duplicates
    unique_blocks = remove_isomorphic_duplicates(all_blocks)

    return unique_blocks


def contains_subgraph(graph, subgraph):
    """
    Check if graph contains subgraph (via subgraph isomorphism).

    Args:
        graph: The larger graph to check
        subgraph: The smaller graph to look for

    Returns:
        Boolean indicating if subgraph is found in graph
    """
    # Quick checks
    if subgraph.number_of_nodes() > graph.number_of_nodes():
        return False
    if subgraph.number_of_edges() > graph.number_of_edges():
        return False

    # Use NetworkX's subgraph isomorphism checker
    from networkx.algorithms import isomorphism

    GM = isomorphism.GraphMatcher(graph, subgraph)
    return GM.subgraph_is_isomorphic()


def generate_triangular_blocks_verbose(n, verbose=True):
    """
    Generate triangular blocks with progress reporting.

    Args:
        n: Number of vertices
        verbose: Print progress information

    Returns:
        List of non-isomorphic triangular blocks
    """
    if verbose:
        print(f"Generating triangular blocks with {n} vertices...")

    blocks = generate_triangular_blocks(n)

    if verbose:
        print(f"Found {len(blocks)} non-isomorphic triangular blocks")
        for i, block in enumerate(blocks):
            print(f"  Block {i+1}: {block.number_of_nodes()} vertices, "
                  f"{block.number_of_edges()} edges")

    return blocks


def is_valid_triangular_block_structure(graph):
    """
    Check if a graph is a valid triangular block structure.

    Simplified definition:
    1. Graph must be planar and connected
    2. Every edge must be part of at least one triangle (no standalone edges)
    3. All triangles in the graph must form a connected structure
       (can reach any triangle from any other by crossing shared edges)

    Args:
        graph: networkx Graph

    Returns:
        Boolean indicating if graph is a valid triangular block
    """
    if graph.number_of_edges() == 0:
        return False
    if not nx.is_connected(graph):
        return False

    # Check if planar
    is_planar, _ = nx.check_planarity(graph)
    if not is_planar:
        return False

    # Find all triangles in the graph
    triangles = []
    nodes = list(graph.nodes())
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes[i+1:], i+1):
            for k, w in enumerate(nodes[j+1:], j+1):
                if graph.has_edge(u, v) and graph.has_edge(v, w) and graph.has_edge(u, w):
                    triangles.append(tuple(sorted([u, v, w])))

    if len(triangles) == 0:
        return False

    # Check: every edge must be part of at least one triangle
    edges_in_triangles = set()
    for tri in triangles:
        edges_in_triangles.add(tuple(sorted([tri[0], tri[1]])))
        edges_in_triangles.add(tuple(sorted([tri[1], tri[2]])))
        edges_in_triangles.add(tuple(sorted([tri[0], tri[2]])))

    for edge in graph.edges():
        if tuple(sorted(edge)) not in edges_in_triangles:
            return False  # This edge is not part of any triangle

    # Check: all triangles must be reachable from each other
    # Build a graph where nodes are triangles, edges connect triangles that share an edge
    if len(triangles) > 1:
        triangle_graph = nx.Graph()
        for i in range(len(triangles)):
            triangle_graph.add_node(i)

        for i in range(len(triangles)):
            for j in range(i+1, len(triangles)):
                tri_i = triangles[i]
                tri_j = triangles[j]

                # Get edges of each triangle
                edges_i = {tuple(sorted([tri_i[0], tri_i[1]])),
                           tuple(sorted([tri_i[1], tri_i[2]])),
                           tuple(sorted([tri_i[0], tri_i[2]]))}
                edges_j = {tuple(sorted([tri_j[0], tri_j[1]])),
                           tuple(sorted([tri_j[1], tri_j[2]])),
                           tuple(sorted([tri_j[0], tri_j[2]]))}

                # Check if triangles share an edge
                if edges_i & edges_j:
                    triangle_graph.add_edge(i, j)

        # Check if triangle graph is connected
        if not nx.is_connected(triangle_graph):
            return False

    return True


def _can_construct_from_edge(graph, edges_list, start_idx):
    """
    Check if the graph can be constructed starting from a specific edge.

    Correct rule: An edge (u,v) can be added if it's part of a triangle (u,v,w)
    where at least one of the other edges (u,w) or (v,w) is already in the subgraph.
    This means the new edge "shares a triangular face" with an existing edge.

    Args:
        graph: The networkx Graph
        edges_list: List of all edges
        start_idx: Index of the starting edge

    Returns:
        Boolean indicating if construction is possible from this edge
    """
    # Build a subgraph with only the added edges
    added_edges = [start_idx]
    subgraph = nx.Graph()
    subgraph.add_edge(*edges_list[start_idx])

    # Keep trying to add edges that share triangular faces with existing edges
    changed = True
    while changed:
        changed = False

        for i, (u, v) in enumerate(edges_list):
            if i in added_edges:
                continue

            # Edge (u,v) can be added if it's part of a triangle (u,v,w) where
            # at least one of (u,w) or (v,w) is already in the subgraph
            can_add = False

            # Find all triangles containing edge (u,v) in the original graph
            u_neighbors = set(graph.neighbors(u))
            v_neighbors = set(graph.neighbors(v))
            common_neighbors = u_neighbors & v_neighbors

            for w in common_neighbors:
                # Triangle (u,v,w) exists in the original graph
                # Check if either (u,w) or (v,w) is in the subgraph
                if subgraph.has_edge(u, w) or subgraph.has_edge(v, w):
                    # This edge shares a triangular face with an existing edge!
                    can_add = True
                    break

            if can_add:
                subgraph.add_edge(u, v)
                added_edges.append(i)
                changed = True

    # Check if we added all edges
    return len(added_edges) == len(edges_list)


def _get_triangular_faces(embedding):
    """
    Extract all triangular faces from a planar embedding.

    Args:
        embedding: PlanarEmbedding from networkx

    Returns:
        List of triangular faces (each face is a list of vertices)
    """
    faces = []
    visited_half_edges = set()

    for v in embedding.nodes():
        for w in embedding.neighbors_cw_order(v):
            half_edge = (v, w)
            if half_edge not in visited_half_edges:
                # Traverse this face
                face = list(embedding.traverse_face(v, w))

                # Mark all half-edges of this face as visited
                for i in range(len(face)):
                    u1 = face[i]
                    u2 = face[(i+1) % len(face)]
                    visited_half_edges.add((u1, u2))

                # Only keep triangular faces
                if len(face) == 3:
                    faces.append(face)

    return faces


def is_maximal_triangular_block_structure(graph):
    """
    Check if a triangular block is maximal.

    A triangular block is maximal if no additional edge can be added
    while maintaining the triangular block property and planarity.

    Args:
        graph: networkx Graph

    Returns:
        Boolean indicating if block is maximal
    """
    nodes = list(graph.nodes())

    # Check all possible edges
    for u in nodes:
        for v in nodes:
            if u >= v:
                continue
            if graph.has_edge(u, v):
                continue

            # Try adding this edge
            test_graph = graph.copy()
            test_graph.add_edge(u, v)

            # Check if still planar
            is_planar, _ = nx.check_planarity(test_graph)
            if not is_planar:
                continue

            # Check if this would still be a valid triangular block
            if is_valid_triangular_block_structure(test_graph):
                return False  # Not maximal, we could add this edge

    return True


def get_block_info(block):
    """
    Get detailed information about a triangular block.

    Args:
        block: networkx Graph

    Returns:
        Dictionary with block statistics
    """
    info = {
        'vertices': block.number_of_nodes(),
        'edges': block.number_of_edges(),
        'degree_sequence': sorted(dict(block.degree()).values(), reverse=True),
        'is_planar': nx.check_planarity(block)[0],
        'is_connected': nx.is_connected(block)
    }

    return info
