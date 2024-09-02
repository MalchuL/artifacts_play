from dataclasses import dataclass
from typing import List, Optional

from src.player.players.player import Player
from src.player.strategy.character_strategy import CharacterStrategy
from src.player.task import Resources, ResourcesTask, TaskInfo, BankTask
from src.playground.characters import Character, SkillType
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.items import Items, Item
from src.playground.map import Map
from src.playground.resources import Resource
from src.playground.utilites.items_finder import ItemFinder
from src.playground.utilites.locations import distance_location
from src.playground.utilites.map_finder import MapFinder


@dataclass
class MapResource:
    resource: Resource
    map: Map
    distance: int
    rate: int


class HarvestStrategy(CharacterStrategy):
    def __init__(self, player: Player, world: PlaygroundWorld, items: Optional[Items] = None,
                 resources: Optional[Resources] = None, skill_type: Optional[SkillType] = None,
                 farm_until_level: Optional[int] = None):

        super().__init__(player, world)
        self.items = items
        self.resources = resources
        self.farm_until_level = farm_until_level
        self.skill_type = skill_type

    def locate_items_position(self, character: Character, items: Items):
        world = self.world
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

    def locate_resources_position(self, character: Character, resource: Resource):
        world = self.world
        map_finder = MapFinder(world)
        resources_locations = []
        locations: List[Map] = map_finder.find_resource(resource)
        assert locations
        for resource_location in locations:
            x, y = character.position
            distance = distance_location(x, y, resource_location.x, resource_location.y)

            resources_locations.append(MapResource(resource=resource,
                                                   map=resource_location,
                                                   distance=distance,
                                                   rate=1))
        target_map = min(resources_locations, key=lambda loc: loc.distance)
        max_drops = max([item.max_quantity for item in resource.drops])

        x_map = target_map.map.x
        y_map = target_map.map.y
        return (x_map, y_map), max_drops, target_map

    def run(self):
        player = self.player
        items = self.items
        resources = self.resources
        farm_until_level = self.farm_until_level
        skill_type = self.skill_type

        character = player.character
        if items:
            (x_map, y_map), max_drops, target_map = self.locate_items_position(character, items)
            iterations = items.quantity * target_map.rate
        elif resources:
            (x_map, y_map), max_drops, target_map = self.locate_resources_position(character,
                                                                                   resources.resource)
            iterations = resources.count
        else:
            raise ValueError(f"Either items or monster must be specified")

        harvested_count = 0

        self.logger.info(f"Harvest for resources at {target_map} for {items}")
        character.wait_until_ready()
        for i in range(iterations):
            if not character.inventory.is_possible_to_add_item(Item("new_item"), max_drops):
                self.logger.info(f"Inventory is full, depositing all items")
                if resources:
                    resources_task = ResourcesTask(
                        resources=Resources(resource=resources.resource,
                                            count=resources.count - harvested_count),
                        skill_type=skill_type,
                        skill_level=farm_until_level,
                    )
                else:
                    resources_task = ResourcesTask(
                        items=Items(item=items.item, quantity=items.quantity - harvested_count),
                        skill_type=skill_type,
                        skill_level=farm_until_level,
                    )
                out_tasks = [TaskInfo(resources_task=resources_task),
                             TaskInfo(bank_task=BankTask(deposit_all=True))]
                return out_tasks
            x, y = character.position
            character.wait_until_ready()
            if x != x_map or y != y_map:
                character.move(x=x_map, y=y_map)
                character.wait_until_ready()
            harvest_result = character.harvest()
            character.wait_until_ready()
            # Check is conditions are met
            if items is not None:
                for fight_items in harvest_result.drops:
                    if fight_items.item.code == items.item.code:
                        harvested_count += fight_items.quantity
                        self.logger.info(
                            f"Harvest items {items.item.code}={harvested_count}/{items.quantity}, "
                            f"harvest_result={harvest_result}")
                if harvested_count >= items.quantity:
                    break
            elif resources is not None:
                harvested_count += 1
                self.logger.info(
                    f"Harvest resources {resources.resource.code}={harvested_count}/{resources.count}, "
                    f"harvest_result={harvest_result}")
                if harvested_count >= resources.count:
                    break
            elif farm_until_level is not None:
                if character.stats.skills.get_skill(skill_type).level >= farm_until_level:
                    break
        return [TaskInfo(bank_task=BankTask(deposit_all=True))]