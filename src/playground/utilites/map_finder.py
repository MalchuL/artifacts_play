from enum import Enum
from typing import List

from src.playground.characters import SkillType
from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.map import MapType, Map
from src.playground.monsters import Monster
from src.playground.resources import Resource


class BuildingType(Enum):
    WEAPON_CRAFTING_WORKSHOP = "weaponcrafting"
    GEAR_CRAFTING_WORKSHOP = "gearcrafting"
    JEWERLY_CRAFTING_WORKSHOP = "jewelrycrafting"
    COOKING = "cooking"
    MINING = "mining"
    WOODCUTTING = "woodcutting"
    BANK = "bank"
    GRAND_EXCHANGE = "grand_exchange"
    TASKS_MANAGER = "tasks_master"


class MapFinder:
    def __init__(self, world: PlaygroundWorld):
        self.world = world

    def find_monster(self, monster: Monster) -> List[Map]:
        map_tiles = self.world.map.get_maps(map_type=MapType.MONSTER, code=monster.code)
        return map_tiles

    def find_resource(self, resource: Resource):
        map_tiles = self.world.map.get_maps(map_type=MapType.RESOURCE, code=resource.code)
        return map_tiles

    def find_building(self, building_type: BuildingType) -> List[Map]:
        search_method = self.world.map.get_maps
        if building_type == BuildingType.BANK:
            return search_method(map_type=MapType.BANK)
        elif building_type == BuildingType.GRAND_EXCHANGE:
            return search_method(map_type=MapType.GRAND_EXCHANGE)
        elif building_type == BuildingType.TASKS_MANAGER:
            return search_method(map_type=MapType.TASKS_MANAGER)
        # Skill
        elif building_type == BuildingType.WEAPON_CRAFTING_WORKSHOP:
            return search_method(map_type=MapType.WORKSHOP, code=SkillType.WEAPON_CRAFTING.value)
        elif building_type == BuildingType.GEAR_CRAFTING_WORKSHOP:
            return search_method(map_type=MapType.WORKSHOP, code=SkillType.GEAR_CRAFTING.value)
        elif building_type == BuildingType.JEWERLY_CRAFTING_WORKSHOP:
            return search_method(map_type=MapType.WORKSHOP, code=SkillType.JEWERLY_CRAFTING.value)
        elif building_type == BuildingType.COOKING:
            return search_method(map_type=MapType.WORKSHOP, code=SkillType.COOKING.value)
        elif building_type == BuildingType.MINING:
            return search_method(map_type=MapType.WORKSHOP, code=SkillType.MINING.value)
        elif building_type == BuildingType.WOODCUTTING:
            return search_method(map_type=MapType.WORKSHOP, code=SkillType.WOODCUTTING.value)
