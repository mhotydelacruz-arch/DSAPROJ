"""01 — OOP: Plant and resource inventory for Garden Sanctuary.

The CROP_BOOK and addPlantsToDropdown function match the game's plant catalog.
Run this file directly for a small presentation demonstration.
"""

# DATA STRUCTURE: dictionary/hash map. Crop names map to their metadata for
# average O(1) lookup of emoji, seed cost, watering requirement, and growth.
CROP_BOOK = {
    "Eggplant": {"emoji": "🍆", "seed_cost": 20, "water_need": 14, "days": 2, "yield": 3, "sell": 34, "unlock": 1},
    "Apples": {"emoji": "🍎", "seed_cost": 50, "water_need": 20, "days": 4, "yield": 2, "sell": 72, "unlock": 1},
    "Banana": {"emoji": "🍌", "seed_cost": 10, "water_need": 10, "days": 2, "yield": 4, "sell": 20, "unlock": 1},
    "Melon": {"emoji": "🍈", "seed_cost": 30, "water_need": 18, "days": 3, "yield": 2, "sell": 52, "unlock": 1},
    "Pineapple": {"emoji": "🍍", "seed_cost": 70, "water_need": 24, "days": 4, "yield": 2, "sell": 108, "unlock": 1},
    "Carrot": {"emoji": "🥕", "seed_cost": 7, "water_need": 10, "days": 2, "yield": 3, "sell": 12, "unlock": 1},
    "Berry": {"emoji": "🍓", "seed_cost": 10, "water_need": 12, "days": 2, "yield": 3, "sell": 17, "unlock": 1},
    "Sunflower": {"emoji": "🌻", "seed_cost": 12, "water_need": 14, "days": 3, "yield": 2, "sell": 24, "unlock": 1},
    "Pumpkin": {"emoji": "🎃", "seed_cost": 16, "water_need": 18, "days": 3, "yield": 2, "sell": 32, "unlock": 1},
}

# DATA STRUCTURE: list of tuples; each tuple supplies the displayed name,
# emoji, and seed price to the plant dropdown.
PLANT_DROPDOWN = [
    ("Eggplant", "🍆", 20),
    ("Apples", "🍎", 50),
    ("Banana", "🍌", 10),
    ("Melon", "🍈", 30),
    ("Pineapple", "🍍", 70),
    ("Carrot", "🥕", 7),
    ("Berry", "🍓", 10),
    ("Sunflower", "🌻", 12),
    ("Pumpkin", "🎃", 16),
]


def addPlantsToDropdown(items=PLANT_DROPDOWN):
    """Return UI-ready plant options from (name, emoji, seed-cost) tuples."""
    options = []
    for name, emoji, cost in items:
        metadata = CROP_BOOK[name]
        options.append({
            "name": name,
            "emoji": emoji,
            "seed_cost": cost,
            "water_need": metadata["water_need"],
            "days": metadata["days"],
            "yield": metadata["yield"],
            "sell": metadata["sell"],
            "unlock": metadata["unlock"],
        })
    return options


# DATA STRUCTURE: OOP. Plant encapsulates the properties and behavior of one plant.
class Plant:
    def __init__(self, name, water_need=None):
        if name not in CROP_BOOK:
            raise ValueError(f"Unknown plant: {name}")
        self.name = name
        self.water_need = water_need if water_need is not None else CROP_BOOK[name]["water_need"]
        self.health = 100

    def water(self, resources):
        """Spend this plant's water requirement and restore its health."""
        if not resources.take("water", self.water_need):
            return False
        self.health = min(100, self.health + 10)
        return True

    def __repr__(self):
        return (f"Plant(name={self.name!r}, water_need={self.water_need}, "
                f"health={self.health})")


# DATA STRUCTURE: OOP inventory object; the items dictionary is a hash map.
class ResourceBag:
    def __init__(self, water=200, seeds=90, energy=110, hope=80, coins=999):
        self.items = {
            "water": water,
            "seeds": seeds,
            "energy": energy,
            "hope": hope,
            "coins": coins,
            **{crop_name: 0 for crop_name in CROP_BOOK},
        }

    def amount(self, name):
        return self.items.get(name, 0)

    def take(self, name, quantity=1):
        if quantity < 0 or self.amount(name) < quantity:
            return False
        self.items[name] = self.amount(name) - quantity
        return True

    def add(self, name, quantity=1):
        if quantity < 0:
            raise ValueError("quantity must be non-negative")
        self.items[name] = self.amount(name) + quantity

    def updateResources(self, water=200, seeds=90, energy=110, hope=80, coins=999):
        """Set resources using the values shown in the game example."""
        self.items.update({
            "water": water,
            "seeds": seeds,
            "energy": energy,
            "hope": hope,
            "coins": coins,
        })

    def __repr__(self):
        return f"ResourceBag({self.items})"


if __name__ == "__main__":
    resources = ResourceBag()
    eggplant = Plant("Eggplant")
    print("Congratulations!, you created a plant!")
    print(eggplant)
    print("Starting resources:", resources)
    print("Watered successfully:", eggplant.water(resources))
    print("Updated plant:", eggplant)
    print("Updated water:", resources.amount("water"))
    print("Resource Storage and Plant Dropdown is Unlocked!")
    print("Plant choices:", [option["name"] for option in addPlantsToDropdown()])
