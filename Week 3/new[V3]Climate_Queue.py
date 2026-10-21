"""03 — Queue: FIFO weather forecasts for Garden Sanctuary."""
from collections import deque
import random


# DATA STRUCTURE: Queue, implemented with collections.deque.
# popleft() processes the oldest forecast first; append() adds a forecast at the back.
class ClimateQueue:
    WEATHER = ("Sunny", "Rain", "Cloudy", "Breezy")

    def __init__(self, forecasts=None):
        self._items = deque(forecasts or ["Rain", "Cloudy", "Sunny", "Breezy"])

    def peek(self):
        return list(self._items)

    def advance_day(self):
        """Remove today's oldest forecast, then enqueue tomorrow's forecast."""
        if not self._items:
            raise IndexError("cannot advance an empty climate queue")
        todays_weather = self._items.popleft()
        self._items.append(random.choice(self.WEATHER))
        return todays_weather

    def __len__(self):
        return len(self._items)


if __name__ == "__main__":
    climate = ClimateQueue(["Rain", "Cloudy", "Sunny"])
    print("Forecast before daybreak:", climate.peek())
    print("Today's weather:", climate.advance_day())
    print("Forecast after daybreak:", climate.peek())
