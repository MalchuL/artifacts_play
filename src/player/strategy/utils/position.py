from typing import List

from src.playground.characters import Character
from src.playground.map import Map
from src.playground.utilites.locations import distance_location


def find_closest_position(character: Character, locations: List[Map]) -> Map:
    x, y = character.position
    return min(locations, key=lambda location: distance_location(x, y, location.x, location.y))
