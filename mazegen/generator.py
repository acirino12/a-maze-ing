import random
import sys
from typing import Optional, TextIO
from .grid import Grid
from .cell import Cell
from .recursive_backtracker import recursive_backtracker
from .mask import mask_42
from .dijkstra_distance import find_shortest_path, path_output


class MazeGenerator:
    """
    Main generator class.
    Encapsulates grid creation, masking, carving, braiding, and solving.

    Attributes:
    grid
    solution

    Example usage:
    from mazegen import MazeGenerator

    maze = MazeGenerator(
            width=21,
            height=21,
            entry=(0,0),
            exit=(15, 15),
            perfect=True,
            seed=42
            )
    maze.output()
    grid = maze.grid
    shortest_path = maze.solution
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool = False,
        seed: Optional[int] = None,
    ) -> None:
        if not (self.valid_dimension(height) and self.valid_dimension(width)):
            raise ValueError("Maze's dimensions should be positive numbers")
        self.rows = height
        self.columns = width
        self.perfect = perfect
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed)
        self._grid = self.generate()
        if entry == exit:
            raise ValueError("Entry and exit must be distinct coordinates")
        if not self.valid_point(entry) or not self.valid_point(exit):
            raise ValueError(
                "Entry or exit point is invalid",
                " (outside bounds or blocked by mask)",
            )
        self.start = self._grid[entry[1], entry[0]]
        self.end = self._grid[exit[1], exit[0]]
        self._solution = self.solve()

    @staticmethod
    def valid_dimension(dim: int) -> bool:
        """
        Used to validate maze dimensions.
        """
        return dim > 0

    def valid_point(self, coordinates: tuple[int, int]) -> bool:
        """
        Validates that coordinates (x, y) are inside the grid
        and not turned off by mask_42.
        """
        c, r = coordinates
        if not (0 <= r < self.rows and 0 <= c < self.columns):
            return False
        cell = self._grid[r, c]
        return cell is not None and len(cell.neighbors()) > 0

    def generate(self) -> Grid:
        """
        Executes the full generation pipeline.
        """
        grid = Grid(self.rows, self.columns)
        mask_42(grid)
        recursive_backtracker(grid)
        if not self.perfect:
            grid.braid()
        return grid

    def solve(self) -> list[Cell]:
        """
        Calculates and returns the shortest path.
        """
        if not self.start or not self.end:
            raise ValueError("Coordinates out of maze bounds")
        return find_shortest_path(self.start, self.end)

    @property
    def grid(self) -> Grid:
        """Access to the generated grid structure."""
        return self._grid

    @property
    def solution(self) -> list[Cell]:
        """Access to the solved path."""
        return self._solution

    def output(self, file: TextIO = sys.stdout) -> None:
        """
        Writes the maze and solution to the specified output stream.
        """
        self._grid.output(file=file)
        if not self.start or not self.end:
            return
        print(
            "",
            f"{self.start.col}, {self.start.row}",
            f"{self.end.col}, {self.end.row}",
            sep="\n",
            file=file,
        )
        path_output(self._solution, file=file)
