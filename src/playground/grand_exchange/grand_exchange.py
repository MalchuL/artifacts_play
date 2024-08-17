from dataclasses import dataclass

from src.playground.items.item import Item


@dataclass
class GrandExchangePosition:
    item: Item
    quantity: int
    price: int
