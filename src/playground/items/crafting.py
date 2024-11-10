from dataclasses import dataclass
from typing import List, Optional

from src.playground.characters.character_stats import SkillType
from src.playground.items.item import Item, ItemType, Items, ItemEffect


@dataclass(frozen=True)
class ItemDetails(Item):
    name: str  # Item name.
    level: int  # Item level.
    type: ItemType  # Type for item, it can be weapon, resource and so on
    subtype: str  # Detailed description of what it is or how to retrieve
    effects: List[ItemEffect]
    description: str


@dataclass(frozen=True)
class CraftInfo:
    skill: SkillType
    level: int
    items: List[Items]  # Items to craft
    quantity: int


@dataclass(frozen=True)
class CraftingItem(ItemDetails):
    craft: Optional[CraftInfo]
