from abc import abstractmethod
from enum import Enum

from src.playground.crafting import CraftingRecipe
from src.playground.item import Item


class ItemSlot(Enum):
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
    CONSUMABLE = "consumable1"
    CONSUMABLE2 = "consumable2"


class Character:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def move(self, x, y):
        # Moves a character on the map using the map's X and Y position.
        pass

    @abstractmethod
    def equip_item(self, item: Item, item_slot: ItemSlot):
        # Equip an item on your character.
        pass

    @abstractmethod
    def unequip_item(self, item_slot: ItemSlot):
        # Unequip an item on your character.
        pass

    @abstractmethod
    def fight(self):
        # Start a fight against a monster on the character's map.
        pass

    @abstractmethod
    def harvest(self):
        # Harvest a resource on the character's map.
        pass

    @abstractmethod
    def craft(self, recipe: CraftingRecipe, amount: int):
        # Crafting an item. The character must be on a map with a workshop.
        pass

    @abstractmethod
    def deposit_item(self, item: Item, amount: int):
        # Deposit an item in a bank on the character's map.
        pass

    @abstractmethod
    def deposit_gold(self, amount: int):
        # Deposit golds in a bank on the character's map.
        pass

    @abstractmethod
    def recycle(self, item: Item, amount: int):
        # Recycling an item. The character must be on a map with a workshop (only for equipments
        # and weapons).
        pass

    @abstractmethod
    def withdraw_item(self, item: Item, amount: int):
        # Take an item from your bank and put it in the character's inventory.
        pass

    @abstractmethod
    def withdraw_gold(self, amount: int):
        # Withdraw gold from your bank.
        pass

    @abstractmethod
    def grand_exchange_buy_item(self, item: Item, amount: int):
        # Buy an item at the Grand Exchange on the character's map.
        pass

    @abstractmethod
    def grand_exchange_sell_item(self, item: Item, amount: int):
        # Sell an item at the Grand Exchange on the character's map.
        pass

    @abstractmethod
    def accept_new_task(self):
        # Accepting a new task.
        pass

    @abstractmethod
    def complete_task(self):
        # Completing a task.
        pass

    @abstractmethod
    def delete_item(self, item: Item):
        # Deleting an item from your inventory.
        pass
