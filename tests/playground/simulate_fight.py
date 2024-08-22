from pprint import pprint

from dynaconf import settings

from src.playground.characters import Character, RestApiCharacter
from src.playground.monsters import MonsterManager, RestApiMonsterManager
from src.playground.utilites.fight_results import FightEstimator
from src.rest_api_client.client import AuthenticatedClient


def test_fight_simulation():
    simulator = FightEstimator()
    char_name = settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    character: Character = RestApiCharacter(char_name, client=client)
    monster = RestApiMonsterManager(client=client)

    pprint(simulator.estimate_fight(character,
                                   monster.get_monster_info(monster.monster_from_id("red_slime"))))
