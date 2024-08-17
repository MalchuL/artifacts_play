from abc import abstractmethod, ABC
from enum import Enum

from src.playground.character_stats import CharacterStats
from src.playground.character_task import CharacterQuest
from src.playground.crafting import CraftingRecipe
from src.playground.inventory import Inventory
from src.playground.item import Item, Items


class FightResult(Enum):
    WIN = 1
    LOSE = 2
    DRAW = 3


class Character(ABC):
    def __init__(self, name):
        self._name = name

    # Properties

    @property
    def name(self):  # Abstract getter
        return self._name

    @name.setter
    def name(self, name):  # Abstract setter
        self._name = name

    @property
    @abstractmethod
    def inventory(self) -> Inventory:
        pass

    @property
    @abstractmethod
    def character_quest(self) -> CharacterQuest:
        pass

    @property
    @abstractmethod
    def stats(self) -> CharacterStats:
        pass

    # Methods

    @abstractmethod
    def is_busy(self) -> bool:
        pass

    def wait_until_ready(self):
        while self.is_busy():
            continue

    @property
    @abstractmethod
    def position(self) -> tuple:
        pass

    @abstractmethod
    def move(self, x, y):
        # Moves a character on the map using the map's X and Y position.
        pass

    @abstractmethod
    def fight(self) -> FightResult:
        # Start a fight against a monster on the character's map.
        pass

    @abstractmethod
    def harvest(self):
        # Harvest a resource on the character's map.
        pass

    @abstractmethod
    def craft(self, recipe: CraftingRecipe, amount: int):
        # Crafting an item. The character must be on a map with a workshop.
        pass

    @abstractmethod
    def recycle(self, item: Item, amount: int):
        # Recycling an item. The character must be on a map with a workshop (only for equipments
        # and weapons).
        pass

    @abstractmethod
    def deposit_item(self, item: Item, amount: int):
        # Deposit an item in a bank on the character's map.
        pass

    @abstractmethod
    def deposit_gold(self, amount: int):
        # Deposit golds in a bank on the character's map.
        pass

    @abstractmethod
    def withdraw_item(self, item: Item, amount: int):
        # Take an item from your bank and put it in the character's inventory.
        pass

    @abstractmethod
    def withdraw_gold(self, amount: int):
        # Withdraw gold from your bank.
        pass

    @abstractmethod
    def grand_exchange_buy_item(self, item: Item, amount: int, price: int):
        # Buy an item at the Grand Exchange on the character's map.
        pass

    @abstractmethod
    def grand_exchange_sell_item(self, item: Item, amount: int, price: int):
        # Sell an item at the Grand Exchange on the character's map.
        pass

