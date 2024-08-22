from abc import abstractmethod, ABC

from src.playground.bank import Bank
from src.playground.characters import Character
from src.playground.items import ItemCraftingInfoManager
from src.playground.map import MapManager
from src.playground.monsters import MonsterManager
from src.playground.resources import ResourceManager


# Fabric
class PlaygroundWorld(ABC):
    @property
    @abstractmethod
    def bank(self) -> Bank:
        pass

    @property
    @abstractmethod
    def item_details(self) -> ItemCraftingInfoManager:
        pass

    @property
    @abstractmethod
    def map(self) -> MapManager:
        pass

    @property
    @abstractmethod
    def monsters(self) -> MonsterManager:
        pass

    @property
    @abstractmethod
    def resources(self) -> ResourceManager:
        pass

    @abstractmethod
    def get_character(self, name: str) -> Character:
        pass
