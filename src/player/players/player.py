from abc import abstractmethod, ABC
from typing import List, Optional

from src.player.players.player_types import PlayerType
from src.player.task import TaskInfo
from src.player.task_manager import WorldTaskManager
from src.playground.characters import Character, EquipmentSlot
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Items


class Player(ABC):
    """
    Player that doing something automatically.
    """

    @property
    @abstractmethod
    def player_type(self) -> PlayerType:
        pass

    def __init__(self, character: Character, world: PlaygroundWorld,
                 world_tasks: WorldTaskManager):
        self._character = character
        self._world = world
        self._reserved_items: List[Items] = []
        self._world_tasks = world_tasks

    @property
    def player_id(self) -> str:
        return self._character.name

    @property
    def reserve_items(self):
        return self._reserved_items.copy()

    @property
    def character(self) -> Character:
        return self._character

    @abstractmethod
    def _deposit_items(self, deposit_items: Optional[List[Items]] = None, deposit_gold: int = 0,
                       withdraw_gold: int = 0, withdraw_items: Optional[List[Items]] = None,
                       deposit_all: bool = False):
        pass

    @abstractmethod
    def _equip_items(self, items: Items, slot: Optional[EquipmentSlot]):
        pass

    @abstractmethod
    def _do_something(self) -> TaskInfo:
        pass

    @abstractmethod
    def _task_to_actions(self, task_info: TaskInfo) -> List[TaskInfo]:
        pass

    @abstractmethod
    def _is_player_task(self, task_info: TaskInfo) -> bool:
        pass

    @abstractmethod
    def _can_complete_task(self, task: TaskInfo):
        pass

    def do(self):
        world_tasks = self._world_tasks
        while True:
            is_task_assigned = False
            # If player has tasks to do, do them
            if world_tasks.tasks_to_do(self):
                for task in world_tasks.tasks_to_do(self):
                    # Check is character can complete those tasks
                    if self._can_complete_task(task.task_info):
                        is_task_assigned = True
                        out_task_infos = self._task_to_actions(task.task_info)
                        # If task has additional steps add to queue
                        # And reassign to new path
                        parent_task = world_tasks.parent_task(task)
                        for out_task_info in out_task_infos:
                            is_player_task = self._is_player_task(out_task_info)
                            player_for_task = self if is_player_task else None
                            parent_task = world_tasks.add_task(out_task_info,
                                                               player=player_for_task,
                                                               depend_on=parent_task)
                        # By any keys remove task, because it splitted or completed
                        # We already reorder them
                        world_tasks.remove_task(task)
                        break
            if not is_task_assigned:
                if world_tasks.unassigned_tasks():
                    for task in world_tasks.unassigned_tasks():
                        if self._is_player_task(task.task_info):
                            world_tasks.assign_task(self, task)
                            # Set to rerun loop
                            is_task_assigned = True
            if not is_task_assigned:
                smth_task = self._do_something()
                print(smth_task)
                assert self._is_player_task(smth_task), f"Task {smth_task} is not for {self.player_type}"
                world_tasks.add_task(smth_task, player=self)
                is_task_assigned = True
