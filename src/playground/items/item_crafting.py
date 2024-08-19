from abc import abstractmethod, ABC
from typing import List

from src.playground.items.crafting import CraftingItem, ItemDetails
from src.playground.items.item import Item


class ItemCraftingInfoManager(ABC):

    @property
    @abstractmethod
    def items(self) -> List[ItemDetails]:
        """
        Returns all items available in world
        :return list of items:
        """
        pass

    @abstractmethod
    def get_item(self, item: Item) -> ItemDetails:
        pass

    @abstractmethod
    def get_crafts(self) -> List[CraftingItem]:
        """
        Returns all items that can be crafted
        :return list of items:
        """
        pass

    @abstractmethod
    def get_craft(self, item: Item) -> CraftingItem:
        pass

    def item_from_id(self, unique_id: str) -> Item:
        return Item(unique_id)
