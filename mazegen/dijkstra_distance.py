from .cell import Cell
from typing import TextIO
import sys


def get_distances(start: Cell, end: Cell) -> dict[Cell, int]:
    """
    Calculates the distances between two cells (start, end)
    Returns:
    a dictionary key = cell, value = cell's distance from the start
    """
    distances: dict[Cell, int] = {start: 0}
    frontier: list[Cell] = [start]
    while frontier:
        if end is not None and end in distances:
            break
        new_frontier: list[Cell] = []
        for cell in frontier:
            for n in cell.neighbors():
                if cell.is_linked(n) and n not in distances:
                    new_frontier.append(n)
                    distances[n] = distances[cell] + 1
        frontier = new_frontier
    return distances


def find_shortest_path(start: Cell, end: Cell) -> list[Cell]:
    """
    Finds the shortest path starting from 'end'
     and tracing back the distances to 'start'.
    """
    distances = get_distances(start, end)
    if end not in distances:
        return []

    # Back tracking:
    path: list[Cell] = [end]
    curr = end
    while curr != start:
        for n in curr.neighbors():
            if curr.is_linked(n) and distances.get(n) == distances[curr] - 1:
                curr = n
                path.append(curr)
                break
    return path[::-1]


def path_output(path: list[Cell], file: TextIO = sys.stdout) -> None:
    """
    Convert a list of Cells in a string of directions (N, E, S, W)
    and writes to a file or streams
    """
    directions: list[str] = []
    for i in range(len(path) - 1):
        curr = path[i]
        nxt = path[i + 1]
        if nxt == curr.north:
            directions.append("N")
        elif nxt == curr.east:
            directions.append("E")
        elif nxt == curr.south:
            directions.append("S")
        elif nxt == curr.west:
            directions.append("W")
    output = "".join(directions)
    print(output, file=file)
