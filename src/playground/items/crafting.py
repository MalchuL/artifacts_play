from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from src.playground.characters.character_stats import SkillType
from src.playground.items.item import Item, ItemType, Items


class EffectType(Enum):
    RESTORE_HP = "restore"
    BOOST_HP = "boost_hp"
    HASTE = "haste"
    HP = "hp"
    # Skill
    MINING = "mining"
    WOODCUTTING = "woodcutting"
    FISHING = "fishing"
    # Attack effects
    ATTACK_EARTH = "attack_earth"
    ATTACK_FIRE = "attack_fire"
    ATTACK_AIR = "attack_air"
    ATTACK_WATER = "attack_water"
    # Resistance (in percents)
    RESIST_EARTH = "res_earth"
    RESIST_FIRE = "res_fire"
    RESIST_AIR = "res_air"
    RESIST_WATER = "res_water"
    # Additional Damage (in percents)
    DAMAGE_EARTH = "dmg_earth"
    DAMAGE_FIRE = "dmg_fire"
    DAMAGE_AIR = "dmg_air"
    DAMAGE_WATER = "dmg_water"
    # Boost damage (in percents)
    BOOST_DAMAGE_EARTH = "boost_dmg_earth"
    BOOST_DAMAGE_FIRE = "boost_dmg_fire"
    BOOST_DAMAGE_AIR = "boost_dmg_air"
    BOOST_DAMAGE_WATER = "boost_dmg_water"


@dataclass(frozen=True)
class ItemEffect:
    type: EffectType
    value: int


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
