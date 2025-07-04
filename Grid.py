from __future__ import annotations

"""Console grid renderer (Python 3.13‑ready)

Improvements
────────────
• Uses a **single `render`** call that rewrites the screen in‑place (no scrolling backlog / ghosting).
• Only clears the screen once; further frames just move the cursor to HOME.
• Fully typed (`mypy --strict`).
• No external deps – plain ANSI, works on modern Windows 10+ & UNIX terms.
"""

from dataclasses import dataclass
from typing import Final
import sys
import time

# ────────────────────────────────────────────────────────────────────────────
# Domain model
# ────────────────────────────────────────────────────────────────────────────

@dataclass(slots=True, frozen=True)
class Cell:
    """Single grid cell containing *one* printable character."""

    display: str  # one‑char string


Grid = list[list[Cell]]

# ────────────────────────────────────────────────────────────────────────────
# Mock data – replace with real data as needed
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
# Rendering constants
# ────────────────────────────────────────────────────────────────────────────

CELL_SEP:   Final[str]   = "  "  # two spaces
SLEEP_SEC:  Final[float] = 0.5

ANSI_CLEAR: Final[str] = "\033[2J"  # clear whole screen
ANSI_HOME:  Final[str] = "\033[H"   # move cursor to 0,0

# Pre‑compute the static character rows to avoid recomputing every frame
CHAR_ROWS: Final[list[str]] = [CELL_SEP.join(cell.display for cell in row) for row in GRID]
ROW_WIDTH: Final[int] = len(CHAR_ROWS[0])  # width in characters (all rows equal)


# ────────────────────────────────────────────────────────────────────────────
# Render function (no scrolling artefacts)
# ────────────────────────────────────────────────────────────────────────────

def render(caret_row: int, caret_col: int) -> None:
    """Render the current frame *in place*.

    The function moves the cursor to HOME and writes the entire view in a
    single `sys.stdout.write`, then flushes – so the terminal history keeps
    **one copy** of the frame, not an ever‑growing backlog.
    """

    lines: list[str] = []
    for r in range(ROWS):
        lines.append(CHAR_ROWS[r])

        if r == caret_row:
            # Build a row with a caret under the active column
            caret_parts = ["^" if c == caret_col else " " for c in range(COLS)]
            caret_line = CELL_SEP.join(caret_parts)
            # Ensure identical width so we fully overwrite prior frame
            lines.append(caret_line.ljust(ROW_WIDTH))
        else:
            lines.append(" " * ROW_WIDTH)

        lines.append("")  # blank line between grid rows

    frame: str = "\n".join(lines)
    sys.stdout.write(ANSI_HOME + frame)
    sys.stdout.flush()


# ────────────────────────────────────────────────────────────────────────────
# Main loop
# ────────────────────────────────────────────────────────────────────────────

def main() -> None:
    caret_row = 0
    caret_col = 0

    # Clear once at start so we begin with a blank screen
    sys.stdout.write(ANSI_CLEAR)
    sys.stdout.flush()

    try:
        while True:
            render(caret_row, caret_col)

            # Advance caret position (right → wrap)
            caret_col += 1
            if caret_col >= COLS:
                caret_col = 0
                caret_row = (caret_row + 1) % ROWS

            time.sleep(SLEEP_SEC)
    except KeyboardInterrupt:
        sys.stdout.write("\nExited.\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
