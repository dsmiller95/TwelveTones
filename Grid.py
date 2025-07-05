from __future__ import annotations

from conifg import Config
from sound_system import play_note

"""Grid demo using **RichRenderer** (Python 3.13)

Run with:
    pip install rich keyboard
    python __main__.py
"""

import time
import queue

import keyboard
from rich_renderer import RichRenderer
from models import GameState, InputEvent, GameContext, GameEventEmitSound, GameEventRenderBoard
from grid_factory import create_mock_grid
from input_handler import handle_input, advance_cursor, time_step


# ────────────────────────────────────────────────────────────────────────────
# Interactive demo loop
# ────────────────────────────────────────────────────────────────────────────

def run_interactive_demo(config: Config) -> None:
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
        cols=cols,
        last_auto_advance_time=time.time()
    )

    # Input queue for thread-safe communication
    input_queue: queue.Queue[InputEvent] = queue.Queue()

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

        last_auto_advance_time = time.time()

        while True:
            game_context = GameContext(
                current_time=time.time(),
                time_per_advance=config.auto_advance_period,
                input_queue=input_queue
            )

            (game_state, emitted_events) = time_step(game_state, game_context)

            # loop through and handel all emitted events
            for event in emitted_events:
                if isinstance(event, GameEventEmitSound):
                    sound_index_in_octave = event.cell.index_in_octave
                    play_note(
                        sound_index_in_octave,
                        duration=config.note_duration
                    )
                elif isinstance(event, GameEventRenderBoard):
                    renderer.render(game_state.grid, game_state.cursor_row, game_state.cursor_col)

            # Small sleep to prevent busy waiting
            time.sleep(0.01)  # 10ms polling interval

    except KeyboardInterrupt:
        renderer.clear()
        keyboard.unhook_all()
        print("Exited.")