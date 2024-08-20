from abc import ABC

from src.playground.fabric.playground_world import PlaygroundWorld
from .state import get_world
from .task import Task


class WorldTask(Task, ABC):

    @property
    def world(self) -> PlaygroundWorld:
        return get_world()
