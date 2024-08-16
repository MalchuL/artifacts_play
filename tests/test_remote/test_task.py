import logging
import time

import pytest
from dynaconf import settings
import pprint

from src.playground.character import Character
from src.playground.characters.remote.openapi_client.artifacts_api_client import AuthenticatedClient
from src.playground.remote.rest_api_character import RestApiCharacter

logger = logging.getLogger(__name__)


@pytest.mark.slow
def test_task():
    char_name = settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    character: Character = RestApiCharacter(char_name, client=client)
    character.accept_new_task()
