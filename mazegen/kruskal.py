from random import shuffle
from .grid import Grid
from .cell import Cell


def kruskal(grid: Grid) -> None:
    """
    Carve passages in a grid using a randomized Kruskal's algorithm.
    Maintains dual lookup maps to track and merge connected sets of cells.

    Args:
        grid (Grid): The target grid to carve in-place.
    """
    neighbors: list[tuple[Cell, Cell]] = list()
    set_for_cell: dict[Cell, int] = {}
    cells_in_set: dict[int, list[Cell]] = {}
    for cell in grid.each_cell():
        set_id = len(set_for_cell)
        set_for_cell[cell] = set_id
        cells_in_set[set_id] = [cell]
        for n in cell.neighbors():
            if (cell.row, cell.col) < (n.row, n.col):
                neighbors.append((cell, n))
    shuffle(neighbors)

    def can_merge(left: Cell, right: Cell) -> bool:
        """
        Check whether two cells belong to different connected sets.

        Args:
            left (Cell): The first cell.
            right (Cell): The adjacent neighbor cell.

        Returns:
            bool: True if the cells have different root identifiers,
            False otherwise.
        """
        return set_for_cell[left] != set_for_cell[right]

    def merge(left: Cell, right: Cell) -> None:
        """
        Link two cells and unify their connected components.

        Carves the passage between the cells, reassigns the set ID of all
        cells from the loser set to the winner set, clears the loser entry.

        Args:
            left (Cell): The source cell.
            right (Cell): The adjacent neighbor cell.
        """
        left.link(right)
        winner: int = set_for_cell[left]
        loser: int = set_for_cell[right]
        losers: list[Cell] = cells_in_set[loser]
        for cell in losers:
            cells_in_set[winner].append(cell)
            set_for_cell[cell] = winner
        del cells_in_set[loser]

    while neighbors:
        left, right = neighbors.pop()
        if can_merge(left, right):
            merge(left, right)
