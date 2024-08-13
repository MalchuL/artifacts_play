from dataclasses import dataclass

from src.playground.item import Item


@dataclass
class GrandExchangePosition:
    item: Item
    quantity: int
    price: int
