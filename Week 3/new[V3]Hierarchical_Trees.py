# """05 — Hierarchical Trees: watering, harvesting, and day-transition actions."""


# # DATA STRUCTURE: Hierarchical Tree. Each ActionNode has a parent and can have
# # zero or more child nodes; actions execute from the root downward.
# class ActionNode:
#     def __init__(self, name, action=None, children=None):
#         self.name = name
#         self.action = action
#         self.children = children or []

#     def add_child(self, child):
#         self.children.append(child)


# # TREE ALGORITHM: recursively visit a node, then each child subtree.
# def run_action_tree(node, context):
#     print("Run:", node.name)
#     if node.action is not None and node.action(context) is False:
#         print("Stopped at:", node.name)
#         return False
#     for child in node.children:
#         if not run_action_tree(child, context):
#             return False
#     return True


# def build_watering_tree():
#     """Check plant -> check supplies -> water plant."""
#     def check_plant(context):
#         return context.get("plant") is not None

#     def check_water(context):
#         return context["water"] >= context["plant"].water_need

#     def water_plant(context):
#         plant = context["plant"]
#         context["water"] -= plant.water_need
#         plant.health = min(100, plant.health + 10)
#         print(f"Watered {plant.name}; health is now {plant.health}%.")
#         return True

#     return ActionNode("Watering", children=[
#         ActionNode("Check that a plant exists", check_plant),
#         ActionNode("Check water supply", check_water),
#         ActionNode("Apply water", water_plant),
#     ])


# def build_harvest_tree():
#     """Check crop -> check ripeness -> gather produce."""
#     def check_crop(context):
#         return context.get("plant") is not None

#     def check_ripe(context):
#         return context["growth"] >= context["days_to_grow"]

#     def gather(context):
#         plant = context["plant"]
#         context["produce"].append(plant.name)
#         context["plant"] = None
#         print("Harvested crop; produce basket:", context["produce"])
#         return True

#     return ActionNode("Harvesting", children=[
#         ActionNode("Check occupied plot", check_crop),
#         ActionNode("Check crop is ripe", check_ripe),
#         ActionNode("Gather harvest", gather),
#     ])


# def build_day_transition_tree():
#     """Advance weather, grow watered crops, handle pests, then start a new day."""
#     def climate_step(context):
#         forecast = context["forecast"]
#         context["weather"] = forecast.pop(0)
#         forecast.append("Sunny")  # Example forecast added to the back of the queue.
#         print("Weather:", context["weather"])
#         return True

#     def growth_step(context):
#         for plot in context["plots"]:
#             if plot.get("plant") and plot.get("watered"):
#                 plot["growth"] = min(plot["days_to_grow"], plot["growth"] + 1)
#                 plot["watered"] = False
#         print("Watered plots advanced by one growth day.")
#         return True

#     def pest_step(context):
#         context["pests_checked"] = True
#         print("Garden pest check complete.")
#         return True

#     def animal_step(context):
#         context["animals_aged"] = context.get("animals_aged", 0) + 1
#         print("Fish and poultry aged one day.")
#         return True

#     def sunrise(context):
#         context["day"] = context.get("day", 1) + 1
#         print("New day:", context["day"])
#         return True

#     return ActionNode("Two-minute day transition", children=[
#         ActionNode("Climate branch", children=[ActionNode("Advance forecast", climate_step)]),
#         ActionNode("Crop branch", children=[ActionNode("Grow watered plants", growth_step)]),
#         ActionNode("Pest branch", children=[ActionNode("Check for pests", pest_step)]),
#         ActionNode("Animal branch", children=[ActionNode("Age animals", animal_step)]),
#         ActionNode("Sunrise branch", children=[ActionNode("Start new day", sunrise)]),
#     ])


# if __name__ == "__main__":
#     from oop_plant_resources import Plant

#     print("--- Watering tree ---")
#     watering_context = {"plant": Plant("Melon", water_need=18), "water": 200}
#     run_action_tree(build_watering_tree(), watering_context)
#     print("Water remaining:", watering_context["water"])

#     print("\n--- Harvest tree ---")
#     harvest_context = {
#         "plant": Plant("Banana", water_need=10),
#         "growth": 2,
#         "days_to_grow": 2,
#         "produce": [],
#     }
#     run_action_tree(build_harvest_tree(), harvest_context)

#     print("\n--- Day-transition tree ---")
#     day_context = {
#         "forecast": ["Rain", "Cloudy"],
#         "plots": [{"plant": "Melon", "watered": True, "growth": 0, "days_to_grow": 3}],
#         "day": 1,
#         "animals_aged": 0,
#     }
#     run_action_tree(build_day_transition_tree(), day_context)
