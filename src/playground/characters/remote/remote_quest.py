import logging
from typing import Optional

from src.playground.character_task import CharacterQuest, CharTask, TaskType
from src.rest_api_client.api.my_characters import ActionAcceptNewTask, ActionCompleteTask, \
    ActionTaskExchange
from src.rest_api_client.model import CharacterSchema, TaskResponseSchema, TaskRewardResponseSchema

logger = logging.getLogger(__name__)


class RemoteCharacterQuest(CharacterQuest):
    def __init__(self, character: "RestApiCharacter"):
        self.character = character
        self.name = self.character.name
        self._client = self.character._client

    @property
    def _state(self) -> CharacterSchema:
        return self.character._state

    @_state.setter
    def _state(self, state: CharacterSchema):
        self.character._state = state

    def accept_new_task(self) -> CharTask:
        result: TaskResponseSchema = ActionAcceptNewTask(self.name, client=self._client)()
        self.character._state = result.data.character
        logger.info(f"Accept task {result.data.task}")
        new_task = result.data.task
        return CharTask(code=new_task.code, task_type=TaskType(new_task.type.value),
                        total=new_task.total, progress=0)

    def complete_task(self):
        result: TaskRewardResponseSchema = ActionCompleteTask(self._name, client=self._client)()
        self.character._state = result.data.character
        logger.info(f"Task complete {result.data.reward}")

    def exchange_tasks(self):
        result: TaskRewardResponseSchema = ActionTaskExchange(self._name, client=self._client)()
        self.character._state = result.data.character
        logger.info(f"Task reward {result.data.reward}")

    def get_current_task(self) -> Optional[CharTask]:
        state = self.character._state
        if state.task:
            return CharTask(code=state.task, task_type=TaskType(state.task_type),
                            total=state.task_total, progress=state.task_progress)
        else:
            return None

    def is_task_completed(self):
        char_task = self.get_current_task()
        if char_task:
            return char_task.progress >= char_task.total
        else:
            return False
