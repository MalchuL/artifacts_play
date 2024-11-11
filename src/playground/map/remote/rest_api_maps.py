import logging
import os
import pickle
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Union

from src.playground.constants import CACHE_FOLDER
from src.playground.map.map import Map, MapContent, MapType, Event
from src.playground.map.map_manager import MapManager
from src.rest_api_client.api.events import GetAllActiveEvents
from src.rest_api_client.api.maps import GetAllMaps
from src.rest_api_client.client import AuthenticatedClient
from src.rest_api_client.model import MapSchema, DataPageMapSchema, ActiveEventSchema, \
    DataPageActiveEventSchema
from dateutil.parser import parse as datetime_parser

logger = logging.getLogger(__name__)

CACHE_FILENAME = "maps_cache.pkl"

class RestApiMapManager(MapManager):

    def __init__(self, client: AuthenticatedClient, cache=True):
        super().__init__()

        # Hidden variables
        self._client = client
        self._maps: Optional[Dict[Tuple[int, int], Map]] = None

        if cache:
            cache_path = os.path.join(CACHE_FOLDER, CACHE_FILENAME)
            if os.path.exists(cache_path):
                logger.info("Saving maps info to local")
                with open(cache_path, 'rb') as f:
                    self._maps = pickle.load(f)
            else:
                logger.info("Pulling maps info from local")
                os.makedirs(CACHE_FOLDER, exist_ok=True)
                self._maps = self.__pull_state()
                with open(cache_path, 'wb') as f:
                    pickle.dump(self._maps, f)
        else:
            self._maps = self.__pull_state()


    @staticmethod
    def __convert_datetime(date_time: Union[str, datetime]):
        if isinstance(date_time, str):
            date_time = datetime_parser(date_time)
        return date_time.astimezone(timezone.utc)

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

    def __parse_event(self, event: ActiveEventSchema) -> Event:
        map_schema = event.map
        return Event(event_name=event.name,
                     map=Map(name=map_schema.name,
                             skin=map_schema.skin,
                             x=map_schema.x,
                             y=map_schema.y,
                             content=MapContent(code=map_schema.content.code,
                                                type=MapType(map_schema.content.type))),
                     expiration=self.__convert_datetime(event.expiration),
                     previous_skin=event.previous_skin)


    def __pull_state(self) -> Dict[Tuple[int, int], Map]:
        date_page_maps: DataPageMapSchema = GetAllMaps(page=1, client=self._client)()
        total_pages = date_page_maps.pages
        schemas: List[MapSchema] = list(date_page_maps.data)

        for page in range(2, total_pages + 1):
            date_page_maps: DataPageMapSchema = GetAllMaps(page=page, client=self._client)()
            schemas.extend(date_page_maps.data)

        maps: Dict[Tuple[int, int], Map] = {}
        for map_schema in schemas:
            parsed_map = self.__parse_map(map_schema)
            new_key = parsed_map.position
            if new_key in maps:
                raise KeyError(
                    f"{new_key}:{maps[new_key]}\n {parsed_map} already defined"
                    f" for object. they are equal={maps[new_key] == parsed_map}")
            maps[new_key] = parsed_map

        # Set default maps to avoid keeping events
        events = self._get_events()
        for position, event in events.items():
            maps[position] = Map(name=event.map.name,
                                 skin=event.previous_skin,
                                 x=event.map.x,
                                 y=event.map.y,
                                 content=None)

        return maps

    def _get_events(self) -> Dict[Tuple[int, int], Event]:
        date_page_maps: DataPageActiveEventSchema = GetAllActiveEvents(page=1, client=self._client)()
        total_pages = date_page_maps.pages
        schemas: List[ActiveEventSchema] = list(date_page_maps.data)

        for page in range(2, total_pages + 1):
            date_page_maps: DataPageActiveEventSchema = GetAllActiveEvents(page=page, client=self._client)()
            schemas.extend(date_page_maps.data)

        events = {}
        for event_schema in schemas:
            parsed_event = self.__parse_event(event_schema)
            new_key = parsed_event.position
            if new_key in events:
                raise KeyError(
                    f"{new_key}:{events[new_key]}\n {parsed_event} already defined"
                    f" for object. they are equal={events[new_key] == parsed_event}")
            events[new_key] = parsed_event

        return events

    @property
    def maps(self) -> list[Map]:
        maps = self._maps.copy()
        for position, event in self._get_events().items():
            assert position in maps
            maps[position] = event.map
        return list(maps.values())

    @property
    def maps_without_events(self) -> List[Map]:
        maps = self._maps.copy()
        return list(maps.values())

    def get_events(self) -> List[Event]:
        return list(self._get_events().values())