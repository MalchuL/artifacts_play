import logging
from dataclasses import dataclass
from typing import List

from src.playground.items import Items, Item
from src.playground.map import Map
from src.playground.monsters import DetailedMonster, Monster
from src.playground.utilites.items_finder import ItemFinder
from src.playground.utilites.locations import distance_location
from src.playground.utilites.map_finder import MapFinder
from .character_task import CharacterTask
from .deposit_items import BankTask

logger = logging.getLogger(__name__)


@dataclass
class MapMonster:
    monster: Monster
    map: Map
    distance: int


class HuntItemsTask(CharacterTask):
    def __init__(self, char_name: str, monster: Monster, count: int = 1):
        super().__init__(char_name)
        self.monster = monster
        self.count = count

    def run(self):
        return self.hunt_monster(self.char_name, monster=self.monster, count=self.count)

    @staticmethod
    def bank_items_task(char_name):
        task = BankTask(char_name=char_name, deposit_all_items=True)
        task.start()

    def locate_position(self, char_name: str, monster: Monster):
        world = self.world
        character = world.get_character(char_name)
        map_finder = MapFinder(world)
        monster_locations: List[MapMonster] = []
        monsters_locs: List[Map] = map_finder.find_monster(monster=monster)
        assert monsters_locs
        for monsters_loc in monsters_locs:
            x, y = character.position
            distance = distance_location(x, y, monsters_loc.x, monsters_loc.y)

            monster_locations.append(MapMonster(monster=monster,
                                                map=monsters_loc,
                                                distance=distance))
        target_map = min(monster_locations, key=lambda loc: loc.distance)

        x_map = target_map.map.x
        y_map = target_map.map.y
        return (x_map, y_map), target_map

    def hunt_monster(self, char_name: str, monster: Monster, count: int):
        (x_map, y_map), target_map = self.locate_position(char_name, monster=monster)
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
            fight_result = character.fight()
            for fight_items in fight_result.drops:
                if fight_items.item.code == items.item.code:
                    hunted_items_count += fight_items.quantity
            self.logger.info(f"Hunt items {items.item.code}={hunted_items_count}/{items.quantity}, fight_result={fight_result}")
            character.wait_until_ready()
            if hunted_items_count >= items.quantity:
                break
