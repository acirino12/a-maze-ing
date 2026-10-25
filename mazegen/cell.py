from typing import Optional


class Cell:
    """
    Represents a single node on the Grid.

    Attributes:
    row,
    column: each cell ought to know where it lives within the grid
    north,
    south,
    east,
    west: the cell's neighbours (will be setted by the Grid)
    links: an hash table which will be used to keep track of which neighboring
     cells are joined by a passage,
     links will be updated by link and unlink methods

    Methods:
    neighbors
    to_hex
    """

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self._links: set["Cell"] = set()
        self.north: Optional["Cell"] = None
        self.south: Optional["Cell"] = None
        self.east: Optional["Cell"] = None
        self.west: Optional["Cell"] = None

    def link(self, cell: "Cell", bidi: bool = True) -> None:
        """
        Link self with a neighbour cell (carve a passage).
        bidi = bi-directional: if true the other cell links will be updated
        """
        self._links.add(cell)
        if bidi:
            cell.link(self, False)

    def unlink(self, cell: "Cell", bidi: bool = True) -> None:
        """
        Unlink self with a neighbour cell (build a wall)
        bidi = bi-directional: if true the other cell links will be updated
        """
        self._links.discard(cell)
        if bidi:
            cell.unlink(self, False)

    def has_links(self) -> bool:
        """
        Checks if self has a link with at least another cell.
        """
        return len(self._links) > 0

    def is_linked(self, cell: Optional["Cell"]) -> bool:
        """
        Check if self is linked to the specified cell.
        """
        if cell is None:
            return False
        return cell in self._links

    def is_dead_end(self) -> bool:
        """
        A cell is a dead end if it has exactly one link
        """
        return len(self._links) == 1

    def neighbors(self) -> list["Cell"]:
        """
        Return a list of existing physical neighbors (excluding None).
        """
        return [
            neighbor
            for neighbor in (self.north, self.east, self.south, self.west)
            if neighbor is not None
        ]

    def to_hex(self) -> str:
        """
        Calculates the 4-bit wall state and returns it as a hex digit
         ('0'-'f').
        Returns a string
        """
        output = 15
        directions = [
            (self.north, 1),
            (self.east, 2),
            (self.south, 4),
            (self.west, 8),
        ]
        for neighbor, mask in directions:
            if neighbor is not None and neighbor in self._links:
                output &= ~mask
        return f"{output:x}"
