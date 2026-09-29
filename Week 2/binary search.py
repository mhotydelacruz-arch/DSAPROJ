# class AnimalNode:
#     def __init__(self, age, name, emoji):
#         self.age = age
#         self.name = name
#         self.emoji = emoji
#         self.health = 100
#         self.thirst = 100
#         self.left = None
#         self.right = None

# class PoultryBST:
#     def __init__(self):
#         self.root = None
#         self.size = 0

#     def insert(self, age, name, emoji):
#         self.root = self._insert(self.root, age, name, emoji)
#         self.size += 1

#     def _insert(self, node, age, name, emoji):
#         if node is None:
#             return AnimalNode(age, name, emoji)
#         if age < node.age:
#             node.left = self._insert(node.left, age, name, emoji)
#         else:
#             node.right = self._insert(node.right, age, name, emoji)
#         return node

#     def in_order(self):
#         animals = []
#         self._in_order(self.root, animals)
#         return animals

#     def _in_order(self, node, animals):
#         if node is None:
#             return
#         self._in_order(node.left, animals)
#         animals.append(node)
#         self._in_order(node.right, animals)

#     def feed_all(self, amount=15):
#         for animal in self.in_order():
#             animal.health = min(100, animal.health + amount)

#     def water_all(self, amount=15):
#         for animal in self.in_order():
#             animal.thirst = min(100, animal.thirst + amount)

#     def find_milking_cow(self):
#         for animal in self.in_order():
#             if animal.name == "Milking Cow":
#                 return animal
#         return None

#     def delete(self, age):
#         self.root, removed = self._delete(self.root, age)
#         if removed:
#             self.size -= 1
#         return removed

#     def _delete(self, node, age):
#         if node is None:
#             return None, False
#         if age < node.age:
#             node.left, removed = self._delete(node.left, age)
#             return node, removed
#         if age > node.age:
#             node.right, removed = self._delete(node.right, age)
#             return node, removed
#         if node.left is None:
#             return node.right, True
#         if node.right is None:
#             return node.left, True
#         successor = node.right
#         while successor.left is not None:
#             successor = successor.left
#         node.age, node.name, node.emoji = successor.age, successor.name, successor.emoji
#         node.health, node.thirst = successor.health, successor.thirst
#         node.right, _ = self._delete(node.right, successor.age)
#         return node, True

#     def harvest_oldest_for_meat(self):
#         candidates = [a for a in self.in_order() if a.name != "Milking Cow"]
#         if not candidates:
#             return None
#         oldest = candidates[-1]
#         snapshot = AnimalNode(oldest.age, oldest.name, oldest.emoji)
#         self.delete(oldest.age)
#         return snapshot

# coop = PoultryBST()
# ANIMAL_EMOJI = {"Chicken": "🐔", "Cow": "🐄", "Pig": "🐖", "Milking Cow": "🐮"}

# addAnimalsToDropdown([
#     ("Chicken", "🐔", 5),
#     ("Cow", "🐄", 25),
#     ("Pig", "🐖", 15),
#     ("Milking Cow", "🐮", 30),
# ])

# def refresh_coop_grid():
#     clearPoultry()
#     for i, animal in enumerate(coop.in_order()):
#         if i >= 4:
#             break
#         addAnimalToGrid(i, animal.name)

# def on_poultry_cell_click(pos, animal):
#     import random
#     age = random.randint(1, 200)
#     coop.insert(age, animal, ANIMAL_EMOJI.get(animal, "🐣"))
#     pushAction(f"Added {animal} (age {age})")
#     refresh_coop_grid()

# def on_poultry_feed():
#     coop.feed_all(15)
#     pushAction("Fed the whole coop (+15 health each)")
#     showMessage("Everyone's fed!")

# def on_poultry_drink():
#     coop.water_all(15)
#     pushAction("Watered the whole coop (+15 thirst each)")
#     showMessage("Trough refilled!")

# def on_poultry_process_meat():
#     harvested = coop.harvest_oldest_for_meat()
#     if harvested:
#         pushAction(f"Processed {harvested.name} for meat (age {harvested.age})")
#         showMessage(f"Processed {harvested.name} (age {harvested.age}) for meat.")
#     else:
#         showMessage("No meat-ready animals in the coop.")
#     refresh_coop_grid()

# def on_poultry_milk():
#     cow = coop.find_milking_cow()
#     if cow:
#         pushAction(f"Milked the Milking Cow (age {cow.age})")
#         showMessage(f"Collected milk from the Milking Cow (age {cow.age}).")
#     else:
#         showMessage("No Milking Cow in the coop yet.")

# refresh_coop_grid()

# fish_pond = []

# addFishToDropdown([
#     ("Fish", "🐟", 8),
# ])

# def refresh_pond_grid():
#     clearFish()
#     for i, fish in enumerate(fish_pond):
#         if i >= 4:
#             break
#         addFishToGrid(i, fish["name"])

# def on_fish_cell_click(pos, fish):
#     fish_pond.append({"name": fish, "health": 100})
#     pushAction(f"Stocked {fish}")
#     refresh_pond_grid()

# def on_fish_feed():
#     for fish in fish_pond:
#         fish["health"] = min(100, fish["health"] + 15)
#     pushAction("Fed the whole pond (+15 health each)")
#     showMessage("Pond fed!")

# def on_fish_process_meat():
#     if not fish_pond:
#         showMessage("Pond is empty.")
#         return
#     harvested = fish_pond.pop(0)
#     pushAction(f"Processed {harvested['name']} for meat")
#     showMessage(f"Processed {harvested['name']} for meat.")
#     refresh_pond_grid()

# refresh_pond_grid()