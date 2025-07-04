from __future__ import annotations

"""Domain models for the grid application."""

from dataclasses import dataclass
from enum import Enum


@dataclass(slots=True, frozen=True)
class Cell:
    """A single grid cell containing one printable character.

    Note: Use create_cell() function to create instances instead of direct construction.
    """

    display: str
    index_in_octave: int


def create_cell(text: str, index_in_octave: int = 0) -> Cell:
    """Create a Cell with display set to the first character of the text.

    Args:
        text: String to extract the first character from
        index_in_octave: Optional index value for the cell

    Returns:
        A new Cell instance with display set to text[0]
    """
    if not text:
        raise ValueError("Text cannot be empty")
    return Cell(display=text[0], index_in_octave=index_in_octave)


# Type aliases
Grid = list[list[Cell]]


class InputEvent(Enum):
    """Domain-mapped input events."""
    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    TOGGLE_PAUSE = "toggle_pause"


@dataclass(slots=True)
class GameState:
    """Complete game state including grid, cursor position, and movement status."""
    grid: Grid
    cursor_row: int
    cursor_col: int
    is_auto_moving: bool
    rows: int
    cols: int
