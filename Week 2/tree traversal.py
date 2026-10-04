# import asyncio
# import random
# from collections import deque
# from js import document
# from pyodide.ffi import create_proxy

# CROPS = {
#    "Apple":   ("🍎", 10, 3, 25),
#     "Corn":     ("🌽", 15, 4, 40),
#     "Carrot":   ("🥕", 5, 2, 12),
#     "Eggplant": ("🍆", 20, 5, 60),
#     "Melon":  ("🍈", 30, 3, 70),
#     "Pineaple": ("🍍", 70, 6, 50)
# }
# WATER_COST = 5
# PEST_EMOJI = "🐛"
# state = {"water": 200, "seeds": 90, "energy": 110, "hope": 65, "coins": 999}

# class Node:
#     def __init__(self, name, pos=None):
#         self.name, self.pos = name, pos
#         self.children = []
#         self.crop = None      # None = empty, or {"crop": name, "growth": int, "watered": bool}
#         self.pest = False     # pest is its OWN field -- never stored inside .crop

# root = Node("Garden")
# plots = []
# for r in range(5):
#     row = Node(f"Row {r}")
#     root.children.append(row)
#     for c in range(5):
#         plot = Node(f"Plot {r*5+c}", r*5+c)
#         row.children.append(plot)
#         plots.append(plot)

# def is_ripe(c):
#     return c["growth"] >= CROPS[c["crop"]][2]

# def refresh():
#     s = state
#     updateResources(s["water"], s["seeds"], s["energy"], s["hope"], s["coins"])

# def tile_label(plot):
#     # One function, two fields checked in order -- pest always wins the display,
#     # but it never touches plot.crop, so the two states can't get tangled.
#     if plot.pest:
#         return PEST_EMOJI
#     if plot.crop is None:
#         return ""
#     c = plot.crop
#     days = CROPS[c["crop"]][2]
#     if is_ripe(c):
#         return c["crop"]
#     return f'{c["crop"]} {c["growth"]}/{days} ' + ("💧" if c["watered"] else "(needs water)")

# def draw_all():
#     clearGarden()
#     for plot in plots:
#         label = tile_label(plot)
#         if label:
#             addPlantToGrid(plot.pos, label)

# def plant(plot, crop):
#     if plot.pest:
#         showMessage("Clear the pest here first.")
#         return
#     cost = CROPS[crop][1]
#     if state["coins"] < cost: showMessage("Not enough coins!"); return
#     if state["seeds"] < 1:    showMessage("Out of seeds!"); return
#     state["coins"] -= cost
#     state["seeds"] -= 1
#     plot.crop = {"crop": crop, "growth": 0, "watered": False}
#     pushAction(f"Planted {crop} at {plot.pos} (-{cost}c)")

# def water(plot):
#     c = plot.crop
#     if c["watered"]: showMessage("Already watered today"); return
#     if state["water"] < WATER_COST: showMessage("Water reserves empty!"); return
#     state["water"] -= WATER_COST
#     c["watered"] = True
#     pushAction(f'Watered {c["crop"]} at {plot.pos}')

# def harvest(plot):
#     crop = plot.crop["crop"]
#     price = CROPS[crop][3]
#     state["coins"] += price
#     plot.crop = None              # <- fully frees the tile, not just a flag flip
#     pushAction(f"Harvested {crop} at {plot.pos} (+{price}c)")

# def seed_outbreak(count=5):
#     empties = [p for p in plots if p.crop is None and not p.pest]
#     for plot in random.sample(empties, min(count, len(empties))):
#         plot.pest = True

# def clear_pest(plot):
#     plot.pest = False             # <- THE fix: only this field changes.
#     pushAction(f"Cleared pest at Plot {plot.pos}")   #   plot.crop was never touched,
#                                                       #   so the tile is plantable now.

# def on_cell_click(pos, crop):
#     plot = plots[pos]
#     if plot.pest:
#         clear_pest(plot)
#     elif plot.crop is None:
#         plant(plot, crop)
#     elif is_ripe(plot.crop):
#         harvest(plot)
#     else:
#         water(plot)
#     refresh()
#     draw_all()

# def dfs_preorder(node):
#     order, stack = [], [node]
#     while stack:
#         n = stack.pop()
#         if n.pos is not None: order.append(n)
#         stack.extend(reversed(n.children))
#     return order

# def bfs_order(node):
#     order, queue = [], deque([node])
#     while queue:
#         n = queue.popleft()
#         if n.pos is not None: order.append(n)
#         queue.extend(n.children)
#     return order

# async def sweep(order, label):
#     pushAction(f"{label} started")
#     for plot in order:
#         if plot.pest:
#             await asyncio.sleep(0.15)
#             clear_pest(plot)
#             draw_all()
#             await asyncio.sleep(0.05)
#     showMessage(f"{label} complete!")

# sweep_task = {"t": None}
# def run_sweep(mode):
#     old = sweep_task["t"]
#     if old and not old.done(): old.cancel()
#     fn, label = (dfs_preorder, "Preorder Sweep") if mode == "pre" else (bfs_order, "BFS Sweep")
#     sweep_task["t"] = asyncio.ensure_future(sweep(fn(root), label))

# def make_sweep_buttons():
#     toolbar = document.getElementById("garden-grid").parentElement
#     for bid, mode, text, color in [("pre-sweep-btn", "pre", "🔍 Preorder Sweep", "bg-sky-600 hover:bg-sky-500"),
#                                     ("bfs-sweep-btn", "bfs", "🌊 BFS Sweep", "bg-emerald-600 hover:bg-emerald-500")]:
#         old = document.getElementById(bid)
#         if old: old.remove()
#         btn = document.createElement("button")
#         btn.id = bid
#         btn.className = f"{color} text-white text-sm font-bold rounded-xl px-3 py-2 mt-2 mr-2"
#         btn.textContent = text
#         btn.addEventListener("click", create_proxy(lambda e, m=mode: run_sweep(m)))
#         toolbar.appendChild(btn)

# unlockFeature("resources"); unlockFeature("grid"); unlockFeature("stack")
# addPlantsToDropdown([[n, v[0], v[1]] for n, v in CROPS.items()])
# seed_outbreak()
# refresh()
# draw_all()
# make_sweep_buttons()

# print("Click a pest tile to clear it -- it becomes empty soil and is plantable again.")