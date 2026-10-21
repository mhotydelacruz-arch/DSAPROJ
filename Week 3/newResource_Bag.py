"""01 — OOP: Plant and resource inventory for Garden Sanctuary."""

# DATA STRUCTURE: OOP. Plant encapsulates one plant's name, water requirement,
# and health as attributes on an object.
class Plant:
    def __init__(self, name, water_need):
        self.name = name
        self.water_need = water_need
        self.health = 100

    def water(self, resources):
        """Spend this plant's water requirement and restore plant health."""
        if not resources.take("water", self.water_need):
            return False
        self.health = min(100, self.health + 10)
        return True

    def __repr__(self):
        return (f"Plant(name={self.name!r}, water_need={self.water_need}, "
                f"health={self.health})")


# DATA STRUCTURE: OOP inventory object. Its resource dictionary is a hash map
# for average O(1) lookup and updates by resource name.
class ResourceBag:
    def __init__(self, water=200, seeds=90, energy=110, hope=80, coins=999):
        self.items = {
            "water": water,
            "seeds": seeds,
            "energy": energy,
            "hope": hope,
            "coins": coins,
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
        """Set resources using the same names and values as the game example."""
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
    eggplant = Plant("Eggplant", water_need=14)
    print("Congratulations!, you created a plant!")
    print(eggplant)
    print("Starting resources:", resources)
    print("Watered successfully:", eggplant.water(resources))
    print("Updated plant:", eggplant)
    print("Updated water:", resources.amount("water"))
