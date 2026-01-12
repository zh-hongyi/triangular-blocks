"""
Isomorphism checking for triangular blocks using canonical forms.

This module provides efficient graph isomorphism checking using pynauty
for canonical labeling. If pynauty is not available, falls back to networkx.
"""

import networkx as nx

# Try to import pynauty for fast canonical labeling
try:
    import pynauty
    HAS_PYNAUTY = True
except ImportError:
    HAS_PYNAUTY = False
    print("Warning: pynauty not available. Using networkx for isomorphism checking.")
    print("Install pynauty for better performance: pip install pynauty")


def get_canonical_form(graph):
    """
    Get canonical form of a graph for isomorphism checking.

    Args:
        graph: A networkx Graph object

    Returns:
        A hashable representation (certificate) of the graph's canonical form
    """
    if HAS_PYNAUTY:
        return _get_canonical_form_pynauty(graph)
    else:
        return _get_canonical_form_networkx(graph)


def _get_canonical_form_pynauty(graph):
    """Get canonical form using pynauty (fast)."""
    n = len(graph.nodes())

    if n == 0:
        return tuple()

    # Create mapping from graph nodes to sequential indices
    node_to_idx = {node: i for i, node in enumerate(sorted(graph.nodes()))}

    # Create pynauty graph
    g = pynauty.Graph(n, directed=False)

    # Add edges
    adjacency = [[] for _ in range(n)]
    for u, v in graph.edges():
        u_idx = node_to_idx[u]
        v_idx = node_to_idx[v]
        if u_idx != v_idx:  # No self-loops
            adjacency[u_idx].append(v_idx)
            adjacency[v_idx].append(u_idx)

    # Set adjacency lists
    for i in range(n):
        if adjacency[i]:
            g.connect_vertex(i, adjacency[i])

    # Get canonical certificate
    cert = pynauty.certificate(g)

    return cert


def _get_canonical_form_networkx(graph):
    """
    Get canonical form using networkx (slower fallback).

    Uses Weisfeiler-Lehman graph hash as an approximation.
    Not perfect but works well for most cases.
    """
    # Use Weisfeiler-Lehman hash
    try:
        wl_hash = nx.weisfeiler_lehman_graph_hash(graph)
        return wl_hash
    except:
        # Fallback to simple edge list representation
        edges = tuple(sorted([(min(u,v), max(u,v)) for u, v in graph.edges()]))
        return (len(graph.nodes()), edges)


def remove_isomorphic_duplicates(graphs):
    """
    Remove isomorphic duplicates from a list of graphs.

    Args:
        graphs: List of networkx Graph objects

    Returns:
        List of unique (non-isomorphic) graphs
    """
    unique = []
    canonical_forms = set()

    for g in graphs:
        canon = get_canonical_form(g)
        if canon not in canonical_forms:
            canonical_forms.add(canon)
            unique.append(g)

    return unique


def are_isomorphic(graph1, graph2):
    """
    Check if two graphs are isomorphic.

    Args:
        graph1: First networkx Graph
        graph2: Second networkx Graph

    Returns:
        Boolean indicating if graphs are isomorphic
    """
    # Quick checks
    if len(graph1.nodes()) != len(graph2.nodes()):
        return False
    if len(graph1.edges()) != len(graph2.edges()):
        return False

    # Compare canonical forms
    canon1 = get_canonical_form(graph1)
    canon2 = get_canonical_form(graph2)

    if canon1 == canon2:
        return True

    # If using networkx fallback, do explicit isomorphism check
    if not HAS_PYNAUTY:
        return nx.is_isomorphic(graph1, graph2)

    return False
