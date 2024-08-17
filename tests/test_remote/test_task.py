import logging

import pytest
from dynaconf import settings

from src.playground.characters.character import Character
from src.playground.characters.remote.rest_api_character import RestApiCharacter
from src.rest_api_client.client import AuthenticatedClient

logger = logging.getLogger(__name__)


@pytest.mark.slow
def test_task():
    char_name = settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    character: Character = RestApiCharacter(char_name, client=client)
    character.character_quest.accept_new_task()

