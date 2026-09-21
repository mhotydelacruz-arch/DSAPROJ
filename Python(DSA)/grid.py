"""
FarmGrid — 2D list (static rows × cols)
place / remove / get → O(1)
"""


class FarmGrid:
    """2D list; grid[row][col] holds None or an entity id/object."""

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def place(self, entity, row: int, col: int) -> bool:
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        if self.grid[row][col] is not None:
            return False
        self.grid[row][col] = entity
        return True

    def remove(self, row: int, col: int):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return None
        entity = self.grid[row][col]
        self.grid[row][col] = None
        return entity

    def get(self, row: int, col: int):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return None
        return self.grid[row][col]


if __name__ == "__main__":
    g = FarmGrid(3, 3)
    print(g.place("coop", 1, 1))   # True
    print(g.place("pond", 1, 1))   # False (occupied)
    print(g.get(1, 1))             # coop
    print(g.remove(1, 1))          # coop
    print(g.get(1, 1))             # None