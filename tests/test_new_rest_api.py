from dynaconf import settings

from src.rest_api_client.api.my_characters import ActionMove, ActionFight
from src.rest_api_client.client import AuthenticatedClient
from src.rest_api_client.model import DestinationSchema


def test_new_rest_api():
    char_name = settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    movement = ActionMove(name=char_name, client=client)
    char = movement(DestinationSchema(x=-199, y=1))

    print(char)


def test_fight_api():
    char_name = settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    fight = ActionFight(name=char_name, client=client)
    char = fight()

    print(char)
