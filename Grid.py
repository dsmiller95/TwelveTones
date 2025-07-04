from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Final, List


@dataclass(frozen=True, slots=True)
class Cell:
    """Represents a single grid cell.

    Attributes
    ----------
    display
        A *single* character string shown when the grid is rendered.
    """

    display: str


# ---------------------------------------------------------------------------
# Mock data -----------------------------------------------------------------
# ---------------------------------------------------------------------------

# A 5×5 grid of example characters. Feel free to replace with your own data.
MOCK_GRID_LETTERS: Final[list[list[str]]] = [
    ["I", "A", "B", "C", "P"],
    ["K", "E", "F", "A", "M"],
    ["B", "R", "9", "p", "E"],
    ["b", "a", "l", "f", "g"],
    ["p", "e", "f", "w", "m"],
]

# Convert raw letters to a grid of `Cell` objects (typed list of lists).
Grid = List[List[Cell]]
GRID: Final[Grid] = [[Cell(ch) for ch in row] for row in MOCK_GRID_LETTERS]

# Spacing constants for rendering.
CELL_SEPARATOR: Final[str] = "  "  # Two spaces between characters
BLANK_LINE: Final[str] = "\n"      # Single blank line between grid rows


# ---------------------------------------------------------------------------
# Rendering functions --------------------------------------------------------
# ---------------------------------------------------------------------------

def render_grid(grid: Grid, caret_row: int, caret_col: int) -> None:
    """Render the grid to the console, highlighting the caret position.

    The function prints **two** lines per grid row:
    1. The characters themselves, separated by spaces.
    2. Either a caret ("^") under the current cell *or* blank spaces.

    A blank line is printed after each pair to visually separate rows.
    """

    for r, row in enumerate(grid):
        # Line 1: characters with spacing.
        char_line = CELL_SEPARATOR.join(cell.display for cell in row)
        print(char_line)

        # Line 2: caret row if this is the active row; otherwise spaces.
        if r == caret_row:
            caret_parts = []
            for c in range(len(row)):
                caret_parts.append("^" if c == caret_col else " ")
            caret_line = CELL_SEPARATOR.join(caret_parts)
            print(caret_line)
        else:
            # Same width as char_line but blank (spaces only).
            print(" " * len(char_line))

        # Spacer line between rows.
        print(BLANK_LINE, end="")


# ---------------------------------------------------------------------------
# Main loop ------------------------------------------------------------------
# ---------------------------------------------------------------------------

def main() -> None:
    grid = GRID
    rows, cols = len(grid), len(grid[0])

    caret_row = 0
    caret_col = 0

    try:
        while True:
            # Clear screen by printing ANSI escape (works on most modern terms).
            print("\033[2J\033[H", end="")  # Clear and move cursor to home.

            render_grid(grid, caret_row, caret_col)

            # Advance caret position.
            caret_col += 1
            if caret_col >= cols:
                caret_col = 0
                caret_row = (caret_row + 1) % rows

            # Wait 500 ms.
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nExited.")


if __name__ == "__main__":
    main()
