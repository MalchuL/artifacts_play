from dataclasses import dataclass

from src.playground.items.item import Item


@dataclass
class CraftingRecipe:
    item: Item
