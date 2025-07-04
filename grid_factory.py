from __future__ import annotations

import random

"""Grid factory functions for creating grids."""

from typing import Final
from models import Grid, Cell


def create_mock_grid() -> Grid:
    notes = list(range(12))
    random.shuffle(notes)

    root = notes[0]
    delta_from_root = [notes[i] - root for i in range(len(notes))]
    root_column = [root + -delta_from_root[i] for i in range(len(notes))]
    twelve_tone_grid = [
        [root_column[row] + delta_from_root[col] for col in range(len(notes))]
        for row in range(len(notes))
    ]

    return [[create_cell(ch % 12) for ch in row] for row in twelve_tone_grid]


KEY_RENDER: Final[list[str]] = [
    "C ",
    "C#",
    "D ",
    "D#",
    "E ",
    "F ",
    "F#",
    "G ",
    "G#",
    "A ",
    "A#",
    "B ",
    "__",
    "__",
    "__",
    "__"
]

def create_cell(index_in_octave: int) -> Cell:
    """Create a Cell with display set to the first character of the text.

    Args:
        index_in_octave: a value between 0 and 11 representing the index in an octave.

    Returns:
        A new Cell instance with display set to text[0]
    """
    return Cell(display=KEY_RENDER[index_in_octave], index_in_octave=index_in_octave)