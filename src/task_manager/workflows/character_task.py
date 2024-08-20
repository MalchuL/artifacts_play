from abc import ABC
from .world_task import WorldTask


class CharacterTask(WorldTask, ABC):
    def __init__(self, char_name: str):
        super().__init__()
        self.char_name = char_name
