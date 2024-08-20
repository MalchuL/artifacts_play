from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.playground.items import Items, Item
from src.playground.map import Map
from src.playground.resources import Resource
from src.playground.utilites.items_finder import ItemFinder
from src.playground.utilites.locations import distance_location
from src.playground.utilites.map_finder import MapFinder
from .character_task import CharacterTask
from .deposit_items import BankTask


@dataclass
class MapResource:
    resource: Resource
    map: Map
    distance: int
    rate: int


class HarvestItemsTask(CharacterTask):
    def __init__(self, char_name: str, items: Items):
        super().__init__(char_name)
        self.items = items

    @staticmethod
    def bank_items_task(char_name):
        task = BankTask(char_name=char_name, deposit_all_items=True)
        task.start()

    def locate_position(self, char_name: str, items: Items):
        world = self.world
        character = world.get_character(char_name)
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
        target_map = min(resource_locations,
                         key=lambda loc: loc.rate * items.quantity + loc.distance)
        max_drops = max([item.max_quantity for item in target_map.resource.drops])

        x_map = target_map.map.x
        y_map = target_map.map.y
        return (x_map, y_map), max_drops, target_map

    def harvest_items(self, char_name: str, items: Items):

        (x_map, y_map), max_drops, target_map = self.locate_position(char_name, items)
        character = self.world.get_character(char_name)

        harvested_items_count = 0

        self.logger.info(f"Harvest for resources at {target_map} for {items}")
        character.wait_until_ready()
        for i in range(items.quantity * target_map.rate):
            if not character.inventory.is_possible_to_add_item(Item("new_item"), max_drops):
                self.bank_items_task(char_name=self.char_name)
            x, y = character.position
            if x != x_map or y != y_map:
                character.move(x=x_map, y=y_map)
                character.wait_until_ready()
            harvest_result = character.harvest()
            for harvest_items in harvest_result.drops:
                if harvest_items.item.code == items.item.code:
                    harvested_items_count += harvest_items.quantity
            character.wait_until_ready()
            self.logger.info(
                f"Harvest items {items.item.code}={harvested_items_count}/{items.quantity}")
            if harvested_items_count >= items.quantity:
                break

    def run(self):
        return self.harvest_items(self.char_name, items=self.items)
