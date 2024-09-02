from abc import ABC
from typing import Optional, List

from .player import Player
from ..strategy.task.bank import BankStrategy
from ..strategy.task.equip_item import EquipStrategyTask
from ..task import TaskInfo
from ...playground.characters import EquipmentSlot
from ...playground.items import Items


class BasePlayer(Player, ABC):

    def _is_player_task(self, task_info: TaskInfo) -> bool:
        if task_info.bank_task:
            return True
        elif task_info.equip_task:
            return True
        return False

    def _can_complete_task(self, task: TaskInfo):
        if task.bank_task is not None:
            return True
        if task.equip_task is not None:
            return True
        return False

    def _deposit_items(self, deposit_items: Optional[List[Items]] = None, deposit_gold: int = 0,
                       withdraw_gold: int = 0, withdraw_items: Optional[List[Items]] = None,
                       deposit_all: bool = False) -> List[TaskInfo]:
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
                                     deposit_items=deposit_items,
                                     deposit_gold=deposit_gold, withdraw_items=withdraw_items,
                                     withdraw_gold=withdraw_gold)

        return bank_strategy.run()

    def _equip_items(self, items: Items, slot: Optional[EquipmentSlot]):
        return EquipStrategyTask(player=self, world=self._world, item=items.item,
                                 amount=items.quantity, equipment_slot=slot).run()
