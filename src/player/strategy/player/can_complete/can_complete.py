from abc import ABC, abstractmethod

from src.player.players.player import Player
from src.player.task import TaskInfo
from src.playground.fabric.playground_world import PlaygroundWorld


class CanComplete(ABC):
    def __init__(self, player: Player, world: PlaygroundWorld):
        self.player = player
        self.world = world

    @abstractmethod
    def can_complete(self, task_info: TaskInfo):
        pass

    def __call__(self, task_info: TaskInfo):
        return self.can_complete(task_info)
