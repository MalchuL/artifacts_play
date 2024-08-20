import luigi

from src.playground.fabric.playground_world import PlaygroundWorld
from src.task_manager.luigi.state import get_world


class WorldTask(luigi.Task):

    @property
    def world(self) -> PlaygroundWorld:
        return get_world()
