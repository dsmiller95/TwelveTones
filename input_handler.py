from __future__ import annotations

import queue
from typing import Tuple

"""Input handling functions for the grid application."""

from pygame.math import Vector2
from models import InputEvent, GameState, GameContext, GameEventEmitSound, GameEvent, GameEventRenderBoard


def time_step(game_state: GameState, game_context: GameContext) -> Tuple[GameState, list[GameEvent]]:
    """Advance the game state by one time step."""
    emitted_events: list[GameEvent] = []
    any_change = False

    while not game_context.input_queue.empty():
        try:
            input_event = game_context.input_queue.get_nowait()
            (game_state, emitted_tmp) = handle_input(input_event, game_state)
            emitted_events.extend(emitted_tmp)
            any_change = True
        except queue.Empty:
            break

    if game_state.is_auto_moving:
        should_auto_advance = (
                game_state.is_auto_moving and
                game_context.current_time - game_state.last_auto_advance_time >= game_context.time_per_advance
        )
        if should_auto_advance:
            game_state = advance_cursor(game_state)
            game_state.last_auto_advance_time = game_context.current_time
            emitted_events.append(GameEventEmitSound(game_state.cell_at_cursor()))
            any_change = True

    if any_change:
        emitted_events.append(GameEventRenderBoard())

    return game_state, emitted_events

def handle_input(event: InputEvent, current_state: GameState) -> Tuple[GameState, list[GameEvent]]:
    """Process an input event and return a new game state."""
    new_position = Vector2(current_state.primary_cursor)
    new_auto_moving = current_state.is_auto_moving
    should_emit_note: bool = False

    if event == InputEvent.TOGGLE_PAUSE:
        new_auto_moving = not current_state.is_auto_moving
    elif event == InputEvent.MOVE_UP:
        new_auto_moving = False
        new_position.y = (current_state.primary_cursor.y - 1) % current_state.grid_size.y
        should_emit_note = True
    elif event == InputEvent.MOVE_DOWN:
        new_auto_moving = False
        new_position.y = (current_state.primary_cursor.y + 1) % current_state.grid_size.y
        should_emit_note = True
    elif event == InputEvent.MOVE_LEFT:
        new_auto_moving = False
        new_position.x = (current_state.primary_cursor.x - 1) % current_state.grid_size.x
        should_emit_note = True
    elif event == InputEvent.MOVE_RIGHT:
        new_auto_moving = False
        new_position.x = (current_state.primary_cursor.x + 1) % current_state.grid_size.x
        should_emit_note = True

    new_game_state = GameState(
        grid=current_state.grid,
        primary_cursor=new_position,
        cursors=current_state.cursors,
        is_auto_moving=new_auto_moving,
        grid_size=current_state.grid_size,
        last_auto_advance_time=current_state.last_auto_advance_time
    )
    emitted_events: list[GameEvent] = []
    if should_emit_note:
        cell = new_game_state.cell_at_cursor()
        emitted_events.append(GameEventEmitSound(cell))
    return new_game_state, emitted_events


def advance_cursor(state: GameState) -> GameState:
    """Advance cursor automatically (rightwards with wrap)."""
    new_position = state.primary_cursor + Vector2(1, 0)

    if new_position.x >= state.grid_size.x:
        new_position.x = 0
        new_position.y = (state.primary_cursor.y + 1) % state.grid_size.y

    return GameState(
        grid=state.grid,
        primary_cursor=new_position,
        cursors=state.cursors,
        is_auto_moving=state.is_auto_moving,
        grid_size=state.grid_size,
        last_auto_advance_time=state.last_auto_advance_time
    )
