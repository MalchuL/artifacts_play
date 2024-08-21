from typing import List

from dynaconf import settings

from src.playground.characters import Character, RestApiCharacter
from src.playground.items import ItemCraftingInfoManager, RestApiItemCraftingInfoManager
from src.playground.items.crafting import CraftingItem, EffectType
from src.playground.monsters import DetailedMonster, RestApiMonsterManager
from src.playground.utilites.equipment_estimator import EquipmentEstimator
from src.rest_api_client.client import AuthenticatedClient


def test_equipment_estimator():


    char_name = settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    character: Character = RestApiCharacter(char_name, client=client)
    monster = RestApiMonsterManager(client=client)
    items: ItemCraftingInfoManager = RestApiItemCraftingInfoManager(client=client)
    simulator = EquipmentEstimator(items.items)


    print(simulator.optimal_vs_monster(character, monster.get_monster_info(monster.monster_from_id("red_slime"))))

