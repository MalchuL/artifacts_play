from abc import ABC
from typing import Optional, List

from .player import Player
from ..strategy.player.can_complete.craft import CanCompleteCraftingTask
from ..strategy.player.can_complete.monster import CanBeatMonster
from ..strategy.player.can_complete.resource import CanCompleteResourceTask
from ..strategy.strategy import Strategy
from ..strategy.task.bank import BankStrategy
from ..strategy.task.craft_item import CraftStrategy
from ..strategy.task.equip_item import EquipStrategyTask
from ..strategy.task.harvest_items import HarvestStrategy
from ..strategy.task.monster_fight import HuntStrategy
from ..task import TaskInfo
from ...playground.characters import SkillType
from ...playground.items import Items


class BasePlayer(Player, ABC):
    harvest_skills: List[SkillType] = []
    crafting_skills: List[SkillType] = []

    def _is_player_task(self, task_info: TaskInfo) -> bool:
        if task_info.bank_task:
            return True
        elif task_info.equip_task:
            return True
        elif task_info.reserved_task:
            return True
        elif task_info.nothing_task:
            return True
        return False

    def _can_complete_task(self, task: TaskInfo):
        if task.bank_task is not None:
            return True
        elif task.reserved_task is not None:
            return True
        elif task.nothing_task is not None:
            return True
        elif task.equip_task is not None:
            return True
        # Is resource task, check resources and level of resources
        elif task.resources_task is not None:
            return CanCompleteResourceTask(self.character, self._world)(task)
        elif task.monster_task is not None:
            return CanBeatMonster(self.character, self._world)(task)
        elif task.crafting_task is not None:
            return CanCompleteCraftingTask(self.character, self._world, self.crafting_skills)(task)
        else:
            raise ValueError(f"Task is not valid, {task}, player={self.player_type}")

    def _deposit_items_strategy(self, deposit_items: Optional[List[Items]] = None,
                                deposit_gold: int = 0,
                                withdraw_gold: int = 0,
                                withdraw_items: Optional[List[Items]] = None,
                                deposit_all: bool = False) -> Strategy:
        if deposit_all:
            if deposit_items is None:
                deposit_items = []
                reserved_items = self._reserved_items
                for items in self.character.inventory.items:
                    is_in_reserved = False
                    for reserved_item in reserved_items:
                        if reserved_item.item.code == items.item.code and reserved_item.quantity > items.quantity:
                            deposit_items.append(Items(item=items.item,
                                                       quantity=reserved_item.quantity - items.quantity))
                            is_in_reserved = True
                    if not is_in_reserved:
                        deposit_items.append(items)
            deposit_gold = self.character.stats.gold
        bank_strategy = BankStrategy(player=self, world=self._world,
                                     task_manager=self._world_tasks,
                                     deposit_items=deposit_items,
                                     deposit_gold=deposit_gold, withdraw_items=withdraw_items,
                                     withdraw_gold=withdraw_gold)

        return bank_strategy

    def _task_to_actions(self, task: TaskInfo) -> List[TaskInfo]:
        if task.bank_task is not None:
            bank_task = task.bank_task
            strategy = self._deposit_items_strategy(deposit_items=bank_task.deposit.items,
                                                    deposit_gold=bank_task.deposit.gold,
                                                    withdraw_items=bank_task.withdraw.items,
                                                    withdraw_gold=bank_task.withdraw.gold,
                                                    deposit_all=bank_task.deposit_all)
            return strategy.run()
        elif task.reserved_task is not None:
            return []
        elif task.nothing_task is not None:
            return []
        elif task.equip_task is not None:
            equip_task = task.equip_task
            strategy = EquipStrategyTask(player=self, world=self._world,
                                         item=equip_task.items.item,
                                         amount=equip_task.items.quantity,
                                         equipment_slot=equip_task.slot)
            return strategy.run()
        elif task.resources_task is not None:
            resource_task = task.resources_task
            strategy = HarvestStrategy(player=self, world=self._world,
                                       items=resource_task.items,
                                       resources=resource_task.resources,
                                       skill_type=resource_task.skill_level,
                                       farm_until_level=resource_task.skill_level)
            return strategy.run()
        elif task.monster_task is not None:
            monster_task = task.monster_task
            strategy = HuntStrategy(player=self, world=self._world,
                                    items=monster_task.items,
                                    monsters=monster_task.monsters,
                                    farm_until_level=monster_task.character_level)
            return strategy.run()
        elif task.crafting_task is not None:
            crafting_task = task.crafting_task
            strategy = CraftStrategy(player=self, world=self._world,
                                     items=crafting_task.items)
            return strategy.run()
        else:
            raise ValueError("Task is not valid")
