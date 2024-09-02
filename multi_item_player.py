import argparse
import logging
import threading
import time
from threading import Thread

from dynaconf import settings

from src.player.players.barbarian import Barbarian
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
parser.add_argument("--character", default=None)
parser.add_argument("--item-code")
parser.add_argument("--item-count", default=1)
args = parser.parse_args()

item_code = args.item_code

if __name__ == '__main__':
    char_name = args.character or settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    world: PlaygroundWorld = RestApiPlaygroundWorld(client)
    character_harvester = world.get_character("DoraDura")
    character_fighter = world.get_character("TestChar")
    character_creator = world.get_character("AssetManager")

    world_tasks = WorldTaskManager()

    player_barbarian = Barbarian(character_fighter, world, world_tasks)
    player_harvester = Harvester(character_harvester, world, world_tasks)
    player_creator = Creator(character_creator, world, world_tasks)

    dagger_task_info = TaskInfo(equip_task=EquipTask(Items(Item("copper_dagger"), quantity=1)))
    world_tasks.add_task(dagger_task_info, player=player_creator)
    world_tasks.add_task(
        items_to_player_task(Items(Item("yellow_slimeball"), quantity=30), world=world))

    t1 = Thread(target=player_barbarian.do, daemon=True)
    t2 = Thread(target=player_harvester.do, daemon=True)
    t3 = Thread(target=player_creator.do, daemon=True)

    t1.start()
    t2.start()
    time.sleep(3)
    t3.start()

    while True:
        for thread in [t1, t2, t3]:
            if not thread.is_alive():
                exit(1)
