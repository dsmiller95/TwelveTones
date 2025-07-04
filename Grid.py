from __future__ import annotations

"""Grid demo using **RichRenderer** (Python 3.13)

Run with:
    pip install rich
    python main.py
"""

import time
from dataclasses import dataclass
from typing import Final

from rich_renderer import RichRenderer

# ────────────────────────────────────────────────────────────────────────────
# Domain model
# ────────────────────────────────────────────────────────────────────────────

@dataclass(slots=True, frozen=True)
class Cell:
    """A single grid cell containing one printable character."""

    display: str


Grid = list[list[Cell]]

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
# Demo loop
# ────────────────────────────────────────────────────────────────────────────

def run_demo(sleep_seconds: float = 0.5) -> None:
    renderer = RichRenderer()
    caret_row = caret_col = 0

    try:
        while True:
            renderer.render(GRID, caret_row, caret_col)

            # Advance caret (rightwards with wrap)
            caret_col += 1
            if caret_col >= COLS:
                caret_col = 0
                caret_row = (caret_row + 1) % ROWS

            time.sleep(sleep_seconds)
    except KeyboardInterrupt:
        renderer.clear()
        print("Exited.")


if __name__ == "__main__":
    run_demo()
