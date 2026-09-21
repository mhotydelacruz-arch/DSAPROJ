"""
Production Queue + Deque
FIFO (append / popleft) and front-priority (appendleft) for rush orders.
Both operations are O(1) thanks to collections.deque.
"""

from collections import deque


class ProductionQueue:
    """Wraps a deque to demonstrate FIFO and rush-order insertion."""

    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        """Normal order: back of the line. O(1)"""
        self._items.append(item)

    def enqueue_rush(self, item):
        """Rush order: jumps to the front. O(1)"""
        self._items.appendleft(item)

    def dequeue(self):
        """Remove from front. O(1) — unlike list.pop(0) which is O(n)"""
        if not self._items:
            return None
        return self._items.popleft()

    def front(self):
        return self._items[0] if self._items else None

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"ProductionQueue({list(self._items)})"


if __name__ == "__main__":
    q = ProductionQueue()
    q.enqueue("egg")
    q.enqueue("milk")
    q.enqueue_rush("fish")  # rush jumps to front
    print(q)                # fish, egg, milk
    print(q.dequeue())      # fish
    print(q.dequeue())      # egg