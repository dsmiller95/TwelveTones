from __future__ import annotations

import queue

"""Domain models for the grid application."""

from dataclasses import dataclass
from enum import Enum
from pygame.math import Vector2


@dataclass(slots=True, frozen=True)
class Cell:
    """A single grid cell containing one printable character.

    Note: Use create_cell() function to create instances instead of direct construction.
    """

    display: str
    index_in_octave: int

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
    cursors: list[Vector2]
    primary_cursor: Vector2
    is_auto_moving: bool
    grid_size: Vector2
    last_auto_advance_time: float

    def cell_at_cursor(self) -> Cell:
        """Get the cell at the current cursor position."""
        row = int(self.primary_cursor.y)
        col = int(self.primary_cursor.x)
        return self.grid[row][col]

    def cells_at_cursors(self) -> list[Cell]:
        """Get the cells at all cursor positions."""
        all_cursors = self.cursors.copy()
        all_cursors.append(self.primary_cursor)
        return [self.grid[int(cursor.y)][int(cursor.x)] for cursor in all_cursors]

class GameEvent:
    """Base class for game events. Can be extended for specific event types."""
    pass

class GameEventEmitSound(GameEvent):
    """Event to emit a sound for the current cell."""
    def __init__(self, cell: Cell):
        self.cell = cell

class GameEventRenderBoard(GameEvent):
    """Event to render the current board out to the console."""
    def __init__(self):
        pass

@dataclass(slots=True)
class GameContext:
    """Context in which the game operates. contains external information such as time."""
    current_time: float
    time_per_advance: float = 0.5  # Default time per auto-advance in seconds
    input_queue: queue.Queue[InputEvent] = queue.Queue()
