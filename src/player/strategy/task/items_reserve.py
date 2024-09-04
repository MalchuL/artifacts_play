from typing import List

from src.player.strategy.character_strategy import CharacterStrategy
from src.player.task import TaskInfo


class ItemsReserveSimpleStrategy(CharacterStrategy):
    def run(self) -> List[TaskInfo]:
        return []
