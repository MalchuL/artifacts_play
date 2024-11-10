import logging
from pprint import pprint

import pytest
from dynaconf import settings

from src.playground.items.item import EffectType
from src.playground.items.item_crafting import ItemCraftingInfoManager
from src.playground.items.remote.rest_api_crafting import RestApiItemCraftingInfoManager
from src.rest_api_client.client import AuthenticatedClient

logger = logging.getLogger(__name__)


def test_items():
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    items_manages: ItemCraftingInfoManager = RestApiItemCraftingInfoManager(client=client)
    pprint(items_manages.items)
    assert len(items_manages.items) > 100

    craftable_items = items_manages.get_crafts()
    assert len(craftable_items) < len(items_manages.items)
    assert all([item.craft is not None for item in craftable_items])

    for effect in EffectType:
        is_effect_in = False
        for item in items_manages.items:
            for item_effect in item.effects:
                if item_effect.type == effect:
                    is_effect_in = True
                    break
        if not is_effect_in:
            raise Exception(f"Effect {effect} not found")



