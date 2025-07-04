from __future__ import annotations

"""RichRenderer module

Renders a square grid using the **rich** library, highlighting the active cell
(background) *and* showing a caret underneath. Designed for Python 3.13.

Usage example:
    from rich_renderer import RichRenderer
    renderer = RichRenderer()
    renderer.render(grid, caret_row, caret_col)

Requires:
    pip install rich
"""

from typing import Final, Protocol
from rich.console import Console
from rich.text import Text

# ────────────────────────────────────────────────────────────────────────────
# Minimal protocol to decouple from concrete Cell class
# ────────────────────────────────────────────────────────────────────────────

class HasDisplay(Protocol):
    """Any object with a `display` string attribute."""

    display: str


Grid = list[list[HasDisplay]]

# ────────────────────────────────────────────────────────────────────────────
# Renderer implementation
# ────────────────────────────────────────────────────────────────────────────

class RichRenderer:
    """Render 2‑D grids with a highlighted cursor using *rich*."""

    CELL_SEP: Final[str] = "  "  # two spaces between cells
    HIGHLIGHT_STYLE: Final[str] = "bold on yellow"

    def __init__(self) -> None:
        self._console: Console = Console()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(self, grid: Grid, caret_row: int, caret_col: int) -> None:
        """Clear screen and draw a fresh frame."""
        render_out = Text()

        for r, row in enumerate(grid):
            # Row of characters
            for c, cell in enumerate(row):
                style = self.HIGHLIGHT_STYLE if (r == caret_row and c == caret_col) else ""
                render_out.append(cell.display, style=style)
                if c != len(row) - 1:
                    render_out.append(self.CELL_SEP)
            render_out.append("\n")

            # Caret line
            for c in range(len(row)):
                render_out.append("^" if (r == caret_row and c == caret_col) else " ")
                if c != len(row) - 1:
                    render_out.append(self.CELL_SEP)
            render_out.append("\n")
            render_out.append("\n")

        self._console.clear()
        self._console.print(render_out)

    def clear(self) -> None:
        """Clear console, handy on exit."""
        self._console.clear()
