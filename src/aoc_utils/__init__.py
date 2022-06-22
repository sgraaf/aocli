"""A python package and CLI providing various utility functions for Advent of Code puzzles."""
from .data import to_lines, to_numbers
from .functional import (
    Graph,
    find_dimensions_2d,
    find_dimensions_3d,
    find_dimensions_4d,
    find_neighbouring_indices_2d,
    find_neighbouring_indices_3d,
    find_neighbouring_indices_4d,
)
from .io import read

__version__ = "0.2.0"
