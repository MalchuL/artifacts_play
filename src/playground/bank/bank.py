from abc import abstractmethod
from typing import Optional, List

from src.playground.items.item import Items, Item


class Bank:
    @abstractmethod
    def get_bank_items(self) -> List[Items]:
        pass

    @abstractmethod
    def get_bank_item(self, item: Item) -> Optional[Items]:
        pass

    @abstractmethod
    def get_bank_gold(self) -> int:
        pass
