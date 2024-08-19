from abc import ABC, abstractmethod
from typing import List

from src.playground.monsters.monster import Monster, DetailedMonster


class MonsterManager(ABC):

    @property
    @abstractmethod
    def monsters(self) -> List[DetailedMonster]:
        pass

    @abstractmethod
    def get_monster_info(self, monster: Monster) -> DetailedMonster:
        pass

    def monster_from_id(self, unique_id: str) -> Monster:
        return Monster(unique_id)
