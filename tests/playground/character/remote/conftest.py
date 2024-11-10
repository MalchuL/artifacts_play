import logging
import os

import pytest
from dynaconf import settings

from src.playground.characters import RestApiCharacter, Character
from src.rest_api_client.client import AuthenticatedClient

logging.basicConfig(level=logging.INFO)

# Set for dynaconf
os.environ["ENV_FOR_DYNACONF"] = "testing"


@pytest.fixture
def character():
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    character: Character = RestApiCharacter(settings.CHARACTERS[0], client)
    return character