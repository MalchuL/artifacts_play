import logging
import os
import pickle
from typing import Dict, List, Optional

from src.playground.characters.character_stats import SkillType
from src.playground.constants import CACHE_FOLDER
from src.playground.items.item import Item, DropItem
from src.playground.resources.resource import Resource
from src.playground.resources.resources_manager import ResourceManager
from src.rest_api_client.api.resources import GetAllResources
from src.rest_api_client.client import AuthenticatedClient
from src.rest_api_client.model import ResourceSchema, DataPageResourceSchema

logger = logging.getLogger(__name__)

CACHE_FILENAME = "resources_cache.pkl"

class RestApiResourceManager(ResourceManager):

    def __init__(self, client: AuthenticatedClient, pull_status=True, cache=True):
        super().__init__()

        # Hidden variables
        self._client = client
        self._resources: Optional[Dict[str, Resource]] = None
        if cache:
            cache_path = os.path.join(CACHE_FOLDER, CACHE_FILENAME)
            if os.path.exists(cache_path):
                logger.info("Saving resources info to local")
                with open(cache_path, 'rb') as f:
                    self._resources = pickle.load(f)
            else:
                logger.info("Pulling resources info from local")
                os.makedirs(CACHE_FOLDER, exist_ok=True)
                self._resources = self.__pull_state()
                with open(cache_path, 'wb') as f:
                    pickle.dump(self._resources, f)

        if pull_status and not cache:
            logger.info("Pulling resources info from server")
            self._resources = self.__pull_state()

    @staticmethod
    def __parse_resource(state: ResourceSchema) -> Resource:
        return Resource(code=state.code,
                        name=state.name,
                        skill=SkillType(state.skill.value),
                        level=state.level,
                        drops=[DropItem(item=Item(drop.code),
                                        rate=drop.rate,
                                        max_quantity=drop.max_quantity,
                                        min_quantity=drop.max_quantity) for drop in state.drops]
                        )

    def __pull_state(self) -> Dict[str, Resource]:
        date_page_resources: DataPageResourceSchema = GetAllResources(page=1,
                                                                      client=self._client)()
        total_pages = date_page_resources.pages
        schemas: List[ResourceSchema] = list(date_page_resources.data)

        for page in range(2, total_pages + 1):
            date_page_resources: DataPageResourceSchema = GetAllResources(page=page,
                                                                          client=self._client)()
            schemas.extend(date_page_resources.data)

        resources = {}
        for resource_schema in schemas:
            parsed_resource = self.__parse_resource(resource_schema)
            if parsed_resource.code in resources:
                raise KeyError(
                    f"{parsed_resource.code}:{resources[parsed_resource.code]}\n {parsed_resource} already defined"
                    f" for object. they are equal={resources[parsed_resource.code] == parsed_resource}")
            resources[parsed_resource.code] = parsed_resource

        return resources

    @property
    def resources(self) -> list[Resource]:
        return list(self._resources.values())

    def get_resource_info(self, unique_code: str) -> Resource:
        return self._resources[unique_code]
