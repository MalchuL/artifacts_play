from dataclasses import dataclass
from typing import List

from src.playground.characters.character_stats import Stats
from src.playground.items.item import DropItem


@dataclass(frozen=True)
class MonsterStats(Stats):
    level: int


@dataclass(frozen=True)
class Monster:
    code: str


@dataclass(frozen=True)
class DetailedMonster(Monster):
    name: str
    stats: MonsterStats
    drops: List[DropItem]
