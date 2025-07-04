from __future__ import annotations

import random

"""Grid factory functions for creating grids."""

from typing import Final
from models import Grid, create_cell


def create_mock_grid() -> Grid:
    """Create a mock grid with predefined letters."""
    mock_grid_letters: Final[list[list[str]]] = [
        ["I", "A", "B", "C", "P"],
        ["K", "E", "F", "A", "M"],
        ["B", "R", "9", "p", "E"],
        ["b", "a", "l", "f", "g"],
        ["p", "e", "f", "w", "m"],
    ]

    notes = list(range(12))
    random.shuffle(notes)

    return [[create_cell(ch) for ch in row] for row in mock_grid_letters]


