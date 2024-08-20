import logging
from typing import Optional

from src.playground.characters.character_task import CharacterQuest, CharTask, TaskType
from src.playground.characters.remote.errors import char_exception_handler
from src.playground.characters.remote.internal_message import InternalCharacterMessage
from src.rest_api_client.api.my_characters import ActionAcceptNewTask, ActionCompleteTask, \
    ActionTaskExchange
from src.rest_api_client.client import AuthenticatedClient
from src.rest_api_client.model import CharacterSchema, TaskResponseSchema, TaskRewardResponseSchema

logger = logging.getLogger(__name__)


class RemoteCharacterQuest(CharacterQuest):
    def __init__(self, char_state: InternalCharacterMessage):
        self.__state = char_state

    @property
    def name(self) -> str:
        return self.__state.name

    @property
    def _client(self) -> AuthenticatedClient:
        return self.__state.client

    @property
    def _state(self) -> CharacterSchema:
        return self.__state.char_schema

    @_state.setter
    def _state(self, state: CharacterSchema):
        self.__state.char_schema = state

    @char_exception_handler
    def accept_new_task(self) -> CharTask:
        result: TaskResponseSchema = ActionAcceptNewTask(self.name, client=self._client)()
        self._state = result.data.character
        logger.debug(f"Accept task {result.data.task}")
        new_task = result.data.task
        return CharTask(code=new_task.code, task_type=TaskType(new_task.type.value),
                        total=new_task.total, progress=0)

    @char_exception_handler
    def complete_task(self):
        result: TaskRewardResponseSchema = ActionCompleteTask(self.name, client=self._client)()
        self._state = result.data.character
        logger.debug(f"Task complete {result.data.reward}")

    @char_exception_handler
    def exchange_tasks(self):
        result: TaskRewardResponseSchema = ActionTaskExchange(self.name, client=self._client)()
        self._state = result.data.character
        logger.debug(f"Task reward {result.data.reward}")

    def get_current_task(self) -> Optional[CharTask]:
        state = self._state
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
