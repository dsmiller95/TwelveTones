from __future__ import annotations

"""Grid factory functions for creating grids."""

from typing import Final
from models import Cell, Grid


def create_mock_grid() -> Grid:
    """Create a mock grid with predefined letters."""
    mock_grid_letters: Final[list[list[str]]] = [
        ["I", "A", "B", "C", "P"],
        ["K", "E", "F", "A", "M"],
        ["B", "R", "9", "p", "E"],
        ["b", "a", "l", "f", "g"],
        ["p", "e", "f", "w", "m"],
    ]

    return [[Cell(
        display=ch
    ) for ch in row] for row in mock_grid_letters]
