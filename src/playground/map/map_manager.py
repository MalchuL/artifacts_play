from abc import ABC, abstractmethod
from typing import List, Optional

from src.playground.map.map import Map, MapType, Event


class MapManager(ABC):

    @property
    @abstractmethod
    def maps(self) -> List[Map]:
        pass

    def get_maps(self, map_type: Optional[MapType] = None, code: Optional[str] = None) -> List[
        Map]:
        equal_or_true_none = lambda value, target: value == target or target is None
        return [tile for tile in self.maps if tile.content is not None and \
                equal_or_true_none(tile.content.type, map_type) and \
                equal_or_true_none(tile.content.code, code)]


    @abstractmethod
    def get_events(self) -> List[Event]:
        pass