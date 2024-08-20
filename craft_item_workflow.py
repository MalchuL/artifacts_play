import argparse
import logging

from dynaconf import settings

from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.fabric.restapi_playground_world import RestApiPlaygroundWorld
from src.playground.items import Item, Items
from src.rest_api_client.client import AuthenticatedClient

from src.task_manager.workflows.state import set_world
from src.task_manager.workflows.craft_item import CraftItemsTask

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
    set_world(world)

    item2craft = Items(Item(args.item_code), int(args.item_count))
    target_task = CraftItemsTask(char_name, item2craft).start()
