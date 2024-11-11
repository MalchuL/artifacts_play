import argparse
import copy
import logging
import threading
import time
from threading import Thread

from dynaconf import settings

from src.player.players.adventurer import Adventurer
from src.player.players.barbarian import Barbarian
from src.player.players.cooker import Cooker
from src.player.players.creator import Creator
from src.player.players.harvester import Harvester
from src.player.task import items_to_player_task, TaskInfo, EquipTask
from src.player.task_manager import WorldTaskManager
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.fabric.restapi_playground_world import RestApiPlaygroundWorld
from src.playground.items import Item, Items
from src.rest_api_client.client import AuthenticatedClient

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
args = parser.parse_args()


if __name__ == '__main__':
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    world: PlaygroundWorld = RestApiPlaygroundWorld(client)
    time.sleep(1)
    character_fighter = world.get_character("Podtekatel")
    time.sleep(1)
    character_adventurer = world.get_character("Sommelier")
    time.sleep(1)
    character_cooker = world.get_character("Kakish")
    time.sleep(1)
    character_harvester = world.get_character("AssetManager")
    time.sleep(1)
    character_creator = world.get_character("Yaroslav")
    time.sleep(1)

    world_tasks = WorldTaskManager()

    player_barbarian = Barbarian(character_fighter, copy.deepcopy(world), world_tasks)
    player_cooker = Cooker(character_cooker, copy.deepcopy(world), world_tasks)
    player_adventurer = Adventurer(character_adventurer, copy.deepcopy(world), world_tasks)
    player_harvester = Harvester(character_harvester, copy.deepcopy(world), world_tasks)
    player_creator = Creator(character_creator, copy.deepcopy(world), world_tasks)


    barbarian_equips = [TaskInfo(equip_task=EquipTask(Items(Item(item_code), quantity=1)))
                        for item_code in ["copper_dagger", "copper_boots", "copper_helmet", "copper_ring", "copper_ring", "wooden_shield",
                                          #"copper_armor", "copper_legs_armor"
                                          ]
                        ]
    for barbarian_equip in barbarian_equips:
        world_tasks.add_task(barbarian_equip, player=player_adventurer)



    t1 = Thread(target=player_barbarian.do, daemon=True)
    t2 = Thread(target=player_adventurer.do, daemon=True)
    t3 = Thread(target=player_cooker.do, daemon=True)
    t4 = Thread(target=player_creator.do, daemon=True)
    t5 = Thread(target=player_harvester.do, daemon=True)

    t1.start()
    time.sleep(1)
    t2.start()
    time.sleep(1)
    t3.start()
    time.sleep(1)
    t4.start()
    time.sleep(1)
    t5.start()
    time.sleep(1)
    #t3.start()

    while True:
        for thread in [t1, t2, t3, t4, t5]:
            if not thread.is_alive():
                exit(1)
