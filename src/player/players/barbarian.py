from typing import List

from src.player.players.base_player import BasePlayer
from src.player.players.player_types import PlayerType
from src.player.strategy.player.can_complete.monster import CanBeatMonster
from src.player.task import TaskInfo, MonsterTask, Monsters
from src.playground.monsters import DetailedMonster

FARM_COUNT = 10


class Barbarian(BasePlayer):

    player_type = PlayerType.BARBARIAN

    def __find_easy_monster(self) -> DetailedMonster:
        monsters: List[DetailedMonster] = self._world.monsters.monsters
        sorted_monsters = sorted(monsters, key=lambda m: m.stats.level)
        current_monster = sorted_monsters[0]
        for monster in sorted_monsters:
            tmp_task_info = TaskInfo(monster_task=MonsterTask(monsters=Monsters(monster, 1)))
            if CanBeatMonster(self.character, self._world)(tmp_task_info):
                current_monster = monster
            else:
                break
        return current_monster

    def _do_something(self):
        easy_monster = self.__find_easy_monster()
        return TaskInfo(monster_task=MonsterTask(monsters=Monsters(monster=easy_monster, count=FARM_COUNT)))

    def _is_player_task(self, task: TaskInfo):
        if super()._is_player_task(task):
            return True
        elif task.monster_task is not None:
            return True
        else:
            return False
