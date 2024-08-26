import pytest
from dynaconf import settings

from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.fabric.restapi_playground_world import RestApiPlaygroundWorld
from src.playground.items import Item
from src.playground.utilites.items_finder import ItemFinder
from src.playground.utilites.map_finder import MapFinder, BuildingType
from src.rest_api_client.client import AuthenticatedClient


@pytest.fixture
def world() -> PlaygroundWorld:
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    world: PlaygroundWorld = RestApiPlaygroundWorld(client)
    return world


def test_map_finders(world):
    finder = MapFinder(world)
    for building in BuildingType:
        build = finder.find_building(building)
        print(build)
        assert len(build) > 0


def test_map_resource_finders(world):
    finder = MapFinder(world)
    ore_resource = world.resources.get_resource_info("ash_tree")
    resource_location = finder.find_resource(ore_resource)
    print(resource_location)
    assert len(resource_location) > 0


def test_item_search(world):
    finder = ItemFinder(world)
    print(finder.find_item_in_bank(Item("wood")))
    print(finder.find_item_in_bank(Item("copper_ore")))
    print(finder.find_item_in_crafts(Item("copper_ore")))
    print(finder.find_item_in_crafts(Item("copper")))


def test_stick(world):
    finder = ItemFinder(world)
    print(finder.find_item_in_bank(Item("wooden_stick")))
    print(finder.find_item_in_resources(Item("wooden_stick")))
    print(finder.find_item_in_crafts(Item("wooden_stick")))
    print(finder.find_item_in_monsters(Item("wooden_stick")))