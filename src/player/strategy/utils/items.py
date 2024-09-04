from collections import defaultdict
from typing import List, Dict

from src.playground.items import Items, Item


def merge_items(list1: List[Items], list2: List[Items]) -> List[Items]:
    items_count: Dict[str, int] = defaultdict(int)
    for list_items in [list1, list2]:
        for items in list_items:
            if items.quantity > 0:
                items_count[items.item.code] += items.quantity
    return [Items(Item(item), quantity) for item, quantity in items_count.items()]


def subtract_items(list1: List[Items], list2: List[Items]) -> List[Items]:
    items_count: Dict[str, int] = defaultdict(int)
    for list_items, multiplier in [(list1, 1), (list2, -1)]:
        for items in list_items:
            if items.quantity > 0:
                items_count[items.item.code] += items.quantity * multiplier
    return [Items(Item(item), quantity) for item, quantity in items_count.items() if quantity > 0]
