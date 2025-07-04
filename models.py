from __future__ import annotations

"""Domain models for the grid application."""

from dataclasses import dataclass
from enum import Enum


@dataclass(slots=True, frozen=True)
class Cell:
    """A single grid cell containing one printable character."""

    display: str


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
