from .grid import Grid
from .cell import Cell
from random import choice


def recursive_backtracker(grid: Grid) -> None:
    """
    This function implements the Recursive Backtracker algorithm
    starting from a random point
    """
    stack: list[Cell] = []
    start = grid.random_cell()
    stack.append(start)
    while stack:
        current = stack[-1]
        neighbors = [n for n in current.neighbors() if not n.has_links()]
        if not neighbors:
            stack.pop()
        else:
            neighbor = choice(neighbors)
            current.link(neighbor)
            stack.append(neighbor)
