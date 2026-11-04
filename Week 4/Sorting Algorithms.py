"""Garden Sanctuary sorting algorithms.

Insertion Sort: sorts the player's small harvested-inventory list by weight,
current value, or crop growth duration.
Merge Sort: stably ranks the seasonal leaderboard and sorts prices during
stable trading.
Quick Sort: sorts the dynamic price board during a market crash.

Each function returns a new list and leaves its input unchanged.
"""
from typing import Any, Callable, Iterable, List, TypeVar

T = TypeVar("T")


def insertion_sort(items: Iterable[T], key: Callable[[T], Any], reverse: bool = False) -> List[T]:
    """Stable insertion sort; suitable for short inventory lists. O(n^2)."""
    result = list(items)
    for index in range(1, len(result)):
        current = result[index]
        position = index - 1
        while position >= 0:
            previous_key = key(result[position])
            current_key = key(current)
            out_of_order = previous_key < current_key if reverse else previous_key > current_key
            if not out_of_order:
                break
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current
    return result


def merge_sort(items: Iterable[T], key: Callable[[T], Any], reverse: bool = False) -> List[T]:
    """Stable merge sort; O(n log n), useful for fair leaderboard ranking."""
    values = list(items)
    if len(values) < 2:
        return values
    middle = len(values) // 2
    left = merge_sort(values[:middle], key, reverse)
    right = merge_sort(values[middle:], key, reverse)
    merged: List[T] = []
    left_index = right_index = 0
    while left_index < len(left) and right_index < len(right):
        left_key, right_key = key(left[left_index]), key(right[right_index])
        left_first = left_key >= right_key if reverse else left_key <= right_key
        if left_first:  # On ties, take the left item to preserve original order.
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def quick_sort(items: Iterable[T], key: Callable[[T], Any], reverse: bool = False) -> List[T]:
    """In-place partitioning Quick Sort on a copy; average O(n log n)."""
    result = list(items)

    def partition(low: int, high: int) -> int:
        pivot = key(result[(low + high) // 2])
        left, right = low, high
        while left <= right:
            if reverse:
                while key(result[left]) > pivot:
                    left += 1
                while key(result[right]) < pivot:
                    right -= 1
            else:
                while key(result[left]) < pivot:
                    left += 1
                while key(result[right]) > pivot:
                    right -= 1
            if left <= right:
                result[left], result[right] = result[right], result[left]
                left += 1
                right -= 1
        return left

    def sort_range(low: int, high: int) -> None:
        if low >= high:
            return
        split = partition(low, high)
        if low < split - 1:
            sort_range(low, split - 1)
        if split < high:
            sort_range(split, high)

    if result:
        sort_range(0, len(result) - 1)
    return result


if __name__ == "__main__":
    harvest = [
        {"crop": "Carrot", "weight": 0.12, "value": 12, "days": 2},
        {"crop": "Pumpkin", "weight": 2.0, "value": 32, "days": 3},
        {"crop": "Berry", "weight": 0.03, "value": 17, "days": 2},
    ]
    print("Inventory by heaviest first:", [row["crop"] for row in insertion_sort(harvest, key=lambda row: row["weight"], reverse=True)])
    print("Stable-market prices:", [row["crop"] for row in merge_sort(harvest, key=lambda row: row["value"], reverse=True)])
    print("Market-crash prices:", [row["crop"] for row in quick_sort(harvest, key=lambda row: row["value"], reverse=True)])
