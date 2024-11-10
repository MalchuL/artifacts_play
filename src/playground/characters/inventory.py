from abc import abstractmethod, ABC
from enum import Enum
from typing import Dict, List, Optional

from src.playground.items.item import Item, Items


class EquipmentSlot(Enum):
    WEAPON = "weapon"
    SHIELD = "shield"
    HELMET = "helmet"
    BODY_ARMOR = "body_armor"
    LEG_ARMOR = "leg_armor"
    BOOTS = "boots"
    RING1 = "ring1"
    RING2 = "ring2"
    AMULET = "amulet"
    ARTIFACT1 = "artifact1"
    ARTIFACT2 = "artifact2"
    ARTIFACT3 = "artifact3"
    UTILITY1 = "utility1"
    UTILITY2 = "utility2"


class Inventory(ABC):

    @property
    @abstractmethod
    def items(self) -> List[Items]:
        pass

    @property
    @abstractmethod
    def equipment(self) -> Dict[EquipmentSlot, Items]:
        pass

    @property
    @abstractmethod
    def utilities_amount(self) -> Dict[EquipmentSlot, Items]:
        pass

    @property
    @abstractmethod
    def max_inventory_amount(self) -> int:
        """
        Amount of all items
        :return int:
        """
        pass

    @property
    def free_amount(self) -> int:
        amount = self.max_inventory_amount
        for item in self.items:
            amount -= item.quantity
        return amount


    @property
    @abstractmethod
    def capacity(self) -> int:
        """
        Max inventory slots
        :return int:
        """
        pass

    @abstractmethod
    def equip_item(self, item: Item, item_slot: EquipmentSlot, count: int = 1):
        # Equip an item on your character.
        pass

    @abstractmethod
    def unequip_item(self, item_slot: EquipmentSlot, count: int = 1):
        # Unequip an item on your character.
        pass

    @abstractmethod
    def use_item(self, item: Item, count: int = 1):
        pass

    @abstractmethod
    def delete_item(self, item: Item, amount: int):
        # Deleting an item from your inventory.
        pass

    def get_items(self, item: Item) -> Optional[Items]:
        inventory_items = [inv_item for inv_item in self.items if inv_item.item.code == item.code]
        if inventory_items:
            return inventory_items[0]
        else:
            return None

    def get_items_amount(self):
        quantity = 0
        for item in self.items:
            quantity += item.quantity
        return quantity

    def is_possible_to_add_item(self, item: Item, added_quantity: int):
        inventory_items = self.items
        new_items_len = len(inventory_items)
        if item.code in inventory_items:
            new_items_len += 1
        new_quantity = self.get_items_amount() + added_quantity
        return new_items_len <= self.capacity and new_quantity <= self.max_inventory_amount

    def is_inventory_full(self):
        return len(self.items) == self.capacity or \
            self.get_items_amount() == self.max_inventory_amount

    def __repr__(self):
        return f"Inventory(capacity={self.capacity}, max_inventory_size={self.capacity}, items={self.items})"
