import argparse
import logging

from dynaconf import settings

from src.player.players.barbarian import Barbarian
from src.player.players.harvester import Harvester
from src.player.task import items_to_player_task
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
    character = world.get_character(char_name)
    world_tasks = WorldTaskManager()
    #world_tasks.add_task(PlayerTask(items_task=Items(Item(args.item_code), quantity=int(args.item_count))))
    world_tasks.add_task(items_to_player_task(Items(Item("yellow_slimeball"), quantity=30), world=world))
    player = Barbarian(character, world, world_tasks)
    player.do()

