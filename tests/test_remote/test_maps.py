import logging
from pprint import pprint

import pytest
from dynaconf import settings

from src.playground.map.remote.rest_api_maps import RestApiMapManager
from src.rest_api_client.client import AuthenticatedClient

logger = logging.getLogger(__name__)


@pytest.fixture
def maps() -> RestApiMapManager:
    client = AuthenticatedClient(base_url=settings.API_HOST, token=settings.API_TOKEN)
    maps: RestApiMapManager = RestApiMapManager(client=client)
    return maps


def test_maps(maps):
    pprint(maps.maps)
    print(len(maps.maps))
    assert len(maps.maps) > 100



def test_filtered_maps(maps):
    code = "rosenblood"
    assert len(maps.get_maps(code=code)) == 1
    print(maps.get_maps(code=code))


def test_filled_mapg(maps):
    code = "ogre"
    assert len(maps.get_maps(code=code)) == 2
    pprint(maps.get_maps())
