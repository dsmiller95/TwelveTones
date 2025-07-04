from __future__ import annotations

"""Grid demo using **RichRenderer** (Python 3.13)

Run with:
    pip install rich keyboard
    python main.py
"""

import time
from dataclasses import dataclass
from enum import Enum
from typing import Final

import keyboard
from rich_renderer import RichRenderer

# ────────────────────────────────────────────────────────────────────────────
# Domain model
# ────────────────────────────────────────────────────────────────────────────

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

# ────────────────────────────────────────────────────────────────────────────
# Mock data (replace with your own source if desired)
# ────────────────────────────────────────────────────────────────────────────

MOCK_GRID_LETTERS: Final[list[list[str]]] = [
    ["I", "A", "B", "C", "P"],
    ["K", "E", "F", "A", "M"],
    ["B", "R", "9", "p", "E"],
    ["b", "a", "l", "f", "g"],
    ["p", "e", "f", "w", "m"],
]

GRID: Final[Grid] = [[Cell(ch) for ch in row] for row in MOCK_GRID_LETTERS]
ROWS: Final[int] = len(GRID)
COLS: Final[int] = len(GRID[0])

# ────────────────────────────────────────────────────────────────────────────
# Input handling
# ────────────────────────────────────────────────────────────────────────────

def handle_input(event: InputEvent, current_state: GameState) -> GameState:
    """Process an input event and return a new game state."""
    new_row = current_state.cursor_row
    new_col = current_state.cursor_col
    new_auto_moving = current_state.is_auto_moving

    if event == InputEvent.TOGGLE_PAUSE:
        new_auto_moving = not current_state.is_auto_moving
    elif event == InputEvent.MOVE_UP:
        new_auto_moving = False
        new_row = (current_state.cursor_row - 1) % ROWS
    elif event == InputEvent.MOVE_DOWN:
        new_auto_moving = False
        new_row = (current_state.cursor_row + 1) % ROWS
    elif event == InputEvent.MOVE_LEFT:
        new_auto_moving = False
        new_col = (current_state.cursor_col - 1) % COLS
    elif event == InputEvent.MOVE_RIGHT:
        new_auto_moving = False
        new_col = (current_state.cursor_col + 1) % COLS

    return GameState(
        grid=current_state.grid,
        cursor_row=new_row,
        cursor_col=new_col,
        is_auto_moving=new_auto_moving
    )


def advance_cursor(state: GameState) -> GameState:
    """Advance cursor automatically (rightwards with wrap)."""
    new_col = state.cursor_col + 1
    new_row = state.cursor_row

    if new_col >= COLS:
        new_col = 0
        new_row = (state.cursor_row + 1) % ROWS

    return GameState(
        grid=state.grid,
        cursor_row=new_row,
        cursor_col=new_col,
        is_auto_moving=state.is_auto_moving
    )

# ────────────────────────────────────────────────────────────────────────────
# Interactive demo loop
# ────────────────────────────────────────────────────────────────────────────

def run_interactive_demo(sleep_seconds: float = 0.5) -> None:
    """Run the interactive grid demo with keyboard input."""
    renderer = RichRenderer()

    # Initialize game state
    game_state = GameState(
        grid=GRID,
        cursor_row=0,
        cursor_col=0,
        is_auto_moving=True
    )

    # Input queue for thread-safe communication
    import queue
    input_queue = queue.Queue()

    def on_key_event(event):
        """Handle keyboard events and map them to input events."""
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'space':
                input_queue.put(InputEvent.TOGGLE_PAUSE)
            elif event.name == 'up':
                input_queue.put(InputEvent.MOVE_UP)
            elif event.name == 'down':
                input_queue.put(InputEvent.MOVE_DOWN)
            elif event.name == 'left':
                input_queue.put(InputEvent.MOVE_LEFT)
            elif event.name == 'right':
                input_queue.put(InputEvent.MOVE_RIGHT)

    # Set up keyboard listener
    keyboard.hook(on_key_event)

    try:
        print("Use arrow keys to move cursor, space to pause/resume, Ctrl+C to exit")
        while True:
            # Process any pending input
            while not input_queue.empty():
                try:
                    input_event = input_queue.get_nowait()
                    game_state = handle_input(input_event, game_state)
                except queue.Empty:
                    break

            # Render current state
            renderer.render(game_state.grid, game_state.cursor_row, game_state.cursor_col)

            # Auto-advance if enabled
            if game_state.is_auto_moving:
                game_state = advance_cursor(game_state)

            time.sleep(sleep_seconds)

    except KeyboardInterrupt:
        renderer.clear()
        keyboard.unhook_all()
        print("Exited.")


if __name__ == "__main__":
    run_interactive_demo()
