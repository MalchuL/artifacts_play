import logging
from dataclasses import dataclass
from typing import List, Optional

from src.player.players.player import Player
from src.player.strategy.character_strategy import CharacterStrategy
from src.player.task import TaskInfo, BankTask, MonsterTask, Monsters
from src.playground.characters import Character, FightResult
from src.playground.characters.character import Result
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Items, Item
from src.playground.map import Map
from src.playground.monsters import DetailedMonster, Monster
from src.playground.utilites.items_finder import ItemFinder
from src.playground.utilites.locations import distance_location
from src.playground.utilites.map_finder import MapFinder

logger = logging.getLogger(__name__)


@dataclass
class MapResource:
    monster: DetailedMonster
    map: Map
    distance: int
    rate: int


class HuntStrategy(CharacterStrategy):
    def __init__(self, player: Player, world: PlaygroundWorld, items: Optional[Items] = None,
                 monsters: Optional[Monsters] = None, farm_until_level: Optional[int] = None):

        super().__init__(player, world)
        self.items = items
        self.monsters = monsters
        self.farm_until_level = farm_until_level

    def run(self):
        return self.hunt_items(self.player, items=self.items, monsters=self.monsters,
                               farm_until_level=self.farm_until_level)

    def locate_items_position(self, character: Character, items: Items):
        world = self.world
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

    def locate_monster_position(self, character: Character, monster: Monster):
        world = self.world
        map_finder = MapFinder(world)
        monster_locations = []
        locations: List[Map] = map_finder.find_monster(monster)
        detailed_monster = world.monsters.get_monster_info(monster)
        assert locations
        for monster_location in locations:
            x, y = character.position
            distance = distance_location(x, y, monster_location.x, monster_location.y)

            monster_locations.append(MapResource(monster=detailed_monster,
                                                 map=monster_location,
                                                 distance=distance,
                                                 rate=1))
        target_map = min(monster_locations, key=lambda loc: loc.distance)
        max_drops = max([item.max_quantity for item in detailed_monster.drops])

        x_map = target_map.map.x
        y_map = target_map.map.y
        return (x_map, y_map), max_drops, target_map

    def hunt_items(self, player: Player, items: Optional[Items] = None,
                   monsters: Optional[Monsters] = None, farm_until_level: Optional[int] = None) -> List[TaskInfo]:
        character = player.character
        if items:
            (x_map, y_map), max_drops, target_map = self.locate_items_position(character, items)
            iterations = items.quantity * target_map.rate
        elif monsters:
            (x_map, y_map), max_drops, target_map = self.locate_monster_position(character,
                                                                                 monsters.monster)
            iterations = monsters.count
        else:
            raise ValueError(f"Either items or monster must be specified")

        hunted_count = 0

        self.logger.info(f"Hunt for resources at {target_map} for {items}")
        character.wait_until_ready()
        for i in range(iterations):
            if not character.inventory.is_possible_to_add_item(Item("new_item"), max_drops):
                self.logger.info(f"Inventory is full, depositing all items")
                if monsters:
                    monster_task = MonsterTask(monsters=Monsters(monster=monsters.monster,
                                                                 count=monsters.count - hunted_count),
                                               character_level=farm_until_level)
                else:
                    monster_task = MonsterTask(
                        items=Items(item=items.item, quantity=items.quantity - hunted_count),
                        character_level=farm_until_level)
                out_tasks = [TaskInfo(monster_task=monster_task),
                             TaskInfo(bank_task=BankTask(deposit_all=True))]

                return out_tasks
            # Check is correct position
            x, y = character.position
            character.wait_until_ready()
            if x != x_map or y != y_map:
                character.move(x=x_map, y=y_map)
                character.wait_until_ready()
            fight_result = character.fight()
            character.wait_until_ready()
            # Check is conditions are met
            if items is not None:
                for fight_items in fight_result.drops:
                    if fight_items.item.code == items.item.code:
                        hunted_count += fight_items.quantity
                        self.logger.info(
                            f"Hunt items {items.item.code}={hunted_count}/{items.quantity}, "
                            f"fight_result={fight_result}")
                if hunted_count >= items.quantity:
                    break
            elif monsters is not None:
                if fight_result.result == Result.WIN:
                    hunted_count += 1
                self.logger.info(
                    f"Hunt monsters {monsters.monster.code}={hunted_count}/{monsters.count}, "
                    f"fight_result={fight_result}")
                if hunted_count >= monsters.count:
                    break
            elif farm_until_level is not None:
                if character.stats.level.level >= farm_until_level:
                    break
        return [TaskInfo(bank_task=BankTask(deposit_all=True))]