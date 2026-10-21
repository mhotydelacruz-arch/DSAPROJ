"""02 — Stack: LIFO action history for the farm's Undo button."""
from copy import deepcopy


# DATA STRUCTURE: Stack, implemented with a Python list.
# append() pushes a record; pop() removes the most recently saved action (LIFO).
class ActionHistoryStack:
    def __init__(self):
        self._items = []

    def push(self, state_snapshot, action_name):
        record = (deepcopy(state_snapshot), action_name)
        self._items.append(record)

    def pop(self):
        """Return the latest (state, action) record, or None when empty."""
        return self._items.pop() if self._items else None

    def peek(self):
        return self._items[-1] if self._items else None

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)


if __name__ == "__main__":
    history = ActionHistoryStack()
    farm_state = {"coins": 999, "seeds": 90, "planted": []}

    history.push(farm_state, "Before planting Banana")
    farm_state["planted"].append("Banana")
    farm_state["seeds"] -= 1

    print("Current state:", farm_state)
    previous_state, undone_action = history.pop()
    print("Undo snapshot:", undone_action)
    print("Restored state:", previous_state)
    print("Actions remaining:", len(history))
