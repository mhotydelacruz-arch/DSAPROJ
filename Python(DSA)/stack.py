"""
Stack (LIFO)
push / pop / peek → O(1)
Used in game for: Undo / Action History
"""


class Stack:
    """LIFO stack. push/pop/peek are all O(1)."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        return self._items[-1] if self._items else None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)


if __name__ == "__main__":
    s = Stack()
    s.push("place_coop")
    s.push("place_pond")
    print(s.pop())   # place_pond
    print(s.peek())  # place_coop
    print(len(s))    # 1