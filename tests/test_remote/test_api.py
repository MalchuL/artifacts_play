import logging

import pytest
from dynaconf import settings

from src.playground.characters.character import Character
from src.playground.characters.remote.openapi_client.artifacts_api_client import AuthenticatedClient
from src.playground.remote.rest_api_character import RestApiCharacter

logger = logging.getLogger(__name__)


@pytest.mark.slow
def test_api():
    char_name = settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    character: Character = RestApiCharacter(char_name, client=client)
    character.move(1, 3)
