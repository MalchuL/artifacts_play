from dataclasses import dataclass

from src.playground.item import Item


@dataclass
class CraftingRecipe:
    item: Item
