import logging

import pytest
from dynaconf import settings

from src.playground.characters import RestApiCharacter
from src.playground.characters.character import Character
from src.rest_api_client.client import AuthenticatedClient

logger = logging.getLogger(__name__)


@pytest.mark.slow
def test_api():
    char_name = settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    character: Character = RestApiCharacter(char_name, client=client)
    character.move(1, 3)
