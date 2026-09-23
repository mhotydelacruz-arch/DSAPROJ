# import asyncio
# from collections import deque
# from js import document
# from pyodide.ffi import create_proxy

# DAY_SECONDS = 120   # one real "day" = 120 seconds

# # name: (emoji, seed cost, days to grow, sell price)
# CROPS = {
#     "Tomato":   ("🍅", 10, 3, 25),
#     "Corn":     ("🌽", 15, 4, 40),
#     "Carrot":   ("🥕", 5, 2, 12),
#     "Eggplant": ("🍆", 20, 5, 60),
# }
# WATER_COST = 5
# state = {"water": 200, "seeds": 90, "energy": 110, "hope": 65, "coins": 120, "day": 1}
# countdown = {"t": DAY_SECONDS}

# # ---------- Tree: Garden -> Rows -> Plots ----------
# class Node:
#     def __init__(self, name, pos=None):
#         self.name, self.pos = name, pos
#         self.children, self.plant = [], None

# root = Node("Garden")
# plots = []
# for r in range(5):
#     row = Node(f"Row {r}")
#     root.children.append(row)
#     for c in range(5):
#         plot = Node(f"Plot {r*5+c}", r*5+c)
#         row.children.append(plot)
#         plots.append(plot)

# def dfs(node):                       # depth-first: row by row
#     stack = [node]
#     while stack:
#         n = stack.pop()
#         if n.pos is not None:
#             yield n
#         stack.extend(reversed(n.children))

# def bfs(node):                       # breadth-first: level by level
#     q = deque([node])
#     while q:
#         n = q.popleft()
#         if n.pos is not None:
#             yield n
#         q.extend(n.children)

# # ---------- Display ----------
# def refresh():
#     s = state
#     updateResources(s["water"], s["seeds"], s["energy"], s["hope"], s["coins"])
#     document.getElementById("day-counter").innerText = str(s["day"])

# def is_ripe(p):
#     return p["growth"] >= CROPS[p["crop"]][2]

# def draw_all():
#     # Tile shows 🌱 while growing (unknown name) and the crop emoji when ripe.
#     # Hover a tile to see progress and water status.
#     clearGarden()
#     for plot in dfs(root):
#         p = plot.plant
#         if not p:
#             continue
#         days = CROPS[p["crop"]][2]
#         if is_ripe(p):
#             name = p["crop"]
#         else:
#             name = f'{p["crop"]} {p["growth"]}/{days} days ' + ("💧 watered" if p["watered"] else "(needs water)")
#         addPlantToGrid(plot.pos, name)

# # ---------- Actions ----------
# def plant(plot, crop):
#     cost = CROPS[crop][1]
#     if state["coins"] < cost:  showMessage("Not enough coins!"); return
#     if state["seeds"] < 1:     showMessage("Out of seeds!"); return
#     state["coins"] -= cost     # coins go down when you plant
#     state["seeds"] -= 1
#     plot.plant = {"crop": crop, "growth": 0, "watered": False}
#     pushAction(f"Planted {crop} at {plot.pos} (-{cost}c)")

# def water(plot):
#     p = plot.plant
#     if p["watered"]:                showMessage("Already watered today"); return
#     if state["water"] < WATER_COST: showMessage("Water reserves empty!"); return
#     state["water"] -= WATER_COST
#     p["watered"] = True
#     pushAction(f'Watered {p["crop"]} at {plot.pos} (-{WATER_COST}L)')

# def harvest(plot):
#     crop = plot.plant["crop"]
#     price = CROPS[crop][3]
#     state["coins"] += price
#     state["hope"] = min(100, state["hope"] + 2)
#     plot.plant = None
#     pushAction(f"Harvested {crop} at {plot.pos} (+{price}c)")

# def next_day():
#     state["day"] += 1
#     for plot in dfs(root):                     # visit every plot with DFS
#         p = plot.plant
#         if p and p["watered"] and not is_ripe(p):   # only watered plants grow
#             p["growth"] += 1
#         if p:
#             p["watered"] = False
#     state["water"] = min(200, state["water"] + 30)  # daily rain / refill
#     pushAction(f'Day {state["day"]} began')
#     showMessage(f'Day {state["day"]}')
#     refresh()
#     draw_all()

# # One tool, decided by what is on the tile:
# #   empty -> plant | growing -> water | ripe -> harvest
# def on_cell_click(pos, crop):
#     plot = plots[pos]
#     p = plot.plant
#     if p is None:
#         plant(plot, crop)
#     elif is_ripe(p):
#         harvest(plot)
#     else:
#         water(plot)
#     refresh()
#     draw_all()

# # ---------- Real-time day clock ----------
# def skip_day():
#     countdown["t"] = DAY_SECONDS
#     next_day()

# def make_button():
#     old = document.getElementById("next-day-btn")
#     if old:
#         old.remove()
#     btn = document.createElement("button")
#     btn.id = "next-day-btn"
#     btn.className = "bg-amber-600 hover:bg-amber-500 text-white text-sm font-bold rounded-xl px-3 py-2"
#     btn.textContent = f"☀ Next Day ({DAY_SECONDS}s)"
#     btn.addEventListener("click", create_proxy(lambda e: skip_day()))
#     document.getElementById("crop-selector").parentElement.appendChild(btn)
#     return btn

# async def day_loop(btn):
#     try:
#         while True:
#             await asyncio.sleep(1)
#             countdown["t"] -= 1
#             if countdown["t"] <= 0:
#                 countdown["t"] = DAY_SECONDS
#                 next_day()
#             btn.textContent = f'☀ Next Day ({countdown["t"]}s)'
#     except asyncio.CancelledError:
#         pass

# # ---------- Setup ----------
# unlockFeature("resources"); unlockFeature("grid"); unlockFeature("stack")
# addPlantsToDropdown([[n, v[0], v[1]] for n, v in CROPS.items()])
# refresh()
# draw_all()

# old_task = globals().get("day_task")      # stop the clock from a previous Run
# if old_task:
#     old_task.cancel()
# day_task = asyncio.ensure_future(day_loop(make_button()))

# print("Garden tree ready:", len(plots), "plots under", len(root.children), "rows")
# print("Click empty soil = plant, growing plant = water, ripe plant = harvest.")
