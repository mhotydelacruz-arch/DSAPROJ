"""
Inventory — fixed-capacity static array
Demonstrates scarcity (Hay Day silo / barn capacity).
"""


class Inventory:
    """Fixed-size slots. Capacity never grows."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.slots = [None] * capacity  # static array behaviour

    def add_item(self, item) -> bool:
        """O(n) scan for first free slot. Returns False if full."""
        try:
            idx = self.slots.index(None)
            self.slots[idx] = item
            return True
        except ValueError:
            return False

    def remove_at(self, index: int):
        if not (0 <= index < self.capacity):
            return None
        item = self.slots[index]
        self.slots[index] = None
        return item

    @property
    def is_full(self) -> bool:
        return None not in self.slots

    @property
    def count(self) -> int:
        return sum(1 for s in self.slots if s is not None)

    def __repr__(self):
        return f"Inventory({self.count}/{self.capacity}) {self.slots}"


if __name__ == "__main__":
    inv = Inventory(4)
    print(inv.add_item("egg"))
    print(inv.add_item("milk"))
    print(inv)
    print(inv.is_full)  # False