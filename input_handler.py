from __future__ import annotations

"""Input handling functions for the grid application."""

from models import InputEvent, GameState


def handle_input(event: InputEvent, current_state: GameState) -> GameState:
    """Process an input event and return a new game state."""
    new_row = current_state.cursor_row
    new_col = current_state.cursor_col
    new_auto_moving = current_state.is_auto_moving

    if event == InputEvent.TOGGLE_PAUSE:
        new_auto_moving = not current_state.is_auto_moving
    elif event == InputEvent.MOVE_UP:
        new_auto_moving = False
        new_row = (current_state.cursor_row - 1) % current_state.rows
    elif event == InputEvent.MOVE_DOWN:
        new_auto_moving = False
        new_row = (current_state.cursor_row + 1) % current_state.rows
    elif event == InputEvent.MOVE_LEFT:
        new_auto_moving = False
        new_col = (current_state.cursor_col - 1) % current_state.cols
    elif event == InputEvent.MOVE_RIGHT:
        new_auto_moving = False
        new_col = (current_state.cursor_col + 1) % current_state.cols

    return GameState(
        grid=current_state.grid,
        cursor_row=new_row,
        cursor_col=new_col,
        is_auto_moving=new_auto_moving,
        rows=current_state.rows,
        cols=current_state.cols
    )


def advance_cursor(state: GameState) -> GameState:
    """Advance cursor automatically (rightwards with wrap)."""
    new_col = state.cursor_col + 1
    new_row = state.cursor_row

    if new_col >= state.cols:
        new_col = 0
        new_row = (state.cursor_row + 1) % state.rows

    return GameState(
        grid=state.grid,
        cursor_row=new_row,
        cursor_col=new_col,
        is_auto_moving=state.is_auto_moving,
        rows=state.rows,
        cols=state.cols
    )
