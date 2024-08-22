from pprint import pprint
from typing import List

import pytest
from dynaconf import settings

from src.playground.characters import Character, RestApiCharacter
from src.playground.items import ItemCraftingInfoManager, RestApiItemCraftingInfoManager
from src.playground.items.crafting import CraftingItem, EffectType
from src.playground.monsters import DetailedMonster, RestApiMonsterManager
from src.playground.utilites.equipment_estimator import EquipmentEstimator
from src.rest_api_client.client import AuthenticatedClient


@pytest.mark.parametrize('level', [1, 5, 7, 15, 30])
def test_equipment_estimator(level):


    char_name = settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    character: Character = RestApiCharacter(char_name, client=client)
    monster = RestApiMonsterManager(client=client)
    items: ItemCraftingInfoManager = RestApiItemCraftingInfoManager(client=client)
    available_items = [item for item in items.get_crafts() if item.craft.level <= level]
    simulator = EquipmentEstimator(available_items)


    pprint(simulator.optimal_vs_monster(character, monster.get_monster_info(monster.monster_from_id("cow"))))

@pytest.mark.parametrize('monster_name', ['lich', 'owlbear', 'red_slime', 'vampire'])
def test_equipment_all_items_estimator(monster_name):
    char_name = settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    character: Character = RestApiCharacter(char_name, client=client)
    monster = RestApiMonsterManager(client=client)
    items: ItemCraftingInfoManager = RestApiItemCraftingInfoManager(client=client)
    simulator = EquipmentEstimator(items.items)

    pprint(simulator.optimal_vs_monster(character,
                                       monster.get_monster_info(monster.monster_from_id(monster_name))))
