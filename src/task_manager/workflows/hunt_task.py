import logging
from dataclasses import dataclass
from typing import List

from src.playground.items import Items, Item
from src.playground.map import Map
from src.playground.monsters import DetailedMonster
from src.playground.utilites.items_finder import ItemFinder
from src.playground.utilites.locations import distance_location
from src.playground.utilites.map_finder import MapFinder
from .character_task import CharacterTask
from .deposit_items import BankTask

logger = logging.getLogger(__name__)


@dataclass
class MapResource:
    monster: DetailedMonster
    map: Map
    distance: int
    rate: int


class HuntItemsTask(CharacterTask):
    def __init__(self, char_name: str, items: Items):
        super().__init__(char_name)
        self.items = items

    def run(self):
        return self.hunt_items(self.char_name, items=self.items)

    @staticmethod
    def bank_items_task(char_name):
        task = BankTask(char_name=char_name, deposit_all_items=True)
        task.start()

    def locate_position(self, char_name: str, items: Items):
        world = self.world
        character = world.get_character(char_name)
        map_finder = MapFinder(world)
        item_finder = ItemFinder(world)
        monster_locations: List[MapResource] = []
        monsters: List[DetailedMonster] = item_finder.find_item_in_monsters(search_item=items.item)
        assert monsters
        for monster in monsters:
            monster_maps: List[Map] = map_finder.find_monster(monster)
            assert monster_maps
            rate = [item.rate for item in monster.drops if
                    item.item.code == items.item.code][0]
            for map_loc in monster_maps:
                x, y = character.position
                distance = distance_location(x, y, map_loc.x, map_loc.y)

                monster_locations.append(MapResource(monster=monster,
                                                     map=map_loc,
                                                     distance=distance,
                                                     rate=rate))
        target_map = min(monster_locations, key=lambda loc: loc.rate + loc.distance)
        max_drops = max([item.max_quantity for item in target_map.monster.drops])

        x_map = target_map.map.x
        y_map = target_map.map.y
        return (x_map, y_map), max_drops, target_map

    def hunt_items(self, char_name: str, items: Items):
        (x_map, y_map), max_drops, target_map = self.locate_position(char_name, items)
        character = self.world.get_character(char_name)

        self.logger.info(f"Hunt for resources at {target_map} for {items}")
        character.wait_until_ready()
        for i in range(items.quantity * target_map.rate):
            if not character.inventory.is_possible_to_add_item(Item("new_item"), max_drops):
                self.bank_items_task(char_name=self.char_name)
            x, y = character.position
            if x != x_map or y != y_map:
                character.move(x=x_map, y=y_map)
                character.wait_until_ready()
            character.fight()
            character.wait_until_ready()
