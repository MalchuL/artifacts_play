from pprint import pprint

import pytest
from dynaconf import settings

from src.playground.characters import Character, RestApiCharacter
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.fabric.restapi_playground_world import RestApiPlaygroundWorld
from src.playground.items import ItemCraftingInfoManager, RestApiItemCraftingInfoManager
from src.playground.items.crafting import CraftingItem, EffectType
from src.playground.monsters import DetailedMonster, RestApiMonsterManager
from src.playground.utilites.np_hard_equipment_estimator import NPHardEquipmentEstimator
from src.rest_api_client.client import AuthenticatedClient


@pytest.mark.parametrize('level', [1, 5, 10, 15, 30, 40])
def test_equipment_estimator(level):


    char_name = settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    character: Character = RestApiCharacter(char_name, client=client)
    monster = RestApiMonsterManager(client=client)
    items: ItemCraftingInfoManager = RestApiItemCraftingInfoManager(client=client)
    available_items = [item for item in items.get_crafts() if item.craft.level <= level]
    world: PlaygroundWorld = RestApiPlaygroundWorld(client)

    simulator = NPHardEquipmentEstimator(world, available_items)


    pprint(simulator.optimal_vs_monster(character, monster.get_monster_info(
        monster.monster_from_id("cow"))))


@pytest.mark.parametrize('level', [30, 40])
def test_lich_equipment_estimator(level):
    char_name = settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    character: Character = RestApiCharacter(char_name, client=client)
    monster = RestApiMonsterManager(client=client)
    items: ItemCraftingInfoManager = RestApiItemCraftingInfoManager(client=client)
    available_items = [item for item in items.get_crafts() if item.craft.level <= level]
    world: PlaygroundWorld = RestApiPlaygroundWorld(client)

    simulator = NPHardEquipmentEstimator(world, available_items)


    pprint(simulator.optimal_vs_monster(character, monster.get_monster_info(
        monster.monster_from_id("lich"))))