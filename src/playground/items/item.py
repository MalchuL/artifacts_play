from dataclasses import dataclass
from enum import Enum


class ItemType(Enum):
    consumable = 'consumable'  # Out combats
    utility = 'utility'  # In combats
    currency = 'currency'
    body_armor = 'body_armor'
    weapon = 'weapon'
    resource = 'resource'
    leg_armor = 'leg_armor'
    helmet = 'helmet'
    boots = 'boots'
    shield = 'shield'
    amulet = 'amulet'
    ring = 'ring'
    artifact = 'artifact'


@dataclass(frozen=True)
class Item:
    code: str


@dataclass(frozen=True)
class Items:
    item: Item
    quantity: int


@dataclass(frozen=True)
class DropItem:
    item: Item
    rate: int  # After amount of rate items will be dropped
    min_quantity: int
    max_quantity: int


class EffectType(Enum):
    RESTORE_HP = "restore"
    BOOST_HP = "boost_hp"
    HASTE = "haste"
    HP = "hp"
    # Skill
    MINING = "mining"
    WOODCUTTING = "woodcutting"
    FISHING = "fishing"
    ALCHEMY = "alchemy"
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
    # Boost resistance (in percents)
    BOOST_RESIST_EARTH = "boost_res_earth"
    BOOST_RESIST_FIRE = "boost_res_fire"
    BOOST_RESIST_AIR = "boost_res_air"
    BOOST_RESIST_WATER = "boost_res_water"
    # Outside of combat
    INVENTORY_SPACE = "inventory_space"
    HEAL = "heal"
    GOLD = "gold"


@dataclass(frozen=True)
class ItemEffect:
    type: EffectType
    value: int
