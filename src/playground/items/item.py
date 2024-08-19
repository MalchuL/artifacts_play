from dataclasses import dataclass
from enum import Enum


class ItemType(Enum):
    consumable = 'consumable'
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
