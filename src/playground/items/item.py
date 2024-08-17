from dataclasses import dataclass


class ItemType:
    WEAPON = 1
    EQUIPMENT = 2
    CONSUMABLE = 3
    RESOURCE = 4
    BOOST = 5


@dataclass
class Item:
    code: str


@dataclass
class Items:
    item: Item
    quantity: int
