"""Garden Sanctuary plant-lookup hash table.

Maps farm plot coordinates (row, column) to a plant's live data: crop name,
health, water need/current water level, sunlight requirement, and growth.
Separate chaining handles index collisions. The table rehashes (grows and
re-indexes all entries) when its load factor rises above 0.75.

This is an educational hash-table implementation, not Python's built-in dict.
"""
from copy import deepcopy
from typing import Any, Dict, Iterable, List, Optional, Tuple

Coordinate = Tuple[int, int]


class PlantLookupHashTable:
    def __init__(self, capacity: int = 7, max_load: float = 0.75):
        self.capacity = max(3, int(capacity))
        self.max_load = float(max_load)
        self.buckets: List[list] = [[] for _ in range(self.capacity)]
        self.size = 0
        self.collision_events = 0
        self.rehash_count = 0
        self.last_rehash: Optional[Dict[str, int]] = None

    @staticmethod
    def _coordinate(key: Coordinate) -> Coordinate:
        if len(key) != 2:
            raise ValueError("A plot key must be (row, column).")
        row, column = int(key[0]), int(key[1])
        if row < 0 or column < 0:
            raise ValueError("Plot row and column must be non-negative.")
        return row, column

    @staticmethod
    def _stable_hash(key: Coordinate) -> int:
        """A small deterministic coordinate hash for clear classroom examples."""
        row, column = PlantLookupHashTable._coordinate(key)
        return row * 31 + column * 17 + row * column * 13

    def _index(self, key: Coordinate) -> int:
        return self._stable_hash(key) % self.capacity

    def _find_entry(self, key: Coordinate):
        normalized = self._coordinate(key)
        for entry in self.buckets[self._index(normalized)]:
            if entry["key"] == normalized:
                return entry
        return None

    def get(self, key: Coordinate) -> Optional[dict]:
        """Look up one coordinate by hashing it and searching its short chain."""
        entry = self._find_entry(key)
        return deepcopy(entry["value"]) if entry else None

    def set(self, key: Coordinate, plant_data: dict) -> Optional[Dict[str, int]]:
        """Insert or update a plant; return rehash information when resized."""
        key = self._coordinate(key)
        entry = self._find_entry(key)
        if entry:
            entry["value"] = deepcopy(plant_data)
            return None

        resize = None
        if (self.size + 1) / self.capacity > self.max_load:
            resize = self.rehash(self.capacity * 2 + 1)
        bucket = self.buckets[self._index(key)]
        if bucket:
            self.collision_events += 1
        bucket.append({"key": key, "value": deepcopy(plant_data)})
        self.size += 1
        return resize

    def remove(self, key: Coordinate) -> Optional[dict]:
        """Delete a plot mapping (for example, when its crop is harvested)."""
        key = self._coordinate(key)
        bucket = self.buckets[self._index(key)]
        for index, entry in enumerate(bucket):
            if entry["key"] == key:
                removed = bucket.pop(index)
                self.size -= 1
                return deepcopy(removed["value"])
        return None

    def rehash(self, new_capacity: int) -> Dict[str, int]:
        """Grow the bucket array and re-index every plot mapping."""
        old_capacity = self.capacity
        entries = [entry for bucket in self.buckets for entry in bucket]
        self.capacity = max(3, int(new_capacity))
        self.buckets = [[] for _ in range(self.capacity)]
        for entry in entries:
            self.buckets[self._index(entry["key"])].append(entry)
        self.rehash_count += 1
        info = {"from": old_capacity, "to": self.capacity, "entries": len(entries)}
        self.last_rehash = info
        return info

    def sync_plots(self, plots: Iterable[Tuple[Coordinate, dict]]) -> None:
        """Synchronize records from the farm grid without rebuilding unchanged keys."""
        incoming = {self._coordinate(key): data for key, data in plots if data}
        existing_keys = [entry["key"] for bucket in self.buckets for entry in bucket]
        for key in existing_keys:
            if key not in incoming:
                self.remove(key)
        for key, data in incoming.items():
            self.set(key, data)

    def entries(self) -> List[dict]:
        """Return all records with their current bucket index for display."""
        result = []
        for bucket_index, bucket in enumerate(self.buckets):
            for entry in bucket:
                row, column = entry["key"]
                result.append({"row": row, "column": column, "plot": row * 5 + column + 1,
                               "bucket": bucket_index, **deepcopy(entry["value"])})
        return sorted(result, key=lambda item: item["plot"])

    def groups(self) -> List[dict]:
        """Return non-empty buckets with chain nodes for an educational UI."""
        result = []
        for index, bucket in enumerate(self.buckets):
            if bucket:
                result.append({"index": index, "collision": len(bucket) > 1,
                               "entries": [{"key": list(entry["key"]),
                                            "plot": entry["key"][0] * 5 + entry["key"][1] + 1,
                                            "value": deepcopy(entry["value"])}
                                           for entry in bucket]})
        return result

    def summary(self) -> dict:
        return {"capacity": self.capacity, "size": self.size,
                "load_factor": round(self.size / self.capacity, 2),
                "collision_buckets": sum(len(bucket) > 1 for bucket in self.buckets),
                "collision_events": self.collision_events,
                "rehash_count": self.rehash_count,
                "last_rehash": deepcopy(self.last_rehash),
                "entries": self.entries(), "buckets": self.groups()}

    def state_data(self) -> dict:
        """Persist table sizing/history; plant entries are rebuilt from saved plots."""
        return {"capacity": self.capacity, "collision_events": self.collision_events,
                "rehash_count": self.rehash_count, "last_rehash": deepcopy(self.last_rehash)}


if __name__ == "__main__":
    garden = PlantLookupHashTable(capacity=7)
    for row in range(3):
        for column in range(3):
            garden.set((row, column), {
                "crop": "Carrot", "health": 100, "water_need": 10,
                "water_level": 0, "sunlight_need": 6, "growth": 0,
            })
    print("Lookup plot (1, 2):", garden.get((1, 2)))
    print("Table summary:", garden.summary())
    print("Separate-chaining buckets:", garden.groups())
