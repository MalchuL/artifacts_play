import logging
from typing import Dict, List, Optional, Tuple

from src.playground.map.map import Map, MapContent, MapType
from src.playground.map.map_manager import MapManager
from src.rest_api_client.api.maps import GetAllMaps
from src.rest_api_client.client import AuthenticatedClient
from src.rest_api_client.model import MapSchema, DataPageMapSchema

logger = logging.getLogger(__name__)


class RestApiMapManager(MapManager):

    def __init__(self, client: AuthenticatedClient, pull_status=True):
        super().__init__()

        # Hidden variables
        self._client = client
        self._maps: Optional[Dict[Tuple[int, int], Map]] = None
        if pull_status:
            self._maps = self.__pull_state()

    @staticmethod
    def __parse_map(state: MapSchema) -> Map:
        map_content = None
        if state.content is not None:
            map_content = MapContent(code=state.content.code,
                                     type=MapType(state.content.type))
        return Map(name=state.name,
                   skin=state.skin,
                   x=state.x,
                   y=state.y,
                   content=map_content)

    def __pull_state(self) -> Dict[Tuple[int, int], Map]:
        date_page_resources: DataPageMapSchema = GetAllMaps(page=1, client=self._client)()
        total_pages = date_page_resources.pages
        schemas: List[MapSchema] = list(date_page_resources.data)

        for page in range(2, total_pages + 1):
            date_page_resources: DataPageMapSchema = GetAllMaps(page=page, client=self._client)()
            schemas.extend(date_page_resources.data)

        maps = {}
        for map_schema in schemas:
            parsed_map = self.__parse_map(map_schema)
            new_key = parsed_map.position
            if new_key in maps:
                raise KeyError(
                    f"{new_key}:{maps[new_key]}\n {parsed_map} already defined"
                    f" for object. they are equal={maps[new_key] == parsed_map}")
            maps[new_key] = parsed_map

        return maps

    @property
    def maps(self) -> list[Map]:
        return list(self._maps.values())
