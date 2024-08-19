from abc import ABC, abstractmethod
from typing import List

from src.playground.items.item import Item
from src.playground.resources.resource import Resource


class ResourceManager(ABC):

    @property
    @abstractmethod
    def resources(self) -> List[Resource]:
        pass

    @abstractmethod
    def get_resource_info(self, unique_code: str) -> Resource:
        pass
