"""
Validation functions for triangular blocks.

This module provides functions to verify that a graph is a valid triangular block
according to the definition from the paper.
"""

import networkx as nx


def validate_triangular_block(graph):
    """
    Comprehensive validation of a triangular block.

    Checks:
    1. Graph is connected
    2. Graph is planar
    3. Graph is built from triangular faces (all edges reachable through triangles)

    Args:
        graph: networkx Graph to validate

    Returns:
        Tuple (is_valid, message) where is_valid is Boolean and message describes result
    """
    # Test 1: Connectivity
    if not nx.is_connected(graph):
        return False, "Graph is not connected"

    # Test 2: Planarity
    is_planar, _ = nx.check_planarity(graph)
    if not is_planar:
        return False, "Graph is not planar"

    # Test 3: Has triangular structure
    # (For now, just check that graph has triangles if it has >2 vertices)
    if graph.number_of_nodes() >= 3:
        triangles = get_triangles(graph)
        if len(triangles) == 0:
            return False, "Graph has no triangular faces"

    return True, "Valid triangular block"


def is_constructible_as_triangular_block(graph):
    """
    Test if graph can be built following triangular block rules.

    Strategy: Try to deconstruct the graph by removing edges in reverse order,
    ensuring each removed edge forms a triangle with remaining edges.

    Args:
        graph: networkx Graph to test

    Returns:
        Boolean indicating if graph is constructible
    """
    if graph.number_of_edges() == 0:
        return False

    if graph.number_of_edges() == 1:
        return True

    edges_list = list(graph.edges())

    # Try to deconstruct to a single edge
    return _can_deconstruct_to_edge(edges_list)


def _can_deconstruct_to_edge(edges_list):
    """
    Recursively check if we can deconstruct edge list to a single edge.

    Args:
        edges_list: List of edges

    Returns:
        Boolean indicating if deconstruction is possible
    """
    if len(edges_list) == 1:
        return True

    # Try removing each edge
    for i in range(len(edges_list)):
        edge_to_remove = edges_list[i]
        u, v = edge_to_remove

        # Create temporary graph without this edge
        other_edges = edges_list[:i] + edges_list[i+1:]
        temp_graph = nx.Graph()
        temp_graph.add_edges_from(other_edges)

        # Check if the removed edge forms a triangle with remaining edges
        if _forms_triangle_with_edges(temp_graph, u, v):
            # This edge could have been added last, try removing it
            if _can_deconstruct_to_edge(other_edges):
                return True

    return False


def _forms_triangle_with_edges(graph, u, v):
    """
    Check if edge (u, v) forms a triangle with edges in graph.

    Args:
        graph: networkx Graph
        u, v: Vertices of potential edge

    Returns:
        Boolean
    """
    if u not in graph.nodes() or v not in graph.nodes():
        return False

    u_neighbors = set(graph.neighbors(u))
    v_neighbors = set(graph.neighbors(v))

    common = u_neighbors & v_neighbors
    return len(common) > 0


def is_maximal_triangular_block(graph):
    """
    Check if no more edges can be added following triangular block rules.

    Args:
        graph: networkx Graph

    Returns:
        Boolean indicating if graph is maximal
    """
    n = len(graph.nodes())
    nodes = list(graph.nodes())

    # Check all possible edges
    for i, u in enumerate(nodes):
        for v in nodes[i+1:]:
            # Skip if edge already exists
            if graph.has_edge(u, v):
                continue

            # Check if this edge would form a triangle
            u_neighbors = set(graph.neighbors(u))
            v_neighbors = set(graph.neighbors(v))

            if len(u_neighbors & v_neighbors) > 0:
                # This edge could be added, so graph is not maximal
                return False

    return True


def get_triangles(graph):
    """
    Get all triangles (3-cycles) in the graph.

    Args:
        graph: networkx Graph

    Returns:
        List of triangles, where each triangle is a set of 3 vertices
    """
    triangles = []

    nodes = list(graph.nodes())
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes[i+1:], start=i+1):
            if not graph.has_edge(u, v):
                continue

            # Find common neighbors of u and v
            u_neighbors = set(graph.neighbors(u))
            v_neighbors = set(graph.neighbors(v))
            common = u_neighbors & v_neighbors

            for w in common:
                triangle = frozenset([u, v, w])
                if triangle not in [frozenset(t) for t in triangles]:
                    triangles.append({u, v, w})

    return triangles


def count_triangle_faces(graph):
    """
    Count the number of triangular faces in a planar embedding.

    Args:
        graph: networkx Graph

    Returns:
        Number of triangular faces
    """
    is_planar, embedding = nx.check_planarity(graph)

    if not is_planar:
        return 0

    # Get all faces
    faces = []
    visited_half_edges = set()

    for v in embedding.nodes():
        for w in embedding.neighbors_cw_order(v):
            half_edge = (v, w)
            if half_edge not in visited_half_edges:
                # Traverse this face
                face = list(embedding.traverse_face(v, w))

                # Mark all half-edges of this face as visited
                for k in range(len(face)):
                    u1 = face[k]
                    u2 = face[(k+1) % len(face)]
                    visited_half_edges.add((u1, u2))

                faces.append(face)

    # Count triangular faces (length 3)
    triangular_faces = [f for f in faces if len(f) == 3]

    return len(triangular_faces)
