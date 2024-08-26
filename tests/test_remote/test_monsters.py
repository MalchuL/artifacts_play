import logging
from pprint import pprint

import pytest
from dynaconf import settings

from src.playground.monsters.remote.rest_api_monsters import RestApiMonsterManager
from src.rest_api_client.client import AuthenticatedClient

logger = logging.getLogger(__name__)


def test_monsters():
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    monster: RestApiMonsterManager = RestApiMonsterManager(client=client)
    pprint(monster.monsters)
    print(monster.get_monster_info(monster.monster_from_id("chicken")))

