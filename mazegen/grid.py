from .cell import Cell
import sys
from typing import Iterator, Optional, TextIO
import random


class Grid:
    """
    Manages a two-dimensional grid of Cell objects.

    Attributes:
    rows,
    columns,
    grid[row, column]

    Methods:
    random_cell
    each_row
    each_cell
    deadends
    braid
    output
    """

    def __init__(self, rows: int, columns: int) -> None:
        self.rows = rows
        self.columns = columns
        self._grid: list[list[Cell]] = self.prepare_grid()
        self.configure_cells()

    def prepare_grid(self) -> list[list[Cell]]:
        """
        Sets up a two-dimensional array of Cells
        """
        grid: list[list[Cell]] = []
        for r in range(self.rows):
            row: list[Cell] = []
            for c in range(self.columns):
                row.append(Cell(r, c))
            grid.append(row)
        return grid

    def __getitem__(self, pos: tuple[int, int]) -> Optional[Cell]:
        """
        Allows accessing cells using grid[row, col] syntax.
        """
        r, c = pos
        if 0 <= r < self.rows and 0 <= c < self.columns:
            return self._grid[r][c]
        return None

    def random_cell(self) -> Cell:
        """
        Returns a random active cell from the grid.
        """
        while True:
            r = random.randrange(self.rows)
            c = random.randrange(self.columns)
            cell = self._grid[r][c]
            if cell.neighbors():
                return cell

    def each_row(self) -> Iterator[list[Cell]]:
        """
        Yields each row of the grid.
        """
        for row in self._grid:
            yield row

    def each_cell(self) -> Iterator[Cell]:
        """
        Yields each cell of the grid individually.
        """
        for row in self._grid:
            for cell in row:
                yield cell

    def configure_cells(self) -> None:
        """
        Assigns spatial references to each cell in the grid
        """
        for cell in self.each_cell():
            r, c = cell.row, cell.col
            cell.north = self._grid[r - 1][c] if r > 0 else None
            cell.south = self._grid[r + 1][c] if r < self.rows - 1 else None
            cell.west = self._grid[r][c - 1] if c > 0 else None
            cell.east = self._grid[r][c + 1] if c < self.columns - 1 else None

    def deadends(self) -> list[Cell]:
        """
        Returns a list of all dead-end cells in the grid
        """
        return [cell for cell in self.each_cell() if cell.is_dead_end()]

    def braid(self) -> None:
        """
        A maze with no dead ends is called a braid maze.
        This function a maze a braid maze.
        We start out by fetching the list of dead ends.
        For each of those cells we first test to see if it's still a dead end.
        This algorithm prefers to link two dead end together if possible.
        If maze is shaped it's possible that some cells will remain dead-ends.
        """
        dead_ends = self.deadends()
        random.shuffle(dead_ends)
        for cell in dead_ends:
            if cell.is_dead_end():
                unlinked_neighbors = [
                    n for n in cell.neighbors() if not cell.is_linked(n)
                ]
                if not unlinked_neighbors:
                    continue
                best: Optional[Cell] = None
                for n in unlinked_neighbors:
                    if n.is_dead_end():
                        best = n
                        break
                if best:
                    cell.link(best)
                else:
                    cell.link(random.choice(unlinked_neighbors))

    def output(self, file: TextIO = sys.stdout) -> None:
        """
        Writes the hexadecimal maze matrix to a file or stream.
        """
        for row in self.each_row():
            line = "".join(cell.to_hex() for cell in row)
            print(line, file=file)
