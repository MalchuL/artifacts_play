import copy
from typing import Dict

from src.errors import CharacterInventoryFullException
from src.playground.inventory import Inventory
from src.playground.item import Item, Items


class LocalInventory(Inventory):
    def __init__(self, capacity: int, max_inventory_size: int):
        self._items: Dict[str, Items] = {}
        self.max_inventory_size = max_inventory_size
        self.capacity = capacity

    def get_items_quantity(self):
        quantity = 0
        for item in self._items.values():
            quantity += item.quantity
        return quantity

    def is_possible_to_add_item(self, item: Item, added_quantity: int):
        new_items_len = len(self._items)
        if item.code in self._items:
            new_items_len += 1
        new_quantity = self.get_items_quantity() + added_quantity
        return new_items_len <= self.capacity and new_quantity <= self.max_inventory_size

    def is_inventory_full(self):
        return len(self._items) == self.capacity or \
            self.get_items_quantity() == self.max_inventory_size

    def add_item(self, items: Items):
        if items.quantity <= 0:
            raise ValueError("Items quantity must be greater than 0.")
        if not self.is_possible_to_add_item(items.item, items.quantity):
            raise CharacterInventoryFullException("Character inventory is full.")
        item_code = items.item.code
        if item_code in self._items:
            self._items[item_code].quantity += items.quantity
        else:
            self._items[item_code] = copy.deepcopy(items)

    def take_items(self, item: Item, amount: int) -> Items:
        if item.code in self._items and self._items[item.code].quantity <= amount and amount > 0:
            items = Items(item, amount)
            self._items[item.code].quantity -= amount
            if self._items[item.code].quantity <= 0:
                del self._items[item.code]
            return items
        else:
            raise NotImplementedError("This error is not implemented")  # TODO specify exception

    def get_items(self) -> Dict[str, Items]:
        return copy.deepcopy(self._items)

    def clear(self):
        items = self._items
        self._items = {}
        return items

    def __repr__(self):
        return f"Inventory(capacity={self.capacity}, max_inventory_size={self.max_inventory_size}, items={list(self._items.values())})"
