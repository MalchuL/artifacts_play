import logging
import os
import pickle
from dataclasses import dataclass
from datetime import datetime
from typing import List

import luigi
from dynaconf import settings
from luigi.format import Nop

from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Items, Item
from src.playground.map import Map
from src.playground.resources import Resource
from src.playground.utilites.items_finder import ItemFinder
from src.playground.utilites.locations import distance_location
from src.playground.utilites.map_finder import MapFinder
from src.task_manager.luigi.adapters import ItemsAdapter, from_json
from src.task_manager.luigi.deposit_items import BankTask
from src.task_manager.luigi.state import get_world

logger = logging.getLogger(__name__)


@dataclass
class MapResource:
    resource: Resource
    map: Map
    distance: int
    rate: int


class HarvestItemsTask(luigi.Task):
    items: ItemsAdapter = luigi.DictParameter(default=None, significant=False)
    char_name: str = luigi.Parameter()
    datetime = luigi.DateSecondParameter(default=datetime.now(), interval=1)


    def run(self):
        world = get_world()
        items = from_json(self.items, ItemsAdapter)
        character = world.get_character(self.char_name)
        map_finder = MapFinder(world)
        item_finder = ItemFinder(world)
        resource_locations: List[MapResource] = []
        resources: List[Resource] = item_finder.find_item_in_resources(items.item)
        assert resources
        for resource in resources:
            resource_map: List[Map] = map_finder.find_resource(resource)
            assert resource_map
            rate = [item.rate for item in resource.drops if
                    item.item.code == items.item.code][0]
            for map_loc in resource_map:
                x, y = character.position
                distance = distance_location(x, y, map_loc.x, map_loc.y)
                resource_locations.append(MapResource(resource=resource,
                                                      map=map_loc,
                                                      distance=distance,
                                                      rate=rate))
        target_map = min(resource_locations, key=lambda loc: loc.rate + loc.distance)
        max_drops = max([item.max_quantity for item in target_map.resource.drops])

        x_map = target_map.map.x
        y_map = target_map.map.y
        i = 0
        character.wait_until_ready()
        for i in range(items.quantity * target_map.rate):
            if not character.inventory.is_possible_to_add_item(Item("new_item"), max_drops):
                yield BankTask(deposit_all_items=True, char_name=self.char_name)
            x, y = character.position
            if x != x_map or y != y_map:
                character.move(x=x_map, y=y_map)
                character.wait_until_ready()
            character.harvest()
            character.wait_until_ready()

        with self.output().open("w") as f:
            f.write(f"{i}")

    def output(self):
        return luigi.LocalTarget(
            os.path.join(settings.TASK_OUT_DIRECTORY,
                         f"{self.__class__.__name__}_{self.char_name}_{self.datetime}.txt"))