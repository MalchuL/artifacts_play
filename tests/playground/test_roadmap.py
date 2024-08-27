from dynaconf import settings

from src.playground.fabric.playground_world import PlaygroundWorld
from src.playground.fabric.restapi_playground_world import RestApiPlaygroundWorld
from src.playground.items import Item
from src.playground.utilites.build_resources_roadmap import ResourcesRoadmap, graph
from src.rest_api_client.client import AuthenticatedClient
import matplotlib

def test_fight_simulation():
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    world: PlaygroundWorld = RestApiPlaygroundWorld(client)
    roadmap = ResourcesRoadmap(world, world.item_details.items)
    target_item = Item("steel_boots")
    root_node, _ = roadmap.create_items_roadmap()
    matplotlib.use('Qt5Agg')
    graph(root_node, reduce=True)
