"""
Triangular Blocks Package

Generate all non-isomorphic triangular blocks on n vertices.
"""

from .triangular_blocks import (
    generate_triangular_blocks,
    generate_triangular_blocks_verbose,
    find_extendable_edges,
    forms_triangle_with_block,
    get_block_info
)

from .isomorphism import (
    get_canonical_form,
    remove_isomorphic_duplicates,
    are_isomorphic
)

from .validation import (
    validate_triangular_block,
    is_constructible_as_triangular_block,
    is_maximal_triangular_block,
    get_triangles,
    count_triangle_faces
)

__version__ = '0.1.0'

__all__ = [
    'generate_triangular_blocks',
    'generate_triangular_blocks_verbose',
    'find_extendable_edges',
    'forms_triangle_with_block',
    'get_block_info',
    'get_canonical_form',
    'remove_isomorphic_duplicates',
    'are_isomorphic',
    'validate_triangular_block',
    'is_constructible_as_triangular_block',
    'is_maximal_triangular_block',
    'get_triangles',
    'count_triangle_faces'
]
