from typing import Optional, List

from src.player.players.base_player import BasePlayer
from src.player.players.player_types import PlayerType
from src.player.strategy.task.monster_fight import HuntStrategy
from src.player.task import TaskInfo, MonsterTask, Monsters
from src.playground.monsters import DetailedMonster
from src.playground.utilites.fight_results import FightEstimator

FARM_COUNT = 100


class Barbarian(BasePlayer):

    def _can_complete_task(self, task: TaskInfo):
        return True  # TODO: Implement this

    player_type = PlayerType.BARBARIAN

    def __find_easy_monster(self) -> DetailedMonster:
        monsters: List[DetailedMonster] = self._world.monsters.monsters
        sorted_monsters = sorted(monsters, key=lambda m: m.stats.level)
        current_monster = sorted_monsters[0]
        simulator = FightEstimator(world=self._world, simulate_fights_number=100)
        for monster in sorted_monsters:
            fight_result = simulator.simulate_fights(self.character, monster)
            if fight_result.success_rate > 0.99:
                current_monster = monster
            else:
                break
        return current_monster

    def _do_something(self):
        easy_monster = self.__find_easy_monster()
        return TaskInfo(monster_task=MonsterTask(Monsters(monster=easy_monster, count=FARM_COUNT)))

    def _task_to_actions(self, task: TaskInfo):
        if task.bank_task is not None:
            bank_task = task.bank_task
            return self._deposit_items(deposit_items=bank_task.deposit.items,
                                       deposit_gold=bank_task.deposit.gold,
                                       withdraw_items=bank_task.withdraw.items,
                                       withdraw_gold=bank_task.withdraw.gold,
                                       deposit_all=bank_task.deposit_all)
        elif task.equip_task is not None:
            equip_task = task.equip_task
            return self._equip_items(items=equip_task.items, slot=equip_task.slot)
        elif task.monster_task is not None:
            monster_task = task.monster_task
            strategy = HuntStrategy(player=self, world=self._world,
                                    items=monster_task.items,
                                    monsters=monster_task.monster,
                                    farm_until_level=monster_task.character_level)
            strategy.run()

        else:
            raise ValueError("Task is not valid")

    def _is_player_task(self, task: TaskInfo):
        if super()._is_player_task(task):
            return True
        elif task.monster_task is not None:
            return True
        else:
            return False
