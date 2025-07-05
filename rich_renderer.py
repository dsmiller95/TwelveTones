from __future__ import annotations

from models import Grid

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
            caret_pos = -1
            total_chars = 0
            # Row of characters
            for c, cell in enumerate(row):
                style = ""
                if r == caret_row and c == caret_col:
                    caret_pos = total_chars
                    style = self.HIGHLIGHT_STYLE
                render_out.append(cell.display, style=style)
                total_chars += len(cell.display)
                if c != len(row) - 1:
                    render_out.append(self.CELL_SEP)
                    total_chars += len(self.CELL_SEP)
            render_out.append("\n")

            # Caret line
            if caret_pos != -1:
                render_out.append(" " * caret_pos)
                render_out.append("^", style=self.HIGHLIGHT_STYLE)
            render_out.append("\n")

        self._console.clear()
        self._console.print(render_out)

    def clear(self) -> None:
        """Clear console, handy on exit."""
        self._console.clear()
