from dynaconf import settings

from src.playground.characters import RestApiCharacter, Character
from src.rest_api_client.client import AuthenticatedClient


def test_character_load():
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    character: Character = RestApiCharacter(settings.CHARACTERS[0], client, pull_status=False)
    print(character.stats)