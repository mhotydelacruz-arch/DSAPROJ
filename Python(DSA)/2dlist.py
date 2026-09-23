# addPlantToGrid = globals().get(
#     "addPlantToGrid", lambda pos, name: print(f"  [UI] grid cell {pos} <- {name}"))
# addPlantsToDropdown = globals().get(
#     "addPlantsToDropdown", lambda plants: print(f"  [UI] seed bag: {plants}"))
# pushAction = globals().get(
#     "pushAction", lambda action: print(f"  [UI] action: {action}"))
# showMessage = globals().get(
#     "showMessage", lambda text: print(f"  [UI] message: {text}"))
# clearGarden = globals().get(
#     "clearGarden", lambda: print("  [UI] garden cleared"))
 
# GARDEN_SIZE = 5
 
 
# class StaticArray2D:
#     """Fixed-size 2D array. rows x cols is decided once and never changes."""
 
#     def __init__(self, rows, cols, fill=None):
#         if rows < 1 or cols < 1:
#             raise ValueError("rows and cols must be at least 1")
#         self.rows = rows
#         self.cols = cols
#         self._fill = fill
#         self.count = 0  # how many cells hold a value
#         # A comprehension builds a NEW list for every row.
#         # [[fill] * cols] * rows would repeat ONE row, so changing one
#         # cell would change the same column in every row.
#         self._data = [[fill for _ in range(cols)] for _ in range(rows)]
 
#     def _check(self, r, c):
#         if not (0 <= r < self.rows and 0 <= c < self.cols):
#             raise IndexError(
#                 f"({r}, {c}) is outside the fixed {self.rows}x{self.cols} array")
 
#     def get(self, r, c):            # O(1)
#         self._check(r, c)
#         return self._data[r][c]
 
#     def set(self, r, c, value):     # O(1)
#         self._check(r, c)
#         was_empty = self._data[r][c] == self._fill
#         will_be_empty = value == self._fill
#         if was_empty and not will_be_empty:
#             self.count += 1
#         elif not was_empty and will_be_empty:
#             self.count -= 1
#         self._data[r][c] = value
 
#     def is_full(self):
#         return self.count == self.rows * self.cols
 
#     def __str__(self):
#         return "\n".join(
#             " ".join(f"{str(v) if v != self._fill else '.':>9}" for v in row)
#             for row in self._data)
 
 
# class DynamicArray2D:
#     """Growable 2D array. Set a cell outside the current size and it resizes."""
 
#     def __init__(self, rows=2, cols=2, fill=None):
#         if rows < 1 or cols < 1:
#             raise ValueError("rows and cols must be at least 1")
#         self.rows = rows
#         self.cols = cols
#         self._fill = fill
#         self.resize_count = 0  # how many times it had to grow
#         self._data = [[fill for _ in range(cols)] for _ in range(rows)]
 
#     def get(self, r, c):            # O(1) - reading never grows the array
#         if not (0 <= r < self.rows and 0 <= c < self.cols):
#             raise IndexError(f"({r}, {c}) is outside the current "
#                              f"{self.rows}x{self.cols} array")
#         return self._data[r][c]
 
#     def set(self, r, c, value):     # O(1), or O(rows*cols) when it must grow
#         if r < 0 or c < 0:
#             raise IndexError("negative positions are not allowed")
#         if r >= self.rows or c >= self.cols:
#             new_rows, new_cols = self.rows, self.cols
#             while new_rows <= r:    # doubling means resizes get rarer
#                 new_rows *= 2
#             while new_cols <= c:
#                 new_cols *= 2
#             self._resize(new_rows, new_cols)
#         self._data[r][c] = value
 
#     def add_row(self):              # O(cols)
#         self._data.append([self._fill for _ in range(self.cols)])
#         self.rows += 1
 
#     def add_col(self):              # O(rows)
#         for row in self._data:
#             row.append(self._fill)
#         self.cols += 1
 
#     def _resize(self, new_rows, new_cols):
#         # Build a bigger array and copy every old cell across: O(rows*cols)
#         new_data = [[self._fill for _ in range(new_cols)] for _ in range(new_rows)]
#         for r in range(self.rows):
#             for c in range(self.cols):
#                 new_data[r][c] = self._data[r][c]
#         self._data = new_data
#         self.rows, self.cols = new_rows, new_cols
#         self.resize_count += 1
 
#     def __str__(self):
#         return "\n".join(
#             " ".join(f"{str(v) if v != self._fill else '.':>9}" for v in row)
#             for row in self._data)
 
 
# def position_of(row, col):
#     """Row-major index used by the on-screen garden grid."""
#     return row * GARDEN_SIZE + col
 
 
# def plant(array2d, row, col, name, show=True):
#     """Store a plant in the array. If show=True, also update the simulator."""
#     array2d.set(row, col, name)
#     if show:
#         pushAction(f"Planted {name} at ({row}, {col})")
#         addPlantToGrid(position_of(row, col), name)
#     else:
#         print(f"  {name} stored at ({row}, {col})")
 
 
# # The array behind the on-screen garden. It lives at module level so
# # on_cell_click can use it every time you click a tile.
# beds = StaticArray2D(GARDEN_SIZE, GARDEN_SIZE)
 
 
# def on_cell_click(pos, crop):
#     """Called by the simulator when you click a tile.
#     pos  = 0-24 (row * 5 + col)      crop = the seed chosen in the Seed Bag
#     """
#     row, col = divmod(pos, GARDEN_SIZE)
#     if not crop:
#         showMessage("Pick a seed from the Seed Bag first")
#         return
#     if beds.get(row, col) is not None:
#         showMessage(f"({row}, {col}) already has {beds.get(row, col)}")
#         return
#     plant(beds, row, col, crop)
#     if beds.is_full():
#         showMessage("The garden is full!")
 
 
# if __name__ == "__main__":
#     clearGarden()  # start with an empty screen every time you press Run
#     addPlantsToDropdown([
#         ("Eggplant", "🍆", 20),
#         ("Apples", "🍎", 50),
#         ("Banana", "🍌", 10),
#         ("Melon", "🍈", 30),
#         ("Pineapple", "🍍", 70),
#     ])
 
#     # ---- Static: this array is the garden you can click ----
#     print("=== STATIC 2D ARRAY (5 x 5, fixed size) ===")
#     plant(beds, 0, 0, "Eggplant")
#     plant(beds, 0, 1, "Apples")
#     plant(beds, 2, 2, "Banana")
#     print(beds)
#     print(f"Cells used: {beds.count} of {GARDEN_SIZE * GARDEN_SIZE}")
#     try:
#         plant(beds, 5, 0, "Melon")  # row 5 does not exist in a 5x5 array
#     except IndexError as error:
#         print("Blocked:", error)
 
#     # ---- Dynamic: console only (it can outgrow the 5x5 screen) ----
#     print()
#     print("=== DYNAMIC 2D ARRAY (starts 2 x 2, grows) ===")
#     field = DynamicArray2D(2, 2)
#     print(f"Start: {field.rows}x{field.cols}")
#     plant(field, 0, 0, "Eggplant", show=False)
#     plant(field, 1, 1, "Apples", show=False)
#     plant(field, 3, 2, "Pineapple", show=False)  # outside 2x2, so it grows
#     print(f"After growing: {field.rows}x{field.cols} "
#           f"(resized {field.resize_count} time(s))")
#     field.add_row()
#     field.add_col()
#     print(f"After add_row + add_col: {field.rows}x{field.cols}")
#     print(field)
 
#     showMessage("Ready. Pick a seed, then click a soil tile.")
