from pprint import pprint

from dynaconf import settings

from src.playground.characters import Character, RestApiCharacter
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.fabric.restapi_playground_world import RestApiPlaygroundWorld
from src.playground.monsters import MonsterManager, RestApiMonsterManager
from src.playground.utilites.fight_results import FightEstimator
from src.rest_api_client.client import AuthenticatedClient


def test_fight_simulation():
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    world: PlaygroundWorld = RestApiPlaygroundWorld(client)
    simulator = FightEstimator(world)
    char_name = settings.CHARACTERS[0]
    character: Character = RestApiCharacter(char_name, client=client)
    monster_manager = RestApiMonsterManager(client=client)
    monster = monster_manager.get_monster_info(monster_manager.monster_from_id("red_slime"))

    pprint(simulator.estimate_fight(character, monster))

    pprint(simulator.simulate_fights(character=character, monster=monster))