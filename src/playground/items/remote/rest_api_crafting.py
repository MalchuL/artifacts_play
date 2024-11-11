import logging
import os.path
import pickle
from typing import Dict, List, Optional

from src.playground.characters.character_stats import SkillType
from src.playground.constants import CACHE_FOLDER

from src.playground.items.crafting import CraftInfo, CraftingItem
from src.playground.items.item import Item, ItemType, Items, EffectType, ItemEffect
from src.playground.items.item_crafting import ItemCraftingInfoManager
from src.rest_api_client.api.items import GetAllItems
from src.rest_api_client.client import AuthenticatedClient
from src.rest_api_client.model import DataPageItemSchema, ItemSchema

logger = logging.getLogger(__name__)

CACHE_FILENAME = "items_cache.pkl"

class RestApiItemCraftingInfoManager(ItemCraftingInfoManager):

    def __init__(self, client: AuthenticatedClient, pull_status=True, cache=True):
        super().__init__()

        # Hidden variables
        self._client = client
        self._items: Optional[Dict[str, CraftingItem]] = None
        if cache:
            cache_path = os.path.join(CACHE_FOLDER, CACHE_FILENAME)
            if os.path.exists(cache_path):
                logger.info("Saving items info to local")
                with open(cache_path, 'rb') as f:
                    self._items = pickle.load(f)
            else:
                logger.info("Pulling items info from local")
                os.makedirs(CACHE_FOLDER, exist_ok=True)
                self._items = self.__pull_state()
                with open(cache_path, 'wb') as f:
                    pickle.dump(self._items, f)

        if pull_status and not cache:
            logger.info("Pulling items info from server")
            self._items = self.__pull_state()

    @staticmethod
    def __parse_crafting_item(item_schema: ItemSchema) -> CraftingItem:
        craft = None
        if item_schema.craft:
            craft = CraftInfo(skill=SkillType(item_schema.craft.skill.value),
                              level=item_schema.craft.level,
                              items=[Items(Item(craft_item.code), craft_item.quantity)
                                     for craft_item in item_schema.craft.items],
                              quantity=item_schema.craft.quantity)
        return CraftingItem(code=item_schema.code,
                            name=item_schema.name, level=item_schema.level,
                            type=ItemType(item_schema.type), subtype=item_schema.subtype,
                            description=item_schema.description,
                            effects=[ItemEffect(EffectType(effect.name), value=effect.value) for
                                     effect in item_schema.effects],
                            craft=craft)

    def __pull_state(self) -> Dict[str, CraftingItem]:
        date_page_items: DataPageItemSchema = GetAllItems(page=1, client=self._client)()
        total_pages = date_page_items.pages
        schemas: List[ItemSchema] = list(date_page_items.data)

        for page in range(2, total_pages + 1):
            date_page_items: DataPageItemSchema = GetAllItems(page=page, client=self._client)()
            schemas.extend(date_page_items.data)

        items = {}
        for item_schema in schemas:
            parsed_item = self.__parse_crafting_item(item_schema)
            if parsed_item.code in items:
                raise KeyError(
                    f"{parsed_item.code}:{items[parsed_item.code]}\n {parsed_item} already defined"
                    f" for object. they are equal={items[parsed_item.code] == parsed_item}")
            items[parsed_item.code] = parsed_item

        return items

    @property
    def items(self) -> List[CraftingItem]:
        return list(self._items.values())

    def get_item(self, item: Item) -> CraftingItem:
        return self._items[item.code]

    def get_crafts(self) -> List[CraftingItem]:
        return [item for item in self._items.values() if item.craft is not None]

    def get_craft(self, item: Item) -> CraftingItem:
        item = self._items[item.code]
        if item.craft is None:
            raise KeyError(f"{item.code} not in craftable items")
        return item
