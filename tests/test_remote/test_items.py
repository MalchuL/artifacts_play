import logging
from pprint import pprint

import pytest
from dynaconf import settings


from src.playground.items.item_crafting import ItemCraftingInfoManager
from src.playground.items.remote.rest_api_crafting import RestApiItemCraftingInfoManager
from src.rest_api_client.client import AuthenticatedClient

logger = logging.getLogger(__name__)


def test_items():
    char_name = settings.CHARACTERS[0]
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    items: ItemCraftingInfoManager = RestApiItemCraftingInfoManager(client=client)
    pprint(items.items)
    assert len(items.items) > 100

    craftable_items = items.get_crafts()
    assert len(craftable_items) < len(items.items)
    assert all([item.craft is not None for item in craftable_items])


