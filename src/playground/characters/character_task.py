from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TaskType(Enum):
    MONSTERS = 'monsters'
    RESOURCES = 'resources'
    CRAFTS = 'crafts'


@dataclass
class CharTask:
    code: str  # Code of item, monster or resource
    task_type: TaskType  # Task
    total: int  # What count of actions should be done
    progress: int  # Task progress when equals to total task is completed


class CharacterQuest(ABC):

    @abstractmethod
    def accept_new_task(self) -> CharTask:
        # Accepting a new task.
        pass

    @abstractmethod
    def complete_task(self):
        # Completing a task.
        pass

    @abstractmethod
    def get_current_task(self) -> Optional[CharTask]:
        pass

    def is_task_completed(self):
        char_task = self.get_current_task()
        return char_task.progress >= char_task.total

    @abstractmethod
    def exchange_tasks(self):
        pass
