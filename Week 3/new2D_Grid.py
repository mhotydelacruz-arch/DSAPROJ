# """04 — 2D Grid: a row/column garden that stores Plant objects."""
# from oop_plant_resources import Plant, ResourceBag


# # DATA STRUCTURE: 2D Grid represented as a list of lists.
# # A cell is addressed with grid[row][column].
# class FarmGrid:
#     def __init__(self, rows=5, columns=5):
#         self.rows = rows
#         self.columns = columns
#         self.grid = [[None for _ in range(columns)] for _ in range(rows)]

#     def plant_at(self, row, column, plant, resources):
#         self._check_position(row, column)
#         if self.grid[row][column] is not None:
#             return False
#         if not resources.take("seeds", 1):
#             return False
#         self.grid[row][column] = plant
#         return True

#     def get(self, row, column):
#         self._check_position(row, column)
#         return self.grid[row][column]

#     def _check_position(self, row, column):
#         if not (0 <= row < self.rows and 0 <= column < self.columns):
#             raise IndexError("farm row/column is outside the grid")

#     def display(self):
#         for row in self.grid:
#             print(" | ".join(plant.name if plant else "Empty" for plant in row))


# if __name__ == "__main__":
#     resources = ResourceBag()
#     farm = FarmGrid()
#     farm.plant_at(2, 1, Plant("Banana", water_need=10), resources)
#     farm.plant_at(0, 4, Plant("Eggplant", water_need=14), resources)
#     print("Farm grid (row by row):")
#     farm.display()
#     print("Banana at row 2, column 1:", farm.get(2, 1))
#     print("Seeds remaining:", resources.amount("seeds"))
