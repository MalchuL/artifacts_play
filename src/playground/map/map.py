from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Optional

from src.playground.characters.character_stats import Stats, SkillType
from src.playground.items.item import Item, DropItem


class MapType(Enum):
    MONSTER = "monster"
    RESOURCE = "resource"
    WORKSHOP = "workshop"
    BANK = "bank"
    GRAND_EXCHANGE = "grand_exchange"
    TASKS_MANAGER = "tasks_master"


@dataclass(frozen=True)
class MapContent:
    code: str  # UniqueID
    type: MapType


@dataclass(frozen=True)
class Map:
    name: str
    skin: str
    x: int
    y: int
    content: Optional[MapContent]

    @property
    def position(self) -> Tuple[int, int]:
        return self.x, self.y
