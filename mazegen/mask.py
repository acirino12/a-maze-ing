from .cell import Cell
from .grid import Grid
import sys
from typing import Optional


def kill_cell(cell: Optional[Cell]) -> None:
    """
    Cells may be "turned off" by making their neighbors think
    that the cell doesn't exist
    """
    if not cell:
        return
    if cell.north:
        cell.north.south = None
        cell.north = None
    if cell.south:
        cell.south.north = None
        cell.south = None
    if cell.east:
        cell.east.west = None
        cell.east = None
    if cell.west:
        cell.west.east = None
        cell.west = None


def mask_42(grid: Grid) -> None:
    if grid.rows < 7 or grid.columns < 9:
        print(
            f"Warning: Maze dimensions ({grid.columns}x{grid.rows}) are too "
            "small for the '42' pattern (minimum required: 9x7). Proceeding "
            "without it.",
            file=sys.stderr,
        )
        return
    starting_row = (grid.rows - 5) // 2
    starting_col = (grid.columns - 7) // 2
    pattern_4 = [
        (0, 0),
        (1, 0),
        (2, 0),
        (2, 1),
        (2, 2),
        (3, 2),
        (4, 2),
    ]
    for r, c in pattern_4:
        cell = grid[starting_row + r, starting_col + c]
        kill_cell(cell)
    pattern_2 = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (2, 1),
        (2, 0),
        (3, 0),
        (4, 0),
        (4, 1),
        (4, 2),
    ]
    for r, c in pattern_2:
        cell = grid[starting_row + r, starting_col + 4 + c]
        kill_cell(cell)
