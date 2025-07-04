from __future__ import annotations

"""Grid demo using **RichRenderer** (Python 3.13)

Run with:
    pip install rich keyboard
    python main.py
"""

import time
import queue

import keyboard
from rich_renderer import RichRenderer
from models import GameState, InputEvent
from grid_factory import create_mock_grid
from input_handler import handle_input, advance_cursor

# ────────────────────────────────────────────────────────────────────────────
# Interactive demo loop
# ────────────────────────────────────────────────────────────────────────────

def run_interactive_demo(sleep_seconds: float = 0.5) -> None:
    """Run the interactive grid demo with keyboard input."""
    renderer = RichRenderer()

    # Create grid and initialize game state
    grid = create_mock_grid()
    rows = len(grid)
    cols = len(grid[0])

    game_state = GameState(
        grid=grid,
        cursor_row=0,
        cursor_col=0,
        is_auto_moving=True,
        rows=rows,
        cols=cols
    )

    # Input queue for thread-safe communication
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
