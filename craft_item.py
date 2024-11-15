import argparse
import logging
import os
import time
from datetime import datetime

from dynaconf import settings

from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.fabric.restapi_playground_world import RestApiPlaygroundWorld
from src.playground.items import Item, Items
from src.rest_api_client.client import AuthenticatedClient
import luigi

from src.task_manager.luigi.adapters import ItemsAdapter, to_json, ListItemAdapter
from src.task_manager.luigi.available_items import AvailableItems
from src.task_manager.luigi.craft_item import CraftItemTask
from src.task_manager.luigi.state import set_world

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

    item2craft = Items(Item(args.item_code), int(args.item_count))
    os.makedirs(settings.TASK_OUT_DIRECTORY, exist_ok=True)
    set_world(world=world)
    crafting_items = ItemsAdapter.dump_python(item2craft)

    #craft_task = CraftItemTask(char_name=args.character, crating_item=crafting_items)
    available_task = AvailableItems(char_name=args.character, required_items=to_json([Item(args.item_code)],ListItemAdapter), datetime=datetime.now())
    CraftItemTask.clear_instance_cache()
    luigi.build([available_task], log_level="WARNING")

