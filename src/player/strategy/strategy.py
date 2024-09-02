import logging
from abc import abstractmethod
from typing import List, Optional

from src.player.task import TaskInfo
from src.playground.fabric.playground_world import PlaygroundWorld


class Strategy:
    def __init__(self, world: PlaygroundWorld, name: Optional[str] = None):
        self.world = world
        if name is None:
            name = self.__class__.__name__
        self._logger = logging.getLogger(name)
        self._logger.propagate = True

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @abstractmethod
    def run(self) -> List[TaskInfo]:
        pass
